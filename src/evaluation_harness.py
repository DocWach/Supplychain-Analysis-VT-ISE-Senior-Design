"""
Evaluation Harness for Titanium Supply Chain Disruption Analyzer
================================================================
Senior Design Project -- Virginia Tech ISE Team 4
Sponsor: The Aerospace Corporation

Evaluates classification accuracy and analysis quality of the LLM
pipeline against hand-labeled ground truth scenarios.

Usage:
    python evaluation_harness.py

Dependencies (optional, for full text metrics):
    pip install bert-score sentence-transformers
"""

from dataclasses import dataclass, field
import sys
import os

# Allow importing sibling modules when run from the src/ directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Ground Truth Data Model
# ---------------------------------------------------------------------------

@dataclass
class GroundTruth:
    scenario_id: str
    title: str
    disruption_text: str
    expected_type: str
    expected_severity: int          # 1-10
    expected_duration_weeks: int
    expected_supplier: str
    reference_analysis: str


# ---------------------------------------------------------------------------
# Example Ground Truth Entries
# ---------------------------------------------------------------------------

GROUND_TRUTH = [
    GroundTruth(
        scenario_id="S01",
        title="Russian Sanctions",
        disruption_text=(
            "Our Russian titanium supplier has been sanctioned due to "
            "escalating geopolitical tensions. We need to fulfill a 5000kg "
            "order for the F-35 program urgently."
        ),
        expected_type="SUPPLIER_FAILURE",
        expected_severity=9,
        expected_duration_weeks=12,
        expected_supplier="Titan-RU",
        reference_analysis=(
            "RECOMMENDATION: Adopt the optimal minimum-cost allocation strategy, "
            "distributing the 5000 kg order across Titan-US, Titan-JP, and Titan-AU "
            "weighted by cost efficiency.\n\n"
            "REASONING: With Titan-RU offline, the remaining qualified suppliers "
            "have a combined 12-week capacity of 31,200 kg, well above the 5000 kg "
            "requirement. The cheapest-first heuristic concentrates too heavily on "
            "Titan-JP, creating single-supplier risk. The LP-optimized cost solution "
            "achieves the lowest total procurement cost while using multiple sources.\n\n"
            "TRADEOFFS: This strategy accepts a slightly longer delivery window "
            "(approximately 6 weeks vs. 5 weeks for fastest-first) in exchange for "
            "roughly 8-12% cost savings and better supplier diversification.\n\n"
            "RISKS: The sanctions environment is volatile; secondary sanctions could "
            "affect Titan-JP or Titan-AU raw-material sourcing from Russia. Quality "
            "consistency across three suppliers must be validated for F-35 "
            "certification requirements.\n\n"
            "CONTINGENCY: Pre-qualify Titan-CN as an emergency backup. Negotiate "
            "buffer-stock agreements with Titan-AU to hedge against further disruptions."
        ),
    ),
    GroundTruth(
        scenario_id="S02",
        title="Japan Earthquake",
        disruption_text=(
            "A major earthquake near Tokyo has disrupted our Japanese titanium "
            "supplier's operations. Estimated recovery time is 6-8 weeks."
        ),
        expected_type="SUPPLIER_FAILURE",
        expected_severity=7,
        expected_duration_weeks=7,
        expected_supplier="Titan-JP",
        reference_analysis=(
            "RECOMMENDATION: Use the fastest-first allocation strategy to minimize "
            "delivery delays, sourcing primarily from Titan-US (4-week lead time) "
            "supplemented by Titan-AU.\n\n"
            "REASONING: Titan-JP normally supplies the highest capacity among "
            "qualified non-Russian sources. Losing it for 7 weeks reduces available "
            "capacity but does not create a shortfall for a 5000 kg order. Titan-RU "
            "remains available and offers the lowest cost, but its 8-week lead time "
            "and geopolitical risk make it less attractive for time-sensitive orders.\n\n"
            "TRADEOFFS: Fastest-first increases total cost by approximately 15-20% "
            "compared to cheapest-first because it prioritizes Titan-US ($32/kg) over "
            "Titan-RU ($22/kg). This is acceptable given the urgency.\n\n"
            "RISKS: Aftershocks or infrastructure damage could extend Titan-JP's "
            "downtime beyond 8 weeks. Port congestion in the region may also delay "
            "shipments from other Asian suppliers.\n\n"
            "CONTINGENCY: Place a partial advance order with Titan-RU as a hedge. "
            "Monitor Titan-JP recovery weekly and shift allocation back as capacity "
            "returns."
        ),
    ),
    GroundTruth(
        scenario_id="S05",
        title="US Factory Fire",
        disruption_text=(
            "A fire at the Titan-US facility in Ohio has shut down production. "
            "The plant will be offline for approximately 10 weeks while repairs "
            "are completed."
        ),
        expected_type="SUPPLIER_FAILURE",
        expected_severity=8,
        expected_duration_weeks=10,
        expected_supplier="Titan-US",
        reference_analysis=(
            "RECOMMENDATION: Use the LP-optimized balanced allocation, splitting "
            "the order between Titan-JP and Titan-RU with a small allocation to "
            "Titan-AU to maintain diversification.\n\n"
            "REASONING: Titan-US produces 800 kg/week, so its loss is manageable "
            "given that Titan-RU (2000 kg/wk) and Titan-JP (1200 kg/wk) together "
            "provide ample capacity. The balanced LP objective keeps cost near "
            "minimum while avoiding the longest possible lead time.\n\n"
            "TRADEOFFS: The balanced strategy costs roughly 5% more than pure "
            "minimum-cost but delivers 1-2 weeks faster. Including Titan-AU "
            "raises the average cost per kg but reduces concentration risk.\n\n"
            "RISKS: Titan-RU carries geopolitical risk; any sudden sanctions "
            "while Titan-US is offline would create a dual-supplier disruption. "
            "Insurance and liability investigations from the fire may affect "
            "Titan-US's return timeline.\n\n"
            "CONTINGENCY: Begin Titan-CN qualification immediately as a "
            "medium-term hedge. Negotiate expedited shipping terms with Titan-JP "
            "to compress lead time if Titan-RU becomes unavailable."
        ),
    ),
]


