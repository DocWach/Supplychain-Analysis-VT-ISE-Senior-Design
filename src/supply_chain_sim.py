"""
Titanium Supply Chain Disruption Simulator
==========================================
Senior Design Project — Virginia Tech ISE Team 4
Sponsor: The Aerospace Corporation

This module simulates a simplified titanium supply chain with multiple
suppliers, a single manufacturer, and configurable disruption events.
It outputs delivery time and cost metrics for each scenario, which can
be passed to the LLM analyst for interpretation and recommendation.

Dependencies:
    pip install simpy

Usage:
    from supply_chain_sim import run_disruption_scenario, load_suppliers

    suppliers = load_suppliers("suppliers.csv")
    results = run_disruption_scenario(
        suppliers=suppliers,
        disrupted_supplier="Titan-RU",
        disruption_weeks=8,
        order_quantity_kg=5000,
    )
    print(results)
"""

import simpy
import csv
import os
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

@dataclass
class Supplier:
    """Represents a single titanium supplier."""
    name: str
    region: str
    lead_time_weeks: float       # Normal delivery lead time
    capacity_kg_per_week: float  # Maximum weekly output
    cost_per_kg: float           # Unit cost in USD
    quality_rating: float        # 0.0 to 1.0 (1.0 = best)
    is_qualified: bool           # Aerospace qualification status


@dataclass
class ScenarioResult:
    """Output of a single simulation run."""
    scenario_name: str
    disrupted_supplier: str
    disruption_weeks: int
    order_quantity_kg: float
    total_delivery_weeks: float
    total_cost_usd: float
    suppliers_used: list
    allocation: dict             # supplier_name -> kg allocated
    feasible: bool               # Whether the order could be fulfilled
    notes: list                  # Warnings or observations


# ---------------------------------------------------------------------------
# Default Supplier Data
# ---------------------------------------------------------------------------

DEFAULT_SUPPLIERS = [
    Supplier(
        name="Titan-US",
        region="United States",
        lead_time_weeks=4,
        capacity_kg_per_week=800,
        cost_per_kg=32.00,
        quality_rating=0.95,
        is_qualified=True,
    ),
    Supplier(
        name="Titan-JP",
        region="Japan",
        lead_time_weeks=6,
        capacity_kg_per_week=1200,
        cost_per_kg=28.00,
        quality_rating=0.92,
        is_qualified=True,
    ),
    Supplier(
        name="Titan-RU",
        region="Russia",
        lead_time_weeks=8,
        capacity_kg_per_week=2000,
        cost_per_kg=22.00,
        quality_rating=0.88,
        is_qualified=True,
    ),
    Supplier(
        name="Titan-CN",
        region="China",
        lead_time_weeks=7,
        capacity_kg_per_week=1500,
        cost_per_kg=24.00,
        quality_rating=0.85,
        is_qualified=False,       # Not yet aerospace-qualified
    ),
    Supplier(
        name="Titan-AU",
        region="Australia",
        lead_time_weeks=5,
        capacity_kg_per_week=600,
        cost_per_kg=35.00,
        quality_rating=0.90,
        is_qualified=True,
    ),
]


# ---------------------------------------------------------------------------
# CSV Loader
# ---------------------------------------------------------------------------

def load_suppliers(csv_path: str) -> list[Supplier]:
    """
    Load supplier data from a CSV file.

    Expected columns:
        name, region, lead_time_weeks, capacity_kg_per_week,
        cost_per_kg, quality_rating, is_qualified

    Returns a list of Supplier objects.
    """
    suppliers = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            suppliers.append(Supplier(
                name=row["name"],
                region=row["region"],
                lead_time_weeks=float(row["lead_time_weeks"]),
                capacity_kg_per_week=float(row["capacity_kg_per_week"]),
                cost_per_kg=float(row["cost_per_kg"]),
                quality_rating=float(row["quality_rating"]),
                is_qualified=row["is_qualified"].strip().lower() in ("true", "1", "yes"),
            ))
    return suppliers


# ---------------------------------------------------------------------------
# Simulation Logic
# ---------------------------------------------------------------------------

def _supplier_process(env, supplier: Supplier, order_kg: float, delivery_log: dict):
    """
    SimPy process: a single supplier fulfilling its allocated order.

    Simulates the lead time for delivery. The supplier produces at its
    capacity rate, so delivery time = max(lead_time, order / capacity).
    """
    production_weeks = order_kg / supplier.capacity_kg_per_week
    actual_weeks = max(supplier.lead_time_weeks, production_weeks)

    yield env.timeout(actual_weeks)

    delivery_log[supplier.name] = {
        "delivered_kg": order_kg,
        "delivery_weeks": actual_weeks,
        "cost_usd": order_kg * supplier.cost_per_kg,
    }


