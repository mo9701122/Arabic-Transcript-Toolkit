import unittest

from arabic_toolkit.lint import lint_text


def rules(text):
    return {i.rule for i in lint_text(text)}


class LintTests(unittest.TestCase):
    def test_clean_text(self):
        self.assertEqual(lint_text("مرحبا بكم [noise] في البرنامج\n"), [])

    def test_unknown_tag(self):
        self.assertIn("unknown-tag", rules("مرحبا [cough] بكم"))

    def test_unbalanced_tag(self):
        self.assertIn("unbalanced-tag", rules("مرحبا [noise بكم"))

    def test_mixed_digits(self):
        self.assertIn("mixed-digits", rules("عام ٢٠٢٦ و 2027"))

    def test_repeated_word(self):
        self.assertIn("repeated-word", rules("ذهبت ذهبت إلى السوق"))

    def test_spacing(self):
        self.assertEqual(rules("كلمة  كلمة "), {"double-space", "trailing-space", "repeated-word"})

    def test_line_numbers(self):
        issues = lint_text("سطر نظيف\nسطر [x] خاطئ")
        self.assertEqual(issues[0].line, 2)


if __name__ == "__main__":
    unittest.main()