# ---------------------------------------------------------------------------
# Classification Evaluation
# ---------------------------------------------------------------------------

def evaluate_classification(llm_output: dict, ground_truth: GroundTruth) -> dict:
    """
    Compare LLM classification output to ground truth.

    Args:
        llm_output: dict with keys 'type', 'severity', 'duration_weeks', 'supplier'
        ground_truth: GroundTruth instance

    Returns:
        dict with individual scores and weighted average.
    """
    # Type match (exact)
    type_score = 1.0 if llm_output.get("type", "").upper() == ground_truth.expected_type.upper() else 0.0

    # Severity match (within tolerance)
    sev_diff = abs(llm_output.get("severity", 0) - ground_truth.expected_severity)
    if sev_diff <= 1:
        severity_score = 1.0
    elif sev_diff <= 2:
        severity_score = 0.5
    else:
        severity_score = 0.0

    # Duration match (within tolerance)
    dur_diff = abs(llm_output.get("duration_weeks", 0) - ground_truth.expected_duration_weeks)
    if dur_diff <= 2:
        duration_score = 1.0
    elif dur_diff <= 4:
        duration_score = 0.5
    else:
        duration_score = 0.0

    # Supplier match (exact)
    supplier_score = 1.0 if llm_output.get("supplier", "").strip() == ground_truth.expected_supplier.strip() else 0.0

    weighted_avg = 0.25 * type_score + 0.25 * severity_score + 0.25 * duration_score + 0.25 * supplier_score

    return {
        "scenario_id": ground_truth.scenario_id,
        "type_score": type_score,
        "severity_score": severity_score,
        "duration_score": duration_score,
        "supplier_score": supplier_score,
        "weighted_average": weighted_avg,
    }


# ---------------------------------------------------------------------------
# Analysis Text Evaluation
# ---------------------------------------------------------------------------

