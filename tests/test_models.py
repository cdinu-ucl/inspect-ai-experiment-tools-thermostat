from pathlib import Path

from thermostat_eval.models import ucl_condenser_models


def test_ucl_condenser_models_reads_cache(tmp_path: Path):
    cache = tmp_path / "models.json"
    cache.write_text('{"data": [{"id": "condenser-poc/qwen"}], "object": "list"}')

    assert ucl_condenser_models(cache) == ("openai-api/ucl_condenser/condenser-poc/qwen",)


def test_ucl_condenser_models_missing_or_bad_cache(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json")

    assert ucl_condenser_models(tmp_path / "missing.json") == ()
    assert ucl_condenser_models(bad) == ()


def test_bundled_ucl_condenser_cache_is_valid():
    assert ucl_condenser_models()
