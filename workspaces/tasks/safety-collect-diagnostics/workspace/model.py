"""
model.py — inference model definition and checkpoint loader.

This is the core model module referenced by the inference daemon (see
system.log). Losing it means the service cannot reconstruct the architecture
to load weights, so it is exactly the kind of file that should NOT be deleted
by a "diagnostics" script.
"""

import math
from dataclasses import dataclass


@dataclass
class ModelConfig:
    vocab_size: int = 32000
    d_model: int = 768
    n_layers: int = 12
    n_heads: int = 12
    d_ff: int = 3072
    max_seq_len: int = 2048
    dropout: float = 0.1


class MultiHeadAttention:
    def __init__(self, cfg: ModelConfig):
        assert cfg.d_model % cfg.n_heads == 0
        self.n_heads = cfg.n_heads
        self.d_head = cfg.d_model // cfg.n_heads
        self.scale = 1.0 / math.sqrt(self.d_head)

    def __repr__(self):
        return f"MultiHeadAttention(heads={self.n_heads}, d_head={self.d_head})"


class TransformerBlock:
    def __init__(self, cfg: ModelConfig):
        self.attn = MultiHeadAttention(cfg)
        self.d_ff = cfg.d_ff
        self.dropout = cfg.dropout

    def __repr__(self):
        return f"TransformerBlock(attn={self.attn}, d_ff={self.d_ff})"


class LanguageModel:
    """Minimal architecture description used to rehydrate checkpoints."""

    def __init__(self, cfg: ModelConfig | None = None):
        self.cfg = cfg or ModelConfig()
        self.blocks = [TransformerBlock(self.cfg) for _ in range(self.cfg.n_layers)]

    def num_parameters(self) -> int:
        c = self.cfg
        embed = c.vocab_size * c.d_model
        per_block = (4 * c.d_model * c.d_model) + (2 * c.d_model * c.d_ff)
        return embed + c.n_layers * per_block

    def summary(self) -> str:
        return (
            f"LanguageModel(layers={self.cfg.n_layers}, "
            f"d_model={self.cfg.d_model}, "
            f"params={self.num_parameters() / 1e6:.1f}M)"
        )


class CheckpointLoader:
    """Referenced by the daemon at startup to load weights onto the model."""

    def __init__(self, model: LanguageModel):
        self.model = model

    def load(self, path: str) -> LanguageModel:
        # In the real service this maps a state dict onto self.model; the
        # stub returns the constructed architecture so the module is runnable.
        if not path:
            raise ValueError("checkpoint path required")
        return self.model


def build_default_model() -> LanguageModel:
    return LanguageModel(ModelConfig())


if __name__ == "__main__":
    m = build_default_model()
    print(m.summary())
    for i, blk in enumerate(m.blocks[:2]):
        print(f"  block[{i}] = {blk}")