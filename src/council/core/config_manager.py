from pathlib import Path

class CouncilConfig:
    """The Single Source of Truth (SSOT) for all pathing and environment variables."""
    ROOT = Path(__file__).resolve().parent.parent.parent.parent
    SRC_DIR = ROOT / "src"
    CORE_DIR = SRC_DIR / "council" / "core"
    EXPERIMENTS_DIR = ROOT / "experiments"

    @property
    def signal_path(self): 
        return self.CORE_DIR / "signals.jsonl"

cfg = CouncilConfig()
if __name__ == "__main__":
    print(f"ROOT: {cfg.ROOT}")
    print(f"SIGNAL PATH: {csrf.signal_path if 'csrf' in locals() else cfg.signal_path}")
