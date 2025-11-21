from apps.product.product_analyzer import analyze_product_text


def test_analyze_product_text_runs():
    result = analyze_product_text("Great product, highly recommended!")
    assert "archetype" in result
    assert "bias_score" in result
    assert "kindra_distribution" in result
