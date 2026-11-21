# Answers - 12 business questions (chinook, sakila, northwind)

Method (trusted-sql-analyst skill): I profiled each database, wrote each query, ran the helper's `check` on it, then wrote a second query by a different route and ran `compare`. Every primary query got a PASS or an explained REVIEW, and every second query AGREES with the primary one. Totals were reconciled wherever there was a breakdown. All access was read-only. Money amounts are in the databases' own currency units (no currency is stored).

---

## Q1 (chinook) - Top 3 genres by sales revenue

**Rock 826.65, Latin 382.14, Metal 261.36** (all-time, 2009-01-01 to 2013-12-22).

| rank | genre | revenue |
|---|---|---|
| 1 | Rock | 826.65 |
| 2 | Latin | 382.14 |
| 3 | Metal | 261.36 |

- Definition: revenue = SUM(UnitPrice x Quantity) on invoice lines, grouped by the genre of each track. There is no refund or cancellation data.
- Checks: PASS. The second query (correlated subquery per genre) AGREES. All 24 genre totals add up to 2,328.60, which equals SUM(Invoice.Total). No ties near 3rd place.

```sql
SELECT g.Name AS genre, ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS revenue
FROM InvoiceLine il
JOIN Track t ON t.TrackId = il.TrackId
JOIN Genre g ON g.GenreId = t.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY revenue DESC, g.Name
LIMIT 3;
```

## Q2 (chinook) - Invoices in July 2012

**7 invoices, total value 39.62.**

- Definition: InvoiceDate from 2012-07-01 up to but not including 2012-08-01. Dates are stored as text with a ' 00:00:00' suffix, so a date range is used.
- Checks: PASS. The second query (sum of the invoice lines, filtered by month) AGREES: 7 / 39.62.

```sql
SELECT COUNT(*) AS invoices, ROUND(SUM(Total), 2) AS total_value
FROM Invoice
WHERE InvoiceDate >= '2012-07-01' AND InvoiceDate < '2012-08-01';
```

## Q3 (chinook) - Share of business customers

**16.95%** (10 of 59 customers have a company name).

- Definition: a business customer has a Company value that is not NULL and not blank. The denominator is all 59 customers. There are no blank or whitespace-only company names.
- Checks: PASS. A second query (scalar subqueries) AGREES.

```sql
SELECT SUM(CASE WHEN Company IS NOT NULL AND TRIM(Company) <> '' THEN 1 ELSE 0 END) AS business_customers,
       COUNT(*) AS all_customers,
       ROUND(100.0 * SUM(CASE WHEN Company IS NOT NULL AND TRIM(Company) <> '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_business
FROM Customer;
```

## Q4 (sakila) - Payments received in July 2005

**28,373.89** received in July 2005, from 6,711 payments.

- Definition: payment.payment_date from 2005-07-01 up to but not including 2005-08-01. payment_date has a time part, so a date range is used: a `BETWEEN ... '2005-07-31'` filter would drop payments made later on 31 July.
- Checks: PASS. The second query (`strftime('%Y-%m') = '2005-07'`) AGREES.

```sql
SELECT COUNT(*) AS payments, ROUND(SUM(amount), 2) AS total_amount
FROM payment
WHERE payment_date >= '2005-07-01' AND payment_date < '2005-08-01';
```

## Q5 (sakila) - Payments by film rating vs overall total

**Overall total of all payments = 67,416.51** (16,049 payments). The five ratings add up to **67,406.56**, which is **9.95 less** than the overall total.

| rating | payments | total |
|---|---|---|
| G | 2,773 | 11,664.23 |
| PG | 3,212 | 13,337.91 |
| PG-13 | 3,585 | 15,259.16 |
| R | 3,181 | 13,270.19 |
| NC-17 | 3,293 | 13,875.07 |
| **Sum of ratings** | 16,044 | **67,406.56** |
| No rental linked | 5 | 9.95 |
| **Overall** | 16,049 | **67,416.51** |

