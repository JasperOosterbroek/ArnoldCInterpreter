from typing import Any
TokenDict = {
    'OPERATOR': {
                    '-': "(GET DOWN)",
                    '+': "(GET UP)",
                    '=': "(YOU SET US UP)",
                    '*': "(YOU'RE FIRED)",
                    '/': "(HE HAD TO SPLIT)",
                    '>': "(LET OFF SOME STEAM BENNET)",
                    '%': "(I LET HIM GO)",
                    '==': "(YOU ARE NOT YOU YOU ARE ME)",
                    '||': "(CONSIDER THAT A DIVORCE)",
                    '&&': "(KNOCK KNOCK)"
                },
    'SEPERATOR': {'STARTASSIGNVARIABLE': "(GET TO THE CHOPPER)",
                    'ENDASSIGNVARIABLE': "(ENOUGH TALK)"},
    'STARTBLOCK': {
        'STARTWHILE': "(STICK AROUND)",
        'STARTMAIN': "(IT'S SHOWTIME)",
        'STARTIF': "(BECAUSE I'M GOING TO SAY PLEASE)",
        'STARTMETHOD': "(LISTEN TO ME VERY CAREFULLY)",
    },
    'ALTERNATIVEBLOCK':{
        'ELSE': "(BULLSHIT)",
        'ENDMETHODVARIABLES': "(GIVE THESE PEOPLE AIR)"
    },
    'ENDBLOCK':{
        'ENDWHILE': "(CHILL)",
        'ENDMAIN': "(YOU HAVE BEEN TERMINATED)",
        'ENDIF': "(YOU HAVE NO RESPECT FOR LOGIC)",
        'ENDMETHOD': "(HASTA LA VISTA, BABY)"
    },
    'IDENTIFIER': {'DECLERATION': "(HEY CHRISTMAS TREE)"},
    'METHOD':{
        'ASSIGNVARIABLE':"(GET YOUR ASS TO MARS)",
        'CALLMETHOD': "(DO IT NOW)",
        'METHODARGUMENT': "(I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE)",
        'RETURN' : "(I'LL BE BACK)"
    },
    'LITERAL': {'SETVALUE': "(HERE IS MY INVITATION)",
                'FALSE': "@NO PROBLEMO",
                'TRUE': "@I LIED"},
    'IO': {'PRINT': "TALK TO THE HAND"}
}


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
        Lines has been omitted with reasons against spamming the console, it is however usefull in error messages
        :return: Representable string of the token
        """
        return "Token( Type: {}, Value: {})".format(self.type, self.value)

    def __str__(self) -> str:
        return "Token: {}, {}".format(self.type, self.value)

