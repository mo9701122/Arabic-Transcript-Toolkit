"""Word error rate with substitution/deletion/insertion breakdown."""
from dataclasses import dataclass

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


def compute_wer(reference: str, hypothesis: str, *, normalize_text: bool = True) -> WERResult:
    if normalize_text:
        reference, hypothesis = normalize(reference), normalize(hypothesis)
    ref, hyp = reference.split(), hypothesis.split()
    n, m = len(ref), len(hyp)

    # dp[i][j] = minimum edits to turn ref[:i] into hyp[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if ref[i - 1] == hyp[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + cost, dp[i - 1][j] + 1, dp[i][j - 1] + 1)

    # Backtrace to count each error type.
    subs = dels = ins = 0
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if ref[i - 1] == hyp[j - 1] else 1):
            if ref[i - 1] != hyp[j - 1]:
                subs += 1
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            dels += 1
            i -= 1
        else:
            ins += 1
            j -= 1
    return WERResult(subs, dels, ins, n)