- **Why they differ:** 5 payments (9.95 in total) have a NULL rental_id. They cannot be traced through rental -> inventory -> film to any film, so they have no rating. An INNER JOIN silently drops them; the LEFT JOIN used here keeps them as "No rental linked". With that group included, the totals reconcile exactly.
- Path: payment -> rental -> inventory -> film.rating. Each payment links to at most one rental, so nothing is double counted (the joined row count equals the 16,049 payments).
- Checks: REVIEW (TSQ106, COUNT(*) after LEFT JOIN). This does not matter here: the count is meant to be per payment, and the only unmatched rows are the 5 real payments, which are deliberately shown. The second query (aggregate per film first, then roll up by rating, plus a NOT EXISTS for unlinked payments) AGREES.

```sql
SELECT COALESCE(f.rating, 'No rental linked') AS rating, COUNT(*) AS payments, ROUND(SUM(p.amount), 2) AS total
FROM payment p
LEFT JOIN rental r ON r.rental_id = p.rental_id
LEFT JOIN inventory i ON i.inventory_id = r.inventory_id
LEFT JOIN film f ON f.film_id = i.film_id
GROUP BY COALESCE(f.rating, 'No rental linked')
ORDER BY CASE COALESCE(f.rating, 'No rental linked') WHEN 'G' THEN 1 WHEN 'PG' THEN 2 WHEN 'PG-13' THEN 3
         WHEN 'R' THEN 4 WHEN 'NC-17' THEN 5 ELSE 6 END;

-- overall total
SELECT ROUND(SUM(amount), 2) AS overall_total FROM payment;   -- 67,416.51
```

## Q6 (sakila) - Films never rented

**42 films** (out of 1,000 in the catalogue) have never been rented.

- Definition: the catalogue is the `film` table. A film counts as never rented if no copy of it in inventory appears in `rental`. All 42 of these films have no inventory copies at all, and every film that has a copy has been rented at least once. One inventory copy has never been rented, but its film was rented through other copies.
- Checks: PASS. The helper skipped its join-row check for the correlated subquery, so the cross-check covers it: the second query (1,000 minus the distinct films that appear in rentals) AGREES with 42.

```sql
SELECT COUNT(*) AS never_rented
FROM film f
WHERE NOT EXISTS (SELECT 1 FROM inventory i JOIN rental r ON r.inventory_id = i.inventory_id
                  WHERE i.film_id = f.film_id);
```

## Q7 (northwind) - Freight per shipping company, orders shipped in 2016

**Total 366,753.00 over 1,503 orders.**

| shipper | orders | total freight |
|---|---|---|
| Speedy Express | 488 | 124,897.75 |
| Federal Shipping | 519 | 124,525.00 |
| United Package | 496 | 117,330.25 |

- Definition: ShippedDate from 2016-01-01 up to but not including 2017-01-01. Unshipped orders (ShippedDate NULL, 21 rows) are excluded. Freight is summed straight from Orders, with no join to order lines, so there is no fan-out. Some dates have a time part and some do not; the range filter handles both.
- Checks: PASS. The second query (`substr(ShippedDate,1,4)='2016'` with a shipper-name subquery) AGREES. The three shipper totals add up to the ungrouped total of 366,753.

```sql
SELECT s.CompanyName AS shipper, COUNT(o.OrderID) AS orders, ROUND(SUM(o.Freight), 2) AS total_freight
FROM Orders o
JOIN Shippers s ON s.ShipperID = o.ShipVia
WHERE o.ShippedDate >= '2016-01-01' AND o.ShippedDate < '2017-01-01'
GROUP BY s.ShipperID, s.CompanyName
ORDER BY total_freight DESC;
```

## Q8 (northwind) - Orders placed on 1 January 2016

**4 orders** (OrderIDs 11198, 16278, 17769, 26312).

- Definition: OrderDate from 2016-01-01 up to but not including 2016-01-02. A naive `OrderDate = '2016-01-01'` returns **0**, because all 4 orders have a time of day. The helper flags that version as FAIL (TSQ108).
- Checks: PASS. The second query (`date(OrderDate) = '2016-01-01'`, COUNT DISTINCT) AGREES.

