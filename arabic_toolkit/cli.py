"""Command-line interface."""
import argparse
import sys
from pathlib import Path

from . import __version__
from .lint import lint_text
from .normalize import normalize
from .wer import compute_wer


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="arabic-toolkit", description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize", help="print normalized text")
    p_norm.add_argument("file")
    p_norm.add_argument("--taa-marbuta", action="store_true", help="also unify ة and ه")

    p_lint = sub.add_parser("lint", help="check a transcript for formatting issues")
    p_lint.add_argument("file")

    p_wer = sub.add_parser("wer", help="word error rate between two transcripts")
    p_wer.add_argument("reference")
    p_wer.add_argument("hypothesis")
    p_wer.add_argument("--raw", action="store_true", help="skip normalization")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "normalize":
        print(normalize(_read(args.file), unify_taa_marbuta=args.taa_marbuta))
        return 0
    if args.command == "lint":
        issues = lint_text(_read(args.file))
        for issue in issues:
            print(issue)
        print(f"{len(issues)} issue(s) found", file=sys.stderr)
        return 1 if issues else 0
    if args.command == "wer":
        r = compute_wer(_read(args.reference), _read(args.hypothesis), normalize_text=not args.raw)
        print(f"WER: {r.wer:.2%}  (S={r.substitutions} D={r.deletions} I={r.insertions} N={r.ref_words})")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
