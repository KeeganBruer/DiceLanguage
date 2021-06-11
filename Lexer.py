from Tokens import Token
from Errors import *
import string
class Position():
    def __init__(self, idx, line, col, fn, ftext):
        self.idx = idx
        self.line = line
        self.col = col
        self.fn = fn
        self.ftext = ftext
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == "\n":
            self.line += 1
            self.col = 0
        return self
    def reverse(self, current_char=None):
        self.idx -= 1
        self.col -= 1
        if current_char == "\n":
            self.line -= 1
            self.col = 0
        return self
    def copy(self):
        return Position(self.idx, self.line, self.col, self.fn, self.ftext)

class Lexer():
    DIGITS = "0123456789"
    LETTERS = string.ascii_letters
    LETTERS_DIGITS = LETTERS + DIGITS
    def __init__(self, fn, text):
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    def reverse(self):
        self.pos.reverse(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    def make_tokens(self):
        tokens = []
        self.advance()
        while self.current_char != None:
            #If the current char is a space tab or newline, skip it
            if self.current_char in " \t":
                self.advance()
                
            #Create a new token based on the current character
            elif self.current_char in ";\n":
                tokens.append(Token(Token.TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in self.DIGITS:
                token, error = self.make_number()
                if error: return [], error
                tokens.append(token)
            elif self.current_char in self.LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == "\"":
                tokens.append(self.make_string())
            elif self.current_char == "+":
                tokens.append(self.make_plus())
            elif self.current_char == "-":
                tokens.append(Token(Token.TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(Token.TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(Token.TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "%":
                tokens.append(Token(Token.TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(Token.TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(Token.TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(Token.TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == "[":
                tokens.append(Token(Token.TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(Token.TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == "{":
                tokens.append(Token(Token.TT_LBRAC, pos_start=self.pos))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(Token.TT_RBRAC, pos_start=self.pos))
                self.advance()
            elif self.current_char == ",":
                tokens.append(Token(Token.TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == ":":
                tokens.append(Token(Token.TT_COLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == "=":
                tokens.append(self.make_equals_or_arrow())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            else:
                #If a token cannot be created from the current input, return an error
                cur_char = self.current_char
                start_pos = self.pos
                self.advance()
                return [], IllegalCharError(start_pos, self.pos, "\"{0}\"".format(cur_char))
            
        tokens.append(Token(Token.TT_EOF, pos_start=self.pos))
        return tokens, None
    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()
        #While it is not end of input and the char is a digit or a period
        while self.current_char != None and self.current_char in self.DIGITS + ".":
            if self.current_char == ".":
                if dot_count > 0: #If more than one dot, it is not an number anymore
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:#No dots is a integer
            return Token(Token.TT_INT, int(num_str), pos_start, self.pos), None
        else:# One dot is a float
            return Token(Token.TT_FLOAT, float(num_str), pos_start, self.pos), None
    def make_string(self):
        string = ""
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()
        escape_characters = {
            "t":"\t",
            "n":"\n"
        }
        while self.current_char != None and (self.current_char != "\"" or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == "\\":
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
            
        self.advance()
        return Token(Token.TT_STRING, string, pos_start, self.pos)
    def make_plus(self):
        tok_type = Token.TT_PLUS
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type =  Token.TT_PLUSEQ
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()
        
        while self.current_char != None and self.current_char in self.LETTERS_DIGITS + "_":
            id_str += self.current_char
            if self.current_char == "d":
                self.advance()
                if self.current_char in self.DIGITS:
                    #self.reverse()
                    return Token(Token.TT_DICE, pos_start=pos_start, pos_end=self.pos)
            else:
                self.advance()
        tok_type = Token.TT_KEYWORD if id_str in Token.KEYWORDS else Token.TT_IDENTIFIER
        
        return Token(tok_type, id_str, pos_start, self.pos)
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            return Token(Token.TT_NE, pos_start=pos_start, pos_end=self.pos), None
        self.advance()
        return None, ExpectedCharError(
            pos_start, self.pos,
            "Expected an '=' after an '!'"
        )
    def make_equals_or_arrow(self):
        tok_type = Token.TT_EQ
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type =  Token.TT_EE
        elif self.current_char == '>':
            self.advance()
            tok_type =  Token.TT_ARROW
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_less_than(self):
        tok_type = Token.TT_LT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type =  Token.TT_LTE
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_greater_than(self):
        tok_type = Token.TT_GT
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            tok_type =  Token.TT_GTE
            
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
