"""α-law calculator: E(n) = E₁ × n^α for chemical bonds."""
__version__ = "0.1.0"

from .calculator import get_bond, predict, compute_alpha, morse_predict_alpha
from .data import BONDS, ATOMIC_ALPHAS
