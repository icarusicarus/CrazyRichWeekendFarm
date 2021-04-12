from enum import Enum

class Type(Enum):
    NIL = 0
    INT = 1
    PAIR = 2
    SYMBOL = 3

class Data:
    def __init__(self, type=Type.NIL, value=0):
        self.type = type
        self.value = value
    def car(self):
        return self.value[0]
    def cdr(self):
        return self.value[1]
    def __str__(self):
        if self.type == Type.NIL:
            return "NIL"
        elif self.type == Type.PAIR:
            try:
                if(self.cdr() == int(self.cdr())):
                    return "("+str(self.car())+" . "+str(self.cdr())+")"
            except:
                retStr = '('
                retStr+=str(self.car())
                atom = self.cdr()
                while(atom.type != Type.NIL):
                    if(atom.type == Type.PAIR):
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
    return Data(Type.PAIR, (d1, d2))

def mkint(n):
    return Data(Type.INT, n)

def mksym(s):
    return Data(Type.SYMBOL, s)

def nilp():
    return Data(Type.NIL)

if __name__ == "__main__":
    print("========YR TEST========")
    print(cons(1, 5))
    print(cons(1, 5).car())
    print(cons(1, 5).cdr())
    print(mkint(3))
    print(mksym('ABC'))
    print(nilp())
    print("========TESTING========")
    print(mkint(42))
    print(mksym("FOO"))
    print(cons(mksym("X"), mksym("Y")))
    print(cons(mkint(1), cons(mkint(2), cons(mkint(3), nilp()))))