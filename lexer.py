# not oop :( vergeet niet _recursie_ woohoo
import typing
import re
import copy
from token import TokenDict, Token

def listNoneCheck(checkList, count = 0):
    if count == len(checkList):
        return None
    if checkList[count] == None:
        return listNoneCheck(checkList, count+1)
    else:
        return checkList[count]

def tokenRegex(fileLine, regexDict, count = 0):
    if count == len(regexDict):
        return None
    if re.match(regexDict[1], fileLine) is not None:
        return regexDict[0]
    return tokenRegex(fileLine, regexDict, count + 1)

def getTokenType(fileLine, tokenDict, count = 0):
    if count == len(tokenDict):
        return None
    tokenr = listNoneCheck(list(map(lambda x: tokenRegex(fileLine, x), tokenDict[1].items())))
    if tokenr is not None:
        return Token(tokenDict[0], tokenr)
    else:
        return getTokenType(fileLine, tokenDict, count + 1)

def getArgument(types : list, string):
    if len(types) == 0:
        return None # should raise an error
    curType = types.pop(0)
    if curType == "string":
        if re.match('^[a-zA-Z]*$', string) is not None:
            return string
    elif curType == "int":
        if re.match('^[0-9]*$', string) is not None:
            return string

    return getArgument(types, string)

def readLine(file, line = 0):
    fileLine = file.readline()
    tokenList = list(map(lambda x: getTokenType(fileLine, x), TokenDict.items()))
    token = listNoneCheck(tokenList)
    tokenlist = []
    if token is None:
        raise SyntaxError
    elif token.value in TokenDict['EOF'].keys():
        return [token] # last return statement, the break of this recursion
    elif token.value in TokenDict['OPERATOR'].keys():
        # operator follows an identifier can be int or string not both
        argument = getArgument(['int', 'string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argument is not None:
            tokenlist.append(Token('LITERAL', argument))
        else:
            raise SyntaxError
    elif token.value in TokenDict['IDENTIFIER'].keys():
        # Identifier is followed by a string
        argument = getArgument(['string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argument is not None:
            tokenlist.append(Token('IDENTIFIER', argument))
        else:
            raise SyntaxError
    elif token.value in TokenDict['IO'].keys():
        # io is followed by a string
        argument = getArgument(['string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argument is not None:
            tokenlist.append(Token('IDENTIFIER', argument))
        else:
            raise SyntaxError
    elif token.value in TokenDict['LITERAL'].keys():
        argument = getArgument(['int'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argument is not None:
            tokenlist.append(Token('IDENTIFIER', argument))
        else:
            raise SyntaxError
    tokenlist.insert(0, token)
    return tokenlist + readLine(file, line+1)

def lex(filename : str):
    f = open(filename, "r")
    print(readLine(f))

if __name__ == '__main__':
    lex("testcode.arnoldc")
