import win32com.client
import win32com.client as win32

class excelSafe(object):
    def __init__(self, f):
        self._f = f

    def __call__(self, *args, **kwargs):
        try:
            return self._f(*args, **kwargs)
        except:
            self._f.excel.Quit()
            return None

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

class attributeAccess(object):
    def __init__(self,f):
        self._f = f
    def __call__(self, *args,**kwargs):
        self._f(*args, **kwargs)
        print self._f.test_word
        
class safeExcel(object):
    def __init__(self, f):
        self._f = f
    def __call__(self,*args,**kwargs):
        global excel
        global wb
        try:
            print self._f.__name__
            return self._f(*args,**kwargs)
    #    except com_error:
    #        print "com_error experienced"
    #        wb.Save()
    #        wb.Close()
    #        excel.Quit()
    #        del excel
    #        return
        except AttributeError:
            print "AttributeError experienced"
            wb.Save()
            wb.Close()
            excel.Quit()
            del excel
            return 'test'
        except TypeError:
            print "TYPE ERROR DAMMIT!"
            return None
        return 'test'

#def safeExcel(func):
#    global excel,wb
#    try:
#        print func.__name__
#        return func()
##    except com_error:
##        print "com_error experienced"
##        wb.Save()
##        wb.Close()
##        excel.Quit()
##        del excel
##        return
#    except AttributeError:
#        print "AttributeError experienced"
#        wb.Save()
#        wb.Close()
#        excel.Quit()
#        del excel
#        return 'test'
#    except TypeError:
#        print "TYPE ERROR DAMMIT!"
#        return None
#    return 'test'

@safeExcel
def excel_test():
    excel = win32.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    raise AttributeError
    wb = excel.Workbooks.Add()
    wb.SaveAs(Filename = "test.xlsx")
    wb.Close()
    excel.Quit()
    return "taco"


@attributeAccess
def h():
#    global test_word
    test_word = 'Can a decorator print this object?'
    return

if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose = True)
    print "\n\n", CountCalls.counts()