def _allocate_order(
    available_suppliers: list[Supplier],
    order_quantity_kg: float,
    strategy: str = "proportional",
) -> dict[str, float]:
    """
    Allocate an order across available suppliers.

    Strategies:
        "proportional" — split by capacity share (default)
        "cheapest_first" — fill from lowest cost, then next cheapest
        "fastest_first" — fill from shortest lead time, then next fastest
        "optimal_cost" — LP minimizing total cost (requires ortools or scipy)
        "optimal_time" — LP minimizing weighted lead time
        "optimal_balanced" — LP balancing cost and lead time

    Returns dict of supplier_name -> allocated_kg.
    """
    # Optimal strategies: delegate to the LP solver
    if strategy.startswith("optimal_"):
        try:
            from supply_chain_optimizer import optimal_allocate
            objective = strategy.replace("optimal_", "min_", 1)
            if objective == "min_balanced":
                objective = "balanced"
            return optimal_allocate(available_suppliers, order_quantity_kg, objective)
        except ImportError:
            # Fall back to proportional if optimizer not available
            strategy = "proportional"

    allocation = {}

    if strategy == "cheapest_first":
        sorted_suppliers = sorted(available_suppliers, key=lambda s: s.cost_per_kg)
        remaining = order_quantity_kg
        for s in sorted_suppliers:
            if remaining <= 0:
                break
            can_supply = s.capacity_kg_per_week * 12  # 12-week planning horizon
            take = min(remaining, can_supply)
            allocation[s.name] = take
            remaining -= take

    elif strategy == "fastest_first":
        sorted_suppliers = sorted(available_suppliers, key=lambda s: s.lead_time_weeks)
        remaining = order_quantity_kg
        for s in sorted_suppliers:
            if remaining <= 0:
                break
            can_supply = s.capacity_kg_per_week * 12
            take = min(remaining, can_supply)
            allocation[s.name] = take
            remaining -= take

    else:  # proportional
        total_capacity = sum(s.capacity_kg_per_week for s in available_suppliers)
        if total_capacity == 0:
            return allocation
        for s in available_suppliers:
            share = s.capacity_kg_per_week / total_capacity
            allocation[s.name] = round(order_quantity_kg * share, 1)

    return allocation


