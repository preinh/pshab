from multiprocessing import Pool
import numpy as np
 
def unwrap_action(*arg, **kwarg):
    #print "unrwap", arg, kwarg
    return arg[0].action(*arg[1:], **kwarg)

class A(object):
    def __init__(self):
        self.a = 1
        self.b = 10
        self.h = np.arange(1,10e3,1)
        #global h
        #pass
    
    
    def cb(self, r):
        print "ballback:", r 
        self.h[r[0]] = r[1] 
        
        
    def action(self, i, h, *kargs):
#        print self, i, kargs
        #print i, self.h[i]
        return i, i*i
        #print "action:", i*i
    
    
    def run(self):
        po = Pool()
        print self.h
        t = self.h.copy()
        for k,v in enumerate(t):
            po.apply_async(unwrap_action, (self, k, self.h), callback=self.cb)
            #print "segue a fila ", k, v
            #print self.h
        po.close()
        po.join()
        print self.h



        
if "__main__" == __name__:
    a = A()
    a.run()
    print a.h
