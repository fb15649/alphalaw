"""Tests for α-law calculator."""
import pytest
from alphalaw.calculator import get_bond, predict, compute_alpha, morse_predict_alpha
from alphalaw.data import BONDS, ATOMIC_ALPHAS, get_bond_data, list_all_bonds


class TestData:
    def test_bonds_not_empty(self):
        assert len(BONDS) >= 23  # 19 s/p + 4 d

    def test_sp_bonds_count(self):
        sp = [b for b in BONDS if b.block == "s/p"]
        assert len(sp) == 19

    def test_d_bonds_count(self):
        d = [b for b in BONDS if b.block == "d"]
        assert len(d) == 4

    def test_lookup_symmetric(self):
        assert get_bond_data("C", "N") is not None
        assert get_bond_data("N", "C") is not None
        assert get_bond_data("C", "N") is get_bond_data("N", "C")

    def test_lookup_case_insensitive(self):
        assert get_bond_data("c", "c") is not None
        assert get_bond_data("MO", "MO") is not None


class TestAlpha:
    def test_cc_alpha(self):
        b = get_bond_data("C", "C")
        assert b is not None
        assert 0.7 < b.alpha < 0.85  # known: ~0.77

    def test_nn_alpha(self):
        b = get_bond_data("N", "N")
        assert b.alpha > 1.8  # known: ~2.01

    def test_momo_alpha(self):
        b = get_bond_data("Mo", "Mo")
        assert 0.5 < b.alpha < 0.8  # known: ~0.65

    def test_compute_alpha_two_points(self):
        a = compute_alpha({1: 346, 2: 614})
        assert 0.7 < a < 0.9

    def test_compute_alpha_three_points(self):
        a = compute_alpha({1: 346, 2: 614, 3: 839})
        assert 0.7 < a < 0.85


class TestReserveLaw:
    """Test the core rule: LP=0 → α<1, LP≥1 → α>1."""

    def test_lp0_alpha_lt1(self):
        sp = [b for b in BONDS if b.block == "s/p" and b.LP_min == 0 and b.alpha is not None]
        lt1 = sum(1 for b in sp if b.alpha < 1)
        assert lt1 / len(sp) >= 0.85  # at least 85% (actual: 93%)

    def test_lp1_alpha_gt1(self):
        sp = [b for b in BONDS if b.block == "s/p" and b.LP_min >= 1 and b.alpha is not None]
        gt1 = sum(1 for b in sp if b.alpha > 1)
        assert gt1 / len(sp) >= 0.75  # at least 75% (actual: 80%)

    def test_d_block_all_lt1(self):
        d = [b for b in BONDS if b.block == "d" and b.alpha is not None]
        assert all(b.alpha < 1 for b in d)


class TestMorse:
    def test_morse_predict_lp0(self):
        # C-C: x_e = 0.00719, LP=0 → α ≈ 0.75
        a = morse_predict_alpha(1854.7, 13.34, LP=0)
        assert 0.6 < a < 0.9

    def test_morse_predict_lp1(self):
        # N-N: x_e = 0.00607, LP=1 → α > 1
        a = morse_predict_alpha(2358.6, 14.32, LP=1)
        assert a > 1.0


class TestPredict:
    def test_predict_cc(self):
        r = predict("C", "C")
        assert "error" not in r
        assert r["alpha"] is not None
        assert "diminishing" in r["prediction"].lower()

    def test_predict_nn(self):
        r = predict("N", "N")
        assert r["alpha"] > 1
        assert "synergy" in r["prediction"].lower()

    def test_predict_unknown(self):
        r = predict("Unobtanium", "Unobtanium")
        assert "error" in r

    def test_predict_mo(self):
        r = predict("Mo", "Mo")
        assert r["block"] == "d"
        assert r["alpha"] < 1
