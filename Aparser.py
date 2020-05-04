import copy

from Ltoken import LToken
from node import Node
import errorClass as er
from typing import List, Union, Tuple, TypeVar


RuleDict = {
    'SOF': [
        ['IDENTIFIER', 'EOF'],
        ['SEPERATOR', 'EOF']
    ],

    'IDENTIFIER': [
        ['=']
    ],
    'DECLERATION':[
        ['=']
    ],
    'OPERATOR': [
        ['LITERAL'],
        ['LITERAL', 'OPERATOR'],
        ['VARIABLE'],
        ['VARIABLE', 'OPERATOR']
    ],
    'STARTASSIGNVARIABLE': [
        ['IDENTIFIER', 'ENDASSIGNVARIABLE']
    ],
    'STARTBLOCK': [
        ['VARIABLE'],
        ['LITERAL']
    ],
    'IO': [
        ['LITERAL'],
        ['VARIABLE'],
        ['LITERALSTRING']
    ]

}

T = TypeVar('T')
def longestListInList(checklist: List[List[T]], count: int = 0) -> List[T]:
    """
    Returns the longest List in a given set of Lists
    :param checklist:
    :param count:
    :return: The longest list in checklist, can return None if all are None
    """
    if count == len(checklist) - 1:
        return checklist[count]
    prevLongest = longestListInList(checklist, count+1)
    if checklist[count] is not None:
        if prevLongest[0] is None:
            return checklist[count]
        if len(prevLongest[0]) > len(checklist[count][0]):
            return prevLongest
        else:
            return checklist[count]
    return prevLongest


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
            nextList = list(map(lambda x: checkRules(tokenList, x, varlist, pos + count + 1), RuleDict[tokenList[pos+count].type]))
            longestInNextList = longestListInList(nextList)
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
            errorList.append(er.ParseError("Expected '{}', got '{}' on line {}".format(rulelist[count],tokenList[pos+1].value, tokenList[pos+1].line)))
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


def createTree(nodeList: List[LToken], count: int = 0, isreversed: bool = False)-> Node:
    """
    Creates an AST from the given nodeList, is reversable
    :param nodeList: List of the nodes to build a tree from
    :param count: current position in the nodelist
    :param isreversed: if the tree has passed an assignment it should reverse to have the correct order determined by the code specifications
    :return: first node in the tree, using this node we can find all the other nodes
    """
    if nodeList[count].type == 'SEPERATOR':
        count = count + 1
    if count >= len(nodeList) -1 or nodeList[count+1].type == 'SEPERATOR':
        return nodeList[count].value
    if nodeList[count].type == "OPERATOR":
        if nodeList[count].value == '=':
            return Node(nodeList[count].value, None, createTree(list(reversed(nodeList[count+1:])), 0, True))
        else:
            newtree = createTree(nodeList, count + 1, isreversed)
            if isreversed:
                return Node(nodeList[count].value, newtree)
            return Node(nodeList[count].value, None, newtree)
    if nodeList[count].type == "IO":
        return Node(nodeList[count].value, createTree(nodeList, count + 1, isreversed))
    operatorNode = createTree(nodeList, count + 1, isreversed)
    if isreversed:
        operatorNode.right = nodeList[count].value
        return operatorNode
    operatorNode.left = nodeList[count].value
    return operatorNode


def parse(tokenList: Tuple[List[LToken], List[er.Error]], varlist: List[str] = [], count:int =0)-> Union[Tuple[List[Node], List[er.Error]], Tuple[list, List[er.Error]]]:
    """
    Parses the current tokenList, checks the rules and creates an ast from the deepest possible rulesafe path
    :param tokenList: List of all the tokens
    :param varlist: List of variables assigned in the program
    :param count: current possition of the tokenList
    :return: returns a tuple containing the list of all the first nodes, and a list of encountered errors if any
    """
    errorList = []
    tmpVarlist = copy.deepcopy(varlist)
    if count == len(tokenList) - 1:
        if tokenList[count].type == 'EOF':
            return [], errorList # error list append eof not found
        else:
            errorList.append(er.ParseError("Unexpected end of file at line {}"))
            return [], errorList
    # First line is always a SOF
    if count == 0:
        if tokenList[count].type == 'SOF':
            nextParse = parse(tokenList,tmpVarlist, count+1)
            return nextParse[0], errorList + nextParse[1]
        else:
            return [], errorList
    elif tokenList[count].type is "ENDBLOCK":
        return [], errorList
    else:
        if tokenList[count].type is not 'OPERATOR':
            if tokenList[count].type == 'DECLERATION':
                if tokenList[count].value not in tmpVarlist:
                    tmpVarlist.append(tokenList[count].value)
                else:
                    errorList.append(er.ParseError('Multiple declerations of {} on line {}'.format(tokenList[count].value, tokenList[count].line)))
            if tokenList[count].type in RuleDict or tokenList[count].value in RuleDict:
                possibleRules = []
                if tokenList[count].type in RuleDict:
                    possibleRules = possibleRules + RuleDict[tokenList[count].type]
                if tokenList[count].value in RuleDict:
                    possibleRules = possibleRules + RuleDict[tokenList[count].value]

                if tokenList[count].type is "STARTBLOCK":
                    nodeValue = None
                    if tokenList[count].value == "STARTWHILE":
                        nodeValue = "while"
                    lhs = createTree(longestListInList(list(map(lambda x: checkRules(tokenList, x, tmpVarlist, count + 1), possibleRules))))
                    rhs = parse(tokenList, tmpVarlist, count + 2)
                    return [Node(nodeValue, lhs, rhs)], errorList
                else:
                    curParseMap = list(map(lambda x: checkRules(tokenList, x, tmpVarlist, count+1), possibleRules))
                    curparse = longestListInList(curParseMap)
                    if len(curparse[1]) > 0:
                        return [], errorList + curparse[1]
                    if len(curparse[0]) is not 0:
                        curparse[0].insert(0, tokenList[count])
                        nextparse = parse(tokenList, tmpVarlist, count + len(curparse[0]))
                        return [createTree(curparse[0])] + nextparse[0], errorList + nextparse[1]
    errorList.append(er.ParseError("Unexpected {} on line: {}".format(tokenList[count].value, tokenList[count].line)))
    return [], errorList
