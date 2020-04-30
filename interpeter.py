import Aparser as prs
import lexer
import node
import copy
import functools
import errorClass as er

def add_command(x, y):
    return x + y

def mul_command(x,y):
    return x * y

def min_command(x,y):
    return x - y

def gTCompare(x, y):
    return int(x > y)

def div_command(x, y):
    return int(x / y) # Cast to int to prevent floats

def mod_command(x,y):
    return x % y

class programstate:

    def __init__(self, variables=None, methods=None, error=None, stepCount=0):
        self.variables = variables if variables else dict()
        self.methods = methods if methods else dict()
        self.errors = error if error else list()
        self.stepCount = stepCount

    def __str__(self):
        return "variable: {}, methods: {}, stepCount: {}".format(self.variables, self.methods, self.stepCount)

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict={}):
        return programstate(self.variables, self.methods,self.errors, self.stepCount)

operatorDict = {
    '-': min_command,
    '+': add_command,
    '>': gTCompare,
    '*': mul_command,
    '/': div_command,
    '%': mod_command
}

def executeStep(curNode, progState):
    progStateCopy = copy.deepcopy(progState)
    if curNode.right is None and curNode.left is None:
        return progStateCopy
    if curNode.data == 'while':
        lhs = curNode.left if curNode.left not in progStateCopy.variables else progStateCopy.variables[curNode.left]
        rhs = curNode.right
        if int(lhs) is 1:
            progStateCopy = functools.reduce(lambda x, y: executeStep(y, x), rhs, progStateCopy)
            return executeStep(curNode, progStateCopy)
        else:
            return progStateCopy
    lhs = curNode.left if curNode.left not in progStateCopy.variables else progStateCopy.variables[curNode.left]
    rhs = curNode.right if curNode.right not in progStateCopy.variables else progStateCopy.variables[curNode.right]
    if curNode.data in operatorDict:
        if type(rhs) == node.Node and type (lhs) == node.Node:
            return operatorDict[curNode.data](executeStep(lhs,progStateCopy), executeStep(rhs, progStateCopy))
        elif type(rhs) == node.Node:
            return operatorDict[curNode.data](int(lhs), executeStep(rhs, progStateCopy))
        elif type(lhs) == node.Node:
            return operatorDict[curNode.data](executeStep(lhs, progStateCopy), int(rhs))
        return operatorDict[curNode.data](int(lhs), int(rhs))
    if curNode.data == '=':
        if type(rhs) == node.Node:
            progStateCopy.variables[curNode.left] = executeStep(rhs, progStateCopy)
            return progStateCopy
        if rhs is not None:
            progStateCopy.variables[curNode.left] = rhs
            return progStateCopy
    if curNode.data == 'PRINT':
        print(lhs)  # JASPER FOR THE LOVE OF GOD DEZE PRINT NIET VERWIJDEREN!!!!!!!!!
        return progStateCopy

def run(filename):
    output = lexer.lex(filename)
    print(output)
    if len(output[1]) > 0:
            print(output[1])
    else:
        pList = prs.parse(output[0])
        print(pList)
        if len(pList[1]) > 0:
            print(pList[1])
        else:
            progstate = programstate()
            print(pList[0])
            for p in pList[0]:
                print(progstate)
                if len(progstate.errors) > 0:
                    print(progstate)
                else:
                    progstate = executeStep(p, progstate)
