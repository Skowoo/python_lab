
import re

class Tokenizer:
    """Konfigurowany tokenizator: HTML strip + case + min length filter."""
    def __init__(self, lower: bool = True, strip_html: bool = True, min_length: int = 1):
        self.lower = lower
        self.strip_html = strip_html
        self.min_length = min_length

    def tokenize(self, text: str) -> list[str]:
        """Tokenizuje tekst: HTML strip -> lowercase -> regex -> length filter."""
        if self.strip_html:
            text = re.sub(r"<[^>]+>", " ", text)
        if self.lower:
            text = text.lower()
        tokens = re.findall(r"\w+", text, re.UNICODE)
        return [t for t in tokens if len(t) >= self.min_length]

    def vocab(self, texts: list[str]) -> set[str]:
        """Zwraca uniê wszystkich unikalnych tokenów ze wszystkich tekstów."""
        result = set()
        for text in texts:
            result.update(self.tokenize(text))
        return result
