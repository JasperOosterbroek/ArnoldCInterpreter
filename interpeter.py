import Aparser as prs
import lexer
from node import Node
import copy
import functools
import errorClass as er
from typing import List, Union, Dict, Callable

def add_command(x:int,y:int)->int:
    return x + y

def mul_command(x:int,y:int)->int:
    return x * y

def min_command(x:int,y:int)->int:
    return x - y

def gt_compare(x:int,y:int)->int:
    return int(x > y)

def div_command(x:int,y:int)->int:
    return int(x / y) # Cast to int to prevent floats

def mod_command(x:int,y:int)->int:
    return x % y

def equals_compare(x:int, y:int)->int:
    return int(x == y)

def or_compare(x:int, y:int)->int:
    return int(x or y)

def and_compare(x:int, y:int)->int:
    return int(x and y)

class programstate:

    def __init__(self, variables: Dict[str, int] = None, methods: Dict[str, prs.Method] = None, error:List[er.Error] = None, stepCount: int = 0) -> None:
        self.variables = variables if variables else dict()
        self.methods = methods if methods else dict()
        self.errors = error if error else list()
        self.stepCount = stepCount

    def __str__(self) -> str:
        return "Programstate: \nvariable: {}, methods: {}, stepCount: {}".format(self.variables, self.methods, self.stepCount)

    def __repr__(self) -> str:
        return str(self)

    def __deepcopy__(self, memodict={}):
        return programstate(self.variables, self.methods, self.errors, self.stepCount)

operatorDict = {
    '-': min_command,
    '+': add_command,
    '>': gt_compare,
    '*': mul_command,
    '/': div_command,
    '%': mod_command,
    '==': equals_compare,
    '||': or_compare,
    '&&': and_compare
}

def executeDebugStep(f: Callable[[Node, programstate], Union[programstate, int, List[str]]]) -> Callable[[Node, programstate], Union[programstate, int, List[str]]]:
    """
    Decorator function for execute step, makes debugging easier
    by printing the current Node and print the current programstate
    :param f: function
    :return:
    """
    def inner(p, progstate):
        print(p)
        print(progstate)
        return f(p, progstate)
    return inner

def executeStep(curNode: Node, progState: programstate)-> Union[programstate, int, List[str]]:
    """
    Execute current Node step
    :param curNode: the current Node that needs to be executed
    :param progState: the programstate, this contains variables and errors
    :return: either programstate if done, or an int if a calculation was made
    """
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
    if curNode.data == 'if':
        condition = curNode.left if curNode.left not in progStateCopy.variables else progStateCopy.variables[curNode.left]
        lhs = curNode.center
        rhs = curNode.right
        if int(condition) == 1:
            progStateCopy = functools.reduce(lambda x,y: executeStep(y, x), lhs, progStateCopy)
        elif rhs is not None:
            progStateCopy = functools.reduce(lambda x,y: executeStep(y, x), rhs, progStateCopy)
        return progStateCopy
    if curNode.data == 'ASSIGNMETHODDARGUMENT':
        varlist = [curNode.right]
        varlist += executeStep(curNode.left, progStateCopy)
        return varlist

    if curNode.data == 'method':
        return [curNode.left]

    lhs = curNode.left if curNode.left not in progStateCopy.variables else progStateCopy.variables[curNode.left]
    rhs = curNode.right if curNode.right not in progStateCopy.variables else progStateCopy.variables[curNode.right]
    if curNode.data in operatorDict:
        if type(rhs) == Node and type(lhs) == Node:
            return operatorDict[curNode.data](executeStep(lhs,progStateCopy), executeStep(rhs, progStateCopy))
        elif type(rhs) == Node:
            return operatorDict[curNode.data](int(lhs), executeStep(rhs, progStateCopy))
        elif type(lhs) == Node:
            return operatorDict[curNode.data](executeStep(lhs, progStateCopy), int(rhs))
        return operatorDict[curNode.data](int(lhs), int(rhs))

    if curNode.data == '=':
        if type(rhs) == Node:
            step = executeStep(rhs, progStateCopy)
            if type(step) == list:
                method = step[-1]
                curmethodvars = step[:-1]
                if method in progStateCopy.methods:
                    callableMethod = progStateCopy.methods[method]
                    newProgstate = programstate()
                    newProgstate.variables = dict(zip(callableMethod.varList, reversed(curmethodvars)))
                    for p in callableMethod.tree:
                        newProgstate = executeStep(p,newProgstate)
                    progStateCopy.variables[curNode.left] = newProgstate
                    return progStateCopy
                else:
                    progStateCopy.errors.append(er.RuntimeError('Call to undefined method: {}'.format(method)))
                    return progStateCopy
            progStateCopy.variables[curNode.left] = step
            return progStateCopy
        if rhs is not None:
            progStateCopy.variables[curNode.left] = rhs
            return progStateCopy
    if curNode.data == 'RETURN':
        return progStateCopy.variables[curNode.left]
    if curNode.data == 'PRINT':
        print(lhs)
        return progStateCopy
    progStateCopy.errors.append(er.RuntimeError("Unhandleable Node Data {}".format(curNode.data)))
    return progStateCopy

def run(lines:List[str])->None:
    """
    Lexes, parses and executes a program written in ArnoldC from given filename file
    :param lines: the lines in the file
    :return: None
    """
    output = lexer.lex(lines)
    # print(output)
    if len(output[1]) > 0:
            print(output[1])
    else:
        parseState = prs.ParseState()
        pList = prs.parse(output[0], parseState)
        if len(pList.errorList) > 0:
            print(pList.errorList)
        else:
            progstate = programstate()
            progstate.methods = pList.methodDict

            if 'main' in pList.methodDict:
                for p in pList.methodDict['main'].tree:
                    if len(progstate.errors) > 0:
                        print(progstate.errors)
                    else:
                        progstate = executeStep(p, progstate)
            else:
                print(er.RuntimeError("No Main method found"))