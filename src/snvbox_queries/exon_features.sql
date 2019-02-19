SELECT 
    rs_exon.rsid, Cons, snp_den, hapmap_snp_den
FROM
    (SELECT 
        exon.UID,
            exon.Exon,
            rs.rsid,
            rs.chromEnd,
            exon.cStart,
            exon.cEnd
    FROM
        SNVBOX.Transcript_Exon AS exon
    INNER JOIN HUMSAVAR.rs_chrom AS rs ON exon.Chr = rs.chrom
    WHERE
        rs.chromEnd BETWEEN exon.cStart AND exon.cEnd AND rs.chromStart BETWEEN exon.cStart AND exon.cEnd) AS rs_exon
        
        INNER JOIN
    SNVBOX.Exon_Features AS exon_features USING (UID , Exon)
