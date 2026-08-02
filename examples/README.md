# Public package examples

From the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-deps .
.\.venv\Scripts\python.exe -m simplyjyotish chart --input examples\sample_birth.json
```

The same calculation is available as a library call:

```powershell
.\.venv\Scripts\python.exe examples\basic_chart.py
```

`expected_chart_output.json` is a small deterministic output excerpt for the
sample input. Full outputs include all planets, houses and provenance fields.
