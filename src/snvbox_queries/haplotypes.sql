SELECT *
FROM
	(SELECT rsid
	FROM (
		SELECT rsid, count(rsid) as total
		FROM HUMSAVAR.rs_chrom
		GROUP BY rsid
		) as t
	WHERE total > 1) as duplicates 
    INNER JOIN
    HUMSAVAR.rs_chrom 
    ON duplicates.rsid = HUMSAVAR.rs_chrom.rsid;
