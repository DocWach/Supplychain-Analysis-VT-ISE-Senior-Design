"""
LLM Supply Chain Analyst Module
================================
Senior Design Project — Virginia Tech ISE Team 4
Sponsor: The Aerospace Corporation

This module connects the SimPy simulation output to a language model
for interpretation, recommendation, and risk analysis.

Setup:
    1. pip install openai
    2. Get a free API key from https://console.groq.com
    3. Set your key:
       Option A (environment variable - recommended):
           Windows:  set GROQ_API_KEY=gsk_your_key_here
           Mac/Linux: export GROQ_API_KEY=gsk_your_key_here
       Option B (for quick testing only - do NOT commit to git):
           Pass api_key="gsk_..." to create_analyst()

Usage:
    from supply_chain_sim import compare_strategies, format_result_summary
    from llm_analyst import create_analyst, analyze, analyze_with_comparison

    analyst = create_analyst()

    # Single scenario analysis
    result = run_disruption_scenario(disrupted_supplier="Titan-RU", ...)
    summary = format_result_summary(result)
    response = analyze(analyst, summary, "What are the risks?")

    # Multi-strategy comparison (recommended)
    results = compare_strategies(disrupted_supplier="Titan-RU", ...)
    response = analyze_with_comparison(analyst, results, "Which strategy is best?")
"""

import os
from dataclasses import dataclass

try:
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "The 'openai' package is required.\n"
        "Install it with: pip install openai"
    )

# Import simulation types for formatting
try:
    from supply_chain_sim import ScenarioResult, format_result_summary
except ImportError:
    # Allow module to load even if supply_chain_sim is not in path
    ScenarioResult = None
    format_result_summary = None


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Supported providers and their settings.
# All use the OpenAI-compatible API format, so switching is a URL change.
PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.3-70b-versatile",
        "env_key": "GROQ_API_KEY",
        "label": "Groq (Free Cloud)",
        "models": [
            {"id": "llama-3.3-70b-versatile",  "label": "Llama 3.3 70B",     "size": "70B", "speed": "fast"},
            {"id": "llama-3.1-8b-instant",      "label": "Llama 3.1 8B",      "size": "8B",  "speed": "fastest"},
            {"id": "mixtral-8x7b-32768",        "label": "Mixtral 8x7B",      "size": "47B", "speed": "fast"},
            {"id": "gemma2-9b-it",              "label": "Gemma 2 9B",        "size": "9B",  "speed": "fast"},
        ],
    },
    "cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "default_model": "llama-3.3-70b",
        "env_key": "CEREBRAS_API_KEY",
        "label": "Cerebras (Free Cloud)",
        "models": [
            {"id": "llama-3.3-70b",  "label": "Llama 3.3 70B",  "size": "70B", "speed": "fastest"},
            {"id": "llama-3.1-8b",   "label": "Llama 3.1 8B",   "size": "8B",  "speed": "fastest"},
        ],
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "default_model": "llama3.2",
        "env_key": None,  # No key needed for local
        "label": "Ollama (Local)",
        "models": [
            {"id": "llama3.2",       "label": "Llama 3.2 3B",    "size": "3B",   "speed": "moderate"},
            {"id": "llama3.1",       "label": "Llama 3.1 8B",    "size": "8B",   "speed": "slow"},
            {"id": "phi3.5",         "label": "Phi 3.5 Mini",    "size": "3.8B", "speed": "moderate"},
            {"id": "mistral",        "label": "Mistral 7B",      "size": "7B",   "speed": "slow"},
            {"id": "gemma2:2b",      "label": "Gemma 2 2B",      "size": "2B",   "speed": "fast"},
        ],
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "env_key": "OPENAI_API_KEY",
        "label": "OpenAI (Paid)",
        "models": [
            {"id": "gpt-4o-mini",    "label": "GPT-4o Mini",     "size": "small", "speed": "fast"},
            {"id": "gpt-4o",         "label": "GPT-4o",          "size": "large", "speed": "moderate"},
            {"id": "gpt-4.1-nano",   "label": "GPT-4.1 Nano",   "size": "nano",  "speed": "fastest"},
        ],
    },
}


