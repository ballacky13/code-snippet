# -*- encoding: utf-8
__author__ = 'michael'

import time

class TimoutException(Exception):
    
    pass

def retry(tries=5, delay=1, backoff=2, expecting=True):
    '''
    tries: maximum times tring to execute the decorated function
    delay: the interval between to two consecutive tries
    backoff: extend the interval by the factor of backoff when not expecting result happens
    expecting: the expecting result of the original function  
    '''
    
    def wrapped_func(func):
        
        def decorated_func(*args, **kwargs):
            count = tries
            interval = delay
            
            while(count > 0):
                count -= 1
                result = func(*args, **kwargs)
                print "executing function %s(), result is" % func.__name__, result 
                
                if result == expecting:
                    return
                else:
                    print "sleep %d seconds before next call" % interval
                    time.sleep(interval)                   
                    interval *= backoff
            
            if count == 0:
                raise TimoutException("Sir, I tried, but...")
            
        return decorated_func
            
    return wrapped_func
            
                
            
    
if __name__ == '__main__':
    
    import random
    
    @retry(tries=5, delay=1, backoff=2, expecting=True)
    def tester_func():
        
        if random.random() > 0.8:
            return True
        else:
            return False
    
    
    tester_func()
