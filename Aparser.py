# we pakken de lexer en bouwen een AST met gebruik van de parser
# de parser kijkt of alles klopt op het niveau van a = 10, als a = wordt gebruikt en daarna geen waarde error
# stappen ish:
# 1. defineer de "regels" ( a = 2, a = b a = 2*3 etc.), inclusief reken regels
# 2. Maak een binary tree (jatten van algoritme en datasctructuren vak)
# 3. loop door de lijst van tokens en check of de regels kloppen, als deze kloppen voeg het toe aan de "boom" zo niet error
# 4. return de boom voor de interperter

from node import Node
import lexer
import functools as ft
# https://en.wikipedia.org/wiki/Order_of_operations
RuleDict = {
    'SOF': [
        ['IDENTIFIER', 'EOF'],
        ['SEPERATOR', 'EOF']
    ],

    'IDENTIFIER': [ #block
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
    'LOOP': [
        ['IDENTIFIER', 'IO', 'SEPERATOR']
    ],
    'IO': [
        ['LITERAL'],
        ['VARIABLE']
    ]

}

def longestListInList(list, count = 0):
    if count == len(list) - 1:
        return list[count]
    prevLongest = longestListInList(list, count+1)
    if list[count] is not None:
        if prevLongest is None:
            return list[count]
        if len(prevLongest) > len(list[count]):
            return prevLongest
        else:
            return list[count]
    return prevLongest

def checkRules(tokenList, rulelist, pos, count = 0):
    if(len(rulelist) == 0):
        return []
    if tokenList[pos+count].type == rulelist[count] or tokenList[pos+count].value == rulelist[count]:
        if tokenList[pos+count].type in RuleDict or tokenList[pos+count].value in RuleDict:
            nextList = list(map(lambda x: checkRules(tokenList, x, pos + count + 1), RuleDict[tokenList[pos+count].type]))
            longestInNextList = longestListInList(nextList)
            if longestInNextList is not None:
                if count is not len(rulelist) - 1:
                    next = checkRules(tokenList, rulelist, pos + len(longestInNextList), count + 1)
                    if next is None:
                        return None
                    return [tokenList[pos + count]] + longestListInList(nextList) + next
                return [tokenList[pos+count]] + longestListInList(nextList)
            return None
        else:
            if count == len(rulelist) - 1:
                return [tokenList[pos+count]]
            else:
                next = checkRules(tokenList, rulelist, pos, count + 1)
                if next is None:
                    return None
                return [tokenList[pos+count]] + next
    elif tokenList[pos+count].type in RuleDict or tokenList[pos+count].value in RuleDict:
        return []
    return None


def createTree(nodeList, count = 0):
    if nodeList[count].type == 'SEPERATOR':
        count = count + 1
    if count >= len(nodeList) -1 or nodeList[count+1].type == 'SEPERATOR':
        return nodeList[count].value
    if nodeList[count].type == "OPERATOR":
        if nodeList[count].value == '=':
            return Node(nodeList[count].value, None, createTree(list(reversed(nodeList[count+1:]))))
        else:
            return Node(nodeList[count].value, None, createTree(nodeList, count+1))
    if nodeList[count].type == "IO":
        return Node(nodeList[count].value, createTree(nodeList, count + 1))

    operatorNode = createTree(nodeList, count + 1)
    operatorNode.left = nodeList[count].value
    return operatorNode

def parse(tokenList, count=0):
    # last line is always an EOF
    if count == len(tokenList) - 1:
        if tokenList[count].type == 'EOF':
            return []
        else:
            return 'error, no EOF'
    # First line is always a SOF
    if count == 0:
        if tokenList[count].type == 'SOF':
            return parse(tokenList, count+1)
        else:
            return 'error, no SOF'
    else:
        if tokenList[count].type is "LOOP":
            print("paniek ", tokenList[count])
            # hoi jasper van morgen, hier misschien iets met die loops doen ofzo

        if tokenList[count].type is not 'OPERATOR':
            print("tokenlist: ",tokenList[count])
            if tokenList[count].type in RuleDict or tokenList[count].value in RuleDict:
                possibleRules = []
                if tokenList[count].type in RuleDict:
                    possibleRules = possibleRules + RuleDict[tokenList[count].type]
                if tokenList[count].value in RuleDict:
                    possibleRules = possibleRules + RuleDict[tokenList[count].value]
                test = longestListInList(list(map(lambda x: checkRules(tokenList, x, count+1), possibleRules)))
                if test is not None:
                    test.insert(0, tokenList[count])
                    return [createTree(test)] + parse(tokenList, count + len(test))
    return []

if __name__ == '__main__':
    output = lexer.lex("testcode.arnoldc")
    pList = parse(output)
    for i in pList:
        print(i)