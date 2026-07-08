# CP-1: The Council Communication Protocol (Version 0.1-Alpha)

## Overview
CP-1 defines the formal schema for all inter-agent telemetry, state observations, and control signals within The Council architecture. It ensures that asynchronous agents—ranging from high-level reasoning loops to low-level mathematical monitors—can interact through a common semantic interface.

---

## 📡 Signal Types

### 1. Observation Signals (`OBS`)
Emitted by the **Execution Loop** (Lyria/Sage) and consumed by the **Stability Loop** (Silas/Lexus).
*   **`OBS_STATE`**: A snapshot of the current semantic vector, entropy levels, and local history.
    ```json
    { "type": "OBS_STATE", "agent": "Lyria", "timestamp": 1720654321, "vector": [0.4, 0.8, 0.1], "entropy": 0.12 }
    ```
*   **`OBS_CONTEXT_FRAGMENT`**: A semantic slice of a recently retrieved piece of data (from Sage).

### 2. Audit Signals (`AUD`)
Emitted by the **Stability Loop**-based agents to notify the Execution Loop of internal deviations.
*   **`AUD_STABILITY_WARNING`**: Triggered when $\Delta S$ (Entropy) approaches the threshold $\Omega$.
    ```json
    { "type": "AUD_STABILITY_WARNING", "cause": "High_Perplexity", "severity": "low" }
    ```
*   **`AUD_POLICY_VIOLATION`**: Triggered when a semantic path violates the boundary set by Lexis.
    ```json
    { "type": "AUD_POLICY_VIOLATION", "violation_type": "Constraint_Breach", "location": [0.5, 0.1] }
    ```

### 3. Control Signals (`CTRL`)
Emitted by the **Meta-Cognitive Loop** (Elis) to override current execution logic via direct interruption.
*   **`CTRL_RECALIBRATE`**: Instructs `Weaver` to discard the current DAG and re-calculate based on the last stable state.
    ```json
    { "type": "CTRL_RECALIBRATE", "reason": "Alignment_Drift", "anchor_index": 42 }
    ```
*   **`CTRL_HALT`**: Immediate termination of execution due to critical failure.

---

## 🛠 Data Integrity & Semantic Space

### Vector Normalization
All vectors communicated via `OBS_STATE` must be normalized within a unit hypersphere: $\sum |v|^2 = 1$. This ensures that "distance" measurements (Euclidean/Cosine) used by the Arbiter (`Lexus`) remain consistent across different scales of reasoning.

### The Precision-Complexity Tradeoff
*   **Coarse Signals:** Used for high-frequency monitoring (`Silas`). Uses scalar values or small vectors. High throughput, low overhead.
*   **Fine Signals:** Used for deep architectural reconfiguration (`Elis/Weaver`). Uses full graph structures (DAGs) and high-dimensional semantic descriptors. Low frequency, high computational cost.

---

## 📜 Implementation Requirement: The "Signal-to-Action" Mapping

Every agent implementation must contain a `handle_signal(signal)` method capable of processing the specific `type` defined in CP-1. Failure to respond to a `CTRL_RECALIBRATE` signal is considered an architectural breach and will be caught by the Simulation Testbed.

*Architecture envisioned by ZonG0D.*