def run_disruption_scenario(
    suppliers: list[Supplier] = None,
    disrupted_supplier: str = "",
    disruption_weeks: int = 0,
    order_quantity_kg: float = 5000.0,
    qualified_only: bool = True,
    allocation_strategy: str = "proportional",
) -> ScenarioResult:
    """
    Run a single disruption scenario through the simulation.

    Args:
        suppliers:           List of Supplier objects (defaults to built-in data)
        disrupted_supplier:  Name of the supplier experiencing disruption ("" for none)
        disruption_weeks:    How many weeks the disrupted supplier is offline
        order_quantity_kg:   Total order size in kilograms
        qualified_only:      If True, only use aerospace-qualified suppliers
        allocation_strategy: "proportional", "cheapest_first", or "fastest_first"

    Returns:
        ScenarioResult with delivery time, cost, allocation, and notes.
    """
    if suppliers is None:
        suppliers = DEFAULT_SUPPLIERS

    notes = []

    # --- Determine available suppliers ---
    available = []
    for s in suppliers:
        if s.name == disrupted_supplier:
            notes.append(
                f"{s.name} ({s.region}) is OFFLINE for {disruption_weeks} weeks."
            )
            continue
        if qualified_only and not s.is_qualified:
            notes.append(
                f"{s.name} ({s.region}) excluded — not aerospace-qualified."
            )
            continue
        available.append(s)

    if not available:
        return ScenarioResult(
            scenario_name=f"Disruption: {disrupted_supplier}",
            disrupted_supplier=disrupted_supplier,
            disruption_weeks=disruption_weeks,
            order_quantity_kg=order_quantity_kg,
            total_delivery_weeks=0,
            total_cost_usd=0,
            suppliers_used=[],
            allocation={},
            feasible=False,
            notes=notes + ["NO SUPPLIERS AVAILABLE. Order cannot be fulfilled."],
        )

    # --- Allocate order ---
    allocation = _allocate_order(available, order_quantity_kg, allocation_strategy)

    # --- Check total capacity ---
    total_allocated = sum(allocation.values())
    feasible = total_allocated >= order_quantity_kg * 0.95  # 5% tolerance
    if not feasible:
        shortfall = order_quantity_kg - total_allocated
        notes.append(
            f"WARNING: Shortfall of {shortfall:.0f} kg. "
            f"Available capacity cannot fully cover the order."
        )

    # --- Run SimPy simulation ---
    env = simpy.Environment()
    delivery_log = {}

    supplier_lookup = {s.name: s for s in available}
    for supplier_name, kg in allocation.items():
        if kg > 0:
            supplier = supplier_lookup[supplier_name]
            env.process(_supplier_process(env, supplier, kg, delivery_log))

    env.run()

    # --- Compute results ---
    if delivery_log:
        total_delivery_weeks = max(
            d["delivery_weeks"] for d in delivery_log.values()
        )
        total_cost = sum(d["cost_usd"] for d in delivery_log.values())
        suppliers_used = list(delivery_log.keys())
    else:
        total_delivery_weeks = 0
        total_cost = 0
        suppliers_used = []

    scenario_name = (
        f"Disruption: {disrupted_supplier} ({disruption_weeks}wk)"
        if disrupted_supplier
        else "Baseline (no disruption)"
    )

    return ScenarioResult(
        scenario_name=scenario_name,
        disrupted_supplier=disrupted_supplier,
        disruption_weeks=disruption_weeks,
        order_quantity_kg=order_quantity_kg,
        total_delivery_weeks=round(total_delivery_weeks, 1),
        total_cost_usd=round(total_cost, 2),
        suppliers_used=suppliers_used,
        allocation=allocation,
        feasible=feasible,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Multi-Scenario Comparison
# ---------------------------------------------------------------------------

def compare_strategies(
    suppliers: list[Supplier] = None,
    disrupted_supplier: str = "",
    disruption_weeks: int = 0,
    order_quantity_kg: float = 5000.0,
    qualified_only: bool = True,
    include_optimal: bool = True,
) -> list[ScenarioResult]:
    """
    Run the same disruption scenario under all allocation strategies.
    Returns a list of ScenarioResult for easy comparison.

    When include_optimal=True, adds LP-optimized strategies (requires
    ortools or scipy).  Falls back gracefully if neither is installed.
    """
    strategies = ["proportional", "cheapest_first", "fastest_first"]
    if include_optimal:
        try:
            import supply_chain_optimizer  # noqa: F401
            strategies += ["optimal_cost", "optimal_time", "optimal_balanced"]
        except ImportError:
            pass
    results = []
    for strategy in strategies:
        result = run_disruption_scenario(
            suppliers=suppliers,
            disrupted_supplier=disrupted_supplier,
            disruption_weeks=disruption_weeks,
            order_quantity_kg=order_quantity_kg,
            qualified_only=qualified_only,
            allocation_strategy=strategy,
        )
        result.scenario_name += f" [{strategy}]"
        results.append(result)
    return results


def format_result_summary(result: ScenarioResult) -> str:
    """Format a ScenarioResult as a human-readable string for LLM context."""
    lines = [
        f"Scenario: {result.scenario_name}",
        f"Order: {result.order_quantity_kg:,.0f} kg titanium",
        f"Feasible: {'Yes' if result.feasible else 'NO'}",
        f"Total Delivery Time: {result.total_delivery_weeks} weeks",
        f"Total Cost: ${result.total_cost_usd:,.2f}",
        f"Suppliers Used: {', '.join(result.suppliers_used)}",
        "Allocation:",
    ]
    for name, kg in result.allocation.items():
        lines.append(f"  - {name}: {kg:,.0f} kg")
    if result.notes:
        lines.append("Notes:")
        for note in result.notes:
            lines.append(f"  - {note}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Standalone Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("TITANIUM SUPPLY CHAIN DISRUPTION SIMULATOR")
    print("=" * 65)

    # --- Baseline: no disruption ---
    print("\n--- BASELINE (No Disruption) ---\n")
    baseline = run_disruption_scenario()
    print(format_result_summary(baseline))

    # --- Scenario: Russia offline for 12 weeks ---
    print("\n--- SCENARIO: Titan-RU Offline (12 weeks) ---\n")
    results = compare_strategies(
        disrupted_supplier="Titan-RU",
        disruption_weeks=12,
        order_quantity_kg=5000,
    )
    for r in results:
        print(format_result_summary(r))
        print()

    # --- Scenario: US offline, allow non-qualified suppliers ---
    print("--- SCENARIO: Titan-US Offline, Non-Qualified Allowed ---\n")
    result = run_disruption_scenario(
        disrupted_supplier="Titan-US",
        disruption_weeks=8,
        order_quantity_kg=5000,
        qualified_only=False,
        allocation_strategy="cheapest_first",
    )
    print(format_result_summary(result))
