SELECT 
    rs_local.rsid, local_structure.*
FROM
    (SELECT 
        rs_codon.rsid, codon_local.*
    FROM
        (SELECT 
        a.rsid, b.UID, b.Pos
    FROM
        HUMSAVAR.rs_chrom AS a
    INNER JOIN SNVBOX.CodonTable AS b ON a.chrom = b.chrom
        AND a.chromEnd = b.pos2) AS rs_codon
    INNER JOIN SNVBOX.CodonToLocalStructure AS codon_local ON rs_codon.UID = codon_local.UID
        AND rs_codon.Pos = codon_local.Pos) AS rs_local
        INNER JOIN
    SNVBOX.Local_Structure AS local_structure ON rs_local.LocalStructureId = local_structure.id
