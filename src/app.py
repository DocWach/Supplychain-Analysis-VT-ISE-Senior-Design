"""
Titanium Supply Chain Disruption Analyzer
==========================================
Senior Design Project — Virginia Tech ISE Team 4
Sponsor: The Aerospace Corporation

Run with:
    cd src
    streamlit run app.py

Requirements:
    pip install streamlit openai simpy
"""

import streamlit as st
import json
import time

from supply_chain_sim import (
    DEFAULT_SUPPLIERS,
    Supplier,
    load_suppliers,
    run_disruption_scenario,
    compare_strategies,
    format_result_summary,
)
from llm_analyst import (
    render_model_selector,
    detect_available_providers,
    create_analyst,
    auto_select_provider,
    classify_disruption,
    analyze,
    analyze_with_comparison,
    assess_risk,
    full_pipeline,
)


# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Titanium Supply Chain Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #861f41 0%, #4a0e23 100%);
        color: white;
        padding: 20px 28px;
        border-radius: 10px;
        margin-bottom: 24px;
    }
    .main-header h1 { color: white; font-size: 24px; margin: 0; }
    .main-header p { color: rgba(255,255,255,0.85); font-size: 14px; margin: 4px 0 0 0; }
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 4px solid #861f41;
    }
    .status-online { color: #27ae60; font-weight: 600; }
    .status-offline { color: #e74c3c; font-weight: 600; }
    .status-excluded { color: #f39c12; font-weight: 600; }
    .pipeline-step {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        margin: 2px;
    }
    .best-badge {
        background: #e8f8f0;
        color: #1a9a5a;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown("""
<div class="main-header">
    <h1>Titanium Supply Chain Disruption Analyzer</h1>
    <p>Virginia Tech ISE Senior Design — The Aerospace Corporation</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar: LLM Provider & Model Selection
# ---------------------------------------------------------------------------

st.sidebar.markdown("## Configuration")

analyst = render_model_selector()

st.sidebar.markdown("---")
st.sidebar.markdown("### Simulation Settings")

qualified_only = st.sidebar.checkbox(
    "Aerospace-qualified suppliers only",
    value=True,
    help="Exclude suppliers without aerospace qualification (e.g., Titan-CN).",
)

order_qty = st.sidebar.number_input(
    "Order Quantity (kg)",
    min_value=100,
    max_value=50000,
    value=5000,
    step=100,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:11px; color:#888;'>"
    "Prototype — Not validated for production decisions.<br>"
    "All recommendations require human review."
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------

tab_pipeline, tab_manual, tab_suppliers, tab_about = st.tabs([
    "Full Pipeline",
    "Manual Scenario",
    "Supplier Database",
    "About",
])


# ---------------------------------------------------------------------------
# Tab 1: Full Pipeline (Free-text -> Classify -> Simulate -> Analyze)
# ---------------------------------------------------------------------------

with tab_pipeline:

    st.markdown("### Describe a Supply Chain Disruption")
    st.caption(
        "Enter a free-text description. The system will classify the disruption, "
        "run simulations across allocation strategies, and provide AI analysis."
    )

    user_input = st.text_area(
        "Disruption Description",
        placeholder=(
            "Example: Russia has imposed export restrictions on titanium sponge "
            "due to escalating geopolitical tensions. Expected to last at least 3 months."
        ),
        height=100,
        label_visibility="collapsed",
    )

    col_run, col_example = st.columns([1, 3])
    with col_run:
        run_pipeline = st.button(
            "Run Full Analysis",
            type="primary",
            use_container_width=True,
            disabled=not analyst or not user_input.strip(),
        )
    with col_example:
        examples = {
            "Russian sanctions": (
                "Our Russian titanium supplier has been sanctioned due to "
                "geopolitical tensions. We need to fulfill a 5000kg order "
                "for the F-35 program urgently."
            ),
            "Japanese earthquake": (
                "A major earthquake near Tokyo has disrupted our Japanese "
                "titanium supplier's operations. Estimated recovery time "
                "is 6-8 weeks."
            ),
            "US factory fire": (
                "A fire at the Titan-US facility in Ohio has shut down "
                "production. The plant will be offline for approximately "
                "10 weeks while repairs are completed."
            ),
            "Demand spike": (
                "Boeing has announced a 40% increase in 787 production rate, "
                "causing a surge in titanium demand across the aerospace "
                "supply chain."
            ),
        }
        selected_example = st.selectbox(
            "Or try an example:",
            options=[""] + list(examples.keys()),
            label_visibility="collapsed",
        )
        if selected_example and selected_example in examples:
            user_input = examples[selected_example]
            st.info(f"Loaded example: {selected_example}")

    if not analyst:
        st.warning(
            "No LLM provider configured. Set up a provider in the sidebar "
            "to enable AI analysis. Simulation-only mode is available in "
            "the Manual Scenario tab."
        )

    if run_pipeline and analyst and user_input.strip():

        # --- Step 1: Classify ---
        with st.status("Running full analysis pipeline...", expanded=True) as status:

            st.write("**Step 1/4:** Classifying disruption...")
            t0 = time.time()
            try:
                classification_raw = classify_disruption(analyst, user_input)
                try:
                    classification = json.loads(classification_raw)
                except json.JSONDecodeError:
                    classification = {
                        "category": "UNKNOWN",
                        "severity": "medium",
                        "estimated_duration_weeks": 8,
                        "summary": classification_raw,
                    }
                t1 = time.time()
                st.write(f"Classified in {t1-t0:.1f}s")
            except Exception as e:
                st.error(f"Classification failed: {e}")
                st.stop()

            # --- Step 2: Map to supplier ---
            st.write("**Step 2/4:** Mapping to supplier and running simulation...")
            disrupted = ""
            desc_lower = user_input.lower()
            supplier_keywords = {
                "Titan-RU": ["russia", "russian", "moscow"],
                "Titan-US": ["us", "united states", "american", "ohio", "domestic"],
                "Titan-JP": ["japan", "japanese", "tokyo", "earthquake"],
                "Titan-CN": ["china", "chinese", "beijing"],
                "Titan-AU": ["australia", "australian"],
            }
            for supplier_name, keywords in supplier_keywords.items():
                if any(kw in desc_lower for kw in keywords):
                    disrupted = supplier_name
                    break

            duration = classification.get("estimated_duration_weeks", 8)

            sim_results = compare_strategies(
                disrupted_supplier=disrupted,
                disruption_weeks=duration,
                order_quantity_kg=order_qty,
                qualified_only=qualified_only,
            )
            sim_context = "\n\n".join(format_result_summary(r) for r in sim_results)
            t2 = time.time()
            st.write(f"Simulation complete in {t2-t1:.1f}s")

            # --- Step 3: Analyze ---
            st.write("**Step 3/4:** AI analyzing results...")
            try:
                analysis_response = analyze(
                    analyst,
                    sim_context,
                    f"The disruption is: {user_input}\n\n"
                    f"Classification: {classification.get('category', 'UNKNOWN')} "
                    f"(severity: {classification.get('severity', 'unknown')})\n\n"
                    f"Which allocation strategy do you recommend and why?",
                )
                t3 = time.time()
                st.write(f"Analysis complete in {t3-t2:.1f}s")
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                analysis_response = None

            # --- Step 4: Risk assessment ---
            st.write("**Step 4/4:** Assessing risk...")
            try:
                risk_response = assess_risk(analyst, sim_context)
                t4 = time.time()
                st.write(f"Risk assessment complete in {t4-t3:.1f}s")
            except Exception as e:
                st.error(f"Risk assessment failed: {e}")
                risk_response = None

            status.update(label=f"Analysis complete ({t4-t0:.1f}s total)", state="complete")

        # --- Display Results ---
        st.markdown("---")

        # Classification
        col_cat, col_sev, col_dur, col_sup = st.columns(4)
        with col_cat:
            cat = classification.get("category", "UNKNOWN")
            cat_display = cat.replace("_", " ").title()
            st.metric("Disruption Type", cat_display)
        with col_sev:
            sev = classification.get("severity", "unknown")
            sev_colors = {"low": "normal", "medium": "normal", "high": "inverse", "critical": "inverse"}
            st.metric("Severity", sev.upper(), delta_color=sev_colors.get(sev, "normal"))
        with col_dur:
            st.metric("Est. Duration", f"{duration} weeks")
        with col_sup:
            st.metric("Affected Supplier", disrupted if disrupted else "None identified")

        st.markdown("---")

        # Simulation comparison
        st.markdown("### Simulation Results")

        # Find best strategy (lowest cost among feasible)
        feasible = [r for r in sim_results if r.feasible]
        best_idx = -1
        if feasible:
            min_cost = min(r.total_cost_usd for r in feasible)
            for i, r in enumerate(sim_results):
                if r.feasible and r.total_cost_usd == min_cost:
                    best_idx = i
                    break

        strategy_cols = st.columns(len(sim_results))
        for i, (col, result) in enumerate(zip(strategy_cols, sim_results)):
            with col:
                strategy_name = result.scenario_name.split("[")[-1].rstrip("]") if "[" in result.scenario_name else "Strategy"
                is_best = i == best_idx

                if is_best:
                    st.success(f"**{strategy_name}** — Best Option")
                elif result.feasible:
                    st.info(f"**{strategy_name}**")
                else:
                    st.error(f"**{strategy_name}** — Infeasible")

                st.metric("Delivery", f"{result.total_delivery_weeks} weeks")
                st.metric("Total Cost", f"${result.total_cost_usd:,.2f}")
                st.metric("Cost/kg", f"${result.total_cost_usd / order_qty:.2f}")
                st.metric("Suppliers", f"{len(result.suppliers_used)}")

                # Allocation breakdown
                if result.allocation:
                    st.caption("Allocation:")
                    for name, kg in result.allocation.items():
                        pct = (kg / order_qty) * 100
                        st.progress(pct / 100, text=f"{name}: {kg:,.0f} kg ({pct:.0f}%)")

        # Notes
        all_notes = []
        for r in sim_results:
            all_notes.extend(r.notes)
        if all_notes:
            unique_notes = list(dict.fromkeys(all_notes))
            with st.expander("Simulation Notes"):
                for note in unique_notes:
                    st.write(f"- {note}")

        st.markdown("---")

        # AI Analysis
        col_analysis, col_risk = st.columns([3, 2])

        with col_analysis:
            st.markdown("### AI Strategy Analysis")
            if analysis_response:
                st.markdown(analysis_response)
            else:
                st.warning("Analysis unavailable.")

        with col_risk:
            st.markdown("### Risk Assessment")
            if risk_response:
                st.markdown(risk_response)
            else:
                st.warning("Risk assessment unavailable.")

        # Raw prompt context (expandable for transparency)
        with st.expander("View prompt context sent to LLM"):
            st.code(sim_context, language=None)


# ---------------------------------------------------------------------------
# Tab 2: Manual Scenario (No LLM required)
# ---------------------------------------------------------------------------

with tab_manual:

    st.markdown("### Manual Scenario Configuration")
    st.caption("Run simulations without AI. Select disruption parameters directly.")

    col_config, col_results = st.columns([1, 2])

    with col_config:
        disrupted_supplier = st.selectbox(
            "Disrupted Supplier",
            options=["(None - Baseline)"] + [s.name for s in DEFAULT_SUPPLIERS],
        )
        if disrupted_supplier == "(None - Baseline)":
            disrupted_supplier = ""

        disruption_weeks = st.slider("Disruption Duration (weeks)", 1, 52, 12)

        manual_order_qty = st.number_input(
            "Order Quantity (kg)",
            min_value=100,
            max_value=50000,
            value=order_qty,
            step=100,
            key="manual_order_qty",
        )

        manual_qualified = st.checkbox(
            "Qualified suppliers only",
            value=qualified_only,
            key="manual_qualified",
        )

        run_manual = st.button(
            "Run Simulation",
            type="primary",
            use_container_width=True,
            key="run_manual",
        )

    with col_results:
        if run_manual:
            results = compare_strategies(
                disrupted_supplier=disrupted_supplier,
                disruption_weeks=disruption_weeks,
                order_quantity_kg=manual_order_qty,
                qualified_only=manual_qualified,
            )

            # Summary table
            table_data = []
            feasible_results = [r for r in results if r.feasible]
            best_cost = min((r.total_cost_usd for r in feasible_results), default=None)

            for r in results:
                strategy = r.scenario_name.split("[")[-1].rstrip("]") if "[" in r.scenario_name else r.scenario_name
                is_best = r.feasible and r.total_cost_usd == best_cost
                table_data.append({
                    "Strategy": f"{'* ' if is_best else ''}{strategy}",
                    "Delivery (wk)": r.total_delivery_weeks,
                    "Cost ($)": f"${r.total_cost_usd:,.2f}",
                    "$/kg": f"${r.total_cost_usd / manual_order_qty:.2f}",
                    "Suppliers": ", ".join(r.suppliers_used),
                    "Feasible": "Yes" if r.feasible else "No",
                })

            st.markdown("#### Strategy Comparison")
            st.dataframe(table_data, use_container_width=True, hide_index=True)

            # Detailed cards
            for r in results:
                strategy = r.scenario_name.split("[")[-1].rstrip("]") if "[" in r.scenario_name else r.scenario_name
                with st.expander(f"{strategy} — ${r.total_cost_usd:,.2f} / {r.total_delivery_weeks} wk"):
                    st.text(format_result_summary(r))

            # Optional: send to LLM if available
            if analyst:
                st.markdown("---")
                if st.button("Send results to AI for analysis", key="manual_ai"):
                    with st.spinner("AI analyzing..."):
                        sim_context = "\n\n".join(format_result_summary(r) for r in results)
                        response = analyze_with_comparison(
                            analyst,
                            results,
                            "Which allocation strategy do you recommend and why?",
                        )
                    st.markdown("#### AI Analysis")
                    st.markdown(response)
        else:
            st.info("Configure a scenario and click **Run Simulation** to see results.")


# ---------------------------------------------------------------------------
# Tab 3: Supplier Database
# ---------------------------------------------------------------------------

with tab_suppliers:

    st.markdown("### Supplier Database")
    st.caption("Current titanium supplier data used by the simulation.")

    supplier_data = []
    for s in DEFAULT_SUPPLIERS:
        supplier_data.append({
            "Name": s.name,
            "Region": s.region,
            "Lead Time (wk)": s.lead_time_weeks,
            "Capacity (kg/wk)": f"{s.capacity_kg_per_week:,.0f}",
            "Cost ($/kg)": f"${s.cost_per_kg:.2f}",
            "Quality": f"{s.quality_rating:.0%}",
            "Qualified": "Yes" if s.is_qualified else "No",
        })

    st.dataframe(supplier_data, use_container_width=True, hide_index=True)

    # Baseline metrics
    st.markdown("#### Baseline Analysis (No Disruption)")
    baseline = run_disruption_scenario(order_quantity_kg=order_qty, qualified_only=qualified_only)

    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        st.metric("Delivery Time", f"{baseline.total_delivery_weeks} wk")
    with col_b2:
        st.metric("Total Cost", f"${baseline.total_cost_usd:,.2f}")
    with col_b3:
        st.metric("Cost/kg", f"${baseline.total_cost_usd / order_qty:.2f}")
    with col_b4:
        st.metric("Active Suppliers", f"{len(baseline.suppliers_used)}")

    with st.expander("Baseline allocation detail"):
        st.text(format_result_summary(baseline))


# ---------------------------------------------------------------------------
# Tab 4: About
# ---------------------------------------------------------------------------

with tab_about:

    st.markdown("### About This Tool")

    st.markdown("""
**Project:** AI Risk Modeling for Titanium Supply Chains

**Team:** Virginia Tech ISE Senior Design Team 4
- Boleslav Econa
- Jonathan Michael
- Camilo Gomez
- Juan Oleaga Alba

**Sponsor:** The Aerospace Corporation

**Faculty Advisor:** Paul Wach

---

#### System Architecture

This tool combines discrete-event simulation with large language model
analysis to evaluate titanium supply chain disruptions.

**Pipeline:**
1. **Classification** — LLM classifies free-text disruption descriptions
   into structured categories (supplier failure, logistics delay, demand spike,
   quality issue) with severity and estimated duration.
2. **Simulation** — SimPy discrete-event simulation models the supply chain
   with multiple suppliers, allocation strategies, and capacity constraints.
3. **Analysis** — LLM interprets simulation results in business terms and
   recommends an allocation strategy with reasoning.
4. **Risk Assessment** — LLM evaluates risks not captured by the simulation
   (geopolitical, regulatory, concentration risk).

**Allocation Strategies:**
- **Proportional** — Split order by supplier capacity share
- **Cheapest First** — Prioritize lowest-cost suppliers
- **Fastest First** — Prioritize shortest lead-time suppliers

---

#### Limitations

- This is a **research prototype** and is not validated for production
  procurement decisions.
- Simulation uses simplified supplier models that do not capture all
  real-world dynamics.
- LLM analysis may produce plausible but incorrect recommendations.
- **All outputs require human review** before action.
- Supply chain data is illustrative, not based on actual supplier contracts.

---

#### Technology Stack

| Component | Technology |
|-----------|-----------|
| Simulation | SimPy (Python) |
| LLM Integration | OpenAI-compatible API |
| Default Provider | Groq (Llama 3.3 70B) |
| UI Framework | Streamlit |
| Language | Python 3.10+ |
""")

    # Provider status
    st.markdown("#### Current LLM Provider Status")
    providers = detect_available_providers()
    for p in providers:
        status_icon = "+" if p["status"] == "available" else "-"
        st.markdown(f"- {p['label']}: **{p['status']}** — {p['reason']}")
