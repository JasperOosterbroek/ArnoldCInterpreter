# not oop :( vergeet niet _recursie_ woohoo
import typing
import re
import copy
from Ltoken import TokenDict, LToken

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
        return LToken(tokenDict[0], tokenr)
    else:
        return getTokenType(fileLine, tokenDict, count + 1)

def getArgument(types : list, string, count = 0):
    if len(types) == count:
        # last check incase of marcos
        if re.match('(@NO PROBLEMO)', string):
            return 1, 'int'
        elif re.match('(@I LIED)', string):
            return 0, 'int'
        return None
    if types[count] == "string":
        if re.match('^[a-zA-Z][\\w]*$', string) is not None:
            return string, types[count]
    elif types[count] == "int":
        if re.match('^[0-9]*$', string) is not None:
            return string, types[count]

    return getArgument(types, string, count+1)

def readLine(file, line = 0):
    fileLine = file.readline()
    tokenList = list(map(lambda x: getTokenType(fileLine, x), TokenDict.items()))
    token = listNoneCheck(tokenList)
    tokenlist = []
    if token is None:
        print(fileLine)
        raise SyntaxError (fileLine)
    elif token.value in TokenDict['EOF'].keys():
        return [token] # last return statement, the break of this recursion
    elif token.value in TokenDict['OPERATOR'].keys():
        # operator follows an identifier can be int or string not both
        argumentValue, argumentType = getArgument(['int', 'string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argumentValue is not None:
            if argumentType == 'int':
                tokenlist.append(LToken('LITERAL', argumentValue.rstrip()))
            elif argumentType == 'string':
                tokenlist.append(LToken('VARIABLE', argumentValue.rstrip()))
        else:
            raise SyntaxError
    elif token.value in TokenDict['IDENTIFIER'].keys():
        argumentValue, argumentType = getArgument(['string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argumentValue is not None:
            token.value = argumentValue.rstrip()
        else:
            raise SyntaxError
    elif token.value in TokenDict['IO'].keys():
        # io is followed by a string
        argumentValue, argumentType = getArgument(['string', 'int'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argumentValue is not None:
            tokenlist.append(LToken('VARIABLE', argumentValue.rstrip()))
        else:
            raise SyntaxError
    elif token.value in TokenDict['LITERAL'].keys():
        argumentValue, argumentType = getArgument(['int', 'string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
        if argumentValue is not None:
            token.value = argumentValue.rstrip()
        else:
            raise SyntaxError

    elif token.value in TokenDict['SEPERATOR'].keys():
        if token.value == "STARTASSIGNVARIABLE":
            argumentValue, argumentType = getArgument(['string'], re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip())
            if argumentValue is not None:
                tokenlist.append(LToken('IDENTIFIER', argumentValue.rstrip()))
                tokenlist.append(LToken('OPERATOR', '='))
            else:
                raise SyntaxError

    tokenlist.insert(0, token)
    return tokenlist + readLine(file, line+1)

def lex(filename : str):
    f = open(filename, "r")
    return readLine(f)

if __name__ == '__main__':
    lex("testcode.arnoldc")
