# Trusted SQL Analyst - measured results

All numbers come from the files in this folder. Databases: three public SQLite samples -
Chinook (music store, 11 tables), Northwind extended (trading company, 30 tables/views,
609,283 order lines) and Sakila (DVD rental, 21 tables/views).

## 1. Blind test (the headline number) - `holdout2_*`
A separate AI agent that never saw the tool wrote 24 realistic wrong queries plus the
correct query for each, labelled "sql-mechanics" (the SQL silently does something other
than intended) or "business-meaning" (valid SQL for a different question). The checker
(v1.1.0, frozen) was run once.

| | flagged | genuine catch* |
|---|---|---|
| sql-mechanics mistakes | 15 / 16 | **14 / 16** |
| business-meaning mistakes | 0 / 8 | 0 / 8 |
| correct queries given a REVIEW note | 2 / 24 | |

\* genuine = the wrong query gets a medium/high finding that its correct version does not.
Missed mechanics: a join on the wrong key (CustomerId = EmployeeId) and swapped roles in a
self-join. Business-meaning mistakes (wrong date column, list price vs price charged,
wrong definition) are by design not detectable from SQL + data; the skill handles them
with the glossary step and the two-route cross-check, which this test does not measure.

## 2. First blind set - `holdout_*` (no longer blind)
Written the same way by another fresh agent. Run once on v1.0.0: 10 / 24 flagged (one for
the wrong reason), 3 correct queries flagged. Its misses led to five new checks
(TSQ121-TSQ125) and fewer false alarms in v1.1.0: now 13 / 24 flagged, 1 correct query
flagged - but this set was used to improve the tool, so it is not a blind number any more.

## 3. Development cases - `cases.py`, `results.json`
32 realistic wrong/right pairs written while building the tool (tuned on them):
31 / 32 wrong queries flagged, 0 / 32 correct queries flagged, all 32 wrong answers differ
from the right ones (e.g. Chinook revenue by genre 20,848.62 vs 2,328.60 - a 9x
double-count; Northwind freight 206.9M vs 4.0M). The one miss is intended: an INNER JOIN
that drops rows in a plain list is now a low note, not a warning.

## 4. With vs without the skill - 12 business questions
Two fresh agents (same model) answered the same 12 questions on the three databases; one
had the skill. Both got **12 / 12** right against answers verified two ways. On questions
like these a strong model working carefully does not need the skill to be accurate; the
measured value of the skill is catching mistakes (sections 1-3) and producing answers with
stated assumptions and checks. The skill agent's feedback (one output folder for several
databases; a check that errored on a correlated subquery) was fixed in v1.1.0.

## 5. Speed
Profiling: Chinook 0.05 s, Sakila 0.24 s, Northwind 2.8 s. `check`: median 0.005 s, max
0.5 s on the 609k-line database.

## 6. Tests
46 pytest tests (every rule fires on a bad query and stays quiet on a good one, read-only
guard, timeout, CSV via DuckDB, CLI), CI on Python 3.10 and 3.13.
