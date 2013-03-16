        # -*- encoding: utf-8
__author__ = 'michael'

import time

class TimoutException(Exception):
    
    pass

class Retry(object):
    
    def __init__(self, tries, delay, backoff, expecting):
        '''
        tries: maximum times tring to execute the decorated function
        delay: the interval between to two consecutive tries
        backoff: extend the interval by the factor of backoff
        expecting: the expecting result of the original function  
        '''
        self.tries = tries
        self.delay = delay
        self.backoff = backoff
        self.expecting = expecting
        
    def __call__(self, func):
        
        def decorated_func(*args, **kwargs):
            
            while(self.tries > 0):
                
                self.tries -= 1
                
                result = func(*args, **kwargs)
                print "executing function %s(), result is" % func.__name__, result 
                
                if result == self.expecting:
                    return
                else:
                    print "sleep %d seconds before next call" % self.delay
                    time.sleep(self.delay)                   
                    self.delay *= self.backoff
            
            if self.tries == 0:
                raise TimoutException("Sir, I tried, but...")
            
        return decorated_func
            
                
            
    
if __name__ == '__main__':
    
    import random
    
    @Retry(5, 1, 2, expecting=True)
    def tester_func():
        
        if random.random() > 0.99:
            return True
        else:
            return False
    
    
    tester_func()
