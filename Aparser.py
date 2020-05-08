import copy

from Ltoken import LToken
from node import Node, IfElseNode
import errorClass as er
from typing import List, Union, Tuple, Dict

class Method:
    def __init__(self, varList: List[str]=None, methodName: List[str]=None, tree: List[Node]=None) -> None:
        self.varList = varList if varList else list()
        self.methodName = methodName if methodName else None
        self.tree = tree if tree else list()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Method {}:, varlist: {}, tree:{}".format(self.methodName, self.varList, self.tree)

class ParseState:

    def __init__(self, curPosTokenList:List[LToken] = None, varList:List[str]=None, methodDict:Dict[str, Method]=None, errorList:List[er.Error]=None, treeList:List[Node]=None ,assignableVar:List[str]=None) -> None:
        self.curPosTokenList = curPosTokenList if curPosTokenList else 0
        self.varList = varList if varList else list()
        self.methodDict = methodDict if methodDict else dict()
        self.assignableVar = assignableVar if assignableVar else list()
        self.errorList = errorList if errorList else list()
        self.treeList = treeList if treeList else list()
    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Parse state: current position:{}, variable list: {}, method list: {}, errorList: {}: treelist: {}".format(self.curPosTokenList, self.varList, self.methodDict, self.errorList, self.treeList)

    def __deepcopy__(self, memodict={}):
        return ParseState(self.curPosTokenList, self.varList, self.methodDict, self.errorList, self.assignableVar)

RuleDict = {
    'STARTMAIN': [
        ['IDENTIFIER', 'ENDMAIN'],
        ['SEPERATOR', 'ENDMAIN']
    ],
    'STARTMETHOD': [
        ['IDENTIFIER'],
        ['SEPERATOR'],
        ['METHODARGUMENT', 'IDENTIFIER'],
        ['METHODARGUMENT', 'SEPERATOR'],
        ['IDENTIFIER', 'RETURN'],
        ['SEPERATOR', 'RETURN'],
        ['METHODARGUMENT', 'IDENTIFIER', 'RETURN'],
        ['METHODARGUMENT', 'SEPERATOR', 'RETURN']
    ],
    'METHODARGUMENT': [
        ['METHODARGUMENT'],
        ['ENDMETHODVARIABLES']
    ],
    'RETURN':[
        ['VARIABLE']
    ],
    'STARTIF':[
        ['VARIABLE'],
        ['LITERAL']
    ],
    'ELSE': [
        ['IDENTIFIER'],
        ['SEPERATOR'],
        ['IO']
    ],
    'IDENTIFIER': [
        ['=']
    ],
    'DECLERATION':[
        ['=']
    ],
    'ASSIGNVARIABLE':[
        ['IDENTIFIER']
    ],
    'OPERATOR': [
        ['LITERAL'],
        ['LITERAL', 'OPERATOR'],
        ['VARIABLE'],
        ['VARIABLE', 'OPERATOR'],
        ['CALLMETHOD']
    ],
    'CALLMETHOD': [
        ['METHODNAME'],
        ['METHODNAME', 'ASSIGNMETHODDARGUMENT']
    ],
    'ASSIGNMETHODDARGUMENT': [
        ['ASSIGNMETHODDARGUMENT'],
        ['ENDMETHODCALL']
    ],
    'STARTASSIGNVARIABLE': [
        ['IDENTIFIER', 'ENDASSIGNVARIABLE']
    ],
    'STARTWHILE': [
        ['VARIABLE'],
        ['LITERAL']
    ],
    'IO': [
        ['LITERAL'],
        ['VARIABLE'],
        ['LITERALSTRING']
    ]

}

