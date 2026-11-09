import unittest

from arabic_toolkit.wer import compute_wer


class WERTests(unittest.TestCase):
    def test_identical(self):
        r = compute_wer("هذا اختبار بسيط", "هذا اختبار بسيط")
        self.assertEqual(r.errors, 0)
        self.assertEqual(r.wer, 0.0)

    def test_substitution(self):
        r = compute_wer("هذا اختبار بسيط", "هذا امتحان بسيط")
        self.assertEqual((r.substitutions, r.deletions, r.insertions), (1, 0, 0))

    def test_deletion_and_insertion(self):
        r = compute_wer("a b c", "a c d")
        self.assertEqual(r.errors, 2)

    def test_normalization_ignores_diacritics(self):
        self.assertEqual(compute_wer("كَتَبَ", "كتب").errors, 0)

    def test_empty_reference(self):
        self.assertEqual(compute_wer("", "").wer, 0.0)
        self.assertEqual(compute_wer("", "كلمة").wer, float("inf"))


if __name__ == "__main__":
    unittest.main()
