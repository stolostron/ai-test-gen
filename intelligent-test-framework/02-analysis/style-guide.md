# Test Plan Style Guide (Manual-First)

## Principles
- Keep it manual-first: steps must be human-executable, concise, and deterministic.
- Description + Setup before every table.
- 8–10 steps per table; create additional tables if needed.
- Provide CLI and UI variants where applicable in the same row.
- Avoid timing/flaky patterns (no `--watch`). Prefer outcome checks with sample outputs.
- Use simple commands; avoid complex regex/nested jsonpath unless absolutely necessary and always include a sample output line.
- Use namespace `ocm` for hub-controller resources unless specified otherwise.

## Table Template
```markdown
### Test Case X: <Descriptive Name>
**Description**:
- What this validates and why it matters (1–3 lines).

**Setup**:
- Environment prerequisites
- Test data/configuration

| Test Steps | Expected Results |
|------------|------------------|
| 1. CLI: <cmd><br/>UI: <path or N/A> | CLI verification: <example output line><br/>UI verification: <expected UI state or N/A> |
```

## Quality Checklist
- Coverage includes core success, one negative/error case, and relevant environment/RBAC variants only if meaningful.
- Each step includes a brief rationale in Expected Results.
- Sample YAMLs provided when applicable.
- Logs and outputs shown as examples, not exhaustive dumps.

