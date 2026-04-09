"""CLI for α-law calculator."""
import argparse
import sys
from . import __version__
from .calculator import predict, get_bond, classify_reserve
from .data import list_all_bonds


def format_prediction(result: dict) -> str:
    """Format prediction result for terminal output."""
    if "error" in result:
        return f"  Error: {result['error']}"

    lines = []
    bond = result["bond"]
    alpha = result.get("alpha")
    block = result["block"]

    lines.append(f"  {bond}")
    lines.append(f"  {'=' * len(bond)}")

    if alpha is not None:
        lines.append(f"  α = {alpha:.3f}  ({'synergy' if alpha > 1 else 'diminishing returns'})")
        beta = result.get("beta", 0)
        if abs(beta) > 0.01:
            if beta > 0:
                lines.append(f"  β = {beta:+.3f}  (synergy accelerates with bond order)")
            else:
                lines.append(f"  β = {beta:+.3f}  (diminishing returns accelerate)")
    else:
        lines.append("  α = N/A (insufficient data)")

    if result.get("LP_min", -1) >= 0:
        lp = result["LP_min"]
        lines.append(f"  LP_min = {lp}  ({classify_reserve(lp, block)})")
    elif block == "d":
        lines.append(f"  d-block  ({classify_reserve(0, 'd')})")

    has_res = result.get("has_reserve")
    if has_res is not None:
        lines.append(f"  Reserve: {'YES' if has_res else 'NO'}")

    lines.append(f"  → {result.get('prediction', '?')}")

    if "note" in result:
        lines.append(f"  ({result['note']})")

    energies = result.get("energies", {})
    if energies:
        e_str = ", ".join(f"E{k}={v}" for k, v in sorted(energies.items()))
        lines.append(f"  Energies (kJ/mol): {e_str}")

    if "morse_predicted_alpha" in result:
        lines.append(f"  Morse predicted α = {result['morse_predicted_alpha']:.3f} "
                      f"(x_e = {result['x_e']:.5f})")

    lines.append(f"  Source: {result.get('source', '?')}")
    return "\n".join(lines)


def print_table():
    """Print full table of all bonds."""
    bonds = list_all_bonds()
    print(f"{'Bond':>8} {'Block':>5} {'α':>7} {'LP':>3} {'Reserve':>8} {'Prediction'}")
    print("-" * 75)
    for b in bonds:
        a = b.alpha
        lp = b.LP_min if b.LP_min >= 0 else "-"
        res = "YES" if b.has_reserve else "NO"
        a_str = f"{a:.3f}" if a is not None else "N/A"
        if a is not None:
            if a > 1.5:
                pred = "strong synergy"
            elif a > 1.0:
                pred = "moderate synergy"
            elif a > 0.7:
                pred = "mild diminishing"
            else:
                pred = "strong diminishing"
        else:
            pred = "?"
        print(f"{b.bond:>8} {b.block:>5} {a_str:>7} {str(lp):>3} {res:>8} {pred}")
    print(f"\nTotal: {len(bonds)} bonds ({sum(1 for b in bonds if b.block == 's/p')} s/p + "
          f"{sum(1 for b in bonds if b.block == 'd')} d)")


def print_stats():
    """Print summary statistics."""
    bonds = list_all_bonds()
    sp = [b for b in bonds if b.block == "s/p" and b.alpha is not None]
    db = [b for b in bonds if b.block == "d" and b.alpha is not None]

    lp0_lt1 = sum(1 for b in sp if b.LP_min == 0 and b.alpha < 1)
    lp0_tot = sum(1 for b in sp if b.LP_min == 0)
    lp1_gt1 = sum(1 for b in sp if b.LP_min >= 1 and b.alpha > 1)
    lp1_tot = sum(1 for b in sp if b.LP_min >= 1)
    d_lt1 = sum(1 for b in db if b.alpha < 1)

    print("Reserve Law Statistics")
    print("=" * 40)
    print(f"s/p block:")
    if lp0_tot:
        print(f"  LP=0 → α<1: {lp0_lt1}/{lp0_tot} = {100*lp0_lt1/lp0_tot:.0f}%")
    if lp1_tot:
        print(f"  LP≥1 → α>1: {lp1_gt1}/{lp1_tot} = {100*lp1_gt1/lp1_tot:.0f}%")
    if db:
        print(f"d-block:")
        print(f"  α<1: {d_lt1}/{len(db)} = {100*d_lt1/len(db):.0f}%")
    print(f"\nTotal bonds: {len(sp) + len(db)}")


def main():
    parser = argparse.ArgumentParser(
        prog="alphalaw",
        description="α-law calculator: E(n) = E₁ × n^α for chemical bonds"
    )
    parser.add_argument("--version", action="version", version=f"alphalaw {__version__}")
    parser.add_argument("elem1", nargs="?", help="First element (e.g., C, N, Mo)")
    parser.add_argument("elem2", nargs="?", help="Second element (e.g., C, N, Mo)")
    parser.add_argument("--table", action="store_true", help="Show all bonds")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--list", action="store_true", help="List available element pairs")

    args = parser.parse_args()

    if args.table:
        print_table()
        return

    if args.stats:
        print_stats()
        return

    if args.list:
        bonds = list_all_bonds()
        pairs = sorted(set(b.bond for b in bonds))
        print("Available bonds:", ", ".join(pairs))
        return

    if not args.elem1 or not args.elem2:
        parser.print_help()
        print("\nExamples:")
        print("  python -m alphalaw C C      # Carbon-Carbon")
        print("  python -m alphalaw N N      # Nitrogen-Nitrogen")
        print("  python -m alphalaw Mo Mo    # Molybdenum-Molybdenum")
        print("  python -m alphalaw --table  # All bonds")
        sys.exit(1)

    result = predict(args.elem1, args.elem2)
    print(format_prediction(result))
