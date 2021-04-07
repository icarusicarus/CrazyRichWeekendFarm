# Data Type
#   1: int
#   2: pair(in python, Tuple)
#   3: nil(in python, None)
#   4: symbol

Types = ['Int', 'Pair', 'Nil', 'Symbol']

class Data:
    def __init__(self, type=0, value=0):
        self.type = type
        self.value = value
    def car(self):
        return self.value[0]
    def cdr(self):
        return self.value[1]
    def __str__(self):
        if self.type == 2:
            try:
                if(self.cdr() == int(self.cdr())):
                    return "("+str(self.car())+" . "+str(self.cdr())+")"
            except:
                retStr = '('
                retStr+=str(self.car())
                atom = self.cdr()
                while(str(atom) != 'None'):
                    if(atom.type == 2):
                        retStr+=' . '
                        retStr+=str(atom.car())
                        atom = atom.cdr()
                    else:
                        retStr+=' . '
                        retStr+=str(atom)
                        break
                retStr+=')'
                return str(retStr)

        else:
            return str(self.value)
        #return "babo~ya"

def cons(d1, d2):
    return Data(2, (d1, d2))

def mkint(n):
    return Data(1, n)

def mksym(s):
    return Data(4, s)

def nil():
    return Data(3, None)

if __name__ == "__main__":
    print("========YR TEST========")
    print(cons(1, 5))
    print(cons(1, 5).car())
    print(cons(1, 5).cdr())
    print(mkint(3))
    print(mksym('ABC'))
    print(nil())
    print("========TESTING========")
    print(mkint(42))
    print(mksym("FOO"))
    print(cons(mksym("X"), mksym("Y")))
    print(cons(mkint(1), cons(mkint(2), cons(mkint(3), nil()))))