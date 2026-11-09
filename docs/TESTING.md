# Testing

The automated tests can be run locally; no CI service is required.

## Backend

Run the fast, dependency-light tests:

```bash
pytest -m 'not requires_eda and not slow and not requires_services' -q
```

Tests that need installed EDA tools, containers, databases, or hosted services are marked and can be selected separately:

```bash
pytest -m 'requires_eda or slow or requires_services' -q
```

Relevant markers are registered in `pytest.ini`:

- `requires_eda`: needs an EDA tool or flow, such as Icarus Verilog, Yosys, SymbiYosys, XLS, or ORFS.
- `requires_services`: needs an external service or daemon.
- `slow`: long-running integration coverage.

## Frontend

```bash
cd frontend
npm test
npx tsc --noEmit
```
