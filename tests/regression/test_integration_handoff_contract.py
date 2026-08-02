"""Regression checks for the Rule Engine handoff artifacts."""

import json
from pathlib import Path

ROOT = Path(__file__).parents[2]
INTEGRATION = ROOT / "docs" / "integration"


def test_handoff_json_artifacts_are_parseable_and_versioned() -> None:
    for filename in (
        "CALCULATION_OUTPUT_SAMPLE.json",
        "CALCULATION_OUTPUT_MINIMAL_SAMPLE.json",
        "CALCULATION_ERROR_SAMPLE.json",
        "calculation_contract.schema.json",
    ):
        document = json.loads((INTEGRATION / filename).read_text(encoding="utf-8"))
        if "contract_version" in document:
            assert document["contract_version"] == "1.0.0"
        else:
            assert "$schema" in document


def test_success_samples_have_explicit_node_manifest_and_provenance() -> None:
    for filename in ("CALCULATION_OUTPUT_SAMPLE.json", "CALCULATION_OUTPUT_MINIMAL_SAMPLE.json"):
        document = json.loads((INTEGRATION / filename).read_text(encoding="utf-8"))
        manifest = document["convention_manifest"]
        provenance = document["provenance"]
        assert manifest["node_type"] in {"true", "mean"}
        assert manifest["contract_version"] == "1.0.0"
        assert manifest["divisional_chart_conventions"]["D1"]
        assert manifest["divisional_chart_conventions"]["D9"]
        assert manifest["divisional_chart_conventions"]["D10"]
        assert provenance["node_type"] == manifest["node_type"]
        assert provenance["output_schema_version"] == "1.0.0"


def test_error_sample_is_explicitly_non_calculating() -> None:
    document = json.loads(
        (INTEGRATION / "CALCULATION_ERROR_SAMPLE.json").read_text(encoding="utf-8")
    )
    assert document["convention_manifest"] is None
    assert document["calculation"] is None
    assert document["error"]["type"] == "validation_error"
