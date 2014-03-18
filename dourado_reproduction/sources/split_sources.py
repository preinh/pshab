

f = open("_all_polygon.src", 'r')
l = f.readline().strip()

while l:
    print l
    if not l.isdigit():
    
        nf = open(l+".eq.src", "w")
        _ = f.readline().strip()

        c = f.readline().strip()

        while c:
            #print c
            nf.write(c+"\n")
            c = f.readline().strip()
            
        nf.close()
    
    l = f.readline().strip()
f.close()
