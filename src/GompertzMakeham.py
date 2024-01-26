from dataclasses import dataclass

import numpy as np


def law_function(x, alpha, beta, gamma):
    return alpha * np.exp(beta * x) + gamma

@dataclass
class GompertzMakeham:
    alpha: np.float64
    beta: np.float64
    gamma: np.float64

    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    @staticmethod
    def from_sequence(seq):
        return GompertzMakeham(alpha=seq[0], beta=seq[1], gamma=seq[2])

    def to_tuple(self):
        return (self.alpha, self.beta, self.gamma)

    def __str__(self) -> str:
        return f'(alpha={self.alpha:.4f}, beta={self.beta:.4f}, gamma={self.gamma:.4f})'

    def __repr__(self) -> str:
        return f'(alpha={self.alpha:.4f}, beta={self.beta:.4f}, gamma={self.gamma:.4f})'