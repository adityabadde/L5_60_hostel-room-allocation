# Lab 5: Static Code Analysis Reflection

> Note: The supplied three-page PDF explains the learning outcomes and deliverables but does not show the exact four reflection question wordings. These draft responses address the main reflection topics described in the handout. If your instructor provided the questions separately, align each heading with that exact wording.

## 1. What did static analysis help identify?

Static analysis examines source code without running the application. Reviewing the original hostel allocation script showed security concerns such as unsafe YAML loading, a hard-coded password, and debug mode enabled in Flask. It also helped identify code-quality problems such as unused imports and an unsafe mutable default argument. Reviewing the logic separately was important because tools may not detect every functional bug.

## 2. How were the issues prioritized and fixed?

Security-related issues were prioritized first because unsafe configuration handling, exposed credentials, and debug mode can create avoidable risk. The allocation logic was then corrected to respect room capacity and gender, prevent duplicate allocations, and remove occupants when a student vacates a room. Input checks and consistent naming and formatting were also improved. Fixes were intended to preserve the program's core room allocation functionality rather than merely hiding warnings.

## 3. How do Pylint, Bandit, and Flake8 differ?

Pylint reviews broader code quality and maintainability, including naming, unused imports, and programming practices. Bandit focuses on common security risks in Python source. Flake8 checks style and common lint errors, including whitespace, line length, and unused names. Their purposes overlap slightly, so using all three gives a more useful review than relying on only one tool.

## 4. What was learned, and what are the limitations of static analysis?

Static analysis can catch many issues early, before the program is executed or deployed, and its reports provide a repeatable way to check code quality. However, the tools cannot reliably identify every logical error. For example, whether a room's capacity is handled correctly and whether a vacated bed becomes available should also be checked with test cases and by inspecting program output. Static analysis is most useful when combined with running the program, testing realistic scenarios, and reviewing the changes.