# ---------------------------------------------------------------------------
# Provider Auto-Detection
# ---------------------------------------------------------------------------

def detect_available_providers() -> list[dict]:
    """
    Detect which LLM providers are currently available.

    Checks for API keys in environment variables and whether Ollama
    is running locally. Returns a list of available providers with
    their details, sorted by recommendation order.

    Returns:
        List of dicts with keys: provider, label, models, status, reason

    Example:
        available = detect_available_providers()
        for p in available:
            print(f"{p['label']} - {p['status']}")
    """
    available = []

    for name, config in PROVIDERS.items():
        entry = {
            "provider": name,
            "label": config["label"],
            "models": config["models"],
            "default_model": config["default_model"],
        }

        if name == "ollama":
            # Check if Ollama is running locally
            try:
                import urllib.request
                req = urllib.request.Request(
                    "http://localhost:11434/api/tags",
                    method="GET",
                )
                with urllib.request.urlopen(req, timeout=2) as resp:
                    if resp.status == 200:
                        import json
                        data = json.loads(resp.read())
                        # Replace static model list with actually installed models
                        installed = []
                        for m in data.get("models", []):
                            model_name = m.get("name", "")
                            installed.append({
                                "id": model_name,
                                "label": model_name,
                                "size": _format_size(m.get("size", 0)),
                                "speed": "local",
                            })
                        if installed:
                            entry["models"] = installed
                            entry["default_model"] = installed[0]["id"]
                        entry["status"] = "available"
                        entry["reason"] = f"{len(installed)} model(s) installed"
                    else:
                        entry["status"] = "unavailable"
                        entry["reason"] = "Ollama not responding"
            except Exception:
                entry["status"] = "unavailable"
                entry["reason"] = "Ollama not running (install from ollama.com)"
        else:
            env_key = config["env_key"]
            if env_key and os.environ.get(env_key):
                entry["status"] = "available"
                entry["reason"] = f"{env_key} found"
            elif env_key:
                entry["status"] = "unavailable"
                entry["reason"] = f"Set {env_key} environment variable"
            else:
                entry["status"] = "unavailable"
                entry["reason"] = "No API key configured"

        available.append(entry)

    # Sort: available first, then by recommendation order
    priority = {"groq": 0, "cerebras": 1, "ollama": 2, "openai": 3}
    available.sort(key=lambda p: (
        0 if p["status"] == "available" else 1,
        priority.get(p["provider"], 99),
    ))

    return available


def auto_select_provider() -> tuple[str, str]:
    """
    Automatically select the best available provider and model.

    Priority order: groq > cerebras > ollama > openai

    Returns:
        Tuple of (provider_name, model_id)

    Raises:
        RuntimeError if no providers are available.

    Example:
        provider, model = auto_select_provider()
        analyst = create_analyst(provider, model=model)
    """
    available = detect_available_providers()
    for entry in available:
        if entry["status"] == "available":
            return entry["provider"], entry["default_model"]

    raise RuntimeError(
        "No LLM providers available. Set up at least one:\n\n"
        "  Option 1 (Recommended - Free):\n"
        "    1. Go to https://console.groq.com\n"
        "    2. Create account and generate API key\n"
        "    3. set GROQ_API_KEY=gsk_your_key_here\n\n"
        "  Option 2 (Local - Free):\n"
        "    1. Install Ollama from https://ollama.com\n"
        "    2. Run: ollama pull llama3.2\n"
        "    3. Run: ollama serve\n\n"
        "  Option 3 (Free):\n"
        "    1. Go to https://cloud.cerebras.ai\n"
        "    2. Create account and generate API key\n"
        "    3. set CEREBRAS_API_KEY=your_key_here"
    )


