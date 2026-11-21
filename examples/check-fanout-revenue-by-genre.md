## SQL check: FAIL ❌

Rows returned: **24** · dialect sqlite · sqlanalyst 1.1.0

| # | severity | rule | problem |
|---|---|---|---|
| 1 | high | TSQ105 Join multiplies rows before SUM/AVG/COUNT (fan-out) | After the joins, each `Invoice` row appears 5.44 times on average (2,240 joined rows for 412 Invoice rows). SUM(i.total) therefore adds up the same `Invoice` rows several times. |

**Fixes**
1. Aggregate `Invoice` at its own grain before joining (subquery/CTE), or use COUNT(DISTINCT key); never SUM/AVG a parent-table column after joining to its child rows.

**Verified**
- Reconciled (internal consistency): the 24 group totals of `revenue` add up to the ungrouped total of the same rows, 20,848.62. This does not prove the rows themselves are right.

**Result preview**

| Name | revenue |
|---|---|
| Rock | 7,720.02 |
| Latin | 3,472.55 |
| Metal | 2,093.13 |
| Alternative & Punk | 1,961.66 |
| TV Shows | 817.71 |
| Jazz | 746.46 |
| Drama | 544.61 |
| Blues | 429.66 |
| R&B/Soul | 338.62 |
| Reggae | 332.64 |
| Classical | 317.04 |
| Soundtrack | 242.55 |
| Pop | 239.75 |
| Alternative | 211.17 |
| Sci Fi & Fantasy | 198.87 |
| World | 182.18 |
| Hip Hop/Rap | 166.41 |
| Heavy Metal | 161.37 |
| Electronica/Dance | 149.62 |
| Easy Listening | 138.6 |

