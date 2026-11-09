import unittest

from arabic_toolkit.normalize import normalize


class NormalizeTests(unittest.TestCase):
    def test_strips_diacritics_and_tatweel(self):
        self.assertEqual(normalize("مُحَمَّـــد"), "محمد")

    def test_unifies_alef_and_yaa(self):
        self.assertEqual(normalize("إسلام أحمد على"), "اسلام احمد علي")

    def test_converts_digits(self):
        self.assertEqual(normalize("٢٠٢٦ و ۱۲"), "2026 و 12")

    def test_collapses_whitespace(self):
        self.assertEqual(normalize("  مرحبا   بك \n"), "مرحبا بك")

    def test_optional_taa_marbuta(self):
        self.assertEqual(normalize("مدرسة", unify_taa_marbuta=True), "مدرسه")
        self.assertEqual(normalize("مدرسة"), "مدرسة")


if __name__ == "__main__":
    unittest.main()
