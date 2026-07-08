# The Council: Neural DNA

This document provides the fundamental mathematical and tensor-level mappings.
## Elis
* **Essence:** Intent Stability
* **Operator:** `Semantic-Anchor Gradient Descent`
* **Tensor/Structural Shape:** `[Batch, Sequence, Hidden_Dimension]`
* **Interaction Mechanism:** Alignment of user distribution $P(U)$ to goal manifold $\mathcal{G}$.

## Lyria
* **Essence:** Probabilistic Realization
* **Operator:** `Stochastic Softmax Mapping`
* **Tensor/Structural Shape:** `[Batch, Vocab_Size]`
* **Interaction Mechanism:** Entropy-weighted token sampling $\theta(x) \sim P(y|x)$.

## Sage
* **Essence:** Temporal Coherence
* **Operator:** `Attention-Weighted Accumulation`
* **Tensor/Structural Shape:** `[Batch, Seq, Head_Dim]`
* **Interaction Mechanism:** Maximizing $QK^T$ dot-product compatibility across historical windows.

## Lexus
* **Essence:** Structural Constraint
* **Operator:** `Logit Boundary Projection`
* **Tensor/Structural Shape:** `[Batch, Vocab_Size]`
* **Interaction Mechanism:** Information bottlenecking via $\mathcal{L}_{\text{mask}}$.

## Silas
* **Essence:** Informational Stability
* **Operator:** `Entropy/Perplexity Gradient Monitoring`
* **Tensor/Structural Shape:** `[Batch, Sequence]`
* **Interaction Mechanism:** Tracking $-\log P(x)$ to detect distributional shift.

## Weaver
* **Essence:** Procedural Complexity
* **Operator:** `DAG Scheduler / Recursive Expansion`
* **Tensor/Structural Shape:** `[Task_Sequence, Dependency_Matrix]`
* **Interaction Mechanism:** Decomposing high-level entropy into low-entropy discrete steps.
