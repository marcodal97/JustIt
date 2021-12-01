myArgs <- commandArgs(trailingOnly = TRUE)

n <- length(myArgs)/3
result <- split(myArgs, 1:n)

count1 <- 0
count2 <- 0
count3 <- 0
count4 <- 0
count5 <- 0

for(x in result){
    if(x[[3]] == 1){
        count1 = count1 + 1
        next
    }        
    if(x[[3]] == 2){
        count2 = count2 + 1
        next
    }
    if(x[[3]] == 3){
        count3 = count3 + 1
        next
    }
    if(x[[3]] == 4){
        count4 = count4 + 1
        next
    }
    if(x[[3]] == 5){
        count5 = count5 + 1
        next
    }
}

vet <- c(count1,count2,count3,count4,count5)

lbls<-paste(c("1 stella:", "2 stelle:", "3 stelle:", "4 stelle:", "5 stelle:"), vet)
jpeg("stats3.jpg")
pie(vet, main="Tempo di consegna", labels=lbls)
dev.off()
paste("ok")