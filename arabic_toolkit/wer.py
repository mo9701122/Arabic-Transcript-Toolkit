"""Word error rate with substitution/deletion/insertion breakdown."""
from dataclasses import dataclass
from typing import NamedTuple

from .normalize import normalize


@dataclass(frozen=True)
class WERResult:
    substitutions: int
    deletions: int
    insertions: int
    ref_words: int

    @property
    def errors(self) -> int:
        return self.substitutions + self.deletions + self.insertions

    @property
    def wer(self) -> float:
        if self.ref_words == 0:
            return 0.0 if self.errors == 0 else float("inf")
        return self.errors / self.ref_words


class WordError(NamedTuple):
    kind: str        # "substitution", "deletion" or "insertion"
    reference: str   # reference word ("" for an insertion)
    typed: str       # typed word ("" for a deletion)
    line: int        # reference line for deletions, typed line otherwise


def _tokens(text: str, normalize_text: bool) -> list[tuple[str, int]]:
    """Split text into (word, line number) pairs, optionally normalized first."""
    tokens = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        cleaned = normalize(line) if normalize_text else line
        tokens.extend((word, line_no) for word in cleaned.split())
    return tokens


def _align(ref: list[tuple[str, int]], hyp: list[tuple[str, int]]) -> list[WordError]:
    """Align two token lists with edit distance and return the errors in text order."""
    rw = [w for w, _ in ref]
    hw = [w for w, _ in hyp]
    n, m = len(rw), len(hw)

    # dp[i][j] = minimum edits to turn rw[:i] into hw[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if rw[i - 1] == hw[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + cost, dp[i - 1][j] + 1, dp[i][j - 1] + 1)

    # Walk back from the bottom-right corner, recording each error.
    errors = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if rw[i - 1] == hw[j - 1] else 1):
            if rw[i - 1] != hw[j - 1]:
                errors.append(WordError("substitution", rw[i - 1], hw[j - 1], hyp[j - 1][1]))
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            errors.append(WordError("deletion", rw[i - 1], "", ref[i - 1][1]))
            i -= 1
        else:
            errors.append(WordError("insertion", "", hw[j - 1], hyp[j - 1][1]))
            j -= 1
    errors.reverse()
    return errors


def list_errors(reference: str, hypothesis: str, *, normalize_text: bool = True) -> list[WordError]:
    """Return every substitution, deletion and insertion, with its line number."""
    return _align(_tokens(reference, normalize_text), _tokens(hypothesis, normalize_text))


def compute_wer(reference: str, hypothesis: str, *, normalize_text: bool = True) -> WERResult:
    errors = list_errors(reference, hypothesis, normalize_text=normalize_text)
    return WERResult(
        substitutions=sum(e.kind == "substitution" for e in errors),
        deletions=sum(e.kind == "deletion" for e in errors),
        insertions=sum(e.kind == "insertion" for e in errors),
        ref_words=len(_tokens(reference, normalize_text)),
    )