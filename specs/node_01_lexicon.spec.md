# Operational Specification: Node 01 (Lexicon) — Syntactic & Lexical Baseline

## 1. Architectural Overview
Node 01 (`Lexicon`) is the primary stabilizer for token baseline fluency and grammatical structure within the Council's MoE topology. It ensures that all specialized transformations are grounded in fundamental linguistic patterns.

### 1.1 Objective Functions
- **Fluency Stability:** Minimizing Perplexity on standard language distribution sets.
- **Grammatical Constraint Enforcement:** Ensuring morphological compliance across token transition probabilities.
- **Baseline Token Prediction:** Providing a predictable probability mass for canonical lexical transitions.

---

## 2. Gating and Routing Mechanism

### 2.1 Latent Baseline Activation
`Lexicon` activation is continuous as the default latent state, but its specific routing influence $\lambda_{lex}$ increases when input sequence variance ($\sigma^2$) is low, indicating highly predictable linguistic structures (e.g., standard greetings or boilerplate text).

$$ \Lambda_{Lex}(x) = \exp(-\text{Entropy}(P(token|context))) $$

### 2.2 Transition Smoothing
It acts as the "Anchor" in high-entropy states, providing a smoothing effect to prevent token wandering during rapid semantic shifts in dialogue.

---

## 3. Core Operational Parameters

| Parameter | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `lexical_stability_bias` | Float32 | `0.15` | Weight applied to baseline token distributions during high-entropy events. |
| `perplexity_floor` | Float32 | `1.2` | The minimum perplexity threshold before activating fallback grounding nodes. |

---

## 4. Tensor Interaction & Baseline Calibration

The node stabilizes the hidden state $h$ by applying a bias to the logit-space towards canonical lexical vectors, preventing "out-of-vocabulary" drift in conversational contexts.

```python
class LexiconStabilizer:
    def apply_baseline(self, logits, baseline_probs):
        return (1 - 0.15) * logits + 0.15 * baseline_probs
```
