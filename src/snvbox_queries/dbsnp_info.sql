-- Join humsavar rsids with dbsnp info (e.g Chrom Start) and keep only one rsid per snp (delete haplotypes, for now).

CREATE TABLE HUMSAVAR.rs_chrom


SELECT dbsnp.rsid, snp150.chrom, snp150.chromStart, snp150.chromEnd, snp150.observed, snp150.class
FROM HUMSAVAR.dbsnp as dbsnp INNER JOIN HG19.snp150 as snp150 on dbsnp.rsid = snp150.name;
