import re
from Ltoken import TokenDict, LToken
import errorClass as ec
from typing import List, Sequence, TypeVar, Union, Tuple, Dict, IO

T = TypeVar('T')
def listNoneCheck(checkList: List[T], count: int = 0)-> Union[T, None]:
    """
    Returns the first instance of an item in the list that is not None or None if every item in the list is None
    :param checkList: The list we check for not None items
    :param count: The current index where we are searching
    :return: The first instance of an item in the list that is not None or None of all are None
    """
    if count == len(checkList):
        return None
    if checkList[count] == None:
        return listNoneCheck(checkList, count+1)
    else:
        return checkList[count]

def tokenRegex(fileLine: str, regexDict: Tuple[str, str])-> Union[None, str]:
    """
    Uses regex to check what type of token is used
    :param fileLine: Current line of the file to check for the regex
    :param regexDict: A tuple of dictionary item to get the regex from
    :return: None or the name of the found token
    """
    if re.match(regexDict[1], fileLine) is not None:
        return regexDict[0]
    else:
        return None


def getTokenType(fileLine: str, tokenDict: Dict[str,List[str]], lineNum: int)-> Union[None, LToken]: #object == Ltoken
    """
    Returns the type of the token from the current fileLine if any else return None
    :param fileLine: current line of the executed file
    :param tokenDict: dictionary containing all the possible tokens of a certain type
    :param lineNum: current line number added to Ltoken for error reporting possibilities
    :return:
    """
    tokenr = listNoneCheck(list(map(lambda x: tokenRegex(fileLine, x), tokenDict[1].items())))
    if tokenr is not None:
        return LToken(tokenDict[0], tokenr, lineNum)
    else:
        return None


def getArgument(types: list, string: str, count: int = 0) -> Union[Tuple[str, str], Tuple[None,None]]:
    """
    Returns the argument after a certain statement if any else return None, None
    :param types: The possible options of types the string could contain
    :param string: String to check for arguments
    :param count: current index of typelist
    :return: None,None if no argument was found else the argument type and value of the argument
    """
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
            return string[1:-1], types[count]  # remove " from string

    return getArgument(types, string, count+1)

expectedArguments = {
    'OPERATOR': ['int', 'variable'],
    'IO': ['variable', 'int', 'string'],
    'LITERAL': ['int', 'variable'],
    'STARTWHILE': ['int', 'variable'],
    'IDENTIFIER': ['variable'],
    'STARTIF': ['int', 'variable'],
    'ASSIGNVARIABLE': ['variable'],
    'ASSIGNMETHODDARGUMENT': ['variable'],
    'STARTMETHOD': ['variable'],
    'METHODARGUMENT': ['variable'],
    'RETURN':['variable', 'int']
}

def readLine(fileList: List[str], line: int = 0)->Tuple[List[LToken], List[str]]:
    """
    Reads the current fileLine from a file and determines if it a valid token for the parser.
    If the token should have an argument it will add this as another token to the list
    :param file: current file we are reading
    :param line: the linenumber we are on (for debugging mostly)
    :return: returns a tuple of two lists the first list contains the tokens the second list contains errors if any
    """
    if line == len(fileList):
        return ([LToken('ENDOFFILE', None, line+1)], [])

    fileLine = fileList[line].rstrip()
    if fileLine == "":
        line += 1
        next = readLine(fileList, line)
        return next[0], next[1]
    tokenTypeList = list(map(lambda x: getTokenType(fileLine, x, line), TokenDict.items()))
    line += 1
    token = listNoneCheck(tokenTypeList)
    tokenlist = []
    errorList = []

    if token is None:
        errorList.append(ec.SyntaxError("Invalid syntax {} on line {}".format(fileLine, line+1)))
    elif token.value in TokenDict[token.type].keys() and (token.type in expectedArguments or token.value in expectedArguments):
        substring = re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip().rstrip()
        if len(substring) > 0:
            if token.type in expectedArguments:
                argumentValue, argumentType = getArgument(expectedArguments[token.type], substring)
            elif token.value in expectedArguments:
                argumentValue, argumentType = getArgument(expectedArguments[token.value], substring)
            if argumentValue is not None:
                if token.value == 'DECLERATION' or token.type == 'LITERAL' or token.value == 'STARTMETHOD' or token.value == 'METHODARGUMENT':
                    if token.value == 'DECLERATION' or token.value == 'STARTMETHOD' or token.value == 'METHODARGUMENT':
                        token.type = token.value
                    token.value = argumentValue
                elif token.value == 'STARTASSIGNVARIABLE' or token.value == "ASSIGNVARIABLE":
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
                errorList.append(ec.SyntaxError("Invalid argument \"{}\" on line {}".format(substring, line)))
        else:
            errorList.append(ec.SyntaxError("missing argument after \"{}\" on line {}".format(fileLine, line)))
    elif token.value in TokenDict['SEPERATOR'].keys():
        if token.value == "STARTASSIGNVARIABLE":
            substring = re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip().rstrip()
            if len(substring) > 0:
                argumentValue, argumentType = getArgument(['variable'], substring)
                if argumentValue is not None:
                    tokenlist.append(LToken('IDENTIFIER', argumentValue.rstrip(), line))
                    tokenlist.append(LToken('OPERATOR', '=', line))
                else:
                    errorList.append(ec.SyntaxError("Invalid argument \"{}\" on line {}".format(substring, line)))
            else:
                errorList.append(ec.SyntaxError("missing argument after \"{}\" on line {}".format(fileLine, line)))
    elif token.value in TokenDict['METHOD'].keys():
        substring = re.sub(TokenDict[token.type][token.value], '', fileLine).lstrip().rstrip()
        arguments = re.findall('[a-zA-Z][\\w]*|-?[0-9]*', substring)
        tokens = list(map(lambda x: LToken('ASSIGNMETHODDARGUMENT', x, line), filter(None, arguments)))
        tokens[0].type = 'METHODNAME'
        tokenlist += tokens
        tokenlist.append(LToken('METHOD', 'ENDMETHODCALL', line))
        # altijd minimaal 1 argument (method call) , en x aantal argumenten (method arguments) waar x 0 kan zijn
    tokenlist.insert(0, token)
    next = readLine(fileList, line)
    return tokenlist + next[0], errorList + next[1]



def lex(filename : str):
    """
    Lexes the file of the given filename
    :param filename: the name of the file
    :return: A tuple of list containing the tokens and errors given bij the readLine function
    """
    # f = open(filename, "r")
    return readLine(filename)
