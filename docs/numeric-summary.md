# Numeric summary helper

`src.stats.summarize_numbers` converts a mixed iterable into a typed metrics payload.
It accepts finite `int` and `float` values, excludes booleans, and ignores `NaN`,
`Infinity`, `-Infinity`, strings, `None`, and objects.

The return value is a `NumberSummary` `TypedDict` with these keys:

| Key | Meaning |
| --- | --- |
| `count` | Number of accepted numeric values. |
| `total` | Sum of accepted numeric values. |
| `minimum` | Lowest accepted numeric value, or `None` when there are no values. |
| `maximum` | Highest accepted numeric value, or `None` when there are no values. |
| `average` | Arithmetic mean, or `None` when there are no values. |
| `values` | Accepted values in their original order. |

```python
from src.stats import summarize_numbers

summary = summarize_numbers([1, None, "2", True, 3.5])
assert summary["values"] == [1, 3.5]
assert summary["average"] == 2.25
```

The boolean exclusion is deliberate because Python treats `bool` as an `int`
subclass. The finite-number check prevents `NaN` or infinity from propagating
through `sum`, `min`, `max`, and `average`.

## Review notes

This PR is the clean Froholdt end-to-end demo for check-run lifecycle validation.
