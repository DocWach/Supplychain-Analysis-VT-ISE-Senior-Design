# Titanium Supply Chain Disruption Analyzer -- User Manual

**Application Version:** 2.0
**Document Audience:** All users, from first-time beginners to software developers

---

## Table of Contents

1. [Section 1: Beginner Guide](#section-1-beginner-guide)
2. [Section 2: Intermediate Guide](#section-2-intermediate-guide)
3. [Section 3: Advanced / Expert Guide](#section-3-advanced--expert-guide)

---

# Section 1: Beginner Guide

*This section assumes no prior experience with programming, command-line tools, or artificial intelligence. Every concept is explained from scratch.*

## 1.1 What This Application Does

Imagine you manage the purchasing of titanium for an aerospace company. Titanium is a critical metal used in jet engines and airframes, and you buy it from several suppliers around the world. Now imagine one of those suppliers suddenly cannot deliver -- perhaps due to a natural disaster, political sanctions, or a factory accident. What happens to your production schedule? How much more will it cost? Which backup suppliers should you turn to?

This application answers those questions. It does four things:

1. **Simulates** your supply chain on a computer, modeling how orders flow from suppliers to your factory over weeks of simulated time.
2. **Compares heuristic strategies** for redistributing orders when a supplier goes offline (split evenly, go cheapest, or go fastest).
3. **Optimizes** using linear programming to find the mathematically best allocation (minimize cost, minimize lead time, or balance both).
4. **Uses AI** (a large language model, similar to ChatGPT) to write a plain-English analysis of the results and assess risk.

Think of it as a flight simulator, but for your supply chain instead of an airplane. The optimizer adds a "GPS" that finds the mathematically shortest route, while the heuristic strategies represent common rules of thumb that procurement managers actually use.

## 1.2 Key Concepts Explained

| Term | Plain-Language Meaning |
|---|---|
| Supply chain | The network of companies that produce and deliver materials to you. |
| Disruption | An unexpected event that stops or slows a supplier (earthquake, sanctions, fire). |
| Allocation strategy | The rule you follow when re-distributing an order among remaining suppliers. |
| Simulation | Running a simplified model of reality on a computer to see what would happen. |
| LLM (Large Language Model) | An AI program that reads text and writes text, like a very fast analyst. |
| API key | A password-like code that lets the application connect to an AI service. |
| Terminal / Command line | A text-based window where you type commands to control your computer. |
| Streamlit | The software framework that creates the interactive web page you see. |
| Environment variable | A named value stored in your operating system that programs can read. |
| Linear programming (LP) | A mathematical method for finding the best outcome (e.g., lowest cost) given constraints (e.g., supplier capacity limits). |
| Optimizer | The part of the application that uses LP to calculate the mathematically best allocation, as opposed to heuristic rules of thumb. |
| OR-Tools | Google's open-source optimization library used by the optimizer. |

## 1.3 What You Will Need

- A computer running Windows 10/11, macOS, or Linux.
- An internet connection (for installing software and using cloud AI providers).
- About 15 minutes for initial setup.

## 1.4 Step-by-Step Installation

### Step 1: Open a Terminal

- **Windows:** Press the Windows key, type `cmd`, and click "Command Prompt." Alternatively, search for "PowerShell" and open it.
- **macOS:** Open the "Terminal" application found in Applications > Utilities.
- **Linux:** Open your distribution's terminal emulator (often Ctrl+Alt+T).

You will see a blinking cursor waiting for you to type. This is where you enter commands.

### Step 2: Check if Python Is Installed

Type the following and press Enter:

```
python --version
```

You should see something like `Python 3.10.12`. If you see an error ("not recognized" or "command not found"), you need to install Python:

1. Go to https://www.python.org/downloads/
2. Download the latest Python 3 installer for your operating system.
3. **Windows users:** During installation, check the box that says "Add Python to PATH." This is critical.
4. After installation, close and reopen your terminal, then try `python --version` again.

### Step 3: Download the Application Files

You need the `src/` folder containing these files: `app.py`, `supply_chain_sim.py`, `supply_chain_optimizer.py`, `llm_analyst.py`, `evaluation_harness.py`, `suppliers.csv`, `requirements.txt`, and `demo.html`. Place them in a folder you can find easily, for example `C:\Users\YourName\titanium-analyzer\src` on Windows or `~/titanium-analyzer/src` on macOS/Linux.

The easiest way is to clone the repository:

```
git clone https://github.com/DocWach/Supplychain-Analysis-VT-ISE-Senior-Design.git
cd Supplychain-Analysis-VT-ISE-Senior-Design
```

### Step 4: Install Required Libraries

In your terminal, navigate to the `src` folder. If your files are at the path above:

**Windows:**
```
cd C:\Users\YourName\titanium-analyzer\src
```

**macOS / Linux:**
```
cd ~/titanium-analyzer/src
```

Then install all required libraries using the provided requirements file:

```
pip install -r requirements.txt
```

This installs:
- **streamlit** -- builds the interactive web interface
- **openai** -- connects to AI language models
- **simpy** -- runs the supply chain simulation
- **ortools** -- Google's optimization library for LP-based allocation (if unavailable on your platform, **scipy** is used as a fallback)
- **scipy** -- scientific computing library (fallback LP solver)

Wait for the installation to finish. You will see text scrolling; this is normal.

### Step 5: Set Up an AI Provider (Optional but Recommended)

The application can run simulations without AI, but the AI analysis feature requires access to a language model. The easiest free option is Groq:

1. Go to https://console.groq.com in your web browser.
2. Create a free account.
3. Navigate to "API Keys" and click "Create API Key."
4. Copy the key (it looks like a long string of letters and numbers).
5. Set it as an environment variable:

**Windows (Command Prompt):**
```
set GROQ_API_KEY=gsk_your_key_here
```

**Windows (PowerShell):**
```
$env:GROQ_API_KEY="gsk_your_key_here"
```

**macOS / Linux:**
```
export GROQ_API_KEY=gsk_your_key_here
```

Note: This setting lasts only for the current terminal session. If you close the terminal and reopen it, you will need to set it again.

### Step 6: Launch the Application

Make sure you are still in the `src` folder, then type:

```
streamlit run app.py
```

After a few seconds, your web browser will open automatically to the address `http://localhost:8501`. You will see the Titanium Supply Chain Disruption Analyzer interface.

## 1.5 Your First Analysis (Walkthrough)

### Using the Sidebar

On the left side of the screen, you will see the sidebar with configuration options:

1. **Language Model:** If you set up an API key in Step 5, you will see a dropdown listing detected providers (for example, "Groq (Free Cloud)"). Select one, then choose a model from the second dropdown. You will see the model's size and speed rating displayed below.
2. **Simulation Settings:**
   - "Aerospace-qualified suppliers only" -- when checked, the simulation excludes suppliers that have not passed aerospace quality certification. Leave this checked for realistic aerospace scenarios.
   - "Order Quantity (kg)" -- the amount of titanium you need to order. The default is a reasonable starting point; leave it as-is for your first run.

### Tab 1: Full Pipeline (Recommended First Step)

1. Click the "Full Pipeline" tab at the top.
2. You will see a text box labeled for describing a disruption, and four pre-built example buttons below it.
3. Click the button labeled **"Russian sanctions"** (or whichever scenario interests you). The text box will populate with a description.
4. Click the "Run" or "Analyze" button.
5. The application runs a four-step pipeline:
   - **Step 1 -- Classify:** The AI reads your disruption description and determines the type (geopolitical, natural disaster, etc.), severity (1-10), estimated duration in weeks, and which supplier is most likely affected.
   - **Step 2 -- Map:** The system identifies which supplier in the database matches the disruption.
   - **Step 3 -- Simulate:** Six allocation strategies are evaluated. Three are heuristic rules (proportional, cheapest first, fastest first) and three are LP-optimized (optimal min cost, optimal min time, optimal balanced). Each shows a card with cost, lead time, and supplier count, plus colored progress bars for how orders are allocated across suppliers. The results are grouped into "Heuristic Strategies" and "LP-Optimized Strategies" sections.
   - **Step 4 -- Analyze:** The AI writes a narrative analysis comparing all strategies and provides a risk assessment.
6. Scroll down to read the full results. If you want to see exactly what was sent to the AI, expand the "View prompt context sent to LLM" section at the bottom.

### Tab 2: Manual Scenario

This tab gives you direct control:

1. Select a supplier to disrupt from the dropdown (or "None" for a baseline with no disruption).
2. Use the slider to set how many weeks the disruption lasts (1 to 52).
3. Adjust order quantity and qualification filtering if desired.
4. Click Run. You will see a comparison table of all six strategies (three heuristic, three optimized). The table includes a "Type" column showing whether each strategy is heuristic or optimal.
5. Expand any strategy row for detailed metrics.
6. Optionally click "Send results to AI for analysis" to get a narrative interpretation.

### Tab 3: Supplier Database

This tab is informational. It shows a table of the five default suppliers with their specifications. Use it as a reference to understand which suppliers exist and their characteristics:

| Supplier | Region | Lead Time | Capacity | Cost | Quality | Qualified |
|---|---|---|---|---|---|---|
| Titan-US | United States | 4 weeks | 800 kg/week | $32/kg | 95% | Yes |
| Titan-JP | Japan | 6 weeks | 1,200 kg/week | $28/kg | 92% | Yes |
| Titan-RU | Russia | 8 weeks | 2,000 kg/week | $22/kg | 88% | Yes |
| Titan-CN | China | 7 weeks | 1,500 kg/week | $24/kg | 85% | No |
| Titan-AU | Australia | 5 weeks | 600 kg/week | $35/kg | 90% | Yes |

Notice that Titan-RU has the largest capacity and lowest cost but the longest lead time. Titan-CN is not aerospace-qualified, so it will be excluded when the "qualified only" checkbox is active.

### Tab 4: About

Contains project background information, architecture notes, known limitations, and team credits.

## 1.6 Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `python: command not found` | Python is not installed or not on PATH. | Reinstall Python and ensure "Add to PATH" is checked. |
| `pip: command not found` | Same as above, or pip not installed. | Try `python -m pip install ...` instead. |
| `ModuleNotFoundError: No module named 'streamlit'` | Libraries not installed. | Run `pip install streamlit openai simpy` again. |
| Browser does not open automatically. | Firewall or browser setting. | Manually open `http://localhost:8501` in your browser. |
| "No LLM providers detected" in sidebar. | No API keys set. | Follow Step 5 to set an API key, then restart the app. |
| AI analysis shows an error. | API key is invalid or expired, or the service is down. | Verify your key at the provider's website. Try a different provider. |
| Simulation runs but results seem wrong. | Order quantity may be too large for available capacity. | Reduce order quantity or uncheck "qualified only" to include more suppliers. |
| Sidebar shows "No LP solver" warning. | Neither OR-Tools nor SciPy is installed. | Run `pip install ortools` or `pip install scipy`. The optimizer will use whichever is available. |
| Only 3 strategies appear (no optimal). | Optimizer module not found or solver not installed. | Ensure `supply_chain_optimizer.py` is in the same folder as `app.py` and a solver is installed. |

## 1.7 Understanding the Six Allocation Strategies

The application offers two groups of strategies: heuristic rules of thumb and mathematically optimized solutions.

### Heuristic Strategies

Think of ordering titanium like ordering food for a large event from multiple restaurants:

- **Proportional:** You split the order across all available restaurants based on how much each can cook. A restaurant that can make 200 plates gets twice the order of one that can make 100. This spreads the risk.
- **Cheapest First:** You fill as much of the order as possible from the cheapest restaurant, then move to the next cheapest, and so on. This minimizes cost but concentrates risk.
- **Fastest First:** You fill the order starting with whichever restaurant can deliver soonest. This minimizes wait time but may cost more.

### LP-Optimized Strategies

These use linear programming (a mathematical optimization technique) to find the provably best allocation given the constraints. Think of it as having a calculator that tests every possible combination and picks the winner:

- **Optimal (Min Cost):** Finds the allocation that produces the absolute lowest total cost while respecting each supplier's capacity limits. This often matches "Cheapest First" but can find better solutions when capacity constraints create complex trade-offs.
- **Optimal (Min Time):** Finds the allocation that minimizes the weighted average lead time. This pushes orders toward the fastest suppliers.
- **Optimal (Balanced):** Finds the allocation that balances cost (60% weight) and lead time (40% weight). This is useful when you care about both but do not want to sacrifice one entirely for the other.

### Which Should I Trust?

The optimized strategies are mathematically guaranteed to be the best *given the model's assumptions*. However, the heuristic strategies reflect how procurement managers actually make decisions in practice. Comparing them is the point: if the optimizer finds a significantly cheaper or faster solution than the heuristic you would normally use, that is actionable insight. If they are similar, your current approach is already close to optimal.

No strategy is universally best. The application helps you compare trade-offs for your specific scenario.

---

# Section 2: Intermediate Guide

*This section assumes you are comfortable with a terminal, can install Python packages, and understand basic programming concepts.*

## 2.1 Configuration Deep Dive

### Switching LLM Providers

The application auto-detects providers by checking for environment variables and local services in this order:

| Provider | Detection Method | Cost | Setup |
|---|---|---|---|
| Groq | `GROQ_API_KEY` env var present | Free tier available | `export GROQ_API_KEY=gsk_...` |
| Cerebras | `CEREBRAS_API_KEY` env var present | Free tier available | `export CEREBRAS_API_KEY=csk_...` |
| Ollama | HTTP ping to `localhost:11434` | Free (local) | Install Ollama, `ollama pull llama3.2`, `ollama serve` |
| OpenAI | `OPENAI_API_KEY` env var present | Paid per token | `export OPENAI_API_KEY=sk-...` |

To use multiple providers simultaneously, set all relevant environment variables. The sidebar dropdown will list every detected provider, and you can switch between them at any time without restarting the app.

**Ollama (fully local, no data leaves your machine):**

```bash
# Install Ollama from https://ollama.com
ollama pull llama3.2       # Download a model (~2 GB)
ollama serve               # Start the local server
# Then launch the app in a separate terminal
```

### Simulation Settings in Detail

- **Aerospace-qualified suppliers only:** Filters out suppliers where the `qualified` field in `suppliers.csv` is `FALSE`. In the default dataset, this excludes only Titan-CN. Disabling this filter increases total available capacity by 1,500 kg/week but introduces a supplier with lower quality rating (85%).
- **Order Quantity (kg):** Determines the total demand the simulation attempts to fulfill. If total available capacity across non-disrupted suppliers cannot meet this quantity, you will see partial fulfillment in the results. Experiment with values between 500 and 5,000 to see how the system behaves under different demand levels.

## 2.2 Modifying the Supplier Database

The supplier data lives in `src/suppliers.csv`. Open it in any spreadsheet application or text editor. The format is:

```csv
name,region,lead_time_weeks,capacity_kg_per_week,cost_per_kg,quality_rating,qualified
Titan-US,United States,4,800,32,0.95,TRUE
Titan-JP,Japan,6,1200,28,0.92,TRUE
Titan-RU,Russia,8,2000,22,0.88,TRUE
Titan-CN,China,7,1500,24,0.85,FALSE
Titan-AU,Australia,5,600,35,0.90,TRUE
```

### Adding a New Supplier

Append a new row:

```csv
Titan-IN,India,9,1000,20,0.82,FALSE
```

Rules to follow:
- `name` must be unique.
- `lead_time_weeks` is an integer (weeks from order to delivery).
- `capacity_kg_per_week` is the maximum the supplier can ship per week.
- `cost_per_kg` is in US dollars.
- `quality_rating` is a decimal between 0 and 1.
- `qualified` is `TRUE` or `FALSE`.

After saving the CSV, restart the Streamlit app (`Ctrl+C` in the terminal, then `streamlit run app.py`). The new supplier will appear in the Supplier Database tab and be available in simulations.

### Removing a Supplier

Delete the corresponding row from the CSV and restart.

## 2.3 Understanding and Modifying Allocation Strategies

### Heuristic Strategies

The three heuristic strategies are implemented in `supply_chain_sim.py`. Each is a function that takes a list of available (non-disrupted) suppliers and an order quantity, then returns an allocation dict mapping supplier names to kg amounts.

**Proportional allocation logic:**
```
For each supplier:
    share = supplier.capacity / total_capacity_of_all_available
    allocation = order_quantity * share
```

**Cheapest first logic:**
```
Sort suppliers by cost_per_kg ascending.
remaining = order_quantity
For each supplier (cheapest to most expensive):
    allocate = min(remaining, supplier.capacity * duration)
    remaining -= allocate
```

**Fastest first logic:**
```
Sort suppliers by lead_time_weeks ascending.
remaining = order_quantity
For each supplier (fastest to slowest):
    allocate = min(remaining, supplier.capacity * duration)
    remaining -= allocate
```

To modify a heuristic strategy (for example, to add a quality weighting to proportional allocation), edit the corresponding function in `supply_chain_sim.py`. Search for the strategy name to find the relevant code block.

### LP-Optimized Strategies

The three optimized strategies are implemented in `supply_chain_optimizer.py`. They solve a linear program (LP) using either Google OR-Tools (preferred) or SciPy (fallback).

**LP formulation (min cost example):**
```
Decision variables: x[i] = kg allocated to supplier i

Minimize:   sum( cost_per_kg[i] * x[i] )
Subject to:
    sum(x[i]) = order_quantity              (demand satisfied)
    0 <= x[i] <= capacity[i] * 12 weeks     (per-supplier capacity)
```

The `min_time` objective replaces `cost_per_kg[i]` with `lead_time_weeks[i]`. The `balanced` objective uses a weighted combination: `0.6 * normalized_cost[i] + 0.4 * normalized_time[i]`, where both are scaled to [0, 1] so they are comparable.

**Why the optimizer matters:** Heuristic strategies follow simple rules and can miss non-obvious solutions. For example, when multiple suppliers have similar costs but different capacities, the optimizer finds the exact split that minimizes total cost while respecting all constraints simultaneously. In testing, the optimizer matched or beat every heuristic in every scenario (155/155 test cases).

**Solver backends:** The sidebar shows which solver is active. OR-Tools (GLOP solver) is preferred for its speed and reliability. SciPy's HiGHS solver is the fallback. Both produce identical results for these LP problems.

### Strategy Comparison Summary

| Strategy | Type | Optimizes For | Diversification | Best When |
|---|---|---|---|---|
| Proportional | Heuristic | Risk spreading | High | Long-term disruptions, relationship preservation |
| Cheapest First | Heuristic | Cost | Low | Cost is dominant concern, single supplier can handle load |
| Fastest First | Heuristic | Speed | Low | Urgent orders, time-critical programs |
| Optimal (Min Cost) | LP | Cost | Low | Same as Cheapest First but handles complex constraints better |
| Optimal (Min Time) | LP | Speed | Low | Same as Fastest First but with provably optimal allocation |
| Optimal (Balanced) | LP | Cost + Speed | Low | Trade-off analysis, when both cost and time matter |

## 2.4 Customizing LLM Prompts

The file `src/llm_analyst.py` contains the system prompts and user prompts sent to the language model. Key areas to customize:

1. **Classification prompt:** Controls how the AI interprets a free-text disruption description. Look for the prompt that asks the model to output disruption type, severity, duration, and affected supplier.

2. **Analysis prompt:** Controls the narrative analysis of simulation results. You can adjust the tone (more formal, more concise), add domain-specific terminology, or request specific output structures.

3. **Risk assessment prompt:** Controls the final risk evaluation. You can modify the risk framework (e.g., add probability estimates, change the severity scale).

When editing prompts, keep these guidelines in mind:
- Be explicit about the desired output format (JSON, bullet points, numbered list).
- Include the simulation data as structured context, not embedded in the instruction.
- Test changes with multiple scenarios to ensure robustness.

## 2.5 Interpreting Results Critically

The AI analysis is generated text, not ground truth. Keep these caveats in mind:

- **Simulation fidelity:** The SimPy model is a simplification. Real supply chains have partial disruptions, quality variability, contractual minimums, transportation delays, and cascading failures that are not modeled.
- **LLM hallucination:** The AI may state facts about suppliers, geopolitics, or industry practices that sound authoritative but are fabricated. Cross-check any factual claims.
- **Strategy comparison:** Cost and lead time numbers come from the simulation and are deterministic given the inputs. The AI narrative is an interpretation layer on top of those numbers. Trust the numbers; read the narrative as a starting point for discussion.
- **Qualified-only filtering:** In aerospace, qualification is not binary in practice. A supplier may be qualified for some alloys but not others, or qualified by some customers but not others. The checkbox is a simplification.

## 2.6 Running the Static Demo

If you want to demonstrate the interface without Python or dependencies:

```bash
# Simply open in a browser
open src/demo.html        # macOS
xdg-open src/demo.html    # Linux
start src/demo.html        # Windows
```

This shows a static HTML version of the UI with no live simulation or AI capabilities.

---

# Section 3: Advanced / Expert Guide

*This section assumes proficiency with Python, familiarity with discrete-event simulation concepts, and experience with LLM APIs and cloud deployment.*

## 3.1 Architecture Overview

```
User Browser
    |
    v
Streamlit (app.py)
    |
    +---> supply_chain_sim.py        [SimPy discrete-event simulation]
    |         |
    |         +---> suppliers.csv     [data layer]
    |         |
    |         +---> supply_chain_optimizer.py  [LP allocation solver]
    |                   |
    |                   +---> OR-Tools (GLOP) or SciPy (HiGHS)
    |
    +---> llm_analyst.py             [OpenAI-compatible API client]
    |         |
    |         +---> Groq / Cerebras / Ollama / OpenAI  [external LLM]
    |
    +---> evaluation_harness.py      [BERTScore + cosine similarity]
```

**Data flow for Tab 1 (Full Pipeline):**

1. User enters disruption text.
2. `app.py` sends text to `llm_analyst.py` for classification (LLM call 1).
3. Classification result maps to a supplier in `suppliers.csv`.
4. `app.py` invokes `supply_chain_sim.py` six times (once per strategy). For the three heuristic strategies, SimPy runs a discrete-event simulation directly. For the three optimized strategies, `supply_chain_sim.py` delegates to `supply_chain_optimizer.py`, which solves an LP, then SimPy simulates the resulting allocation.
5. Each run returns metrics (total cost, delivery time, per-supplier allocations, feasibility).
6. `app.py` formats all six results into a prompt context and sends to `llm_analyst.py` for analysis (LLM call 2) and risk assessment (LLM call 3).
7. Results are rendered in the Streamlit UI, grouped into "Heuristic Strategies" and "LP-Optimized Strategies" sections.

## 3.2 SimPy Simulation Internals

The simulation in `supply_chain_sim.py` uses SimPy's process-based discrete-event paradigm. Key components:

- **Environment:** `simpy.Environment()` manages the simulation clock (unit: weeks).
- **Supplier resources:** Each supplier is modeled with a capacity constraint representing their weekly throughput.
- **Order process:** A generator function that places orders according to the allocation strategy, waits for lead time, and records fulfillment.
- **Disruption modeling:** The disrupted supplier's capacity is set to zero for the specified duration, then restored.

### Simulation Pseudocode

```python
env = simpy.Environment()

for supplier in available_suppliers:
    supplier.resource = simpy.Container(env, capacity=supplier.capacity)

def order_process(env, allocation, supplier):
    yield env.timeout(supplier.lead_time)
    # Record: cost = allocation * supplier.cost_per_kg
    # Record: delivered quantity

for supplier, qty in strategy_allocation.items():
    env.process(order_process(env, qty, supplier))

env.run()
# Collect metrics from recorded events
```

The simulation is deterministic given identical inputs. There are no stochastic elements in the default implementation (see Section 3.5 for how to add them).

## 3.3 LP Optimizer Internals

The optimizer in `supply_chain_optimizer.py` solves supplier allocation as a linear program. It integrates with the simulation via the `optimal_allocate()` function, which is called by `supply_chain_sim._allocate_order()` when the strategy name starts with `optimal_`.

### Solver Backend Selection

The module tries to import OR-Tools first, then falls back to SciPy:

```python
try:
    from ortools.linear_solver import pywraplp
    _SOLVER_BACKEND = "ortools"
except ImportError:
    from scipy.optimize import linprog
    _SOLVER_BACKEND = "scipy"
```

Both solvers produce identical results for these LP problems. OR-Tools uses the GLOP simplex solver; SciPy uses HiGHS.

### LP Formulation Details

**Variables:** `x[i]` = kilograms allocated to supplier `i` (continuous, non-negative)

**Constraints:**
- `sum(x[i]) = demand` — total allocation meets the order quantity
- `0 <= x[i] <= capacity[i] * 12` — each supplier capped at 12-week planning horizon

**Objectives:**

| Objective | Coefficient for x[i] |
|---|---|
| `min_cost` | `cost_per_kg[i]` |
| `min_time` | `lead_time_weeks[i]` |
| `balanced` | `0.6 * norm_cost[i] + 0.4 * norm_time[i]` |

Where `norm_cost` and `norm_time` are min-max normalized to [0, 1] so the two dimensions are comparable in the balanced objective.

### Infeasibility Handling

If total capacity is less than the order quantity, the optimizer relaxes the equality constraint to an inequality (`sum(x[i]) <= demand`) and maximizes total allocation. This produces a partial fulfillment result with a feasibility warning.

### Adding New Objectives

To add a custom objective (e.g., maximize quality-weighted allocation):

```python
# In supply_chain_optimizer.py
OBJECTIVE_MAX_QUALITY = "max_quality"

# Add to the objective coefficient builder:
if objective == OBJECTIVE_MAX_QUALITY:
    # Negative because we minimize; negating quality maximizes it
    obj_coeffs = [-s.quality_rating for s in available]
```

Then register the new strategy in `supply_chain_sim._allocate_order()` and `compare_strategies()`.

## 3.4 LLM Integration Architecture

`llm_analyst.py` uses the `openai` Python library as a universal client. All four providers expose OpenAI-compatible `/v1/chat/completions` endpoints.

### Provider Auto-Detection

The PROVIDERS dict maps provider names to configuration:

```python
PROVIDERS = {
    "groq": {
        "name": "Groq (Free Cloud)",
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "models": [
            {"id": "llama-3.3-70b-versatile", "size": "70B", "speed": "fast"},
            # ... additional models
        ]
    },
    "cerebras": {
        "name": "Cerebras (Free Cloud)",
        "base_url": "https://api.cerebras.ai/v1",
        "api_key_env": "CEREBRAS_API_KEY",
        "models": [...]
    },
    "ollama": {
        "name": "Ollama (Local)",
        "base_url": "http://localhost:11434/v1",
        "api_key_env": None,  # No key needed
        "models": [...]
    },
    "openai": {
        "name": "OpenAI (Paid)",
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "models": [...]
    }
}
```

Detection iterates through this dict, checking `os.environ.get(api_key_env)` for cloud providers and attempting an HTTP GET to the base URL for Ollama.

### Adding a New LLM Provider

To add a provider (e.g., Together AI), add an entry to the PROVIDERS dict in `llm_analyst.py`:

```python
"together": {
    "name": "Together AI",
    "base_url": "https://api.together.xyz/v1",
    "api_key_env": "TOGETHER_API_KEY",
    "models": [
        {"id": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "size": "70B", "speed": "fast"},
        {"id": "mistralai/Mixtral-8x22B-Instruct-v0.1", "size": "8x22B", "speed": "medium"},
    ]
}
```

The only requirement is that the provider exposes an OpenAI-compatible chat completions endpoint.

## 3.5 Adding New Pipeline Steps and Agent Types

The pipeline in Tab 1 follows a sequential chain: classify -> map -> simulate -> analyze -> risk assess. Each step is a function call. To add a new step:

1. **Define a new system prompt** in `llm_analyst.py` for the agent's role (e.g., a "mitigation planner" that suggests concrete actions).

```python
MITIGATION_PLANNER_PROMPT = """You are a supply chain mitigation specialist.
Given disruption analysis and simulation results, propose a ranked list of
concrete mitigation actions with estimated implementation time and cost.
Format as a numbered list."""
```

2. **Create a wrapper function** that calls the LLM with the new prompt:

```python
def plan_mitigations(client, model, context: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": MITIGATION_PLANNER_PROMPT},
            {"role": "user", "content": context}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
```

3. **Integrate into the pipeline** in `app.py` by calling the new function after the existing analysis step and rendering its output in the UI.

## 3.6 Extending the Simulation Model

### Adding Stochastic Elements

The default simulation is deterministic. To introduce randomness:

```python
import random

def stochastic_lead_time(base_lead_time):
    """Lead time varies +/- 20% uniformly."""
    return base_lead_time * random.uniform(0.8, 1.2)

def stochastic_capacity(base_capacity):
    """Capacity follows a normal distribution (95% of nominal, 5% std dev)."""
    return max(0, random.gauss(base_capacity * 0.95, base_capacity * 0.05))
```

Integrate these into the SimPy order process, replacing fixed values with stochastic calls. Run Monte Carlo analysis by executing the simulation N times and aggregating:

```python
results = []
for _ in range(1000):
    result = run_simulation(strategy, disrupted_supplier, ...)
    results.append(result)

mean_cost = statistics.mean(r['total_cost'] for r in results)
p95_cost = sorted(r['total_cost'] for r in results)[949]
```

### Multi-Tier Supply Chains

The current model is single-tier (your company buys directly from titanium suppliers). To model sub-tier disruptions:

1. Add a `tier` and `sub_suppliers` field to the CSV or a separate relationships file.
2. Model each tier as a SimPy process that feeds into the next.
3. Propagate disruptions upstream: if a Tier 2 supplier is disrupted, the Tier 1 supplier's effective capacity decreases.

### New Disruption Types

Currently disruptions are binary (supplier fully offline for N weeks). To model partial disruptions:

```python
class PartialDisruption:
    def __init__(self, supplier, capacity_reduction_pct, duration_weeks, ramp_back_weeks):
        self.supplier = supplier
        self.reduction = capacity_reduction_pct  # e.g., 0.6 = 60% capacity lost
        self.duration = duration_weeks
        self.ramp_back = ramp_back_weeks  # gradual recovery period
```

Modify the SimPy process to reduce (not zero) the supplier's capacity and implement a linear or exponential ramp-back.

## 3.7 Cloud Deployment

### Streamlit Community Cloud (Simplest)

1. Push the `src/` directory to a public GitHub repository (already done: `DocWach/Supplychain-Analysis-VT-ISE-Senior-Design`).
2. The `requirements.txt` is already included in `src/`.
3. Go to https://share.streamlit.io, connect your GitHub account, and select the repository.
4. Set environment variables (API keys) in the Streamlit Cloud "Secrets" panel using TOML format:
   ```toml
   GROQ_API_KEY = "gsk_..."
   ```
5. Deploy. The app will be available at `https://your-app.streamlit.app`.

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY src/ .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t titanium-analyzer .
docker run -p 8501:8501 -e GROQ_API_KEY=gsk_... titanium-analyzer
```

### AWS Deployment (ECS Fargate)

1. Build and push the Docker image to Amazon ECR.
2. Create an ECS task definition referencing the image, with environment variables for API keys stored in AWS Secrets Manager.
3. Create an ECS service on Fargate with an Application Load Balancer.
4. Configure HTTPS via ACM certificate on the ALB.

Estimated cost: $15-30/month for a single-task Fargate service with minimal traffic.

## 3.8 Performance Optimization

### Streamlit Caching

Decorate expensive functions with `@st.cache_data` (for data) or `@st.cache_resource` (for connections):

```python
@st.cache_data(ttl=3600)
def load_suppliers(csv_path):
    return pd.read_csv(csv_path)

@st.cache_resource
def get_llm_client(provider, api_key):
    return openai.OpenAI(base_url=provider["base_url"], api_key=api_key)
```

### Async LLM Calls

When the pipeline makes multiple LLM calls (classify, analyze, risk assess), parallelize the independent ones using `asyncio`:

```python
import asyncio
from openai import AsyncOpenAI

async def parallel_analysis(client, model, sim_results):
    analysis_task = asyncio.create_task(
        client.chat.completions.create(model=model, messages=analysis_messages)
    )
    risk_task = asyncio.create_task(
        client.chat.completions.create(model=model, messages=risk_messages)
    )
    analysis, risk = await asyncio.gather(analysis_task, risk_task)
    return analysis, risk
```

Note: Classification must complete before simulation (it determines the disrupted supplier), and simulation must complete before analysis. But analysis and risk assessment can run in parallel.

### Simulation Performance

For Monte Carlo runs (Section 3.5), use `multiprocessing` to parallelize across CPU cores:

```python
from multiprocessing import Pool

def run_single_sim(seed):
    random.seed(seed)
    return run_simulation(...)

with Pool() as pool:
    results = pool.map(run_single_sim, range(1000))
```

## 3.9 Integration Patterns

### REST API Wrapper

Wrap the simulation and analysis pipeline as a FastAPI service:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DisruptionRequest(BaseModel):
    description: str
    order_quantity_kg: float = 2000
    qualified_only: bool = True

@app.post("/analyze")
async def analyze_disruption(req: DisruptionRequest):
    classification = classify(req.description)
    sim_results = run_all_strategies(classification, req.order_quantity_kg, req.qualified_only)
    analysis = analyze_results(sim_results)
    return {"classification": classification, "simulation": sim_results, "analysis": analysis}
```

### Webhook Triggers

For automated monitoring, add a webhook endpoint that triggers analysis when an external system detects a disruption event:

```python
@app.post("/webhook/disruption-alert")
async def handle_alert(alert: dict):
    description = alert.get("description", "")
    result = await analyze_disruption(DisruptionRequest(description=description))
    # Forward result to Slack, email, or dashboard
    notify_stakeholders(result)
    return {"status": "processed"}
```

### Database Backend

Replace the CSV file with a database for multi-user, auditable deployments:

```python
# SQLAlchemy model
class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    region = Column(String)
    lead_time_weeks = Column(Integer)
    capacity_kg_per_week = Column(Float)
    cost_per_kg = Column(Float)
    quality_rating = Column(Float)
    qualified = Column(Boolean)

class AnalysisRun(Base):
    __tablename__ = "analysis_runs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    disruption_text = Column(Text)
    classification_json = Column(JSON)
    simulation_results_json = Column(JSON)
    llm_analysis = Column(Text)
    llm_provider = Column(String)
    llm_model = Column(String)
```

This enables historical tracking, comparison across runs, and audit trails.

## 3.10 Evaluation Metrics for LLM Output Quality

To systematically assess whether the AI analysis is useful, implement automated evaluation:

### BERTScore

Compare LLM output against expert-written reference analyses:

```python
from bert_score import score

def evaluate_analysis(generated: str, reference: str) -> dict:
    P, R, F1 = score([generated], [reference], lang="en", rescale_with_baseline=True)
    return {"precision": P.item(), "recall": R.item(), "f1": F1.item()}
```

### Cosine Similarity Against Ground Truth

For structured outputs (classification), embed both the predicted and true labels and measure similarity:

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def classification_similarity(predicted: str, ground_truth: str) -> float:
    embeddings = model.encode([predicted, ground_truth])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
```

### Building an Evaluation Dataset

Create a JSON file of test cases:

```json
[
  {
    "disruption_text": "Earthquake in Osaka region disrupts manufacturing",
    "expected_classification": {
      "type": "natural_disaster",
      "severity": 7,
      "duration_weeks": 12,
      "affected_supplier": "Titan-JP"
    },
    "reference_analysis": "The earthquake disruption to Titan-JP removes 1200 kg/week..."
  }
]
```

Run all test cases against each provider/model combination and track scores over time to detect regressions when switching models.

---

*End of User Manual*