def evaluate_analysis(llm_analysis: str, reference_analysis: str) -> dict:
    """
    Compare LLM-generated analysis text to a reference analysis.

    Uses BERTScore and cosine similarity via sentence-transformers when
    available; falls back gracefully if neither library is installed.

    Args:
        llm_analysis:       Text produced by the LLM analyst
        reference_analysis: Expert-written reference text from GroundTruth

    Returns:
        dict with bertscore_f1, cosine_similarity, and combined_score.
    """
    bertscore_f1 = None
    cosine_sim = None

    # BERTScore
    try:
        from bert_score import score as bert_score_fn
        _P, _R, F1 = bert_score_fn(
            [llm_analysis],
            [reference_analysis],
            lang="en",
            verbose=False,
        )
        bertscore_f1 = float(F1[0])
    except ImportError:
        pass
    except Exception as e:
        print(f"  [BERTScore error: {e}]")

    # Cosine similarity via sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer("all-MiniLM-L6-v2")
        emb_llm = model.encode(llm_analysis, convert_to_tensor=True)
        emb_ref = model.encode(reference_analysis, convert_to_tensor=True)
        cosine_sim = float(util.cos_sim(emb_llm, emb_ref)[0][0])
    except ImportError:
        pass
    except Exception as e:
        print(f"  [Cosine similarity error: {e}]")

    if bertscore_f1 is None and cosine_sim is None:
        print(
            "  WARNING: Neither bert-score nor sentence-transformers is installed.\n"
            "  Install with: pip install bert-score sentence-transformers\n"
            "  Returning placeholder scores."
        )
        bertscore_f1 = -1.0
        cosine_sim = -1.0

    # Combined score: average of available metrics
    valid = [v for v in (bertscore_f1, cosine_sim) if v is not None and v >= 0]
    combined = sum(valid) / len(valid) if valid else -1.0

    return {
        "bertscore_f1": bertscore_f1,
        "cosine_similarity": cosine_sim,
        "combined_score": combined,
    }


# ---------------------------------------------------------------------------
# Full Evaluation Run
# ---------------------------------------------------------------------------

def run_evaluation(
    ground_truths: list[GroundTruth],
    llm_classifications: list[dict],
    llm_analyses: list[str],
) -> dict:
    """
    Evaluate a batch of LLM outputs against ground truth.

    Args:
        ground_truths:       List of GroundTruth objects
        llm_classifications: List of dicts with keys type, severity,
                             duration_weeks, supplier (one per scenario)
        llm_analyses:        List of analysis strings (one per scenario)

    Returns:
        dict with per-scenario results and aggregate summary.
    """
    classification_results = []
    analysis_results = []

    for gt, cls, analysis_text in zip(ground_truths, llm_classifications, llm_analyses):
        cls_eval = evaluate_classification(cls, gt)
        classification_results.append(cls_eval)

        ana_eval = evaluate_analysis(analysis_text, gt.reference_analysis)
        ana_eval["scenario_id"] = gt.scenario_id
        analysis_results.append(ana_eval)

    # Aggregate classification scores
    n = len(classification_results)
    avg_cls = {
        "avg_type_score": sum(r["type_score"] for r in classification_results) / n,
        "avg_severity_score": sum(r["severity_score"] for r in classification_results) / n,
        "avg_duration_score": sum(r["duration_score"] for r in classification_results) / n,
        "avg_supplier_score": sum(r["supplier_score"] for r in classification_results) / n,
        "avg_weighted": sum(r["weighted_average"] for r in classification_results) / n,
    }

    # Aggregate analysis scores (only valid metrics)
    valid_bert = [r["bertscore_f1"] for r in analysis_results if r["bertscore_f1"] is not None and r["bertscore_f1"] >= 0]
    valid_cos = [r["cosine_similarity"] for r in analysis_results if r["cosine_similarity"] is not None and r["cosine_similarity"] >= 0]

    avg_ana = {
        "avg_bertscore_f1": sum(valid_bert) / len(valid_bert) if valid_bert else -1.0,
        "avg_cosine_similarity": sum(valid_cos) / len(valid_cos) if valid_cos else -1.0,
    }

    return {
        "classification_results": classification_results,
        "analysis_results": analysis_results,
        "classification_summary": avg_cls,
        "analysis_summary": avg_ana,
        "num_scenarios": n,
    }


# ---------------------------------------------------------------------------
# Report Formatter
# ---------------------------------------------------------------------------

