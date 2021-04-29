from enum import Enum


class Type(Enum):
    NIL = 0
    INT = 1
    REAL = -2
    SYM = -1
    PAIR = 2
    BUILTIN = 3
    CLOSURE = 4


class ErrorType(Enum):
    UNEXPECTED_TOKEN = "Unexpected Token"
    ID_INVALID_TOKEN = "invaild type"
    NO_INPUT_FILE = "No Input File"
    ERROR_OK = "No Error"
    ERROR_SYNTAX = "Syntax Error"


class Error(Exception):
    pass


def Err(token, type):
    raise Error("{0} : {1}".format(str(type), str(token)))


class Token(object):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return (
            self.__class__.__name__ + "(" + str(self.value) + ")" + "." + str(self.type)
        )

    def __repr__(self):
        return self.__str__()


class Input:
    def __init__(self):
        self.text = ""

    def _input(self):
        self.text = input(">> ")
        if self.text == "exit":
            exit()
        return self.text


class Keyword(Enum):
    LPAREN = 4
    RPAREN = 5
    DEFINE = 6
    LAMBDA = 7
    PLUS_OP = 8
    SUB_OP = 9
    DIV_OP = 10
    MUL_OP = 11
    DEF = 12
    EQ_OP = 13
    LESS_OP = 14


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

    def __repr__(self):
        return self.__str__()


class Nil:
    pass


class Symbol:
    def __init__(self, value, type):
        self.value = str(value.value)
        self.type = str(value.type)


class Pair:
    def __init__(self, root=None, LV=None, RV=None):
        self.root = root
        self.LV = LV
        self.RV = RV


def isNil(d):
    return d.type == Type.NIL


def nilp():
    return Data(Type.NIL)


def cons(d1, d2):
    return Data(Type.PAIR, [d1, d2])


def mkint(n):
    return Data(Type.INT, n)


def mksym(s):
    return Data(Type.SYM, s)


class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text if len(text) != 0 else Err(Type.NIL, ErrorType.NO_INPUT_FILE)
        self.currentToken = self.text[self.pos]

    def eat(self, tokenType):
        if self.currentToken == tokenType:
            return True
        return False

    def jmp(self):
        if self.pos == len(self.text) - 1:
            self.currentToken = None
            return False
        else:
            self.pos += 1
            self.currentToken = self.text[self.pos]
            return True

    def lex(self):
        lexR = []
        # print("===== === LEX === =====")
        while True:
            if self.pos == len(self.text) or self.currentToken == None:
                break

            if self.currentToken.isspace():
                try:
                    while self.currentToken.isspace():
                        self.jmp()
                except:
                    break

            elif self.currentToken == ".":
                self.jmp()

            elif self.currentToken == "(":
                if not self.eat("("):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("(", Keyword.LPAREN))
                self.jmp()
                if self.currentToken == ")":
                    lexR.append(Token(")", Keyword.RPAREN))
                    self.jmp()

            elif self.currentToken == ")":
                if not self.eat(")"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token(")", Keyword.RPAREN))
                self.jmp()

            elif self.currentToken.isalpha():
                id = ""
                while self.currentToken.isalpha() and self.currentToken is not None:
                    if self.currentToken.isalpha():
                        id += self.currentToken
                        if self.jmp():
                            pass
                        else:
                            break
                if id == "lambda":
                    lexR.append(Token("LAM", Keyword.LAMBDA))
                elif id == "define":
                    lexR.append(Token("DEF", Keyword.DEF))
                elif id == "Nil":
                    lexR.append(Token("NIL", Type.NIL))
                else:
                    lexR.append(Token(id, Type.SYM))

            elif self.currentToken.isdigit():
                num = ""
                realFlag = False
                while self.currentToken.isdigit() or self.currentToken == ".":
                    if self.currentToken == ".":
                        realFlag = True
                        num += self.currentToken
                        if self.jmp():
                            pass
                        else:
                            break
                    else:
                        num += self.currentToken
                        if self.jmp():
                            pass
                        else:
                            break
                if realFlag:
                    lexR.append(Token(num, Type.REAL))
                else:
                    lexR.append(Token(num, Type.INT))

            elif self.currentToken == "+":
                if not self.eat("+"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("+", Keyword.PLUS_OP))
                self.jmp()

            elif self.currentToken == "-":
                if not self.eat("-"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("-", Keyword.SUB_OP))
                self.jmp()

            elif self.currentToken == "*":
                if not self.eat("*"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("*", Keyword.MUL_OP))
                self.jmp()

            elif self.currentToken == "/":
                if not self.eat("/"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("/", Keyword.DIV_OP))
                self.jmp()

            elif self.currentToken == "=":
                if not self.eat("="):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("=", Keyword.EQ_OP))
                self.jmp()

            elif self.currentToken == "<":
                if not self.eat("<"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("<", Keyword.LESS_OP))
                self.jmp()

        # print(lexR)
        # print("===== === OUT === =====")
        return lexR


