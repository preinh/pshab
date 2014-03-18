
f = open("_sources_clean.beta", 'r')
l = f.readline().strip()

while l:
    print l
    if not l.isdigit():
    
        nf = open(l+".eq.rates", "w")

        c = f.readline().strip()

        while c:
            #print c
            nf.write(c+"\n")
            c = f.readline().strip()
            
        nf.close()
    
    l = f.readline().strip()
f.close()
