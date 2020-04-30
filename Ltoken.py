from enum import Enum
from typing import Any

# class TokenEnum(Enum):
#
#     OPERATOR =
#     EOF = {}
#     SOF = {}
#
#
#     def __new__(cls, index, content):
#         member = object.__new__(cls)
#         member.index = index
#         member.content = content
#         return member
#
#     def __int__(self):
#         return self.value
#


# literal is floatingin the aether :[
# keyword for if while, etc https://en.wikipedia.org/wiki/Lexical_analysis
TokenDict = {
    'OPERATOR': {
                    '-': "(GET DOWN)",
                    '+': "(GET UP)",
                    '=': "(YOU SET US UP)",
                    '*': "(YOU'RE FIRED)",
                    '/': "(HE HAD TO SPLIT)",
                    '>': "(LET OFF SOME STEAM BENNET)",
                    '%': "(I LET HIM GO)"
                },
    'SEPERATOR': {'STARTASSIGNVARIABLE': "(GET TO THE CHOPPER)",
                    'ENDASSIGNVARIABLE': "(ENOUGH TALK)"},
    'STARTBLOCK': {
        'STARTWHILE': "(STICK AROUND)"
    },
    'ENDBLOCK':{
        'ENDWHILE': "(CHILL)"
    },
    'SOF': {'start': "(IT'S SHOWTIME)"},
    'EOF': {'end': "(YOU HAVE BEEN TERMINATED)"},
    'IDENTIFIER': {'DECLERATION': "(HEY CHRISTMAS TREE)"},
    # for literals it's not so interesting what the 'value' is rather then
    # that it is a literal and what the actual value is
    'LITERAL': {'SETVALUE': "(HERE IS MY INVITATION)",
                'FALSE': "@NO PROBLEMO",
                'TRUE': "@I LIED"},
    'IO': {'PRINT': "TALK TO THE HAND"}
}


# name Ltoken to not conflict while debugging using pycharm, token is an stl class name
class LToken:

    def __init__(self, tType : str, tValue : Any, line : int) -> None:
        """
        Token constructor, constructs token.
        :param tType: Type of token, must be in enum TokenEnum,
        :param tValue: Value of the token, can be any type
        :param line: Line the token originated from, used for error logging
        """
        self.type = tType
        self.value = tValue
        self.line = line

    def __repr__(self) -> str:
        """
        String representation of the class instance, used for debugging
        :return: Representable string of the token
        """
        return "Token( Type: {}, Value: {})".format(self.type, self.value)

    def __str__(self) -> str:
        return "Token: {}, {}".format(self.type, self.value)

