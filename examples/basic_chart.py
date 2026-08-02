from pathlib import Path

from simplyjyotish_engine import BirthDetails, calculate_birth_chart

birth = BirthDetails.model_validate_json(
    (Path(__file__).parent / "sample_birth.json").read_text(encoding="utf-8")
)
chart = calculate_birth_chart(birth)
print(chart.model_dump_json(indent=2))
