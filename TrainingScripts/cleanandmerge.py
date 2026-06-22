import emoji
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent
datafolder = BASE_DIR / "Data" / "V2"
output_file = BASE_DIR / "Data" / "V2" / "cleanedtxt" / "merged.txt"

output_file.parent.mkdir(parents=True, exist_ok=True)


# ---------------- CLEANING FUNCTIONS ----------------

def clean_text(text: str) -> str:
    text = emoji.replace_emoji(text, replace="")

    text = text.replace("\x0c", "\n")

    text = re.sub(r"\bContents\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bForeword\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bIndex\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bReferences\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bDraft.*?\n", "", text, flags=re.IGNORECASE)
    text = re.sub(r"https?://\S+", "", text)

    text = re.sub(r"\n\s*\d+\s*\n", "\n", text)
    text = re.sub(r"\n\s*[ivxlcdm]+\s*\n", "\n", text, flags=re.IGNORECASE)

    text = re.sub(r"\n\s*[a-zA-Z0-9]\s*\n", "\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def get_txt(datafolder: Path) -> str:
    text = ""
    for file in datafolder.rglob("*.txt"):
        text += file.read_text(encoding="utf-8")
    return text


# ---------------- MERGE + CLEAN ----------------
def merge_presort() -> None:
    with output_file.open("w", encoding="utf-8") as out:
        for file in datafolder.rglob("*.txt"):
            if file.is_file():
                raw = file.read_text(encoding="utf-8", errors="ignore")
                cleaned = clean_text(raw)
                out.write(f"\n\n===== {file.name} =====\n\n")
                out.write(cleaned)
                out.write("\n")

    print("successfully merged & cleaned!")


# ---------------- MERGE + SECONDARY CLEAN ----------------
def merge_sort(input: Path, output: Path) -> None:
    cleaned_list = []
    with input.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if re.match(r'^\(\d+\.\d+\)$', stripped):
            continue

        if re.match(r'^\d*\.?\d+$', stripped):
            continue

        if len(line) < 10 and not line.endswith("."):
            continue

        cleaned_list.append(line)

    with output.open("w", encoding="utf-8") as out:
        out.writelines(cleaned_list)


if __name__ == "__main__":
    merge_presort()
    merge_sort(input=output_file, output=output_file)