def iCons(d_list):
    if len(d_list) != 1:
        return cons(d_list[0], iCons(d_list[1:]))
    else:
        return cons(d_list[0], nilp())


def Parser(tokenlist):
    if len(tokenlist) == 0:
        return Err(Nil(), ErrorType.NO_INPUT_FILE)

    LA = tokenlist.pop(0)
    if LA.type == Keyword.LPAREN:
        if tokenlist[0].type == Keyword.RPAREN:
            return nilp()
        L = []
        while tokenlist[0].type != Keyword.RPAREN:
            L.append(Parser(tokenlist))
        tokenlist.pop(0)
        LR = iCons(L)
        return LR
    elif LA.type == Keyword.RPAREN:
        return Err(LA, ErrorType.UNEXPECTED_TOKEN)
    elif LA.value == "0":
        return Data(Type.INT, int(LA.value))
    else:
        try:
            if int(LA.value):
                return Data(Type.INT, int(LA.value))
        except:
            return Data(Type.SYM, LA.value)


class Bindings:
    def __init__(self, parent):
        self.parent = parent
        self.symbols = dict()
        # self.children_list = []
        # # 부모 -> 자식으로 가는경우

    def add_symbol(self, symbol, value):
        if symbol.type == Type.SYM:
            self.symbols[symbol.value.upper()] = value

    # def add_child(self, child):
    #     self.children_list.append(child)

    def __str__(self):
        if isNil(self.parent):
            return f"ENV class : root"
        else:
            return f"ENV class : {str(self.parent)}"

    def __repr__(self):
        return self.__str__()


def env_create(parent):
    new_bindings = Bindings(parent)
    # if not isNil(parent):
    #     parent.add_child(new_bindings)
    return new_bindings


def env_get(env, symbol):
    parent = env.parent

    if symbol.value.upper() in env.symbols:
        return env.symbols[symbol.value.upper()]

    if type(parent) is Bindings:
        pass
    elif isNil(parent):
        return "Error unbound", nilp()

    return env_get(parent, symbol)


def env_set(env, symbol, value):
    env.add_symbol(symbol, value)
    return ErrorType.ERROR_OK


def listp(expr):
    while not isNil(expr):
        if expr.type != Type.PAIR:
            return False
        expr = expr.cdr()
    return True


def eval_expr(expr, env):
    if expr.type == Type.SYM:
        return ErrorType.ERROR_OK, env_get(env, expr)
    elif expr.type != Type.PAIR:
        return ErrorType.ERROR_OK, expr

    if not listp(expr):
        return ErrorType.ERROR_SYNTAX, nilp()

    op = expr.car()
    args = expr.cdr()

    if op.type == Type.SYM:
        env_val = env_get(env, op)

        if op.value.upper() == "QUOTE":
            if isNil(args) or not isNil(args.cdr()):
                return "Error_Args", nilp()
            return "Error_OK", args.car()
        elif op.value.upper() == "DEF":
            if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
                return "Error_Args", nilp()
            sym = args.car()
            if sym.type != Type.SYM:
                return "Error_Type", nilp()
            err, val = eval_expr(args.cdr().car(), env)

            env_set(env, sym, val)
            return "Error_OK", sym
        elif op.value.upper() == "LAM":
            if isNil(args) or isNil(args.cdr()):
                return "Error_Type", nilp()
            return mk_closure(env, args.car(), args.cdr())
        elif op.value.upper() == "IF":
            if (
                isNil(args)
                or isNil(args.cdr())
                or isNil(args.cdr().cdr())
                or not isNil(args.cdr().cdr().cdr())
            ):
                return "Error_Args", nilp()
            err, result = eval_expr(args.car(), env)
            if isNil(result):
                val = args.cdr().cdr().car()
            else:
                val = args.cdr().car()

            return "Error_OK", eval_expr(val, env)
        # elif env_val and env_val.type == Type.BUILTIN:
        #     return apply(env_val, args)
    err, op = eval_expr(op, env)
    # if err:
    #     return err
    args = copy_list(args)
    p = args
    while not isNil(p):
        err, p.value[0] = eval_expr(p.car(), env)
        # if err:
        #     return err
        p = p.cdr()
    return apply(op, args)

    return "Error_Syntax", nilp()


