mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A < $1 | tr "	" "," > $2 
