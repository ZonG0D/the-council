# Council Protocol - CP-1 (Communication Protocol v1.0)

## 💠 Overview
CP-1 defines the structural requirements for all inter-agentic signals within The Council. Its purpose is to mitigate **Semantic Drift** by ensuring that messages are not merely text, but validated mathematical and contextual envelopes.

---

## 🏗️ I. Signal Envelope Anatomy (Topological Structure)

Every signal flowing through the Meso or Macro scales must conform to the following structured hierarchy:

### 1. Logical Header (Routing Meta-data)
*   `origin_id`: The archetype name of the sender (e.g., `Silas`).
*   `target_id`: The archetype name of the intended recipient (e.g., `Lyria`).
*   `sequence_id`: A monotonic incrementing integer for causal ordering.
*   `timestamp`: ISO-8601 high-resolution timestamp for temporal anchoring.

### 2. Contextual Payload (Semantic Core)
The payload must distinguish between the **Intent** and the **Observed Reality**:
*   **Intent Vector ($\vec{I}$)**: A compressed latent representation of the goal being communicated.
*   **Observation Set ($\mathcal{O}$)**: Structured data including:
    *   `perceived_entropy`: Floating-point measure of local signal chaos.
    *   `observation_vector`: Numerical data representing the detected state change.

### 3. Integrity Signature (Verification Layer)
To prevent **Technical Entropy** during transmission, every message must include:
*   `checksum`: A cryptographic hash of the payload to detect bit-rot or corruption.
*   `validation_token`: A signature derived from the current `LoopState`.

---

## 🔄 II. The Reciprocity Pattern (Interaction Logic)

Communication is not passive; it is a **Dialectic Process**.

1.  **Proffer**: Agent $A$ emits an `ObservationSignal(CP-1)`.
2.  **Perception**: Agent $B$ receives the signal, calculating the $\Delta S$ (Semantic Shift) between its own internal state and $A$'s observation.
3.  **Response/Adjustment**: If $\Delta S > \epsilon$, Agent $B$ must emit a `ControlSignal(CP-1)` to adjust the local orchestration loop.

---

## 📐 III. Mathematical Constraints for Signalling

To maintain **Systemic Precision**, all signals must respect the following:
*   **Causal Consistency**: $\text{Timestamp}(t_{n+1}) > \text{Timestamp}(t_n)$.
*   **Entropy Budgeting**: Total system entropy ($\sum H$) must not increase by more than $k\cdot\Delta t$ per orchestration tick without an accompanying `AuditSignal`.

---
*Spec finalized via RAR Protocol: Phase 2 - Documentation/Schema Update.*