def checkRules(tokenList: Tuple[List[LToken], List[er.Error]], rulelist: List[str], varlist: List[str], pos: int, count:int = 0) -> Tuple[List[LToken], List[er.Error]]:
    """
    Checks if the current list of tokens is conform to the given rules in the RuleDict
    :param tokenList: list of all the tokens of the program
    :param rulelist: list of the rules to use as guidlines
    :param varlist: List of currently assigned variables
    :param pos: post to start in the tokenList
    :param count: current stepcount in the tokenList and in ruleList
    :return: A tuple, first element is a list of the tokens, the second element is a list of the encountered errors
    """

    errorList = []
    if(len(rulelist) == 0):
        return [], errorList
    if tokenList[pos+count].type == 'IDENTIFIER' and tokenList[pos+count].value not in varlist:
        errorList.append(er.ParseError("Undeclared variable {} on line {}".format(tokenList[pos+count].value, tokenList[pos+count].line)))
        return [], errorList
    if tokenList[pos+count].type == 'VARIABLE' and tokenList[pos+count].value not in varlist:
        errorList.append(er.ParseError("Undefined variable {} on line {}".format(tokenList[pos + count].value, tokenList[pos + count].line)))
        return [], errorList
    if tokenList[pos+count].type == rulelist[count] or tokenList[pos+count].value == rulelist[count]:
        if tokenList[pos+count].type in RuleDict or tokenList[pos+count].value in RuleDict:
            if tokenList[pos+count].value in RuleDict:
                nextList = list(map(lambda x: checkRules(tokenList, x, varlist, pos + count + 1), RuleDict[tokenList[pos+count].value]))
            elif tokenList[pos+count].type in RuleDict:
                nextList = list(map(lambda x: checkRules(tokenList, x, varlist, pos + count + 1), RuleDict[tokenList[pos+count].type]))
            longestInNextList = max(nextList, key=lambda x: len(x[0]))
            if len(longestInNextList[0]) > 0:
                if count is not len(rulelist) - 1:
                    next = checkRules(tokenList, rulelist, varlist, pos + len(longestInNextList[0]), count + 1)
                    if next[0] is None:
                        errorList.append(er.ParseError("Expected '{}', got '{}' on line {}".format(rulelist[count+1],tokenList[pos].value, tokenList[pos].line)))
                        return [], errorList
                    return [tokenList[pos + count]] + longestInNextList[0] + next[0], errorList + longestInNextList[1] + next[1]
                return [tokenList[pos+count]] + longestInNextList[0], errorList + longestInNextList[1]
            if len(longestInNextList[1]) > 0:
                return [], longestInNextList[1]
            errorList.append(er.ParseError("Expected '{}', got '{}' on line {}".format(rulelist[count], tokenList[pos+1], tokenList[pos+1].line)))
            return [], errorList
        else:
            if count == len(rulelist) - 1:
                return [tokenList[pos+count]], errorList
            else:
                next = checkRules(tokenList, rulelist, varlist, pos, count + 1)
                if len(next[0]) is 0:
                    errorList.append(er.ParseError("Expected '{}', got '{}' on line {}".format(rulelist[count+1], tokenList[pos].value, tokenList[pos].line)))
                    return [], errorList
                return [tokenList[pos+count]] + next[0], errorList + next[1]
    elif tokenList[pos+count].type in RuleDict or tokenList[pos+count].value in RuleDict:
        return [], errorList
    return [], errorList


def createTree(nodeList: List[LToken], count: int = 0, isreversed: bool = False) -> Union[Node,str]:
    """
    Creates an AST from the given nodeList, is reversable
    :param nodeList: List of the nodes to build a tree from
    :param count: current position in the nodelist
    :param isreversed: if the tree has passed an assignment it should reverse to have the correct order determined by the code specifications
    :return: first node in the tree, using this node we can find all the other nodes
    """
    if nodeList[count].type == 'SEPERATOR' or nodeList[count].value == 'ENDMETHODCALL' or nodeList[count].value == 'ENDMETHODVARIABLES' or nodeList[count].value == 'ASSIGNVARIABLE':
        count = count + 1
    if count >= len(nodeList) -1 or nodeList[count+1].type == 'SEPERATOR'or nodeList[count+1].value == 'ENDMETHODCALL' or nodeList[count+1].value == 'ENDMETHODVARIABLES':
        return nodeList[count].value
    if nodeList[count].type == "OPERATOR":
        if nodeList[count].value == '=':
            return Node(nodeList[count].value, None, createTree(list(reversed(nodeList[count+1:])), 0, True))
        else:
            newtree = createTree(nodeList, count + 1, isreversed)
            if isreversed:
                return Node(nodeList[count].value, newtree)
            return Node(nodeList[count].value, None, newtree)
    if nodeList[count].type == "IO" or nodeList[count].value == "RETURN":
        return Node(nodeList[count].value, createTree(nodeList, count + 1, isreversed))
    if nodeList[count].type == 'METHODNAME':
        return Node('method', nodeList[count].value, createTree(nodeList, count + 1, isreversed))
    if nodeList[count].type == 'ASSIGNMETHODDARGUMENT':
        if isreversed:
            return Node(nodeList[count].type, createTree(nodeList, count + 1, isreversed), nodeList[count].value)
        else:
            return Node(nodeList[count].type, nodeList[count].value, createTree(nodeList, count+1, isreversed))
    if nodeList[count].type == "METHODARGUMENT":
        if isreversed:
            return Node(nodeList[count].type, createTree(nodeList, count + 1, isreversed), nodeList[count].value)
        else:
            return Node(nodeList[count].type, nodeList[count].value, createTree(nodeList, count+1, isreversed))
    operatorNode = createTree(nodeList, count + 1, isreversed)
    if isreversed:
        operatorNode.right = nodeList[count].value
        return operatorNode

    operatorNode.left = nodeList[count].value
    return operatorNode

