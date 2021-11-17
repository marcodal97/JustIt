myArgs <- commandArgs(trailingOnly = TRUE)

#n <- length(myArgs)/3
#result <- split(myArgs, 1:n)

lista = strtoi(myArgs)
paste(mean(lista))

