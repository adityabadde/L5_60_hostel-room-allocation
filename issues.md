# Static Code Analysis Issue Log

This table documents issues found by reviewing the original `hostel_allocation.py`. The workflow in `.github/workflows/static-analysis.yml` generates the actual Pylint, Bandit, and Flake8 baseline reports and updated reports. Line numbers below refer to `baseline/hostel_allocation_before.py`, the preserved original version.

| Issue | Type / severity | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe YAML loader | Security / high | 21 | `yaml.load(..., Loader=yaml.Loader)` can construct Python objects from untrusted input. | Use `yaml.safe_load()` and validate the expected configuration structure. |
| Hard-coded password | Security / high | 66 | A credential is embedded in source code and can be exposed through repository history. | Read connection settings from environment variables and never return the password. |
| Remote logging configuration listener | Security / high | 72 | A network logging configuration listener can introduce unsafe configuration handling if enabled. | Remove the unused listener function and its import. |
| Flask debug mode | Security / medium | 80 | Debug mode can expose sensitive debugging information and must not be enabled in deployment. | Run the portal with `debug=False`. |
| Mutable default argument | Bug / medium | 29 | `preferred=[]` is a shared mutable default. | Use `None` and create a new list for each call. |
| Room capacity comparison | Logic bug / high | 34 | The original `>` check allows another occupant when a room is exactly full. | Reject allocation when occupant count is greater than or equal to capacity. |
| Missing gender validation | Logic bug / medium | 32–38 | The allocator does not compare a student's gender with the room's configured gender. | Skip rooms whose configured gender does not match the student's gender. |
| Vacating does not free the bed | Logic bug / medium | 41–44 | Removing the student from `allocations` leaves their ID in the room's occupant list. | Remove the ID from both the allocation map and room occupant list. |
| Duplicate allocations | Logic bug / medium | 32–38 | Allocating the same student again can append duplicate occupant entries. | Reject a student ID that already has an allocation. |
| Vacancy count only counts empty rooms | Logic bug / low | 58–62 | Partially occupied rooms may have free beds, but the original function ignores them. | Sum each room's capacity minus its occupant count. |
| Unsafe HTML construction | Security / medium | 77 | The lookup endpoint concatenates request input into HTML without escaping it. | Escape the query value and displayed result before returning HTML. |
| Non-cryptographic lottery randomness | Security / low | 3, 55 | The original lottery uses the default pseudo-random generator. | Use a system-backed secure sampler for lottery ordering. |
| Broad / weak input validation | Code quality | 30, 47–48 | The year and stay length are not validated consistently; invalid data can produce unexpected behaviour. | Validate types and ranges, and raise a clear error for invalid stay lengths or missing allocations. |
| Unused imports and inconsistent style | Code quality / style | 1–6 and throughout | The original file includes unused imports, camelCase names, long lines, and missing blank lines. | Remove unused imports, use snake_case names, and format the code consistently. |

## Verification

The workflow runs all three tools against both the preserved original file and the cleaned `hostel_allocation.py`, saving six reports at the repository root:

- `pylint_report_before.txt` and `pylint_report_after.txt`
- `bandit_report_before.txt` and `bandit_report_after.txt`
- `flake8_report_before.txt` and `flake8_report_after.txt`

Use the generated reports as the evidence for which warnings were raised by each tool. The logic issues in this table were also found through code review; not every logic bug is necessarily detected by a static analysis tool.
