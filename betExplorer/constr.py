class Igor():

    def __init__(self):
        self.x = 1
        self.y = 2

    def teste(self,*args):
        at =  self.__dict__
        print (at)
        for k in args:
            print(k)

    def __repr__(self):
        return str(a)

i = Igor()
i.teste('x','y')