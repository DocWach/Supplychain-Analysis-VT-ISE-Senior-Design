# Titanium Supply Chain Disruption Analyzer

**Virginia Tech ISE Senior Design Project — AY 2025-26**
**Sponsor:** The Aerospace Corporation
**Faculty Advisor:** Paul Wach

## Overview

This tool combines discrete-event simulation (SimPy) with large language model analysis to evaluate titanium supply chain disruptions for aerospace manufacturing. Users describe a disruption in free text, and the system classifies it, simulates allocation strategies, and provides AI-powered recommendations.

## Team

- Boleslav Econa
- Jonathan Michael
- Camilo Gomez
- Juan Oleaga Alba

## System Architecture

The analysis pipeline has four stages:

1. **Classification** — An LLM classifies a free-text disruption description into a structured category (supplier failure, logistics delay, demand spike, quality issue) with severity and estimated duration.
2. **Simulation** — A SimPy discrete-event simulation models the supply chain with five titanium suppliers, three allocation strategies, and capacity constraints.
3. **Analysis** — An LLM interprets simulation results in business terms and recommends an allocation strategy with reasoning.
4. **Risk Assessment** — An LLM evaluates risks not captured by the simulation (geopolitical, regulatory, concentration risk).

### Allocation Strategies

| Strategy | Description |
|---|---|
| Proportional | Split order across suppliers by capacity share |
| Cheapest First | Prioritize lowest-cost suppliers |
| Fastest First | Prioritize shortest lead-time suppliers |

### Supplier Database

| Supplier | Region | Lead Time (wk) | Capacity (kg/wk) | Cost ($/kg) | Aerospace Qualified |
|---|---|---|---|---|---|
| Titan-US | United States | 4 | 800 | $32.00 | Yes |
| Titan-JP | Japan | 6 | 1,200 | $28.00 | Yes |
| Titan-RU | Russia | 8 | 2,000 | $22.00 | Yes |
| Titan-CN | China | 7 | 1,500 | $24.00 | No |
| Titan-AU | Australia | 5 | 600 | $35.00 | Yes |

## Project Structure

```
src/
  app.py                 # Streamlit web application (main entry point)
  supply_chain_sim.py    # SimPy discrete-event simulation engine
  llm_analyst.py         # LLM integration (classification, analysis, risk)
  suppliers.csv          # Supplier data (CSV format)
  demo.html              # Standalone HTML demo (simulation only, no LLM)
Planning/                # Project planning documents
```

## Setup

### Requirements

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [SimPy](https://simpy.readthedocs.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python) (for LLM features)

```bash
pip install streamlit simpy openai
```

### LLM Provider Configuration

The tool supports multiple LLM providers via OpenAI-compatible APIs. At least one must be configured for AI analysis features. Simulation runs without an LLM.

| Provider | Type | Setup |
|---|---|---|
| [Groq](https://console.groq.com) | Free cloud | `set GROQ_API_KEY=gsk_...` |
| [Cerebras](https://cloud.cerebras.ai) | Free cloud | `set CEREBRAS_API_KEY=...` |
| [Ollama](https://ollama.com) | Free local | Install and run `ollama serve` |
| [OpenAI](https://platform.openai.com) | Paid cloud | `set OPENAI_API_KEY=sk-...` |

### Running the Application

```bash
cd src
streamlit run app.py
```

The app opens in your browser with four tabs:
- **Full Pipeline** — Enter a free-text disruption description for end-to-end analysis
- **Manual Scenario** — Configure simulation parameters directly (no LLM required)
- **Supplier Database** — View supplier data and baseline metrics
- **About** — Project details and system architecture

### Standalone Demo (No Python Required)

Open `src/demo.html` in any web browser for a JavaScript-only simulation demo. This mirrors the SimPy simulation logic but does not include LLM integration.

## Technology Stack

| Component | Technology |
|---|---|
| Simulation Engine | SimPy (Python) |
| LLM Integration | OpenAI-compatible API |
| Default LLM Provider | Groq (Llama 3.3 70B) |
| Web UI | Streamlit |
| Language | Python 3.10+ |

## Limitations

- This is a **research prototype** and is not validated for production procurement decisions.
- Simulation uses simplified supplier models that do not capture all real-world dynamics.
- LLM analysis may produce plausible but incorrect recommendations.
- **All outputs require human review** before action.
- Supply chain data is illustrative, not based on actual supplier contracts.