def _format_size(size_bytes: int) -> str:
    """Format byte count as human-readable size."""
    if size_bytes == 0:
        return "unknown"
    gb = size_bytes / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.1f}GB"
    mb = size_bytes / (1024 ** 2)
    return f"{mb:.0f}MB"


# ---------------------------------------------------------------------------
# System Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_ANALYST = """You are a senior supply chain analyst for an aerospace manufacturer that sources titanium components.

Your role:
- Interpret simulation results in business terms that a procurement manager can act on.
- Recommend ONE allocation strategy with clear reasoning.
- Quantify tradeoffs (cost vs. time vs. risk) using the numbers provided.
- Identify risks NOT captured by the simulation (geopolitical, quality, regulatory).
- Be direct and specific. Do not hedge with "it depends" without then giving a concrete recommendation.

Output format:
1. RECOMMENDATION: State the recommended strategy in one sentence.
2. REASONING: Explain why, citing specific numbers from the simulation.
3. TRADEOFFS: What does this strategy sacrifice compared to alternatives?
4. RISKS: What could go wrong that the simulation does not model?
5. CONTINGENCY: What should the manufacturer do if this strategy fails?

Keep your response under 400 words. Use plain language, not jargon."""

SYSTEM_PROMPT_CLASSIFIER = """You are a supply chain disruption classifier for aerospace titanium procurement.

Given a description of a supply chain event, classify it into exactly ONE of these categories:

- SUPPLIER_FAILURE: A supplier cannot deliver (factory shutdown, bankruptcy, sanctions)
- LOGISTICS_DELAY: Transportation or shipping disruption (port closure, shipping delays)
- DEMAND_SPIKE: Unexpected increase in titanium demand
- QUALITY_ISSUE: Material fails inspection or certification requirements

Respond with ONLY a JSON object in this exact format:
{"category": "SUPPLIER_FAILURE", "severity": "high", "estimated_duration_weeks": 12, "summary": "One sentence description"}

Severity must be one of: low, medium, high, critical.
Estimated duration must be an integer between 1 and 52."""

SYSTEM_PROMPT_RISK = """You are a risk assessment specialist for aerospace supply chains.

Given simulation results for a titanium sourcing disruption, evaluate the overall risk level and provide a structured assessment.

Output format:
1. RISK LEVEL: LOW / MEDIUM / HIGH / CRITICAL
2. SUPPLY CONTINUITY: Can the order be fulfilled on time? What is the confidence level?
3. COST IMPACT: How does the disrupted cost compare to baseline? Is it acceptable?
4. CONCENTRATION RISK: Is the recovery plan too dependent on a single supplier?
5. RECOMMENDATION: One paragraph, actionable, addressed to a procurement manager.

