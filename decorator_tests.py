

class CountCalls(object):
    """
    Decorator:  Count number of calls to function
    
    ## For doctests ##
    >>> f();f();f()
    >>> g();g();g();g();g()
    >>> f.count()
    3
    >>> g.count()
    5
     
    """
    _instances = {}
    
    def __init__(self, f):
        self._f = f
        self.__numcalls = 0
        CountCalls._instances[f] = self
    
    def __call__(self, *args, **kwargs):
        self.__numcalls += 1
        return self._f(*args, **kwargs)
    
    def count(self):
        return self.__numcalls
    
    @staticmethod
    def counts():
        return dict([(f.__name__ , inst.__numcalls ) for f, inst in CountCalls._instances.iteritems()])
    
    
@CountCalls
def f():
    return
    
@CountCalls
def g():
    return

if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose = True)
    print "\n\n", CountCalls.counts()