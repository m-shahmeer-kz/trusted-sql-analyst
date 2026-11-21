## SQL check: REVIEW ⚠️

Rows returned: **5** · dialect sqlite · sqlanalyst 1.1.0

| # | severity | rule | problem |
|---|---|---|---|
| 1 | medium | TSQ125 Grouping by a name merges different records | Grouping by first_name, last_name merges different `actor` records that share the same value: e.g. 2 different actor_id values are called 'SUSAN DAVIS'. |

**Fixes**
1. GROUP BY actor_id (and show the name next to it).

**Verified**
- COUNT(*) counts rows at the grain of `film_actor` (5,462 rows after joins and filters).

**Result preview**

| actor | films |
|---|---|
| SUSAN DAVIS | 54 |
| GINA DEGENERES | 42 |
| WALTER TORN | 41 |
| MARY KEITEL | 40 |
| MATTHEW CARREY | 39 |