def print_report(evaluation: dict) -> None:
    """Print a human-readable evaluation report."""
    n = evaluation["num_scenarios"]
    cls_summary = evaluation["classification_summary"]
    ana_summary = evaluation["analysis_summary"]

    print("=" * 65)
    print("EVALUATION REPORT")
    print(f"Scenarios evaluated: {n}")
    print("=" * 65)

    print("\n--- Classification Accuracy ---\n")
    print(f"  Type match:      {cls_summary['avg_type_score']:.2f}")
    print(f"  Severity match:  {cls_summary['avg_severity_score']:.2f}")
    print(f"  Duration match:  {cls_summary['avg_duration_score']:.2f}")
    print(f"  Supplier match:  {cls_summary['avg_supplier_score']:.2f}")
    print(f"  Weighted avg:    {cls_summary['avg_weighted']:.2f}")

    for r in evaluation["classification_results"]:
        print(f"\n  [{r['scenario_id']}] type={r['type_score']:.1f}  "
              f"sev={r['severity_score']:.1f}  dur={r['duration_score']:.1f}  "
              f"sup={r['supplier_score']:.1f}  avg={r['weighted_average']:.2f}")

    print("\n--- Analysis Quality ---\n")
    bert = ana_summary["avg_bertscore_f1"]
    cos = ana_summary["avg_cosine_similarity"]
    print(f"  BERTScore F1:       {'N/A (library not installed)' if bert < 0 else f'{bert:.4f}'}")
    print(f"  Cosine similarity:  {'N/A (library not installed)' if cos < 0 else f'{cos:.4f}'}")

    for r in evaluation["analysis_results"]:
        b = r["bertscore_f1"]
        c = r["cosine_similarity"]
        print(f"\n  [{r['scenario_id']}] BERTScore={'N/A' if b is None or b < 0 else f'{b:.4f}'}  "
              f"Cosine={'N/A' if c is None or c < 0 else f'{c:.4f}'}")

    print("\n" + "=" * 65)


# ---------------------------------------------------------------------------
# Standalone Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from supply_chain_sim import run_disruption_scenario, format_result_summary

    print("=" * 65)
    print("EVALUATION HARNESS — Standalone Demo")
    print("=" * 65)

    # --- Run simulations for the 3 ground-truth scenarios ---
    scenario_params = [
        ("S01", "Titan-RU", 12),
        ("S02", "Titan-JP", 7),
        ("S05", "Titan-US", 10),
    ]

    print("\n--- Simulation Results (no LLM) ---\n")
    for sid, supplier, weeks in scenario_params:
        result = run_disruption_scenario(
            disrupted_supplier=supplier,
            disruption_weeks=weeks,
            order_quantity_kg=5000,
        )
        print(f"[{sid}] {result.scenario_name}")
        print(f"  Delivery: {result.total_delivery_weeks} weeks")
        print(f"  Cost:     ${result.total_cost_usd:,.2f}")
        print(f"  Feasible: {result.feasible}")
        print(f"  Suppliers: {', '.join(result.suppliers_used)}")
        print()

    # --- Show evaluation framework structure ---
    print("--- Evaluation Framework ---\n")
    print("Ground truth scenarios loaded:", len(GROUND_TRUTH))
    for gt in GROUND_TRUTH:
        print(f"  [{gt.scenario_id}] {gt.title}")
        print(f"    Type: {gt.expected_type}  Severity: {gt.expected_severity}/10  "
              f"Duration: {gt.expected_duration_weeks} wk  Supplier: {gt.expected_supplier}")

    # --- Demo: evaluate with mock perfect classifications ---
    print("\n--- Demo: Perfect Classification Scores ---\n")

    mock_classifications = [
        {"type": "SUPPLIER_FAILURE", "severity": 9, "duration_weeks": 12, "supplier": "Titan-RU"},
        {"type": "SUPPLIER_FAILURE", "severity": 7, "duration_weeks": 7, "supplier": "Titan-JP"},
        {"type": "SUPPLIER_FAILURE", "severity": 8, "duration_weeks": 10, "supplier": "Titan-US"},
    ]

    # Use the reference analyses as the LLM output to show perfect text scores
    mock_analyses = [gt.reference_analysis for gt in GROUND_TRUTH]

    evaluation = run_evaluation(GROUND_TRUTH, mock_classifications, mock_analyses)
    print_report(evaluation)

    # --- Show what metrics would be computed with real LLM output ---
    print("\n--- Metrics Computed ---\n")
    print("Classification metrics (per scenario):")
    print("  - type_score:       1.0 if exact match, else 0.0")
    print("  - severity_score:   1.0 if within +/-1, 0.5 if within +/-2, else 0.0")
    print("  - duration_score:   1.0 if within +/-2 wk, 0.5 if within +/-4, else 0.0")
    print("  - supplier_score:   1.0 if exact match, else 0.0")
    print("  - weighted_average: 25% each\n")
    print("Analysis quality metrics (per scenario):")
    print("  - bertscore_f1:       Semantic similarity via BERTScore")
    print("  - cosine_similarity:  Embedding cosine similarity via sentence-transformers")
    print("  - combined_score:     Average of available metrics")
