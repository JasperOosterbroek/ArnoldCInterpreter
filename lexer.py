# not oop :( vergeet niet _recursie_ woohoo
import typing
import re
import copy
from token import TokenDict, Token


def tokenRegex(fileLine, regexDict : dict):
    regex = regexDict.popitem()
    if re.match(regex[1], fileLine):
        print("found: {}".format(regex[1]))
        return regex[0]
    else:
        if len(regexDict) == 0:
            return None
        print(regexDict)
        tokenRegex(fileLine, regexDict)




def getTokenType(fileLine, tokenDictCopy):
    if len(tokenDictCopy) == 0:
        return None
    curTokenTuple = tokenDictCopy.popitem()
    tokenr = tokenRegex(fileLine, curTokenTuple[1])
    print("tokenr: {}".format(tokenr))
    if tokenr is not None:
        return tokenr

    else:
        return getTokenType(fileLine, tokenDictCopy)

def getToken(fileLine, tokenDictCopy):
    return getTokenType(fileLine, tokenDictCopy)


def readLine(file, line = 0):
    fileLine = file.readline()
    tokenDictCopy = copy.deepcopy(TokenDict)
    token = getToken(fileLine, tokenDictCopy)
    #als token een operator check of waarde erna
    print(fileLine, token)

    if token is None:
        raise SyntaxError
    elif token in TokenDict['EOF'].keys():
        print("EOF")
    elif token in TokenDict['SOF'].keys():
        print("SOF")

    return readLine(file, line+1)

def lex(filename : str):
    f = open(filename, "r")
    readLine(f)
    #line
    #pos
    #get token?


if __name__ == '__main__':
    lex("testcode.arnoldc")




