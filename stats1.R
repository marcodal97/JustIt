myArgs <- commandArgs(trailingOnly = TRUE)

n <- length(myArgs)/3
result <- split(myArgs, 1:n)

count1 <- 0
count2 <- 0
count3 <- 0
count4 <- 0
count5 <- 0

for(x in result){
    if(x[[1]] == 1){
        count1 = count1 + 1
        next
    }        
    if(x[[1]] == 2){
        count2 = count2 + 1
        next
    }
    if(x[[1]] == 3){
        count3 = count3 + 1
        next
    }
    if(x[[1]] == 4){
        count4 = count4 + 1
        next
    }
    if(x[[1]] == 5){
        count5 = count5 + 1
        next
    }
}

vet <- c(count1,count2,count3,count4,count5)

lbls<-paste(c("1 stella:", "2 stelle:", "3 stelle:", "4 stelle:", "5 stelle:"), vet)
jpeg("stats1.jpg")
pie(vet, main="Qualita' Cibo", labels=lbls)
dev.off()
paste("ok")