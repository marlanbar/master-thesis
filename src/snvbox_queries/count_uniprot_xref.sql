SELECT Uniprot, UniprotPos, total
FROM (
	SELECT Uniprot, UniprotPos, count(*) as total
	FROM SNVBOX.Uniprot_Xref
	GROUP BY Uniprot, UniprotPos
) as t
WHERE total > 1
