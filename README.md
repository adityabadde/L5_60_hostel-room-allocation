# Lab 5: Static Code Analysis: Hostel Room Allocation System

**Main program:** `hostel_allocation.py`

This repository is for Lab 5. The goal is to review Python code using Pylint, Bandit, and Flake8, fix security, logic, and style issues, and document the results.

## About the program

The example hostel allocation system loads a room configuration, allocates rooms by gender and capacity, vacates rooms, calculates fees, orders students by seniority, runs a lottery, counts vacant beds, and provides a small Flask room lookup endpoint.

## Run locally

Create and activate a virtual environment, then install the dependencies and tools:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the packages:

```bash
python -m pip install flask markupsafe pyyaml pylint bandit flake8
```

Run the program:

```bash
python hostel_allocation.py
```

## Static analysis reports

The GitHub Actions workflow at `.github/workflows/static-analysis.yml` runs all three tools against the preserved original version in `baseline/hostel_allocation_before.py` and the cleaned program in `hostel_allocation.py`. It also compiles and runs the cleaned program.

The workflow generates and commits these files to the repository:

- `pylint_report_before.txt` and `pylint_report_after.txt`
- `bandit_report_before.txt` and `bandit_report_after.txt`
- `flake8_report_before.txt` and `flake8_report_after.txt`

The reports include each tool's output and exit status. Review the generated results after the GitHub Actions run completes. The intended target is a Pylint score above 9.5, no remaining Bandit findings requiring action, and no Flake8 errors.

## Assignment documentation

- `issues.md`: documented security, logic, and code-quality findings, with original line numbers.
- `reflection.md`: reflection responses about the use and limitations of static analysis.
- `baseline/hostel_allocation_before.py`: preserved original code used to generate before-fix reports.

The supplied lab handout does not show the exact wording of the four reflection questions. If your instructor provided those questions separately, update the reflection headings to match them.

## Main improvements

- Uses `yaml.safe_load` and validates the room configuration.
- Uses a fresh list for each allocation call rather than a mutable default argument.
- Checks the room's capacity and gender before allocation, and prevents duplicate allocations.
- Removes a student from both the allocation map and room occupants when vacating.
- Counts remaining beds in partially occupied rooms.
- Reads database settings from environment variables instead of embedding a password.
- Disables Flask debug mode, escapes user-controlled text in the lookup response, and removes the remote logging configuration listener.
- Uses a system-backed random sampler for the lottery.
