library(ggplot2)
library(scales)

myArgs <- c(5,4,3,2,1,1,5,4,5,1,2,2,3,3,2)

n <- length(myArgs)/3
result <- split(myArgs, 1:n)

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
paste("ok")