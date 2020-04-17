# not oop :( vergeet niet _recursie_ woohoo
import typing
import re
import copy
from token import TokenDict, Token


def tokenRegex(fileLine, regexDict : dict):
    regex = regexDict.popitem()
    if re.match(regex[1], fileLine) is not None:
        return regex[0]
    else:
        if len(regexDict) == 0:
            return None
        return tokenRegex(fileLine, regexDict)

def getTokenType(fileLine, tokenDictCopy):
    if len(tokenDictCopy) == 0:
        return None
    curTokenTuple = tokenDictCopy.popitem()
    curTokenTupleDictCopy = copy.deepcopy(curTokenTuple[1])
    tokenr = tokenRegex(fileLine, curTokenTupleDictCopy)
    if tokenr is not None:
        return tokenr

    else:
        return getTokenType(fileLine, tokenDictCopy)

def readLine(file, line = 0):
    fileLine = file.readline()
    tokenDictCopy = copy.deepcopy(TokenDict)
    token = getTokenType(fileLine, tokenDictCopy)
    # print(token, fileLine)
    #
    #
    # todo
    # voor dingen waarna een waarde of variable kan zijn check dit
    # aanmaken van de token
    #
    if token is None:
        raise SyntaxError
    elif token in TokenDict['OPERATOR'].keys():
        print('operator')
    elif token in TokenDict['SEPERATOR'].keys():
        print('seperator')
    elif token in TokenDict['SOF'].keys():
        # start of script so end this current function
        print('start of function')
    elif token in TokenDict['EOF'].keys():
        print('end of function')
        return []
    elif token in TokenDict['IDENTIFIER'].keys():
        print("identifier")
    elif token in TokenDict['IO'].keys():
        print('IO')

    # return a list of tokens for the parser to handle
    # recursive so insert the result of this one to the left of the list
    # return value from the if statements above pushed to the front of the list
    return readLine(file, line+1)

def lex(filename : str):
    f = open(filename, "r")
    readLine(f)
    #line
    #pos
    #get token?


if __name__ == '__main__':
    lex("testcode.arnoldc")




