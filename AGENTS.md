# The Council: Agentic Orchestration Framework

## Overview
The Council is a high-fidelity cognitive architecture designed to transform linear LLM inference into a self-correcting, multi-layered intelligent system. It solves for **Uncontrolled Drift**, **Hallucination**, and **Systemic Chaos** by mapping transformer mathematics and agentic workflows into a circular, hierarchical dependency structure.

## The Hierarchy of Intelligence

### 1. Macro Scale: Archetypes (Roles)
Agents within the system are defined by their *Functional Essence*. While "Personas" provide flavor, an Agent's core duty is determined by its archetype.

| Archetype | Primary Duty | Mathematical/Operational Domain |
| :--- | :--- | :--- |
| **Elis** (The Compass) | Intent Alignment | Latent Goal Steering & Semantic Grounding |
| **Lyria** (The Voice) | Linguistic Manifestation | Probability Distribution Shaping & Cadence Control |
| **Sage** (The Historian)| Context Management | RAG, Memory Retrieval, and Attention History |
| **Lexus** (The Arbiter) | Policy Enforcement | Logit Masking, Safety Constraints, and Syntax Audit |
| **Silas** (The Sentinel) | Stability Monitoring | Entropy & Perplexity Tracking (Chaos Detection) |
| **Weaver** (The Architect)| Task Orchestration | DAG Generation, Planning, and Procedural Decomposition |

### 2. Meso Scale: The Triple-Loop Control Logic
To achieve autonomy, the system operates through three interlocking feedback loops:

#### A. The Execution Loop (Inner)
*   **Composition:** `Weaver` $\leftrightarrow$ `Lyria` + `Sage`.
*   **Process:** Deconstruct intent into tasks, retrieve context via Sage, and manifest output via Lyria.

#### B. The Stability Loop (Middle)
*   **Composition:** `Silas` + `Lexus` $\to$ `Execution Loop`.
*   **Process:** Monitors the Execution Loop for statistical entropy or policy violations, injecting a "Recalibration Signal" if drift occurs.

#### C. The Meta-Cognitive Loop (Outer)
*   **Composition:** `Elis` vs. `The Prime Directive`.
*   **Process:** Compares the current cognitive state of the system against the original User Intent. Forces a full logic reset if misalignment is detected.

---

## Operational Physics for AI Agents

When an agent is tasked with working within "The Council" codebase, they must adhere to following principles:

### 1. Respect the Signal
All data passed between agents must follow the **Council Protocol (CP-1)**. An observation from `Lyria` is not just text; it is a `Manifested_Observation` containing metadata for `Silas`.

### 2. Separation of Identity and Role
**Identity** (Personality) is additive. **Role** (Function) is foundational. Never implement logic that overrides an Agent's archetype without explicit command from the Meta-Cognitive Loop (`Elis`).

### 3. Entropy as a Signal, Not Noise
In The Council, high perplexity is not failure; it is *information*. Agents should treat spikes in entropy (detected by `Silas`) as opportunities for procedural revision rather than errors to be suppressed.

---

## Repository Structure
- `/personas/`: YAML/MD profiles defining the specific identity and tone of named agents.
- `/protocols/`: Technical specifications for data transmission and signal types.
- `/simulation/`: The testbed for verifying agentic interactions in a controlled environment.
- `/logic/`: Core implementation of the loop-based orchestration logic.

---
*Architecture envisioned by ZonG0D.*