def make_builtin(fn):
    a = Data()
    a.type = Type.BUILTIN
    a.value = fn
    return a


def copy_list(lst):
    if isNil(lst):
        return nilp()

    a = cons(lst.car(), nilp())
    p = a
    lst = lst.cdr()

    while not isNil(lst):
        p.value[1] = cons(lst.car(), nilp())
        p = p.cdr()
        lst = lst.cdr()

    return a


def apply(fn, args):
    if fn.type == Type.BUILTIN:
        return "Error OK", fn.value(args)
    elif fn.type != Type.CLOSURE:
        return "Error_Type", nilp()

    env = env_create(fn.car())
    params = fn.cdr().car()
    body = fn.cdr().cdr()

    while not isNil(params):
        if isNil(args):
            return "Error_Args", nilp()
        env_set(env, params.car(), args.car())
        params = params.cdr()
        args = args.cdr()

    if not isNil(args):
        return "Error_Args", nilp()

    while not isNil(body):
        result = eval_expr(body.car(), env)
        body = body.cdr()

    return "Error_OK", result


def mk_closure(env, params, body):
    if not listp(params) or not listp(body):
        return "Error_Type", nilp()

    p = params

    while not isNil(p):
        if p.car().type != Type.SYM:
            return "Error_Type", nilp()
        p = p.cdr()

    result = cons(env, cons(params, body))
    result.type = Type.CLOSURE

    return "Error_OK", result


def builtin_car(args):
    return "Error OK", args.car()
    # if isNil(args) or not isNil(args.cdr()):
    #     return "Error Args", nilp()
    #
    # if isNil(args.car()):
    #     return "Error OK", nilp()
    # elif args.car().type != Type.PAIR:
    #     return "Error Type", nilp()
    # else:
    #     return "Error OK", args.car().car()


def builtin_cdr(args):
    return "Error OK", args.cdr()
    # if isNil(args) or not isNil(args.cdr):
    #     return "Error Args", nilp()
    #
    # if isNil(args.car()):
    #     return "Error OK", nilp()
    # elif args.car().type != Type.PAIR:
    #     return "Error Type", nilp()
    # else:
    #     return "Error OK", args.car().cdr()


def builtin_cons(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    return "Error OK", cons(args.car(), args.cdr())


def builtin_plus(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        var = (args.car().value) + (args.cdr().car().value)
        return "Error OK", mkint(var)
    return "Error Args", nilp()


def builtin_minus(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        var = (args.car().value) - (args.cdr().car().value)
        return "Error OK", mkint(var)
    return "Error Args", nilp()


def builtin_multi(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        var = (args.car().value) * (args.cdr().car().value)
        return "Error OK", mkint(var)
    return "Error Args", nilp()


def builtin_divide(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        if args.cdr().car().value != 0:
            var = (args.car().value) / (args.cdr().car().value)
            return "Error OK", mkint(var)
        else:
            return "Divide Zero Error", nilp()
    return "Error Args", nilp()


def builtin_numeq(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        if args.car().value == args.cdr().car().value:
            return "Error OK", mksym("T")
        else:
            return "Error OK", nilp()
    return "Error Args", nilp()


def builtin_less(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        if args.car().value < args.cdr().car().value:
            return "Error OK", mksym("T")
        else:
            return "Error OK", nilp()
    return "Error Args", nilp()


if __name__ == "__main__":
    env = env_create(nilp())

    env_set(env, mksym("CAR"), make_builtin(builtin_car))
    env_set(env, mksym("CDR"), make_builtin(builtin_cdr))
    env_set(env, mksym("CONS"), make_builtin(builtin_cons))
    env_set(env, mksym("+"), make_builtin(builtin_plus))
    env_set(env, mksym("-"), make_builtin(builtin_minus))
    env_set(env, mksym("*"), make_builtin(builtin_multi))
    env_set(env, mksym("/"), make_builtin(builtin_divide))
    env_set(env, mksym("="), make_builtin(builtin_numeq))
    env_set(env, mksym("<"), make_builtin(builtin_less))
    env_set(env, mksym("T"), mksym("T"))
    env_set(env, mksym("nil"), nilp())

    while True:
        parsedlist = Parser(Lexer(Input()._input()).lex())
        # print("\n===== === PAR === =====")
        # print(parsedlist)
        # print("===== === OUT === =====")
        print(eval_expr(parsedlist, env))