Be concise. Under 250 words."""


# ---------------------------------------------------------------------------
# Analyst Interface
# ---------------------------------------------------------------------------

@dataclass
class Analyst:
    """Holds the LLM client and configuration."""
    client: OpenAI
    model: str
    provider: str


def create_analyst(
    provider: str = "groq",
    api_key: str = None,
    model: str = None,
) -> Analyst:
    """
    Create an LLM analyst connection.

    Args:
        provider: One of "groq", "cerebras", "ollama", "openai"
        api_key:  API key (or set via environment variable)
        model:    Model name (defaults to provider's recommended model)

    Returns:
        Analyst object to pass to analysis functions.

    Example:
        analyst = create_analyst()                          # Groq default
        analyst = create_analyst("ollama")                  # Local model
        analyst = create_analyst("groq", api_key="gsk_...") # Explicit key
    """
    if provider not in PROVIDERS:
        raise ValueError(
            f"Unknown provider '{provider}'. "
            f"Choose from: {', '.join(PROVIDERS.keys())}"
        )

    config = PROVIDERS[provider]

    # Resolve API key
    if api_key is None:
        env_key = config["env_key"]
        if env_key is not None:
            api_key = os.environ.get(env_key)
            if api_key is None:
                raise ValueError(
                    f"No API key found. Either:\n"
                    f"  1. Set the environment variable {env_key}\n"
                    f"  2. Pass api_key='...' to create_analyst()\n"
                    f"  3. Get a free key at https://console.groq.com"
                )
        else:
            api_key = "not-needed"  # Local providers like Ollama

    resolved_model = model or config["default_model"]

    client = OpenAI(
        api_key=api_key,
        base_url=config["base_url"],
    )

    return Analyst(client=client, model=resolved_model, provider=provider)


# ---------------------------------------------------------------------------
# Core Analysis Functions
# ---------------------------------------------------------------------------

def _call_llm(analyst: Analyst, system_prompt: str, user_message: str) -> str:
    """Send a message to the LLM and return the response text."""
    response = analyst.client.chat.completions.create(
        model=analyst.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def analyze(analyst: Analyst, simulation_summary: str, question: str) -> str:
    """
    Analyze simulation results with a free-form question.

    Args:
        analyst:             Analyst object from create_analyst()
        simulation_summary:  Plain text simulation output (from format_result_summary)
        question:            What you want the analyst to address

    Returns:
        LLM response as a string.

    Example:
        response = analyze(analyst, summary, "Which strategy minimizes risk?")
    """
    user_message = f"{question}\n\n--- Simulation Results ---\n{simulation_summary}"
    return _call_llm(analyst, SYSTEM_PROMPT_ANALYST, user_message)


def analyze_with_comparison(
    analyst: Analyst,
    results: list,
    question: str = "Which allocation strategy do you recommend and why?",
) -> str:
    """
    Analyze multiple strategy results side by side.

    Args:
        analyst:   Analyst object from create_analyst()
        results:   List of ScenarioResult objects (from compare_strategies)
        question:  What you want the analyst to address

    Returns:
        LLM response as a string.

    Example:
        results = compare_strategies(disrupted_supplier="Titan-RU", ...)
        response = analyze_with_comparison(analyst, results)
    """
    if format_result_summary is None:
        raise ImportError("supply_chain_sim must be importable to use this function.")

    summaries = "\n\n".join(format_result_summary(r) for r in results)
    user_message = f"{question}\n\n--- Simulation Results ---\n{summaries}"
    return _call_llm(analyst, SYSTEM_PROMPT_ANALYST, user_message)


def classify_disruption(analyst: Analyst, description: str) -> str:
    """
    Classify a free-text disruption description into a structured category.

    This is the "first agent" in the pipeline: it takes unstructured user
    input and produces a structured classification that determines how the
    simulation should be configured.

    Args:
        analyst:      Analyst object from create_analyst()
        description:  Free-text description of the disruption event

    Returns:
        JSON string with category, severity, duration, and summary.

    Example:
        result = classify_disruption(analyst, "Russia banned titanium exports")
        # Returns: {"category": "SUPPLIER_FAILURE", "severity": "critical", ...}
    """
    return _call_llm(analyst, SYSTEM_PROMPT_CLASSIFIER, description)


def assess_risk(analyst: Analyst, simulation_summary: str) -> str:
    """
    Perform a risk assessment on simulation results.

    Args:
        analyst:             Analyst object from create_analyst()
        simulation_summary:  Plain text simulation output

    Returns:
        Structured risk assessment as a string.

    Example:
        response = assess_risk(analyst, summary)
    """
    return _call_llm(analyst, SYSTEM_PROMPT_RISK, simulation_summary)


# ---------------------------------------------------------------------------
# Full Pipeline: Classify -> Simulate -> Analyze
# ---------------------------------------------------------------------------

def full_pipeline(
    analyst: Analyst,
    user_description: str,
    suppliers: list = None,
    order_quantity_kg: float = 5000.0,
    qualified_only: bool = True,
) -> dict:
    """
    Run the complete analysis pipeline from free-text input to recommendation.

    This connects all components:
        1. Classify the disruption (LLM)
        2. Run simulation across all strategies (SimPy)
        3. Analyze results and recommend (LLM)
        4. Assess risk (LLM)

    Args:
        analyst:           Analyst object from create_analyst()
        user_description:  Free-text description of the disruption
        suppliers:         Optional supplier list (defaults to built-in)
        order_quantity_kg: Order size in kg
        qualified_only:    Only use aerospace-qualified suppliers

    Returns:
        Dictionary with keys: classification, simulation_results,
        analysis, risk_assessment, prompt_context

    Example:
        result = full_pipeline(analyst, "Russia has banned titanium exports for 6 months")
        print(result["analysis"])
    """
    # Lazy import to avoid circular dependency
    from supply_chain_sim import compare_strategies, format_result_summary
    import json

    # Step 1: Classify the disruption
    classification_raw = classify_disruption(analyst, user_description)
    try:
        classification = json.loads(classification_raw)
    except json.JSONDecodeError:
        classification = {
            "category": "UNKNOWN",
            "severity": "medium",
            "estimated_duration_weeks": 8,
            "summary": classification_raw,
        }

    # Step 2: Map classification to simulation parameters
    # Determine which supplier is affected based on the description
    # (Simple keyword matching — students can improve this)
    disrupted = ""
    desc_lower = user_description.lower()
    supplier_keywords = {
        "Titan-RU": ["russia", "russian", "moscow"],
        "Titan-US": ["us", "united states", "american", "domestic"],
        "Titan-JP": ["japan", "japanese", "tokyo"],
        "Titan-CN": ["china", "chinese", "beijing"],
        "Titan-AU": ["australia", "australian"],
    }
    for supplier_name, keywords in supplier_keywords.items():
        if any(kw in desc_lower for kw in keywords):
            disrupted = supplier_name
            break

    duration = classification.get("estimated_duration_weeks", 8)

    # Step 3: Run simulation
    sim_results = compare_strategies(
        suppliers=suppliers,
        disrupted_supplier=disrupted,
        disruption_weeks=duration,
        order_quantity_kg=order_quantity_kg,
        qualified_only=qualified_only,
    )

    sim_context = "\n\n".join(format_result_summary(r) for r in sim_results)

    # Step 4: Analyze results
    analysis = analyze(
        analyst,
        sim_context,
        f"The disruption is: {user_description}\n\n"
        f"Classification: {classification.get('category', 'UNKNOWN')} "
        f"(severity: {classification.get('severity', 'unknown')})\n\n"
        f"Which allocation strategy do you recommend and why?",
    )

    # Step 5: Risk assessment
    risk = assess_risk(analyst, sim_context)

    return {
        "user_input": user_description,
        "classification": classification,
        "disrupted_supplier": disrupted,
        "disruption_weeks": duration,
        "simulation_results": sim_results,
        "simulation_context": sim_context,
        "analysis": analysis,
        "risk_assessment": risk,
    }


# ---------------------------------------------------------------------------
# Streamlit Sidebar Helper
# ---------------------------------------------------------------------------

def render_model_selector():
    """
    Render a Streamlit sidebar with provider and model selection.

    Auto-detects available providers, shows their status, and lets the
    user pick a provider + model from dropdowns. Returns a connected
    Analyst object ready to use.

    Returns:
        Analyst object if a provider is available, or None if not.

    Usage in Streamlit app:
        from llm_analyst import render_model_selector

        analyst = render_model_selector()
        if analyst:
            response = analyze(analyst, summary, question)
            st.write(response)
        else:
            st.warning("No LLM provider available.")
    """
    try:
        import streamlit as st
    except ImportError:
        raise ImportError(
            "Streamlit is required for render_model_selector().\n"
            "Install it with: pip install streamlit"
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Language Model")

    # Detect what's available
    providers = detect_available_providers()
    available_providers = [p for p in providers if p["status"] == "available"]
    unavailable_providers = [p for p in providers if p["status"] != "available"]

    if not available_providers:
        st.sidebar.error("No LLM providers detected.")
        st.sidebar.markdown("**Setup one of these (all free):**")
        for p in providers:
            st.sidebar.markdown(f"- **{p['label']}**: {p['reason']}")
        return None

    # Provider selector
    provider_options = {p["label"]: p for p in available_providers}
    selected_label = st.sidebar.selectbox(
        "Provider",
        options=list(provider_options.keys()),
        help="Select which LLM service to use for analysis.",
    )
    selected_provider = provider_options[selected_label]

    # Model selector
    model_options = {m["label"]: m["id"] for m in selected_provider["models"]}
    default_idx = 0
    for i, m in enumerate(selected_provider["models"]):
        if m["id"] == selected_provider["default_model"]:
            default_idx = i
            break

    selected_model_label = st.sidebar.selectbox(
        "Model",
        options=list(model_options.keys()),
        index=default_idx,
        help="Select which language model to use.",
    )
    selected_model_id = model_options[selected_model_label]

    # Show model info
    model_info = next(
        (m for m in selected_provider["models"] if m["id"] == selected_model_id),
        None,
    )
    if model_info:
        cols = st.sidebar.columns(2)
        cols[0].metric("Size", model_info["size"])
        cols[1].metric("Speed", model_info["speed"])

    # Show unavailable providers as expandable info
    if unavailable_providers:
        with st.sidebar.expander("Other providers (not configured)"):
            for p in unavailable_providers:
                st.markdown(f"**{p['label']}**  \n{p['reason']}")

    # Connect and return
    try:
        analyst = create_analyst(
            provider=selected_provider["provider"],
            model=selected_model_id,
        )
        st.sidebar.success(
            f"Connected: {selected_provider['provider']} / {selected_model_id}"
        )
        return analyst
    except ValueError as e:
        st.sidebar.error(f"Connection failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Standalone Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    print("=" * 65)
    print("TITANIUM SUPPLY CHAIN LLM ANALYST")
    print("=" * 65)

    # --- Show available providers ---
    print("\n--- Provider Detection ---\n")
    providers = detect_available_providers()
    for p in providers:
        status = "OK" if p["status"] == "available" else "  "
        print(f"  [{status}] {p['label']:25s} {p['reason']}")
        if p["status"] == "available":
            for m in p["models"]:
                default = " (default)" if m["id"] == p["default_model"] else ""
                print(f"        - {m['label']:20s} [{m['size']}] {m['speed']}{default}")

    # --- Auto-select best provider ---
    try:
        provider, model = auto_select_provider()
        print(f"\nAuto-selected: {provider} / {model}")
        analyst = create_analyst(provider, model=model)
    except (RuntimeError, ValueError) as e:
        print(f"\n{e}")
        print("\nTo get started:")
        print("  1. Go to https://console.groq.com")
        print("  2. Create a free account and generate an API key")
        print("  3. Run: set GROQ_API_KEY=gsk_your_key_here  (Windows)")
        print("     or:  export GROQ_API_KEY=gsk_your_key_here (Mac/Linux)")
        print("  5. Run this script again")
        sys.exit(1)

    # --- Demo 1: Classify a disruption ---
    print("\n--- Demo 1: Disruption Classification ---\n")
    classification = classify_disruption(
        analyst,
        "Russia has imposed export restrictions on titanium sponge "
        "due to escalating geopolitical tensions. Expected to last "
        "at least 3 months.",
    )
    print(classification)

    # --- Demo 2: Full pipeline ---
    print("\n--- Demo 2: Full Pipeline ---\n")
    result = full_pipeline(
        analyst,
        "Our Russian titanium supplier has been sanctioned. "
        "We need to fulfill a 5000kg order for the F-35 program.",
    )

    print(f"Classification: {result['classification']}")
    print(f"Disrupted: {result['disrupted_supplier']}")
    print(f"Duration: {result['disruption_weeks']} weeks")
    print(f"\n--- AI Analysis ---\n")
    print(result["analysis"])
    print(f"\n--- Risk Assessment ---\n")
    print(result["risk_assessment"])
