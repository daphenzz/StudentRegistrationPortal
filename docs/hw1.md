# HW1 — SQL Injection

## 1. Vulnerable feature
- Feature: Student portal faculty search, `GET /students/by-faculty`.
- Vulnerable location: An earlier working-tree version of `app/registration.py`, function `get_students_by_faculty`, interpolated `faculty` into a raw SQL string. The current working tree has the parameterized fix; no vulnerable commit or tag exists in Git history.
- Test environment: Localhost and seeded fake student records only.

## 2. Attacker
An unauthenticated caller who can reach the student portal can submit a value to the faculty-search feature. Because the value is interpolated into SQL, the database may interpret part of that input as query syntax. The caller's goal is to read seeded student records outside the requested faculty; only fake records on localhost are used in this exercise. Align this description with your registered threat model before submission.

## 3. Exploit
- Reproduction: The author reports that a localhost request returned seeded students outside the selected faculty. The request was not re-run by the assistant. Add the exact localhost request and captured response from the author's own run; do not test external systems or use real records.
- Regression test command: `python -m unittest discover -s tests/security -p "test_*.py" -v`
- Expected result: Only records matching the selected faculty should be returned.
- Actual result: The all-record result is author-reported and has no saved test artifact in this repository. The regression test passes on the fixed working tree and checks that SQL-looking input is treated as a literal value.

## 4. Impact
Potential unauthorized disclosure of student rows across faculty boundaries. The local database contains seeded fake records, so no real personal data was involved in the reported exercise. Severity: Medium for a deployment containing real student records, because one search could expose records beyond the requested faculty. The reported data scope still needs to be backed by the automated test output.

## 5. Fix
- Root cause: User-controlled `faculty` text is interpolated into SQL instead of being bound as a value parameter.
- Change: `app/registration.py` now binds `faculty` as a named SQL parameter instead of interpolating it into SQL. A vulnerable-to-fixed tagged diff is unavailable because neither commit nor tag exists yet.
- Defense layers: Parameter binding at the SQL execution boundary. No input blacklist was added.
- Why it works: A bound parameter keeps the faculty value separate from SQL syntax, so the database compares it as data.

## 6. Verification
- Test pattern: The regression test asserts safe behavior. It passes on the fixed working tree; it has not been run against a committed vulnerable revision.
- CI: `.github/workflows/security.yml` runs the security test on pushes and pull requests. No GitHub Actions run exists yet because the workflow has not been pushed.

## 7. Residual risk
The endpoint has no authentication or authorization; hiding API documentation does not restrict direct access. Keep the service bound to localhost and use fake data for this exercise. A real deployment would also need authorization and access controls appropriate to student records.

## 8. Contribution
- Solo submission: [Your name] — implementation, testing, and documentation.
