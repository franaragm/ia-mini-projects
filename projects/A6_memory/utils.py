import re
import unicodedata

def get_field(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^a-z0-9áéíóúüñ ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_memory_text(text: str) -> str:
    if not text:
        return ""

    invisible = ["\u200b", "\ufeff", "\u200e", "\u200f"]
    for ch in invisible:
        text = text.replace(ch, "")

    text = text.strip()

    if text == "-":
        return ""

    if not text:
        return ""

    non_info = {
        "ok", "vale", "si", "sí", ".", "bien", "correcto",
        "entendido", "perfecto"
    }

    if text.lower() in non_info:
        return ""

    return text
