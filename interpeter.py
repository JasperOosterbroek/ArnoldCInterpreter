import Aparser as prs
import lexer
import node
import copy
import functools

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

    def __init__(self, variables=None, methods=None, stepCount=0):
        self.variables = variables if variables else dict()
        self.methods = methods if methods else dict()
        self.stepCount = stepCount

    def __str__(self):
        return "variable: {}, methods: {}, stepCount: {}".format(self.variables, self.methods, self.stepCount)

    def __repr__(self):
        return str(self)
    def __deepcopy__(self, memodict={}):
        return programstate(self.variables, self.methods, self.stepCount)

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
    # operatord misschien in dict gooien met een functie eraanvast
    # dan if in dict, en dan dict val opzoeken en die functie pakken, kan de code veel kleiner maken
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
            test = executeStep(rhs, progStateCopy)
            progStateCopy.variables[curNode.left] = test
            return progStateCopy
        if rhs is not None:
            progStateCopy.variables[curNode.left] = rhs
            return progStateCopy
        else:
            return progStateCopy
    if curNode.data == 'PRINT':
        print(lhs)  # JASPER FOR THE LOVE OF GOD DEZE PRINT NIET VERWIJDEREN!!!!!!!!!
        return progStateCopy

def run(filename):
    output = lexer.lex(filename)
    if len(output[1]) > 0:
        print(output[1])
        map(lambda x: print(x), output[1])
    else:
        print(output[0])
        pList = prs.parse(output[0])
        print(pList)
        progstate = programstate()
        for p in pList:
            progstate = executeStep(p, progstate)
            print(progstate)
