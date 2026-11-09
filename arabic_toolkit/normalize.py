"""Arabic text normalization helpers."""
import re
import unicodedata

DIACRITICS = re.compile(r"[\u064B-\u0652\u0670\u06D6-\u06ED]")
TATWEEL = "\u0640"
ALEF_VARIANTS = re.compile("[\u0622\u0623\u0625\u0671]")  # آ أ إ ٱ
DIGIT_MAP = str.maketrans(
    "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669"
    "\u06F0\u06F1\u06F2\u06F3\u06F4\u06F5\u06F6\u06F7\u06F8\u06F9",
    "01234567890123456789",
)


def normalize(
    text: str,
    *,
    strip_diacritics: bool = True,
    unify_alef: bool = True,
    unify_yaa: bool = True,
    unify_taa_marbuta: bool = False,
    western_digits: bool = True,
) -> str:
    """Return a normalized version of ``text`` suitable for comparison."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace(TATWEEL, "")
    if strip_diacritics:
        text = DIACRITICS.sub("", text)
    if unify_alef:
        text = ALEF_VARIANTS.sub("\u0627", text)
    if unify_yaa:
        text = text.replace("\u0649", "\u064A")  # ى -> ي
    if unify_taa_marbuta:
        text = text.replace("\u0629", "\u0647")  # ة -> ه
    if western_digits:
        text = text.translate(DIGIT_MAP)
    return re.sub(r"\s+", " ", text).strip()
