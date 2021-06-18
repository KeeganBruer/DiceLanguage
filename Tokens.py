#####################
# TOKENS CLASS
#####################
class Token():
    TT_INT          = "TT_INT"
    TT_FLOAT        = "TT_FLOAT"
    TT_STRING       = "TT_STRING"
    TT_IDENTIFIER   = "TT_IDENTIFIER"
    TT_KEYWORD      = "TT_KEYWORD"
    TT_DICE         = "TT_DICE"
    TT_PLUS         = "TT_PLUS"
    TT_MINUS        = "TT_MINUS"
    TT_MUL          = "TT_MUL"
    TT_DIV          = "TT_DIV"
    TT_MOD          = "TT_MOD"
    TT_POW          = "TT_POW"
    TT_EQ           = "TT_EQ"
    TT_PLUSEQ       = "TT_PLUSEQ"
    TT_EE           = "TT_EE"
    TT_NE           = "TT_NE"
    TT_LT           = "TT_LT"
    TT_GT           = "TT_GT"
    TT_LTE          = "TT_LTE"
    TT_GTE          = "TT_GTE"
    TT_LPAREN       = "TT_LPAREN"
    TT_RPAREN       = "TT_RPAREN"
    TT_LBRAC        = "TT_LBRAC"
    TT_RBRAC        = "TT_RBRAC"
    TT_LSQUARE      = "TT_LSQUARE"
    TT_RSQUARE      = "TT_RSQUARE"
    TT_COMMA        = "TT_COMMA"
    TT_DOT          = "TT_DOT"
    TT_COLON        = "TT_COLON"
    TT_ARROW        = "TT_ARROW"
    TT_NEWLINE      = "TT_NEWLINE"
    TT_EOF          = "TT_EOF"
    KEYWORDS        = [
        "let",
        "not",
        "and",
        "or",
        "if",
        "else",
        "for",
        "while",
        "to",
        "step",
        "function",
        "return",
        "continue",
        "break"
    ]
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end.copy()
    def matches(self, type_, value=None):
        if value == None:
            return self.type == type_
        return self.type == type_ and self.value == value
    def __repr__(self):
        if (self.value):
            return "{0}:{1}".format(self.type, self.value)
        return "{0}".format(self.type)

