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
                if self.cdr() == int(self.cdr()):
                    return "(" + str(self.car()) + " . " + str(self.cdr()) + ")"
            except:
                retStr = "("
                retStr += str(self.car())
                atom = self.cdr()
                while atom.type != Type.NIL:
                    if atom.type == Type.PAIR:
                        retStr += " . "
                        retStr += str(atom.car())
                        atom = atom.cdr()
                    else:
                        retStr += " . "
                        retStr += str(atom)
                        break
                retStr += ")"
                return str(retStr)
        else:
            return str(self.value)
        # return "babo~ya"


def cons(d1, d2):
    return Data(Type.PAIR, (d1, d2))


def mkint(n):
    return Data(Type.INT, n)


def mksym(s):
    return Data(Type.SYMBOL, s)


def nilp():
    return Data(Type.NIL)


class T_Type(Enum):
    NIL = 0
    OP = 1
    CP = 2
    SYM = 3
    ID = 4
    INT = 5


class Token:
    def __init__(self, type=T_Type.NIL, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        if self.type == T_Type.SYM or self.type == T_Type.ID or self.type == T_Type.INT:
            return f"Token [{self.type}, Value: {self.value}]"
        else:
            return f"Token [{self.type}]"


def Lexer(lists):
    TokenList = []

    for i in range(len(lists)):
        LA = lists[i]
        if LA == "(":
            TokenList.append(Token(T_Type.OP))
        elif LA == ")":
            TokenList.append(Token(T_Type.CP))
        elif LA == "quote":
            TokenList.append(Token(T_Type.SYM, "QUOTE"))
        elif LA == "define":
            TokenList.append(Token(T_Type.SYM, "DEF"))
        elif LA == "lambda":
            TokenList.append(Token(T_Type.SYM, "LAM"))
        elif LA == "if":
            TokenList.append(Token(T_Type.SYM, "IF"))
        elif LA == "+":
            TokenList.append(Token(T_Type.SYM, "PLUS"))
        elif LA == "-":
            TokenList.append(Token(T_Type.SYM, "MINUS"))
        elif LA == ">":
            TokenList.append(Token(T_Type.SYM, "GT"))
        elif LA == "<":
            TokenList.append(Token(T_Type.SYM, "LT"))
        else:
            try:
                iL = int(LA)
                isinstance(iL, int)
                TokenList.append(Token(T_Type.INT, iL))
            except:
                TokenList.append(Token(T_Type.ID, LA))

    return TokenList


def iCons(d_list):
    if len(d_list) != 1:
        return cons(d_list[0], iCons(d_list[1:]))
    else:
        return cons(d_list[0], nilp())


def Parser(tokenlist):
    if len(tokenlist) == 0:
        return "[ERROR] Empty List"
    LA = tokenlist.pop(0)
    if LA.type == T_Type.OP:
        if tokenlist[0].type == T_Type.CP:
            return nilp()
        L = []
        while tokenlist[0].type != T_Type.CP:
            L.append(Parser(tokenlist))
        tokenlist.pop(0)
        LR = iCons(L)
        return LR
    elif LA.type == T_Type.CP:
        return "[ERROR] Unexpected ')'"
    else:
        try:
            if int(LA.value):
                return Data(Type.INT, int(LA.value))
        except:
            return Data(Type.SYMBOL, LA.value)


SymbolTable = {}


def SymbTable(lists):
    LA = lists
    if LA.type == Type.SYMBOL:  # get symbol
        if LA.value in SymbolTable:
            return SymbolTable.get(LA.value)
        else:
            return "Symbol not bound"
    elif LA.type == Type.INT:
        return str(LA.value)
    elif LA.type == Type.NIL:
        return str(LA)
    else:
        if LA.car().type == Type.SYMBOL:  # set symbol
            if LA.car().value == "QUOTE":
                SymbolTable[LA.cdr().car().value] = None
                return LA.cdr().car().value
            elif LA.car().value == "DEF":
                SymbolTable[LA.cdr().car().value] = LA.cdr().cdr().car().value
                return LA.cdr().car().value
            else:
                return "IDK :/"


if __name__ == "__main__":
    # env = env_init('Nil')
    # inputList = []

    line = input("If you want Quit, type ':q'\n>>> ")
    while line != ":q":
        if line:
            # inputList.append(line.replace('(', ' ( ').replace(')', ' ) ').split())
            # How can I handle one line code and multi line code at same time?
            line = line.replace("(", " ( ").replace(")", " ) ").split()

            r = Parser(Lexer(line))

            print(SymbTable(r))
        else:
            break
        line = input(">>> ")