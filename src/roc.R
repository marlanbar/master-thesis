#!/usr/bin/env Rscript
suppressPackageStartupMessages(library("optparse"))
suppressPackageStartupMessages(library("pROC"))


option_list <- list( 

    make_option(c("-v", "--verbose"), action="store_true", default=TRUE,
        help="Print extra output [default]"),

    make_option(c("-i", "--ifile"), type="character", default='test', 
        help="input file"),
    
    make_option(c("-o","--ofolder"),type = 'character',default='./outputs/'),

    make_option(c("-r","--score1_column"),type = 'character',default='score1'),

    make_option(c("-q","--score2_column"),type = 'character',default='-'),

    make_option(c("-l","--label_column"),type = 'character',default='y_test'),

    make_option(c("-s","--sep"),type = 'character',default=',')


    )

# get command line options
opt <- parse_args(OptionParser(option_list=option_list))

name_score1 = opt$score1_column
name_score2 = opt$score2_column
print(name_score2)
label = opt$label_column
sep = opt$sep

if (opt$score2_column =='-'){
    mode = '1curve'
}else{
    mode <- '2curves'
}

## get output filenames
odir = opt$ofolder
fbase = basename(opt$ifile)



# create output dir
dir.create(odir)

data = read.csv(opt$ifile,sep=sep)
y_true =  factor(data[,label])
score1 = data[,name_score1]


if(mode == '1curve'){
    print('entro en modo una curva')
    out_rdata = paste(odir,fbase,'_ROC_CI','.Rdata',sep = '')  # rdata object containing ROC curves objects
    out_plot = paste(odir,fbase,'_ROC_CI.png',sep = '')  # rdata object containing ROC curves objects
    report_file = paste(odir,fbase,'_report.csv',sep = '')
    #print('fin paste')

    ##### ROC curves and make plot #### 
    png(out_plot, res = 300, width = 10, height = 10, units = 'in')               
    rocobj <- plot.roc(y_true, score1,
                    main = "ROC Curve", 
                    percent=F,
                    ci = TRUE,                  # compute AUC (of AUC by default)
                    print.auc = TRUE)          # print the AUC (will contain the CI)

    #print('fin rocobj')
    # confidence interval at selected specificities (by boostraping)
    # ciobj <- ci.se(rocobj,  specificities = seq(0, 1, 0.3))  # CI of sensitivity over a select set of specificities
    # plot(ciobj, type = "shape", col = "#1c61b6AA")     # plot as a blue shape

    # print('fin ciobj')

    optim_thr = coords(rocobj,"b", best.method="closest.topleft",ret=c("threshold", "specificity", "sensitivity", "accuracy","tn", "tp", "fn", "fp", "npv", "ppv", "1-specificity","1-sensitivity", "1-accuracy", "1-npv", "1-ppv","precision", "recall"))

    thr_05 = coords(rocobj,0.5, best.method="closest.topleft",ret=c("threshold", "specificity", "sensitivity", "accuracy","tn", "tp", "fn", "fp", "npv", "ppv", "1-specificity","1-sensitivity", "1-accuracy", "1-npv", "1-ppv","precision", "recall"))
    metrics <-cbind(thr_05,optim_thr)
    print('escribiendo tabla')
    write.table(metrics,report_file,sep = ',')

    thr_plot = paste(odir,fbase,'_ThrPlot.png',sep = '')  # rdata object containing ROC curves objects
    print('plotting thr')
    png(thr_plot, res = 300, width = 5, height = 5, units = 'in')               
    plot(specificity + sensitivity ~ threshold, t(coords(rocobj, seq(0, 1, 0.01))), type = "l")




    #save Rdata
    save(rocobj,file = out_rdata)
}else{
    print('emtro en modo dos curvas')
    out_rdata = paste(odir,fbase,'_ROC-comparison','.Rdata',sep = '')  # rdata object containing ROC curves objects
    out_plot = paste(odir,fbase,'_',name_score1,'_',name_score2,'_ROC-comparison.png',sep = '')      
    png(out_plot, res = 300, width = 5, height = 5, units = 'in')               


    score2 = data[,name_score2]
    rocobj1 <- plot.roc(y_true, score1,
                        main="Statistical comparison",
                        percent=F,
                        col="#1c61b6")
    rocobj2 <- lines.roc(y_true, score2, 
                        percent=F, 
                        col="#008600")
    testobj <- roc.test(rocobj1, rocobj2)
    text(0.5, 0.5, labels=paste("p-value =", format.pval(testobj$p.value)), adj=c(0, .5))
    legend("bottomright", legend=c("S100B", "NDKA"), col=c("#1c61b6", "#008600"), lwd=2)

}


#plot(ci(rocobj, of = "thresholds", thresholds = "best"))
