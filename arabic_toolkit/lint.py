"""Rule-based linter for Arabic transcript files."""
import re
from dataclasses import dataclass

ALLOWED_TAGS = {"noise", "music", "laugh", "unclear", "overlap", "foreign"}
ARABIC_INDIC = re.compile("[\u0660-\u0669\u06F0-\u06F9]")
WESTERN_DIGIT = re.compile("[0-9]")
TAG = re.compile(r"\[([^\[\]]*)\]")
WORD = re.compile(r"\S+")


@dataclass(frozen=True)
class Issue:
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: [{self.rule}] {self.message}"


def lint_line(line: str, number: int) -> list[Issue]:
    issues: list[Issue] = []
    if not line.strip():
        return issues
    if line != line.rstrip():
        issues.append(Issue(number, "trailing-space", "line has trailing whitespace"))
    if "  " in line.strip():
        issues.append(Issue(number, "double-space", "multiple consecutive spaces"))
    if "\u0640" in line:
        issues.append(Issue(number, "tatweel", "contains tatweel (kashida) character"))
    if ARABIC_INDIC.search(line) and WESTERN_DIGIT.search(line):
        issues.append(Issue(number, "mixed-digits", "mixes Arabic-Indic and Western digits"))
    if line.count("[") != line.count("]"):
        issues.append(Issue(number, "unbalanced-tag", "unbalanced square brackets"))
    for match in TAG.finditer(line):
        if match.group(1).strip().lower() not in ALLOWED_TAGS:
            issues.append(Issue(number, "unknown-tag", f"unknown tag [{match.group(1)}]"))
    words = WORD.findall(line)
    for a, b in zip(words, words[1:]):
        if a == b and not TAG.fullmatch(a):
            issues.append(Issue(number, "repeated-word", f"word repeated: {a}"))
    return issues


def lint_text(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for number, line in enumerate(text.splitlines(), start=1):
        issues.extend(lint_line(line, number))
    return issues
