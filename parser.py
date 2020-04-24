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
    'SOF':[
        ['IDENTIFIER', 'EOF'],
        ['SEPERATOR', 'EOF']
    ],

    'IDENTIFIER': [
        ['=']
    ],

    'OPERATOR': [
        ['LITERAL'],
        ['LITERAL', 'OPERATOR'],
        ['IDENTIFIER'],
        ['IDENTIFIER', 'OPERATOR']
    ],
    'STARTASSIGNVARIABLE': [
        ['IDENTIFIER', 'ENDASSIGNVARIABLE']
    ],
    'IO': [
        ['IDENTIFIER']
    ]

}
# check of in rule dict, zoja, controleer alle lijsten, als ding in lijst zit controleer lijsten etc.
# return longest list function ?
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
    return None

# def checkRules(tokenList, ruleList, pos, count = 0):
#
#
#
#     return None # hier errort hij!

# def checkRules(tokenList, rulelist, pos, count = 0):
#     if(len(rulelist) == 0):
#         return []
#     if tokenList[pos+count].type == rulelist[count] or tokenList[pos+count].value == rulelist[count]:
#         if tokenList[pos+count].type in RuleDict or tokenList[pos+count].value in RuleDict:
#             nextList = list(map(lambda x: checkRules(tokenList, x, pos + count + 1), RuleDict[tokenList[pos+count].type]))
#             longestInNextList = longestListInList(nextList)
#             if longestInNextList is not None:
#                 if count is not len(rulelist) -1:
#                     next = checkRules(tokenList, rulelist, pos + len(longestInNextList), count + 1)
#                     if next is None:
#                         return None
#                     return [tokenList[pos + count]] + longestListInList(nextList) + next
#                 return [tokenList[pos+count]] + longestListInList(nextList)
#             return None
#
#         else:
#             if count == len(rulelist) - 1:
#                 return [tokenList[pos+count]]
#             else:
#                 next = checkRules(tokenList, rulelist, pos, count + 1)
#                 if next is None:
#                     return None
#                 return [tokenList[pos+count]] + next
#     elif tokenList[pos+count].type in RuleDict or tokenList[pos+count].value in RuleDict:
#         return []
#     return None # error?


def parse(tokenList, count = 0):
    if count == len(tokenList) - 1:
        if tokenList[count].type == 'EOF':
            print('EOF')
            return Node('EOF')
        else:
            return 'error, no EOF'
    if count == 0:
        if tokenList[count].type == 'SOF':
            print('SOF')
            return Node(tokenList[count].type, tokenList[count].value, parse(tokenList, count+1))
        else:
            return 'error, no SOF'
    else:
        if tokenList[count].type in RuleDict or tokenList[count].value in RuleDict:
            possibleRules = []
            if tokenList[count].type in RuleDict:
                possibleRules = possibleRules + RuleDict[tokenList[count].type]
            if tokenList[count].value in RuleDict:
                possibleRules = possibleRules + RuleDict[tokenList[count].value]

            print(possibleRules)
            test = list(map(lambda x: checkRules(tokenList, x, count+1), possibleRules))
            print(test)
            test[0].insert(0, tokenList[count])
            return test + parse(tokenList, count + len(test[0]))
    # print(tokenList, count)

def parseList(tokenList):
    return parse(tokenList)

if __name__ == '__main__':
    output = lexer.lex("testcode.arnoldc")
    print(output)
    print(parseList(output))