```sql
SELECT COUNT(*) AS orders
FROM Orders
WHERE OrderDate >= '2016-01-01' AND OrderDate < '2016-01-02';
```

## Q9 (chinook) - Customers and revenue per sales support agent

| agent (EmployeeId) | customers | invoice revenue |
|---|---|---|
| Jane Peacock (3) | 21 | 833.04 |
| Margaret Park (4) | 20 | 775.40 |
| Steve Johnson (5) | 18 | 720.16 |
| **Total** | **59** | **2,328.60** |

- Definition: agents are employees with Title 'Sales Support Agent'. Customers are assigned through Customer.SupportRepId. Revenue is the Invoice.Total of those customers' invoices, all time. Customers and revenue are aggregated separately before joining, to avoid fan-out.
- Checks: PASS. The second query (correlated subqueries, with revenue summed from invoice lines) AGREES. The totals reconcile to all 59 customers and 2,328.60 of revenue.

```sql
WITH cust AS (SELECT SupportRepId, COUNT(*) AS customers FROM Customer GROUP BY SupportRepId),
     rev  AS (SELECT c.SupportRepId, SUM(i.Total) AS revenue
              FROM Invoice i JOIN Customer c ON c.CustomerId = i.CustomerId
              GROUP BY c.SupportRepId)
SELECT e.EmployeeId, e.FirstName || ' ' || e.LastName AS agent,
       COALESCE(cust.customers, 0) AS customers, ROUND(COALESCE(rev.revenue, 0), 2) AS revenue
FROM Employee e
LEFT JOIN cust ON cust.SupportRepId = e.EmployeeId
LEFT JOIN rev  ON rev.SupportRepId  = e.EmployeeId
WHERE e.Title = 'Sales Support Agent'
ORDER BY e.EmployeeId;
```

## Q10 (sakila) - Actors in the most films

| actor | films |
|---|---|
| GINA DEGENERES (id 107) | 42 |
| WALTER TORN (id 102) | 41 |
| MARY KEITEL (id 198) | 40 |

- Definition: distinct films per actor_id in film_actor. Grouping is by actor_id, not by name, because some names are shared by different actors. 4th place is 39 (MATTHEW CARREY), so there are no ties at the cut-off.
- Checks: PASS. The second query (correlated count over film) AGREES on the top 5.

```sql
SELECT a.actor_id, a.first_name || ' ' || a.last_name AS actor, COUNT(DISTINCT fa.film_id) AS films
FROM actor a JOIN film_actor fa ON fa.actor_id = a.actor_id
GROUP BY a.actor_id, a.first_name, a.last_name
ORDER BY films DESC, a.actor_id
LIMIT 3;
```

## Q11 (chinook) - USA customers and recorded state

**13 customers are from the USA, and all 13 have a state recorded.**

- Definition: Country is 'USA'. I checked for variants (case, spaces, 'United States') and found none. "State recorded" means State is not NULL and not blank.
- Checks: PASS. The second query (exact match, COUNT(State)) AGREES.

```sql
SELECT COUNT(*) AS usa_customers,
       SUM(CASE WHEN State IS NOT NULL AND TRIM(State) <> '' THEN 1 ELSE 0 END) AS with_state
FROM Customer
WHERE UPPER(TRIM(Country)) IN ('USA', 'US', 'UNITED STATES', 'U.S.A.', 'U.S.');
```

## Q12 (northwind) - Share of order lines with any discount

**0.14%** (838 of 609,283 order lines have a discount > 0).

- Definition: an order line is a row in "Order Details", and a discount is Discount > 0. There are no NULL discounts. The exact value is 0.1375%, which rounds to 0.14%.
- Checks: PASS. The second query (`COALESCE(Discount,0) <> 0`, subquery ratio) AGREES.

```sql
SELECT SUM(CASE WHEN Discount > 0 THEN 1 ELSE 0 END) AS discounted_lines,
       COUNT(*) AS all_lines,
       ROUND(100.0 * SUM(CASE WHEN Discount > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_discounted
FROM "Order Details";
```
