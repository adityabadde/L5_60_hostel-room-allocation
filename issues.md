# Static Code Analysis Issue Log

This table documents issues found by reviewing the original `hostel_allocation.py`. The workflow in `.github/workflows/static-analysis.yml` generates the actual Pylint, Bandit, and Flake8 baseline reports and updated reports. Line numbers below refer to `baseline/hostel_allocation_before.py`, the preserved original version.

| Issue | Type / severity | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Flask debug mode | Security / high | 80 | Debug mode can expose the Werkzeug debugger and enable arbitrary code execution. Bandit reported this as B201, high severity. | Run the portal with `debug=False`. |
| Room capacity comparison | Logic bug / high | 34 | The original `>` check allows an additional occupant when a room is already exactly full. | Reject allocation when occupant count is greater than or equal to capacity. |
| Unsafe YAML loader | Security / medium | 21 | `yaml.load(..., Loader=yaml.Loader)` can construct Python objects when parsing untrusted input. Bandit reported B506 at medium severity. | Use `yaml.safe_load()` and validate the expected configuration structure. |
| Remote logging configuration listener | Security / medium | 72 | A network logging configuration listener can introduce unsafe configuration handling if enabled. Bandit reported B612 at medium severity. | Remove the unused listener function and its import. |
| Missing gender validation | Logic bug / medium | 32–38 | The allocator does not compare a student's gender with the room's configured gender. | Skip rooms whose configured gender does not match the student's gender. |
| Vacating does not free the bed | Logic bug / medium | 41–44 | Removing the student from `allocations` leaves their ID in the room's occupant list. | Remove the ID from both the allocation map and room occupant list. |
| Unsafe HTML construction | Security / medium | 77 | The lookup endpoint concatenates request input into HTML without escaping it. | Escape the query value and displayed result before returning HTML. |
| Duplicate allocations | Logic bug / medium | 32–38 | Allocating the same student again can append duplicate occupant entries. | Reject a student ID that already has an allocation. |
| Seniority ordering | Logic bug / medium | 53 | The original sort uses ascending study year even though the demonstration asks for seniors first. | Sort in descending year order. |
| Mutable default argument | Code quality / medium | 29 | `preferred=[]` is a shared mutable default. Pylint reported this as a dangerous default value. | Use `None` and create a new list for each call. |
| Hard-coded password | Security / low | 66 | A credential is embedded in source code. Bandit reported B106 at low severity. | Read connection settings from environment variables and never return the password. |
| Non-cryptographic lottery randomness | Security / low | 3, 56 | The original lottery uses the default pseudo-random generator. Bandit reported B311 at low severity. | Use a system-backed secure sampler for lottery ordering. |
| Vacancy count only counts empty rooms | Logic bug / low | 58–62 | Partially occupied rooms may have free beds, but the original function ignores them. | Sum each room's capacity minus its occupant count. |
| Weak input validation | Code quality | 30, 47–48 | The year and stay length are not validated consistently; invalid data can produce unexpected behaviour. | Validate types and ranges, and raise a clear error for invalid stay lengths or missing allocations. |
| Unused imports and inconsistent style | Code quality / style | 1–6 and throughout | The original file includes unused imports, camelCase names, long lines, and missing blank lines. Pylint and Flake8 reported these issues. | Remove unused imports, use snake_case names, and format the code consistently. |

## Verification

The GitHub Actions workflow runs all three tools against both the preserved original file and the cleaned `hostel_allocation.py`, saving six reports at the repository root:

- `pylint_report_before.txt` and `pylint_report_after.txt`
- `bandit_report_before.txt` and `bandit_report_after.txt`
- `flake8_report_before.txt` and `flake8_report_after.txt`

Use the generated reports as evidence for which warnings were raised by each tool. The logic issues in this table were also found through code review; not every logic bug is necessarily detected by a static analysis tool.
