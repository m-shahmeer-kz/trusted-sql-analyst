# Database map: chinook.db

Dialect: **sqlite** · 11 tables/views · profiled 2026-11-21T14:29:16 by sqlanalyst 1.1.0.
Every number below was measured with a query. Use it to choose tables, joins and filters.

## Album — 347 rows · key: AlbumId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| AlbumId | INTEGER | 0 | 347 | 1 … 347 |  |
| Title | NVARCHAR(160) | 0 | 347 | [1997] Black Light Syndrome (1), Zooropa (1), Worlds (1), Weill: The Seven Deadly Sins (1) |  |
| ArtistId | INTEGER | 0 | 204 | 1 … 275 |  |

## Artist — 275 rows · key: ArtistId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| ArtistId | INTEGER | 0 | 275 | 1 … 275 |  |
| Name | NVARCHAR(120) | 0 | 275 | Zeca Pagodinho (1), Youssou N'Dour (1), Yo-Yo Ma (1), Yehudi Menuhin (1) |  |

## Customer — 59 rows · key: CustomerId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| CustomerId | INTEGER | 0 | 59 | 1 … 59 |  |
| FirstName | NVARCHAR(40) | 0 | 57 | Mark (2), Frank (2), Wyatt (1), Victor (1) |  |
| LastName | NVARCHAR(20) | 0 | 59 | Zimmermann (1), Wójcik (1), Wichterlová (1), Van der Berg (1) |  |
| Company | NVARCHAR(80) | 49 (83%) | 10 | Woodstock Discos (1), Telus (1), Rogers Canada (1), Riotur (1) |  |
| Address | NVARCHAR(70) | 0 | 59 | Via Degli Scipioni, 43 (1), Ullevålsveien 14 (1), Theodor-Heuss-Straße 34 (1), Tauentzienstraße 8 (1) |  |
| City | NVARCHAR(40) | 0 | 53 | São Paulo (2), Prague (2), Paris (2), Mountain View (2) | 1 values with extra spaces |
| State | NVARCHAR(40) | 29 (49%) | 25 | SP (3), CA (3), ON (2), WI (1) |  |
| Country | NVARCHAR(40) | 0 | 24 | USA (13), Canada (8), France (5), Brazil (5) |  |
| PostalCode | NVARCHAR(10) | 4 (7%) | 55 | X1A 1N6 (1), V6C 1G8 (1), T6G 2C7 (1), SW1V 3EN (1) |  |
| Phone | NVARCHAR(24) | 1 (2%) | 58 | +91 080 22289999 (1), +91 0124 39883988 (1), +61 (02) 9332 3633 (1), +56 (0)2 635 4444 (1) |  |
| Fax | NVARCHAR(24) | 47 (80%) | 12 | +55 (61) 3363-7855 (1), +55 (21) 2271-7070 (1), +55 (12) 3923-5566 (1), +55 (11) 3055-8131 (1) |  |
| Email | NVARCHAR(60) | 0 | 59 | wyatt.girard@yahoo.fr (1), vstevens@yahoo.com (1), tgoyer@apple.com (1), terhi.hamalainen@apple.fi (1) |  |
| SupportRepId | INTEGER | 0 | 3 | 3 … 5 |  |

## Employee — 8 rows · key: EmployeeId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| EmployeeId | INTEGER | 0 | 8 | 1 … 8 |  |
| LastName | NVARCHAR(20) | 0 | 8 | Peacock (1), Park (1), Mitchell (1), King (1) |  |
| FirstName | NVARCHAR(20) | 0 | 8 | Steve (1), Robert (1), Nancy (1), Michael (1) |  |
| Title | NVARCHAR(30) | 0 | 5 | Sales Support Agent (3), IT Staff (2), Sales Manager (1), IT Manager (1) |  |
| ReportsTo | INTEGER | 1 (12%) | 3 | 1 … 6 |  |
| BirthDate | DATETIME | 0 | 8 | 1947-09-19 00:00:00 … 1973-08-29 00:00:00 | date stored as ISO text; stored with a ' 00:00:00' suffix: `= 'YYYY-MM-DD'` matches nothing, use ranges |
| HireDate | DATETIME | 0 | 7 | 2002-04-01 00:00:00 … 2004-03-04 00:00:00 | date stored as ISO text; stored with a ' 00:00:00' suffix: `= 'YYYY-MM-DD'` matches nothing, use ranges |
| Address | NVARCHAR(70) | 0 | 8 | 923 7 ST NW (1), 825 8 Ave SW (1), 7727B 41 Ave (1), 683 10 Street SW (1) |  |
| City | NVARCHAR(40) | 0 | 3 | Calgary (5), Lethbridge (2), Edmonton (1) |  |
| State | NVARCHAR(40) | 0 | 1 | AB (8) |  |
| Country | NVARCHAR(40) | 0 | 1 | Canada (8) |  |
| PostalCode | NVARCHAR(10) | 0 | 8 | T5K 2N1 (1), T3B 1Y7 (1), T3B 0C5 (1), T2P 5M5 (1) |  |
| Phone | NVARCHAR(24) | 0 | 7 | +1 (403) 262-3443 (2), 1 (780) 836-9987 (1), +1 (780) 428-9482 (1), +1 (403) 467-3351 (1) |  |
| Fax | NVARCHAR(24) | 0 | 8 | 1 (780) 836-9543 (1), +1 (780) 428-3457 (1), +1 (403) 467-8772 (1), +1 (403) 456-8485 (1) |  |
| Email | NVARCHAR(60) | 0 | 8 | steve@chinookcorp.com (1), robert@chinookcorp.com (1), nancy@chinookcorp.com (1), michael@chinookcorp.com (1) |  |

