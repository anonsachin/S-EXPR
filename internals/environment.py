from .Exceptions import IntpretorException

class Environment:

    def __init__(self, map= {}, parent= None) -> None:
        self.map = map
        self.parent = parent

    def lookup(self, key):
        if key in self.map:
            return self.map[key]
        elif self.parent is not None:
            return self.parent.lookup(key)
        else:
            raise IntpretorException("Undefined variable!!")
        
    def assign(self, key, value):
        if key in self.map:
            self.map[key] = value
            return value
        elif self.parent is not None:
            return self.parent.assign(key, value)
        else:
            raise IntpretorException("Undefined variable!!")
    
    def detect(self, key):
        if key in self.map:
            return True
        elif self.parent is not None:
            return self.parent.detect(key)
        else:
            return False
        
    def set(self, key, value):
        self.map[key] = value
