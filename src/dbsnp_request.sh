mysql --user=genome --host=genome-mysql.cse.ucsc.edu --execute="select bin, chrom, chromStart, chromEnd, name from hg19.snp150CodingDbSnp" | tr "	" "," 