## Genre — 25 rows · key: GenreId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| GenreId | INTEGER | 0 | 25 | 1 … 25 |  |
| Name | NVARCHAR(120) | 0 | 25 | World (1), TV Shows (1), Soundtrack (1), Science Fiction (1) |  |

## Invoice — 412 rows · key: InvoiceId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| InvoiceId | INTEGER | 0 | 412 | 1 … 412 |  |
| CustomerId | INTEGER | 0 | 59 | 1 … 59 |  |
| InvoiceDate | DATETIME | 0 | 354 | 2009-01-01 00:00:00 … 2013-12-22 00:00:00 | date stored as ISO text; stored with a ' 00:00:00' suffix: `= 'YYYY-MM-DD'` matches nothing, use ranges |
| BillingAddress | NVARCHAR(70) | 0 | 59 | Via Degli Scipioni, 43 (7), Ullevålsveien 14 (7), Theodor-Heuss-Straße 34 (7), Tauentzienstraße 8 (7) |  |
| BillingCity | NVARCHAR(40) | 0 | 53 | São Paulo (14), Prague (14), Paris (14), Mountain View (14) | 7 values with extra spaces |
| BillingState | NVARCHAR(40) | 202 (49%) | 25 | SP (21), CA (21), ON (14), WI (7) |  |
| BillingCountry | NVARCHAR(40) | 0 | 24 | USA (91), Canada (56), France (35), Brazil (35) |  |
| BillingPostalCode | NVARCHAR(10) | 28 (7%) | 55 | X1A 1N6 (7), V6C 1G8 (7), T6G 2C7 (7), SW1V 3EN (7) |  |
| Total | NUMERIC(10,2) | 0 | 23 | 0.99 … 25.86 |  |

## InvoiceLine — 2,240 rows · key: InvoiceLineId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| InvoiceLineId | INTEGER | 0 | 2,240 | 1 … 2240 |  |
| InvoiceId | INTEGER | 0 | 412 | 1 … 412 |  |
| TrackId | INTEGER | 0 | 1,984 | 1 … 3500 |  |
| UnitPrice | NUMERIC(10,2) | 0 | 2 | 0.99 … 1.99 |  |
| Quantity | INTEGER | 0 | 1 | 1 … 1 |  |

## MediaType — 5 rows · key: MediaTypeId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| MediaTypeId | INTEGER | 0 | 5 | 1 … 5 |  |
| Name | NVARCHAR(120) | 0 | 5 | Purchased AAC audio file (1), Protected MPEG-4 video file (1), Protected AAC audio file (1), MPEG audio file (1) |  |

## Playlist — 18 rows · key: PlaylistId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| PlaylistId | INTEGER | 0 | 18 | 1 … 18 |  |
| Name | NVARCHAR(120) | 0 | 14 | TV Shows (2), Music (2), Movies (2), Audiobooks (2) |  |

## PlaylistTrack — 8,715 rows · key: PlaylistId, TrackId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| PlaylistId | INTEGER | 0 | 14 | 1 … 18 |  |
| TrackId | INTEGER | 0 | 3,503 | 1 … 3503 |  |

## Track — 3,503 rows · key: TrackId

| column | type | nulls | distinct | values / range | notes |
|---|---|---|---|---|---|
| TrackId | INTEGER | 0 | 3,503 | 1 … 3503 |  |
| Name | NVARCHAR(200) | 0 | 3,257 | Wrathchild (5), The Trooper (5), The Number Of The Beast (5), Iron Maiden (5) |  |
| AlbumId | INTEGER | 0 | 347 | 1 … 347 |  |
| MediaTypeId | INTEGER | 0 | 5 | 1 … 5 |  |
| GenreId | INTEGER | 0 | 25 | 1 … 25 |  |
| Composer | NVARCHAR(220) | 978 (28%) | 852 | Steve Harris (80), U2 (44), Jagger/Richards (35), Billy Corgan (31) |  |
| Milliseconds | INTEGER | 0 | 3,080 | 1071 … 5286953 |  |
| Bytes | INTEGER | 0 | 3,501 | 38747 … 1059546140 |  |
| UnitPrice | NUMERIC(10,2) | 0 | 2 | 0.99 … 1.99 |  |

## Joins (measured)

| from | to | how found | rows matched | orphans | NULL keys | note |
|---|---|---|---|---|---|---|
| Album.ArtistId | Artist.ArtistId | declared | 347 of 347 | 0 | 0 |  |
| Customer.SupportRepId | Employee.EmployeeId | declared | 59 of 59 | 0 | 0 |  |
| Employee.ReportsTo | Employee.EmployeeId | declared | 7 of 7 | 0 | 1 | INNER JOIN drops NULL keys |
| Invoice.CustomerId | Customer.CustomerId | declared | 412 of 412 | 0 | 0 |  |
| InvoiceLine.TrackId | Track.TrackId | declared | 2,240 of 2,240 | 0 | 0 |  |
| InvoiceLine.InvoiceId | Invoice.InvoiceId | declared | 2,240 of 2,240 | 0 | 0 |  |
| PlaylistTrack.TrackId | Track.TrackId | declared | 8,715 of 8,715 | 0 | 0 |  |
| PlaylistTrack.PlaylistId | Playlist.PlaylistId | declared | 8,715 of 8,715 | 0 | 0 |  |
| Track.MediaTypeId | MediaType.MediaTypeId | declared | 3,503 of 3,503 | 0 | 0 |  |
| Track.GenreId | Genre.GenreId | declared | 3,503 of 3,503 | 0 | 0 |  |
| Track.AlbumId | Album.AlbumId | declared | 3,503 of 3,503 | 0 | 0 |  |
