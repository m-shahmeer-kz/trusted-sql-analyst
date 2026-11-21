## SQL check: FAIL ❌

Rows returned: **1** · dialect sqlite · sqlanalyst 1.1.0

| # | severity | rule | problem |
|---|---|---|---|
| 1 | high | TSQ101 NOT IN with a subquery that returns NULL | The subquery in `NOT customer.state IN (SELECT invoice.billingstate AS billingstate FROM invoice AS invoic…` returns 7 NULL value(s). With even one NULL, NOT IN is never true, so this condition removes every row. |

**Fixes**
1. Use NOT EXISTS (… WHERE inner.key = outer.key), or add WHERE key IS NOT NULL inside the subquery.

**Result preview**

| COUNT(*) |
|---|
| 0 |

