"""
Titanium Supply Chain Optimal Allocator
=======================================
Senior Design Project -- Virginia Tech ISE Team 4
Sponsor: The Aerospace Corporation

Solves the supplier allocation problem as a linear program:
given a set of available suppliers, a total order quantity, and
an objective (minimize cost, minimize lead time, or balanced),
find the optimal allocation of kg to each supplier.

Solvers (in priority order):
    1. Google OR-Tools  (pip install ortools)
    2. SciPy linprog    (pip install scipy)

Usage:
    from supply_chain_optimizer import optimize_allocation
    from supply_chain_sim import DEFAULT_SUPPLIERS

    allocation = optimize_allocation(
        suppliers=DEFAULT_SUPPLIERS,
        order_quantity_kg=5000,
        disrupted_supplier="Titan-RU",
        qualified_only=True,
        objective="min_cost",
    )
    print(allocation)
    # {'Titan-US': 1538.5, 'Titan-JP': 2307.7, 'Titan-AU': 1153.8}

Dependencies:
    pip install ortools   (preferred, optional)
    pip install scipy     (fallback, likely already installed)
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

# Import Supplier type from the simulation module
from supply_chain_sim import Supplier, DEFAULT_SUPPLIERS


# ---------------------------------------------------------------------------
# Solver Backend Detection
# ---------------------------------------------------------------------------

_SOLVER_BACKEND = None

try:
    from ortools.linear_solver import pywraplp
    _SOLVER_BACKEND = "ortools"
except ImportError:
    pass

if _SOLVER_BACKEND is None:
    try:
        from scipy.optimize import linprog
        _SOLVER_BACKEND = "scipy"
    except ImportError:
        pass


def get_solver_backend() -> str:
    """Return the name of the active solver backend."""
    if _SOLVER_BACKEND is None:
        raise RuntimeError(
            "No LP solver available. Install one of:\n"
            "  pip install ortools\n"
            "  pip install scipy"
        )
    return _SOLVER_BACKEND


# ---------------------------------------------------------------------------
# Optimization Result
# ---------------------------------------------------------------------------

@dataclass
class OptimizationResult:
    """Output of the optimal allocation solver."""
    allocation: dict[str, float]       # supplier_name -> kg
    objective_value: float             # value of the objective function
    objective_name: str                # "min_cost", "min_time", or "balanced"
    solver_backend: str                # "ortools" or "scipy"
    feasible: bool
    total_cost_usd: float
    weighted_lead_time_weeks: float    # allocation-weighted average lead time
    notes: list[str]


# ---------------------------------------------------------------------------
# Core Optimizer
# ---------------------------------------------------------------------------

PLANNING_HORIZON_WEEKS = 12  # matches supply_chain_sim.py heuristic strategies

# Objectives
OBJECTIVE_MIN_COST = "min_cost"
OBJECTIVE_MIN_TIME = "min_time"
OBJECTIVE_BALANCED = "balanced"
VALID_OBJECTIVES = (OBJECTIVE_MIN_COST, OBJECTIVE_MIN_TIME, OBJECTIVE_BALANCED)


def optimize_allocation(
    suppliers: list[Supplier] = None,
    order_quantity_kg: float = 5000.0,
    disrupted_supplier: str = "",
    qualified_only: bool = True,
    objective: str = OBJECTIVE_MIN_COST,
    planning_horizon_weeks: int = PLANNING_HORIZON_WEEKS,
    cost_weight: float = 0.6,
    time_weight: float = 0.4,
) -> OptimizationResult:
    """
    Find the optimal supplier allocation using linear programming.

    Args:
        suppliers:               List of Supplier objects (defaults to built-in)
        order_quantity_kg:       Total demand to satisfy
        disrupted_supplier:      Supplier name to exclude (offline)
        qualified_only:          If True, exclude non-qualified suppliers
        objective:               "min_cost", "min_time", or "balanced"
        planning_horizon_weeks:  Capacity planning window (default 12)
        cost_weight:             Weight for cost term in balanced objective
        time_weight:             Weight for time term in balanced objective

    Returns:
        OptimizationResult with allocation dict and solver metadata.

    LP Formulation (min_cost):
        minimize   sum( cost_per_kg[i] * x[i] )
        subject to:
            sum(x[i]) = order_quantity_kg           (demand met)
            0 <= x[i] <= capacity[i] * horizon      (per-supplier cap)

    LP Formulation (min_time):
        minimize   sum( lead_time[i] * x[i] )
        subject to:  (same as above)
        Note: this minimizes total lead-time-weighted allocation,
        which drives allocation toward faster suppliers.

    LP Formulation (balanced):
        minimize   w_c * sum( cost_norm[i] * x[i] )
                 + w_t * sum( time_norm[i] * x[i] )
        where cost_norm and time_norm are min-max normalized to [0,1].
    """
    if suppliers is None:
        suppliers = DEFAULT_SUPPLIERS

    if objective not in VALID_OBJECTIVES:
        raise ValueError(
            f"Unknown objective '{objective}'. Use one of: {VALID_OBJECTIVES}"
        )

    notes = []

    # --- Filter available suppliers ---
    available = []
    for s in suppliers:
        if s.name == disrupted_supplier:
            notes.append(f"{s.name} excluded (disrupted).")
            continue
        if qualified_only and not s.is_qualified:
            notes.append(f"{s.name} excluded (not aerospace-qualified).")
            continue
        available.append(s)

    if not available:
        return OptimizationResult(
            allocation={},
            objective_value=0.0,
            objective_name=objective,
            solver_backend=get_solver_backend(),
            feasible=False,
            total_cost_usd=0.0,
            weighted_lead_time_weeks=0.0,
            notes=notes + ["No suppliers available."],
        )

    # --- Compute capacity bounds ---
    n = len(available)
    upper_bounds = [s.capacity_kg_per_week * planning_horizon_weeks for s in available]
    total_capacity = sum(upper_bounds)

    if total_capacity < order_quantity_kg:
        notes.append(
            f"Total available capacity ({total_capacity:,.0f} kg) "
            f"is less than order ({order_quantity_kg:,.0f} kg). "
            f"Solver will maximize fulfillment."
        )

    # --- Build objective coefficients ---
    costs = [s.cost_per_kg for s in available]
    times = [s.lead_time_weeks for s in available]

    if objective == OBJECTIVE_MIN_COST:
        obj_coeffs = costs

    elif objective == OBJECTIVE_MIN_TIME:
        obj_coeffs = times

    else:  # balanced
        # Normalize costs and times to [0, 1] range to make them comparable
        min_c, max_c = min(costs), max(costs)
        min_t, max_t = min(times), max(times)
        range_c = max_c - min_c if max_c != min_c else 1.0
        range_t = max_t - min_t if max_t != min_t else 1.0
        norm_costs = [(c - min_c) / range_c for c in costs]
        norm_times = [(t - min_t) / range_t for t in times]
        obj_coeffs = [
            cost_weight * nc + time_weight * nt
            for nc, nt in zip(norm_costs, norm_times)
        ]

    # --- Solve ---
    demand = min(order_quantity_kg, total_capacity)  # cap demand at capacity

    backend = get_solver_backend()
    if backend == "ortools":
        alloc_values = _solve_ortools(obj_coeffs, upper_bounds, demand)
    else:
        alloc_values = _solve_scipy(obj_coeffs, upper_bounds, demand)

    # --- Build result ---
    allocation = {}
    total_cost = 0.0
    weighted_time_num = 0.0
    total_alloc = 0.0

    for i, s in enumerate(available):
        kg = round(alloc_values[i], 1)
        if kg > 0.5:  # skip negligible allocations
            allocation[s.name] = kg
            total_cost += kg * s.cost_per_kg
            weighted_time_num += kg * s.lead_time_weeks
            total_alloc += kg

    weighted_time = weighted_time_num / total_alloc if total_alloc > 0 else 0.0
    feasible = total_alloc >= order_quantity_kg * 0.95

    if not feasible:
        shortfall = order_quantity_kg - total_alloc
        notes.append(f"Shortfall of {shortfall:,.0f} kg — capacity insufficient.")

    obj_val = sum(obj_coeffs[i] * alloc_values[i] for i in range(n))

    return OptimizationResult(
        allocation=allocation,
        objective_value=round(obj_val, 2),
        objective_name=objective,
        solver_backend=backend,
        feasible=feasible,
        total_cost_usd=round(total_cost, 2),
        weighted_lead_time_weeks=round(weighted_time, 1),
        notes=notes,
    )


# ---------------------------------------------------------------------------
# OR-Tools Solver
# ---------------------------------------------------------------------------

def _solve_ortools(
    obj_coeffs: list[float],
    upper_bounds: list[float],
    demand: float,
) -> list[float]:
    """Solve the allocation LP using Google OR-Tools GLOP solver."""
    from ortools.linear_solver import pywraplp

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        raise RuntimeError("OR-Tools GLOP solver not available.")

    n = len(obj_coeffs)

    # Decision variables: x[i] = kg allocated to supplier i
    x = [solver.NumVar(0.0, upper_bounds[i], f"x_{i}") for i in range(n)]

    # Constraint: total allocation = demand
    solver.Add(sum(x) == demand)

    # Objective: minimize weighted cost/time
    objective = solver.Objective()
    for i in range(n):
        objective.SetCoefficient(x[i], obj_coeffs[i])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        return [x[i].solution_value() for i in range(n)]

    # Fallback: try with inequality (allow partial fulfillment)
    solver2 = pywraplp.Solver.CreateSolver("GLOP")
    x2 = [solver2.NumVar(0.0, upper_bounds[i], f"x_{i}") for i in range(n)]
    solver2.Add(sum(x2) <= demand)
    obj2 = solver2.Objective()
    # Maximize allocation first, then minimize cost
    for i in range(n):
        obj2.SetCoefficient(x2[i], -1000.0 + obj_coeffs[i])
    obj2.SetMinimization()
    solver2.Solve()
    return [x2[i].solution_value() for i in range(n)]


# ---------------------------------------------------------------------------
# SciPy Solver (Fallback)
# ---------------------------------------------------------------------------

def _solve_scipy(
    obj_coeffs: list[float],
    upper_bounds: list[float],
    demand: float,
) -> list[float]:
    """Solve the allocation LP using scipy.optimize.linprog."""
    from scipy.optimize import linprog

    n = len(obj_coeffs)

    # Bounds: 0 <= x[i] <= upper_bounds[i]
    bounds = [(0.0, ub) for ub in upper_bounds]

    # Equality constraint: sum(x) = demand
    A_eq = [[1.0] * n]
    b_eq = [demand]

    result = linprog(
        c=obj_coeffs,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method="highs",
    )

    if result.success:
        return list(result.x)

    # Fallback: relax equality to inequality (allow partial fulfillment)
    # maximize allocation by adding large negative coefficient
    c_fallback = [-1000.0 + obj_coeffs[i] for i in range(n)]
    A_ub = [[1.0] * n]
    b_ub = [demand]
    result2 = linprog(
        c=c_fallback,
        A_ub=A_ub,
        b_ub=b_ub,
        bounds=bounds,
        method="highs",
    )
    if result2.success:
        return list(result2.x)

    warnings.warn("LP solver failed; returning zero allocation.")
    return [0.0] * n


# ---------------------------------------------------------------------------
# Integration Helper
# ---------------------------------------------------------------------------

def optimal_allocate(
    available_suppliers: list[Supplier],
    order_quantity_kg: float,
    objective: str = OBJECTIVE_MIN_COST,
    planning_horizon_weeks: int = PLANNING_HORIZON_WEEKS,
) -> dict[str, float]:
    """
    Drop-in replacement for supply_chain_sim._allocate_order().

    Takes already-filtered suppliers (disrupted/unqualified removed)
    and returns allocation dict.  This allows run_disruption_scenario()
    to call the optimizer without duplicating the filtering logic.
    """
    if not available_suppliers:
        return {}

    n = len(available_suppliers)
    upper_bounds = [
        s.capacity_kg_per_week * planning_horizon_weeks
        for s in available_suppliers
    ]
    demand = min(order_quantity_kg, sum(upper_bounds))

    costs = [s.cost_per_kg for s in available_suppliers]
    times = [s.lead_time_weeks for s in available_suppliers]

    if objective == OBJECTIVE_MIN_COST:
        obj_coeffs = costs
    elif objective == OBJECTIVE_MIN_TIME:
        obj_coeffs = times
    else:
        min_c, max_c = min(costs), max(costs)
        min_t, max_t = min(times), max(times)
        range_c = max_c - min_c if max_c != min_c else 1.0
        range_t = max_t - min_t if max_t != min_t else 1.0
        obj_coeffs = [
            0.6 * (c - min_c) / range_c + 0.4 * (t - min_t) / range_t
            for c, t in zip(costs, times)
        ]

    backend = get_solver_backend()
    if backend == "ortools":
        values = _solve_ortools(obj_coeffs, upper_bounds, demand)
    else:
        values = _solve_scipy(obj_coeffs, upper_bounds, demand)

    allocation = {}
    for i, s in enumerate(available_suppliers):
        kg = round(values[i], 1)
        if kg > 0.5:
            allocation[s.name] = kg
    return allocation


# ---------------------------------------------------------------------------
# Comparison: Heuristic vs Optimal
# ---------------------------------------------------------------------------

def compare_heuristic_vs_optimal(
    suppliers: list[Supplier] = None,
    order_quantity_kg: float = 5000.0,
    disrupted_supplier: str = "",
    qualified_only: bool = True,
) -> dict:
    """
    Run the same scenario through all heuristic strategies AND all
    optimal objectives. Returns a dict with results for easy comparison.

    Useful for evaluating whether OR-Tools improves on the heuristics.
    """
    from supply_chain_sim import run_disruption_scenario

    results = {}

    # Heuristic strategies
    for strategy in ("proportional", "cheapest_first", "fastest_first"):
        r = run_disruption_scenario(
            suppliers=suppliers,
            disrupted_supplier=disrupted_supplier,
            disruption_weeks=12,
            order_quantity_kg=order_quantity_kg,
            qualified_only=qualified_only,
            allocation_strategy=strategy,
        )
        results[strategy] = {
            "allocation": r.allocation,
            "cost": r.total_cost_usd,
            "delivery_weeks": r.total_delivery_weeks,
            "feasible": r.feasible,
        }

    # Optimal strategies
    for obj in VALID_OBJECTIVES:
        opt = optimize_allocation(
            suppliers=suppliers,
            order_quantity_kg=order_quantity_kg,
            disrupted_supplier=disrupted_supplier,
            qualified_only=qualified_only,
            objective=obj,
        )
        results[f"optimal_{obj}"] = {
            "allocation": opt.allocation,
            "cost": opt.total_cost_usd,
            "delivery_weeks": opt.weighted_lead_time_weeks,
            "feasible": opt.feasible,
            "solver": opt.solver_backend,
        }

    return results


# ---------------------------------------------------------------------------
# Standalone Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("TITANIUM SUPPLY CHAIN OPTIMAL ALLOCATOR")
    print(f"Solver backend: {get_solver_backend()}")
    print("=" * 65)

    scenarios = [
        ("Baseline (no disruption)", "", True),
        ("Titan-RU disrupted", "Titan-RU", True),
        ("Titan-US disrupted", "Titan-US", True),
        ("Titan-RU disrupted, non-qualified allowed", "Titan-RU", False),
    ]

    for title, disrupted, qual_only in scenarios:
        print(f"\n--- {title} ---")

        for obj in VALID_OBJECTIVES:
            result = optimize_allocation(
                order_quantity_kg=5000,
                disrupted_supplier=disrupted,
                qualified_only=qual_only,
                objective=obj,
            )
            print(f"\n  Objective: {obj}")
            print(f"  Feasible:  {result.feasible}")
            print(f"  Cost:      ${result.total_cost_usd:,.2f}")
            print(f"  Avg Lead:  {result.weighted_lead_time_weeks} weeks")
            print(f"  Allocation:")
            for name, kg in result.allocation.items():
                print(f"    {name}: {kg:,.1f} kg")
            if result.notes:
                for note in result.notes:
                    print(f"    Note: {note}")

    # Comparison table
    print("\n" + "=" * 65)
    print("HEURISTIC vs OPTIMAL COMPARISON (Titan-RU disrupted, 5000 kg)")
    print("=" * 65)

    comparison = compare_heuristic_vs_optimal(
        order_quantity_kg=5000,
        disrupted_supplier="Titan-RU",
    )

    print(f"\n  {'Strategy':<25} {'Cost':>12} {'Lead Time':>12} {'Feasible':>10}")
    print(f"  {'-'*25} {'-'*12} {'-'*12} {'-'*10}")
    for name, data in comparison.items():
        cost_str = f"${data['cost']:,.2f}"
        time_str = f"{data['delivery_weeks']} wk"
        print(f"  {name:<25} {cost_str:>12} {time_str:>12} {str(data['feasible']):>10}")
