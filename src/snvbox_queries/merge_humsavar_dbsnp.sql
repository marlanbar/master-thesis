--this line dump some interesting columns on dbsnp database restricted to humsavar database
SELECT dbsnp.chrom,dbsnp.chromStart,dbsnp.chromEnd,dbsnp.name,dbsnp.strand,dbsnp.observed,dbsnp.func FROM HG19.snp150 as dbsnp RIGHT JOIN HUMSAVAR.humsavar_full AS hsv 
                 ON (dbsnp.name = hsv.dbSNP) INTO OUTFILE '/var/lib/mysql-files/dbsnp150_humsavar.tsv' FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';