def parse(tokenList: List[LToken], oldState: ParseState) -> ParseStateg:
    state = copy.deepcopy(oldState)
    if(state.curPosTokenList == len(tokenList)):
        return state
    if tokenList[state.curPosTokenList].type == "ENDBLOCK" or tokenList[state.curPosTokenList].type == "ALTERNATIVEBLOCK" or tokenList[state.curPosTokenList].type == 'ENDOFFILE':
        return state
    else:
        if tokenList[state.curPosTokenList].type is not "OPERATOR":
            if tokenList[state.curPosTokenList].type == 'DECLERATION':
                if tokenList[state.curPosTokenList].value not in state.varList:
                    state.varList.append(tokenList[state.curPosTokenList].value)
                else:
                    state.errorList.append(er.ParseError('Multiple declerations of {} on line {}'.format(tokenList[state.curPosTokenList].value, tokenList[state.curPosTokenList].line)))
            if tokenList[state.curPosTokenList].type in RuleDict or tokenList[state.curPosTokenList].value in RuleDict:
                possibleRules = []
                if tokenList[state.curPosTokenList].type in RuleDict:
                    possibleRules = possibleRules + RuleDict[tokenList[state.curPosTokenList].type]
                if tokenList[state.curPosTokenList].value in RuleDict:
                    possibleRules = possibleRules + RuleDict[tokenList[state.curPosTokenList].value]
                if tokenList[state.curPosTokenList].type is "STARTBLOCK" or tokenList[state.curPosTokenList].type is 'STARTMETHOD':
                    if tokenList[state.curPosTokenList].value == "STARTWHILE":
                        nodeValue = "while"
                        state.curPosTokenList += 1
                        lhsList = max(list(map(lambda x: checkRules(tokenList, x, state.varList, state.curPosTokenList), possibleRules)), key=lambda x: len(x[0]))
                        lhs = createTree(lhsList[0])
                        state.curPosTokenList += 1
                        whileContent = parse(tokenList, state)
                        state.curPosTokenList = whileContent.curPosTokenList + 1
                        rhs = parse(tokenList, state)
                        whileNode = Node(nodeValue, lhs, whileContent.treeList)
                        state.treeList.append(whileNode)
                        state.treeList += rhs.treeList
                        state.errorList += rhs.errorList
                        state.varList += rhs.varList
                        return state
                    elif tokenList[state.curPosTokenList].value == "STARTIF":
                        nodeValue = "if"
                        state.curPosTokenList += 1
                        lhsList = max(list(map(lambda x: checkRules(tokenList, x, state.varList, state.curPosTokenList), possibleRules)), key=lambda x: len(x[0]))
                        lhs = createTree(lhsList[0])
                        state.curPosTokenList += 1
                        center = parse(tokenList, state)
                        state.curPosTokenList = center.curPosTokenList
                        if tokenList[state.curPosTokenList].value == "ELSE":
                            state.curPosTokenList += 1
                            rhs = parse(tokenList, state)
                            state.curPosTokenList = rhs.curPosTokenList + 1
                            node = IfElseNode(nodeValue, lhs, center.treeList, rhs.treeList)
                        else:
                            state.curPosTokenList += 1
                            node = IfElseNode(nodeValue, lhs, center.treeList)

                        state.treeList.append(node)

                        nextParse = parse(tokenList, state)
                        state.curPosTokenList = nextParse.curPosTokenList
                        state.treeList += nextParse.treeList
                        state.errorList += nextParse.errorList
                        state.varList += nextParse.varList
                        return state

                    elif tokenList[state.curPosTokenList].value == "STARTMAIN" or tokenList[state.curPosTokenList].type == "STARTMETHOD":
                        if tokenList[state.curPosTokenList].value == "STARTMAIN":
                            methodName = "main"
                        if tokenList[state.curPosTokenList].type == "STARTMETHOD":
                            methodName = tokenList[state.curPosTokenList].value
                        state.curPosTokenList += 1
                        methodDeclarePos = state.curPosTokenList
                        state = parse(tokenList, state)
                        newMethod = Method(state.varList, methodName, state.treeList)

                        if methodName in state.methodDict:
                            state.errorList.append(er.ParseError("Method name: {}, already in use on line {}".format(methodName, methodDeclarePos)))
                        else:
                            state.methodDict[methodName] = newMethod
                            state.varList = []
                            state.treeList = []
                        state.curPosTokenList += 1
                        state = parse(tokenList, state)
                        return state
                else:
                    state.curPosTokenList += 1
                    curParseMap = list(map(lambda x: checkRules(tokenList, x, state.varList, state.curPosTokenList), possibleRules))
                    curparse = max(curParseMap, key=lambda x: len(x[0]))
                    if len(curparse[1]) > 0:
                        state.errorList += curparse[1]
                        return state
                    if len(curparse[0]) is not 0:
                        curparse[0].insert(0, tokenList[state.curPosTokenList -1])
                        if  tokenList[state.curPosTokenList -1].type == "METHODARGUMENT":
                            tmpFilteredList = filter(None, list(map(lambda x: x.value if x.type == "METHODARGUMENT" else None , curparse[0])))
                            state.varList += tmpFilteredList
                            state.assignableVar += tmpFilteredList
                        state.curPosTokenList += len(curparse[0]) -1
                        nextparse = parse(tokenList, state)
                        state.curPosTokenList = nextparse.curPosTokenList
                        state.treeList = [createTree(curparse[0])] + nextparse.treeList
                        state.errorList += nextparse.errorList
                        return state
    state.errorList.append(er.ParseError("Unexpected {} on line: {}".format(tokenList[state.curPosTokenList], tokenList[state.curPosTokenList].line)))
    return state