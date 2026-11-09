# Arabic Transcript Toolkit

A dependency-free Python CLI for people who transcribe and review Arabic audio.

- **normalize**: strips diacritics and tatweel, unifies alef/yaa forms, converts digits
- **lint**: flags formatting problems (unknown or unbalanced tags, mixed digits, repeated words, spacing)
- **wer**: word error rate with substitution/deletion/insertion breakdown

## Usage
```bash
python -m arabic_toolkit lint samples/transcript.txt
python -m arabic_toolkit wer samples/reference.txt samples/hypothesis.txt
python -m arabic_toolkit normalize samples/transcript.txt
python -m unittest discover
```

## Roadmap
- [ ] Dialect-aware normalization (Sudanese, Gulf, Egyptian, Levantine)
- [ ] Character error rate (CER) and per-line WER report
- [ ] Configurable tag set via a config file
- [ ] Batch mode for whole folders and CSV/JSON output
- [ ] Optional ASR integration to auto-compare model output with human transcripts
- [ ] CI with GitHub Actions
