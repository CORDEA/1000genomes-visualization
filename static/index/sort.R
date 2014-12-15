infile <- read.table("s100_chr", sep=",", header=F)
head(infile)
sort <- infile[order(-infile$V3),]
write.table(sort, file="sort_chr", sep=",", col.names=F, row.names=F, quote=F, append=F)
