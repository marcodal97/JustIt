library(ggplot2)

library(scales)

myArgs <- commandArgs(trailingOnly = TRUE)

lista = strtoi(myArgs)

n <- length(lista)/3

result <- split(lista, 1:n)

ordini <- 1:length(result)

valutazioni <- vector()

for(x in result){

    media = mean(strtoi(x))

    valutazioni <- append(valutazioni, media)
}

data <- data.frame(ordini, valutazioni)

p = ggplot(data, aes(x=ordini, y=valutazioni)) + geom_line() + scale_x_continuous(breaks=breaks_pretty(length(ordini))) + ylim(1, 5)

file_name = "mediatemp.jpg"  

ggsave(p,file=file_name)


