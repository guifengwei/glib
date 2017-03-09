# This R script is to generate the TF or histone modification heatmap
# at certain genomic features (TSS, enhancers) from the ChIP-seq data
# the input matrix is got from Homer software. alternative to R, use cluster3 to cluster, and visualize by # java Treeviewer
# generate the matrix by Homer: annotatePeaks.pl peak_file.txt hg19 -size 6000 -hist 10  -ghist -d TF1/ # > outputfile_matrix.txt
# see several posts for heatmap:
# http://davetang.org/muse/2010/12/06/making-a-heatmap-with-r/
# http://www.r-bloggers.com/r-using-rcolorbrewer-to-colour-your-figures-in-r/
# 08/20/13 by Tommy Tang

# it is such a simple script but took me several days to get it work...I mean the desired
# color setting of the heatmap. Making a pretty figure takes time :)


# use either heatmap.2 from gplots or pheatmap

library(gplots)

library(pheatmap) 


# you can compare the heatmaps generated by heatmap.2 and pheatmap

#setwd("/home/tommy/homer")

d1 <- read.table("/usr/people/bioc1387/Project/Pwwp2a_Tianyi/Bam/out_tss_PWWP2Atargets", header=T)

# have a look at the matrix

head(d1)
d1$Gene                               # the dataframe generated by homer has a column named Gene
m1<- as.matrix( d1[,2:ncol(d1)])   # the first column is the TSS id,
rownames(m1)<- d1$Gene            # heatmap.2 works only on matrix, turn the dataframe to matrix, and                                                        # add the TSS id as the row name
m1<- log2(m1+1)                          # log2 transform the raw counts


#exam the data range
range(m1)

hist(m1)    # histogram to look at distributions


# it is from the ChIP-seq count data, many of them are 0s. I transfromed the raw data
# by log2(m+1), so if the log2 value is 0, the raw number is also 0 (count)
# to compare different heatmaps, I have to map the value to the color using the
# break argument in pheatmap or heatmap.2 That's why I examed the data range.
# http://stackoverflow.com/questions/17820143/how-to-change-heatmap-2-color-range-in-r
# https://stat.ethz.ch/pipermail/bioconductor/2011-November/041866.html
# http://seqanswers.com/forums/showthread.php?p=114275&posted=1#post114275

bk = unique(c(seq(-0.1,3, length=100),seq(3,9.7,length=100)))

hmcols<- colorRampPalette(c("white","red"))(length(bk)-1)   


# you can play around with the break points, 9.7 is the max of the matrix m1
# if just use bk =  c(seq(-0.1,1, length=100),seq(1,12.5,length=100)) without the unique function
# the pheatmap gave me error message:
# Error in cut.default(x, breaks = breaks, include.lowest = T) : 
# 'breaks' are not unique
# It is caused by concatenating several seq() results together, which share the same boundaries.
# try ?dist ?hclust


png("test.png", width=300, height = 800)     # width and height are in pixel 

heatmap.2(m1, col=hmcols, breaks = bk, Rowv= TRUE , Colv=FALSE, dendrogram="row", useRaster = TRUE, symkey=FALSE, symm=F, symbreaks=T, scale="none", trace="none", labRow=NA, labCol=NA)


# do not show the row and column labels 
# trace argument should be put to "none", otherwise the trace is cyan and it will "eat" the heatmap
# I asked in Biostar http://www.biostars.org/p/79444/#79457
# look at the documentation for #heatmap.2 http://hosho.ees.hokudai.ac.jp/~kubo/Rdoc/library/gplots/html/heatmap.2.html

# or you can use pheatmap

pheatmap(m1, color=hmcols,  breaks= bk,  cluster_rows=TRUE, cluster_cols=FALSE, legend=FALSE, show_rownames=FALSE, show_colnames=FALSE)

dev.off()
