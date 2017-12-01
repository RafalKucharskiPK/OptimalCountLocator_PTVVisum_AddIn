Na pewno nie JOIN - przeczytaj artykul i sprawdz na rekordach ktore posiadasz w bazie.
http://stackoverflow.com/questions/2726657/inner-join-vs-left-join-performance-in-sql-server

Ale musisz mocno potestowaæ wyniki, poniewa¿ w zaleznosci od struktury bazy moze sie zwykly JOIN okazac szybszy...
Zapytanie skonstruowalbym w ten sposob:

SELECT SUM(p.VOL), COUNT(p.ID_p) FROM 
Paths_Male p INNER JOIN (SELECT ID_P FROM NPI WHERE ID_N = ?) AS n
ON p.ID_P = n.ID_P 
WHERE p.przeciety=0

Czemu? Poniewaz na potrzeby zapytania wymagasz jedynie okreslonego zestawu danych z NPI (dla ID_N = [row[0]]), a co za tym idzie nie trzeba laczyc za kazdym razem z zestawem 30 000 000.
Sprawdzilem na bazie testowej, ktora nie stoi na jakiejs zajebistej maszynie, natomiast wybralem tabele pozycji pojazdow (ok. 100 000 000 rekordow) z tabela pojazdow (ok. 600).
Z prawie 4 min dla zapytania zblizonego do Twojego, zeszlo do 57 sek. Restartowalem baze po drodze zeby oproznic cache. A wlasnie - SQL Server zbuforuje tabele NPI i dla kolejnego 
zapytania czas sie skroci. Dodatkowo potrzebujesz indeksow CLUSTERED, przyklad tworzenia:

USE [TWOJA_BAZA]
GO

CREATE CLUSTERED INDEX [NAZWA_INDEKSU] ON [SCHEMA].[NPI] 
(
	[ID_N] ASC,
	[ID_P] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 100) ON [PRIMARY]
GO

NONCLUSTERED przyklad (tabela moze miec tylko jeden CLUSTERED ale jakbys gdzies chcial uzyc dodatkowego indeksu to wlasnie ten):

USE [TWOJA_BAZA]
GO

CREATE NONCLUSTERED INDEX [NAZWA_INDEKSU] ON [SCHEMA].[NPI] 
(
	[POLE_TABELI] ASC,
	[KOLEJNE_POLE_TABELI] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON, FILLFACTOR = 100) ON [PRIMARY]
GO

Powinienes od razu zobaczyc wzrost wydajnosci (nawet dla 30k rekordow).