# GPT from Scratch in Python

A GPT-style language model built from scratch in PyTorch, trained on ML/AI literature or Wikipedia.  
The goal was to understand and implement the core Transformer architecture end-to-end — tokenization, attention, training loop, and inference, without relying on pre-built model libraries.

A Java implementation of the same concept by us can be found here: [gpt-from-scratch-java](https://github.com/jonaebel/gpt-from-scratch-java) (simmular context but in python we switcht for more comfort and performance )

## Architecture

The model is a decoder-only Transformer (GPT-style) with:

| Component | Details |
|---|---|
| Embedding dim | 256 |
| Attention heads | 5 |
| Transformer blocks | 4 |
| Context length | 128 tokens |
| Tokenizer | SentencePiece (BPE, vocab size 1000) |
| Activation | GELU |
| Regularization | Dropout (0.2), LayerNorm (pre-norm) |
| Optimizer | AdamW (lr 3e-4) |

Each Transformer block consists of:
- Multi-head causal self-attention (with masking)
- Position-wise feed-forward network (4x expansion)
- Residual connections + LayerNorm

## Project Structure

```
.
├── parse_wiki.py              # Extract plain text from a Wikipedia XML dump
├── TrainingScripts/
│   ├── cleanandmerge.py       # Text cleaning and merging of source files
│   ├── training.py            # Model definition + training loop
│   └── loadmodel.py           # Load checkpoint and run inference
├── LLM/
│   ├── AILLM_V2_Optimized.pth # Final trained model weights
│   └── checkpoint_4999.pth    # Checkpoint at step 4999
├── Tokenizer/
│   └── V2Optimized/           # Trained SentencePiece tokenizer
└── Data/
    ├── wikipedia/             # Place raw Wikipedia XML dump here
    └── V2/
        └── cleanedtxt/
            └── merged.txt     # Cleaned training corpus
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Option A — Train on Wikipedia data

Download a Wikipedia dump from [dumps.wikimedia.org](https://dumps.wikimedia.org/dewiki/latest/) (`dewiki-latest-pages-articles.xml.bz2`), extract it, and place the `.xml` file under `Data/wikipedia/`. Then run:

```bash
python parse_wiki.py [max_mb]
```

This extracts clean plain text from all main-namespace articles (no redirects, no templates, no markup) and writes it to `Data/V2/wiki_plain.txt`. The optional `max_mb` argument caps the output size (default: 500 MB).

### Option B — Train on custom text files

Place any `.txt` source files in `Data/V2/`, then run:

```bash
python TrainingScripts/cleanandmerge.py
```

This cleans (removes page numbers, URLs, boilerplate) and merges all files into `Data/V2/cleanedtxt/merged.txt`.

### Train from scratch

```bash
python TrainingScripts/training.py
```

Trains a new model on `Data/V2/cleanedtxt/merged.txt` and saves checkpoints to `LLM/`. The SentencePiece tokenizer is trained automatically on the first run.

### Run inference with trained model

```bash
python TrainingScripts/loadmodel.py
```

Loads `LLM/AILLM_V2_Optimized.pth` and generates 500 tokens, printing to stdout and saving to `generated/generated.txt`.

## Authors

Built together by **[Peer Grunow](https://github.com/peergrunow-star)** and **[Jonathan Ebel](https://github.com/jonaebel)**.
