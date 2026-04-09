"""Tests for α-law calculator."""
import pytest
from alphalaw.calculator import get_bond, predict, compute_alpha, morse_predict_alpha
from alphalaw.data import BONDS, ATOMIC_ALPHAS, get_bond_data, list_all_bonds


class TestData:
    def test_bonds_not_empty(self):
        assert len(BONDS) >= 35

    def test_sp_bonds_count(self):
        sp = [b for b in BONDS if b.block == "s/p"]
        assert len(sp) >= 27

    def test_d_bonds_count(self):
        d = [b for b in BONDS if b.block == "d"]
        assert len(d) >= 7

    def test_lookup_symmetric(self):
        assert get_bond_data("C", "N") is not None
        assert get_bond_data("N", "C") is not None
        assert get_bond_data("C", "N") is get_bond_data("N", "C")

    def test_lookup_case_insensitive(self):
        assert get_bond_data("c", "c") is not None
        assert get_bond_data("MO", "MO") is not None


class TestAlpha:
    """α_simple (OLS through origin) for classification."""

    def test_cc_alpha(self):
        b = get_bond_data("C", "C")
        assert 0.75 < b.alpha < 0.9  # OLS through origin: ~0.81

    def test_nn_alpha_gt1(self):
        b = get_bond_data("N", "N")
        assert b.alpha > 1.0  # synergy: ~1.55

    def test_momo_alpha_lt1(self):
        b = get_bond_data("Mo", "Mo")
        assert b.alpha < 1.0  # diminishing: ~0.71

    def test_oo_alpha_gt1(self):
        b = get_bond_data("O", "O")
        assert b.alpha > 1.5  # strong synergy


class TestTwoParam:
    """2-parameter model (α, β) for prediction accuracy."""

    def test_nn_beta_positive(self):
        b = get_bond_data("N", "N")
        assert b.beta > 0.3  # accelerating synergy

    def test_cc_beta_near_zero(self):
        b = get_bond_data("C", "C")
        assert abs(b.beta) < 0.1  # power law is good for C-C

    def test_momo_beta_negative(self):
        b = get_bond_data("Mo", "Mo")
        assert b.beta < -0.1  # decelerating (δ ceiling)

    def test_predict_energy_exact_2pt(self):
        b = get_bond_data("O", "O")
        E_pred = b.predict_energy(2)
        assert abs(E_pred - 498) < 1  # exact for 2-point bond

    def test_predict_energy_accurate_3pt(self):
        b = get_bond_data("N", "N")
        for n, E_act in b.energies.items():
            E_pred = b.predict_energy(n)
            err = abs(E_pred - E_act) / E_act
            assert err < 0.01, f"N-N n={n}: {E_pred:.0f} vs {E_act}, err={err:.1%}"


class TestReserveLaw:
    """Core rule: LP=0 → α<1 (using simple α)."""

    def test_lp0_alpha_lt1(self):
        sp = [b for b in BONDS if b.block == "s/p" and b.LP_min == 0 and b.alpha is not None]
        lt1 = sum(1 for b in sp if b.alpha < 1)
        assert lt1 / len(sp) >= 0.80  # at least 80%

    def test_d_block_mostly_lt1(self):
        d = [b for b in BONDS if b.block == "d" and b.alpha is not None]
        lt1 = sum(1 for b in d if b.alpha < 1)
        assert lt1 / len(d) >= 0.50  # d-block complex, at least half


class TestMorse:
    def test_morse_predict_lp0(self):
        a = morse_predict_alpha(1854.7, 13.34, LP=0)
        assert 0.6 < a < 0.9

    def test_morse_predict_lp1(self):
        a = morse_predict_alpha(2358.6, 14.32, LP=1)
        assert a > 1.0


class TestPredict:
    def test_predict_cc(self):
        r = predict("C", "C")
        assert "error" not in r
        assert r["alpha"] is not None

    def test_predict_nn_synergy(self):
        r = predict("N", "N")
        assert r["alpha"] > 1

    def test_predict_unknown(self):
        r = predict("Unobtanium", "Unobtanium")
        assert "error" in r

    def test_predict_mo(self):
        r = predict("Mo", "Mo")
        assert r["block"] == "d"
