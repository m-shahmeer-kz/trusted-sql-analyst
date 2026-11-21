# Glossary: chinook.db

Status: GUESS = inferred from names/values (confirm before relying on it) · CONFIRMED = the user said so.

## Business terms

| term | definition (SQL) | status | source |
|---|---|---|---|
| revenue | _fill in: which amount, which status, refunds/discounts?_ | TODO | |
| active customer | _fill in_ | TODO | |

## Tables (grain = what one row is)

- **Album** (347 rows): one row per AlbumId — GUESS
- **Artist** (275 rows): one row per ArtistId — GUESS
- **Customer** (59 rows): one row per CustomerId — GUESS
- **Employee** (8 rows): one row per EmployeeId — GUESS
- **Genre** (25 rows): one row per GenreId — GUESS
- **Invoice** (412 rows): one row per InvoiceId — GUESS
- **InvoiceLine** (2,240 rows): one row per InvoiceLineId — GUESS
- **MediaType** (5 rows): one row per MediaTypeId — GUESS
- **Playlist** (18 rows): one row per PlaylistId — GUESS
- **PlaylistTrack** (8,715 rows): one row per PlaylistId, TrackId — GUESS
- **Track** (3,503 rows): one row per TrackId — GUESS

## Columns worth a definition

- `Customer.Company` — codes: Woodstock Discos, Telus, Rogers Canada, Riotur, Microsoft Corporation — GUESS
- `Customer.Fax` — codes: +55 (61) 3363-7855, +55 (21) 2271-7070, +55 (12) 3923-5566, +55 (11) 3055-8131, +55 (11) 3033-4564 — GUESS
- `Customer.SupportRepId` — codes: 3, 4, 5 — GUESS
- `Employee.Title` — codes: Sales Support Agent, IT Staff, Sales Manager, IT Manager, General Manager — GUESS
- `Employee.ReportsTo` — codes: 2, 1, 6 — GUESS
- `Employee.HireDate` — codes: 2003-10-17 00:00:00, 2004-03-04 00:00:00, 2004-01-02 00:00:00, 2003-05-03 00:00:00, 2002-08-14 00:00:00 — GUESS
- `Employee.City` — codes: Calgary, Lethbridge, Edmonton — GUESS
- `Employee.State` — codes: AB — GUESS
- `Employee.Country` — codes: Canada — GUESS
- `Employee.Phone` — codes: +1 (403) 262-3443, 1 (780) 836-9987, +1 (780) 428-9482, +1 (403) 467-3351, +1 (403) 456-9986 — GUESS
- `Invoice.Total` — meaning/units to confirm — GUESS
- `InvoiceLine.UnitPrice` — codes: 0.99, 1.99; meaning/units to confirm — GUESS
- `InvoiceLine.Quantity` — codes: 1; meaning/units to confirm — GUESS
- `MediaType.MediaTypeId` — meaning/units to confirm — GUESS
- `Track.MediaTypeId` — codes: 1, 2, 3, 5, 4; meaning/units to confirm — GUESS
- `Track.UnitPrice` — codes: 0.99, 1.99; meaning/units to confirm — GUESS
