## SQL check: FAIL ❌

Rows returned: **1** · dialect sqlite · sqlanalyst 1.1.0

| # | severity | rule | problem |
|---|---|---|---|
| 1 | high | TSQ108 Date filter does not match how dates are stored | payment.payment_date includes a time of day, so `<= '2005-07-31'` (or BETWEEN … AND '2005-07-31') stops at midnight and drops 679 rows later on 2005-07-31. |

**Fixes**
1. Use payment_date < (the day after 2005-07-31) as the upper bound.

**Result preview**

| SUM(amount) |
|---|
| 25,505.68 |

