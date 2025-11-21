from kaldra_engine.preprocessing import simple_tokenize


def test_simple_tokenize_runs():
    result = simple_tokenize("hello world test")
    assert isinstance(result, list)
    assert len(result) == 3


def test_simple_tokenize_empty():
    result = simple_tokenize("")
    assert isinstance(result, list)
