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
TokenDict = {
    'OPERATOR': {
                    '-': "(GET DOWN)",
                    '+': "(GET UP)",
                    '=': "(YOU SET US UP)"
                },
    'SOF': {'start': "(IT'S SHOWTIME)"},
    'EOF': {'end': "(YOU HAVE BEEN TERMINATED)"},
    'IDENTIFIER': {'INT': "(HEY CHRISTMAS TREE)"},
    'LITERAL': {'INT': "HERE IS MY INVITATION"}
}

class Token:

    def __init__(self, tType : str, tValue : Any) -> None:
        """
        Token constructor, constructs token.
        :param tType: Type of token, must be in enum TokenEnum,
        :param tValue: Value of the token, can be any type
        """
        self.type = tType
        self.value = tValue

    def __repr__(self) -> str:
        """
        String representation of the class instance, used for debugging
        :return: Representable string of the token
        """
        return "Token( Type: {}, Value: {})".format(self.type, self.value)

    def __str__(self) -> str:
        return "{}, {}".format(self.type, self.value)

