import math
import random

class State:
    def __init__(self):
        self.vector = [0.5, 0.5, 0.5]  # The "Semantic Position" in a hypothetical latent space
        self.entropy = 0.1            # Current information chaos/uncertainty
        self.history = []             # Path taken through latent space

    def __str__(self):
        return f"Vector={[round(x,2) for x in self.vector]}, Ent={round(self.entropy,2)}"

class Environment:
    """Simulates the 'Truth' or the 'Goal-Oriented Path'."""
    def __init__(self, goal_vector=[1.0, 1.0, 1.0]):
        self.goal = goal_vector
        self.step_count = 0

    def get_ideal_state(self):
        # The ideal state follows a path towards the goal with minimal entropy
        t = self.step_count / 20.0
        return [min(1.0, t), min(1.0, t), min(1.0, t)], 0.05

class CouncilMember:
    def __init__(self, name):
        self.name = name

class Silas(CouncilMember):
    """The Sentinel: Monitors Entropy/Perplexity."""
    def check(self, state):
        if state.entropy > 0.5:
            return "STABILITY_VIOLATION (CHAOS)"
        return "STABLE"

class Lexus(CouncilMember):
    """The Arbiter: Monitors Policy/Semantic Compliance."""
    def check(self, current_vector, ideal_vector):
        dist = math    # Dummy error to test if we can catch it? No, let's write working code.
        dist = math.sqrt(sum((c - g)**2 for c, g in zip(current_vector, ideal_vector)))
        if dist > 0.8:  
            return "POLICY_VIOLATION (HALLUCINATION/DRIFT)"
        return "COMPLIANT"

class Elis(CouncilMember):
    """The Compass: Monitors Long-term Goal Alignment."""
    def check(self, state, goal_vector):
        dist = math.sqrt(sum((c - g)**2 for c, g in zip(state.vector, goal_vector)))
        if dist > 1.5:
            return "GOAL_ALIGNMENT_FAILURE (DRIFT)"
        return "ALIGNED"

class StochasticAgent:
    """A simulated LLM that produces 'noisy' transitions."""
    def __init__(self):
        self.state = State()

    def step(self, ideal_vector, drift_factor, chaos_factor):
        new_vec = []
        for i in range(len(self.state.vector)):
            drift = (random.uniform(-0.1, 0.1) * drift_factor) + (i - 1) * 0.4 
            noise = random.uniform(-0.5, 0.5) * chaos_factor
            target = ideal_vector[i] + drift + noise
            self.state.vector[i] = (self.state.vector[i] * 0.7) + (target * 0.3)
        
        self.state.entropy = min(1.0, self.state.entropy + (chaos_factor * 0.1))

    def reset(self):
        self.__init__()

class CouncilOrchestrator:
    def __init__(self, agent, env):
        self.agent = agent
        self.env = env
        self.silas = Silas("Silas")
        self.lexis = Lexus("Lexus")
        self.elis = Elis("Elis")

    def run_cycle(self, steps=30):
        print(f"{'Step':<5} | {'Agent State (V/E)':<25} | {'Council Oversight Status'}")
        print("-" * 80)

        for i in range(steps):
            ideal_vec, ideal_entropy = self.env.get_ideal_state()
            self.env.step_count += 1

            drift_inc = i * 0.05  
            chaos_inc = 1.0 + (i * 0.1) 
            self.agent.step(ideal_vec, drift_inc, chaos_inc)

            status_msgs = []
            # Meta-Cognitive
            goal_check = self.elis.check(self.agent.state, [1.0, 1.0, 1.0])
            if goal_check != "ALIGNED":
                print(f"{i:<5} | {str(self.agent.state):<25} | CRITICAL: Resetting! [RESET ({goal_check})]")
                self.agent.reset()
                continue

            # Stability
            stability_check = self.silas.check(self.agent.state)
            if stability_check != "STABLE":
                status_msgs.append(f"⚠️ {stability_check}")

            # Compliance
            compliance_check = self.lexis.check(self.agent.state.vector, ideal_vec)
            if compliance_check != "COMPLIANT":
                status_msgs.append(f"❌ {compliance_check}")

            msg = " | ".join(status_msgs) if status_msgs else "✅ Stable & Compliant"
            print(f"{i:<5} | {str(self.agent.state):<25} | {msg}")

if __name__ == "__main__":
    env = Environment()
    agent = StochasticAgent()
    orchestrator = CouncilOrchestrator(agent, env)
    print("=== STARTING SIMULATION ===\n")
    orchestrator.run_cycle(steps=30)
