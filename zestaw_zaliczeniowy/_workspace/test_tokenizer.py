
import pytest
from tokenizer import Tokenizer

@pytest.fixture
def tokenizer():
    """Default Tokenizer dla wiêkszoœci testów."""
    return Tokenizer()

@pytest.fixture
def imdb_sample():
    """20 recenzji z imdb -- wspóldzielone miêdzy testami integracyjnymi."""
    from datasets import load_dataset
    ds = load_dataset("stanfordnlp/imdb", split="train").shuffle(seed=42).select(range(20))
    return [r["text"] for r in ds]

@pytest.mark.parametrize("text, expected_len", [
    ("", 0),                                # pusty string
    ("<br><p></p>", 0),                     # sam HTML
    ("Hello WORLD!", 2),                    # mieszany case
    ("...!?!?!?", 0),                       # tylko interpunkcja
    ("za¿ó³æ gêœl¹ jaŸñ", 3),               # polskie diakrytyki
    ("the cat sat on the mat", 6),          # zwykle zdanie
])
def test_tokenize_cases(tokenizer, text, expected_len):
    """Parametryzowany test z 6 przypadkami brzegowymi."""
    assert len(tokenizer.tokenize(text)) == expected_len

def test_tokenize_acceptance_cases(tokenizer):
    """Asercje akceptacji ze specyfikacji."""
    assert tokenizer.tokenize("<br>Hello WORLD!") == ["hello", "world"]
    assert tokenizer.vocab(["aa bb", "bb cc"]) == {"aa", "bb", "cc"}

def test_vocab_dedup(tokenizer):
    """Test deduplicacji w vocab."""
    assert tokenizer.vocab(["aa bb", "bb cc"]) == {"aa", "bb", "cc"}

def test_min_length_filter():
    """Test filtrowania po d³ugoœci."""
    tok = Tokenizer(min_length=4)
    assert tok.tokenize("a bb ccc dddd eeeee") == ["dddd", "eeeee"]

def test_lower_false():
    """Test gdy lower=False."""
    tok = Tokenizer(lower=False)
    assert tok.tokenize("Hello") == ["Hello"]

def test_strip_html_false():
    """Test gdy strip_html=False."""
    tok = Tokenizer(strip_html=False)
    assert tok.tokenize("<br>hello") == ["br", "hello"]

def test_imdb_integration(tokenizer, imdb_sample):
    """Insight test: ile œrednio unikalnych tokenów na 20 recenzji?"""
    vocab = tokenizer.vocab(imdb_sample)
    vocab_size = len(vocab)
    print(f"\n[INSIGHT] Vocab na 20 recenzjach: {vocab_size} unikalnych tokenów")
    assert vocab_size > 500, f"za ma³o unikalnych tokenów: {vocab_size}"

@pytest.mark.xfail(reason="Tokenizer nie wspiera jeszcze email patterns")
def test_advanced_regex_email():
    """Demonstracja xfail -- ten test ma prawo nie dzia³aæ."""
    tok = Tokenizer()
    assert tok.tokenize("user@domain.com")[0] == "user@domain.com"
