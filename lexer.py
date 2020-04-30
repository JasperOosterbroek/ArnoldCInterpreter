# not oop :( vergeet niet _recursie_ woohoo
import typing
import re
import copy
from Ltoken import TokenDict, LToken
import errorClass as ec

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

def getTokenType(fileLine, tokenDict, lineNum, count = 0):
    if count == len(tokenDict):
        return None
    tokenr = listNoneCheck(list(map(lambda x: tokenRegex(fileLine, x), tokenDict[1].items())))
    if tokenr is not None:
        return LToken(tokenDict[0], tokenr, lineNum)
    else:
        return getTokenType(fileLine, tokenDict, lineNum, count + 1)

def getArgument(types : list, string, count = 0):
    if len(types) == count:
        if re.match(r'^(@NO PROBLEMO)', string):
            return '1', 'int'
        elif re.match(r'^(@I LIED)', string):
            return '0', 'int'
        return None, None
    if types[count] == "variable":
        if re.match('^[a-zA-Z][\\w]*$', string) is not None:
            return string, types[count]
    elif types[count] == "int":
        if re.match('^-?[0-9]*$', string) is not None:
            return string, types[count]
    elif types[count] == 'string':
        if re.match(r'^".*"', string) is not None:
            return string[1:-2], types[count]  # remove " from string

    return getArgument(types, string, count+1)

expectedArguments = {
    'OPERATOR': ['int', 'variable'],
    'IO': ['variable', 'int', 'string'],
    'LITERAL': ['int', 'variable'],
    'STARTBLOCK': ['int', 'variable'],
    'IDENTIFIER': ['variable']

}

def readLine(file, line = 0):
    fileLine = file.readline()
    line += 1
    tokenTypeList = list(map(lambda x: getTokenType(fileLine, x, line), TokenDict.items()))
    token = listNoneCheck(tokenTypeList)
    tokenlist = []
    errorList = []
    if token is None:
        errorList.append(ec.Error('Syntax Error', "Invalid syntax {} on line {}".format(fileLine, line)))
    elif token.value in TokenDict['EOF'].keys():
        return ([token], []) # last return statement, the break of this recursion
    elif token.value in TokenDict[token.type].keys() and token.type in expectedArguments:
        substring = re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip().rstrip()
        if len(substring) > 0:
            argumentValue, argumentType = getArgument(expectedArguments[token.type], substring)
            if argumentValue is not None:
                if token.value == 'DECLERATION' or token.type == 'LITERAL':
                    token.value = argumentValue
                elif token.value == 'STARTASSIGNVARIABLE':
                    tokenlist.append(LToken('IDENTIFIER', argumentValue.rstrip(), line))
                    tokenlist.append(LToken('OPERATOR', '=', line))
                else:
                    if argumentType == 'int':
                        tokenlist.append(LToken('LITERAL', argumentValue.rstrip(), line))
                    elif argumentType == 'variable':
                        tokenlist.append(LToken('VARIABLE', argumentValue.rstrip(), line))
                    elif argumentType == 'string':
                        tokenlist.append(LToken('LITERALSTRING', argumentValue.rstrip(), line))
            else:
                errorList.append(ec.Error('Syntax Error', "Invalid argument \"{}\" on line {}".format(substring, line)))
        else:
            errorList.append(ec.Error('Syntax Error', "missing argument after \"{}\" on line {}".format(fileLine, line)))
    elif token.value in TokenDict['SEPERATOR'].keys():
        if token.value == "STARTASSIGNVARIABLE":
            substring = re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip().rstrip()
            if len(substring) > 0:
                argumentValue, argumentType = getArgument(['variable'], substring)
                if argumentValue is not None:
                    tokenlist.append(LToken('IDENTIFIER', argumentValue.rstrip(), line))
                    tokenlist.append(LToken('OPERATOR', '=', line))
                else:
                    errorList.append(ec.Error('Syntax Error', "Invalid argument \"{}\" on line {}".format(substring, line)))
            else:
                errorList.append(ec.Error('Syntax Error', "missing argument after \"{}\" on line {}".format(fileLine, line)))

    tokenlist.insert(0, token)
    next = readLine(file, line)
    return tokenlist + next[0], errorList + next[1]



def lex(filename : str):
    f = open(filename, "r")
    return readLine(f)
