import Aparser as prs
import lexer
import node
import copy

def add_command(x, y):
    return x + y

def mul_command(x,y):
    return x * y

def gTCompare(x, y):
    return x > y

def sTcompare(x,y):
    return x < y



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


def executeStep(curNode, progState):
    progStateCopy = copy.deepcopy(progState)
    if curNode.right is None and curNode.left is None:
        return progStateCopy
    lhs = curNode.left if curNode.left not in progStateCopy.variables else progStateCopy.variables[curNode.left]
    rhs = curNode.right if curNode.right not in progStateCopy.variables else progStateCopy.variables[curNode.right]
    if curNode.data == '+':
        if type(rhs) == node.Node:
            return add_command(int(lhs), executeStep(rhs, progStateCopy))
        return add_command(int(lhs), int(rhs))
    if curNode.data == '*':
        if type(rhs) == node.Node:
            return mul_command(int(lhs), executeStep(rhs, progStateCopy))
        return mul_command(int(lhs), int(rhs))
    if curNode.data == '>':
        if type(rhs) == node.Node:
            return gTCompare(int(lhs), executeStep(rhs, progStateCopy))
        return gTCompare(int(lhs), int(rhs))
    if curNode.data == '<':
        if type(rhs) == node.Node:
            return sTcompare(int(lhs), executeStep(rhs, progStateCopy))
        return sTcompare(int(lhs), int(rhs))
    if curNode.data == '=':
        if type(rhs) == node.Node:
            progStateCopy.variables[curNode.left] = executeStep(rhs, progStateCopy)
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
    pList = prs.parse(output)
    progstate = programstate()
    for p in pList:
        progstate = executeStep(p, progstate)
        print(p, progstate)


if __name__ == '__main__':
    run("testcode.arnoldc")