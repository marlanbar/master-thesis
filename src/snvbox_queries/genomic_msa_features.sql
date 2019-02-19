SELECT 
	t.Humsavar_UID as UID, 
    t.Humsavar_Pos as Pos, 
    t.dbSNP, 
	Entropy, 
	Rel_Entropy, 
	PHC_A, 
	PHC_C, 
	PHC_D, 
	PHC_E, 
	PHC_F, 
	PHC_G, 
	PHC_H, 
	PHC_I, 
	PHC_K, 
	PHC_L, 
	PHC_M, 
	PHC_N, 
	PHC_P, 
	PHC_Q, 
	PHC_R, 
	PHC_S, 
	PHC_T, 
	PHC_V, 
	PHC_W, 
	PHC_Y, 
	PHC_sum, 
	PHC_squaresum
FROM (
	SELECT A.UID as Humsavar_UID, A.WildType, A.Pos as Humsavar_Pos, A.dbSNP, B.*
	FROM HUMSAVAR.humsavar_full as A INNER JOIN SNVBOX.Uniprot_Xref as B ON A.UID = B.Uniprot AND A.Pos = B.UniprotPos
    ) as t INNER JOIN SNVBOX.Genomic_MSA as r ON t.UID = r.UID AND t.Pos = r.Pos
