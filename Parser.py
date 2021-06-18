from Tokens import Token
from Nodes import *
from Errors import InvalidSyntaxError
from Interpreter import *
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    def advance(self, amount=1):
        self.tok_idx += amount
        self.update_current_tok()
        return self.current_tok
    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok
    def update_current_tok(self):
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
    def parse(self):
        res = self.statements()
        if not res.error and not self.current_tok.matches(Token.TT_EOF):
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected int or float"
                )
            )
        return res
    def if_expr(self):
        res = ParseResult()
        cases = []
        
        if not self.current_tok.matches(Token.TT_KEYWORD, "if"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'if'"
            ))
        res.register_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        if res.should_return(): return res
        if self.current_tok.matches(Token.TT_NEWLINE):
            res.register_advancement()
            self.advance()
        statements = None
        if self.current_tok.matches(Token.TT_LBRAC):
            res.register_advancement()
            self.advance()
        
            statements = res.register(self.statements())
            if res.should_return(): return res
            cases.append((condition, statements))
            
            if not self.current_tok.matches(Token.TT_RBRAC):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '}'"
                ))
            res.register_advancement()
            self.advance()
            
        else:
            statements = res.register(self.expr())
            if res.should_return(): return res
            cases.append((condition, statements))
            if self.current_tok.matches(Token.TT_NEWLINE):
                res.register_advancement()
                self.advance()
            
        if self.current_tok.matches(Token.TT_KEYWORD, "else"):    
            res.register_advancement()
            self.advance()
            if self.current_tok.matches(Token.TT_NEWLINE):
                res.register_advancement()
                self.advance()
            if self.current_tok.matches(Token.TT_LBRAC):
                res.register_advancement()
                self.advance()
                else_case = res.register(self.statements())
                if res.should_return(): return res
                if not self.current_tok.matches(Token.TT_RBRAC):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected '}'"
                    ))
                res.register_advancement()
                self.advance()
                return res.success(IfNode(cases, else_case))
                
            elif self.current_tok.matches(Token.TT_KEYWORD, "if"):
                if_expr = res.register(self.if_expr())
                if res.should_return(): return res
                for i in range(len(if_expr.cases)):
                    cases.append(if_expr.cases[i])
                return res.success(IfNode(cases, if_expr.else_case))
             
            else_case = res.try_register(self.expr())
            if not else_case:
                self.reverse(res.to_reverse_count)
            return res.success(IfNode(cases, else_case))
        return res.success(IfNode(cases, None))
    def for_expr(self):
        res = ParseResult()
        if not self.current_tok.matches(Token.TT_KEYWORD, "for"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'for'"
            ))
        res.register_advancement()
        self.advance()
        
        if not self.current_tok.matches(Token.TT_IDENTIFIER):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))
        var_name = self.current_tok
        res.register_advancement()
        self.advance()
        if not self.current_tok.matches(Token.TT_EQ):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '='"
            ))
        res.register_advancement()
        self.advance()
        
        start_value = res.register(self.expr())
        if res.should_return(): return res
        
        if not self.current_tok.matches(Token.TT_KEYWORD, "to"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'to'"
            ))
        res.register_advancement()
        self.advance()
        
        end_value = res.register(self.expr())
        if res.should_return(): return res
        
        if self.current_tok.matches(Token.TT_KEYWORD, "step"):
            res.register_advancement()
            self.advance()
            step_value = res.register(self.expr())
            if res.should_return(): return res
        else:
            step_value = None
        
        if not self.current_tok.matches(Token.TT_LBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))
        res.register_advancement()
        self.advance()
        
        body_node = res.register(self.statements())
        if res.should_return(): return res
        
        if not self.current_tok.matches(Token.TT_RBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))
        res.register_advancement()
        self.advance()
        
        return res.success(ForNode(var_name, start_value, end_value, step_value, body_node))
        
    def while_expr(self):
        res = ParseResult()
        if not self.current_tok.matches(Token.TT_KEYWORD, "while"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'while'"
            ))
        res.register_advancement()
        self.advance()
        
        condition = res.register(self.expr())
        if res.should_return(): return res
        
        if not self.current_tok.matches(Token.TT_LBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))
        res.register_advancement()
        self.advance()
        
        body_node = res.register(self.statements())
        if res.should_return(): return res
        
        if not self.current_tok.matches(Token.TT_RBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))
        res.register_advancement()
        self.advance()
        
        return res.success(WhileNode(condition, body_node))
    def func_def(self):
        res = ParseResult()
        if not self.current_tok.matches(Token.TT_KEYWORD, "function"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'function'"
            ))
        res.register_advancement()
        self.advance()
         
        if self.current_tok.matches(Token.TT_IDENTIFIER):
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            
            if not self.current_tok.matches(Token.TT_LPAREN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '('"
                ))
        else:
            var_name_tok = None
            if not self.current_tok.matches(Token.TT_LPAREN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or '('"
                ))
        res.register_advancement()
        self.advance()
        
        args_name_toks = []
        
        if self.current_tok.matches(Token.TT_IDENTIFIER):
            args_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            
            while self.current_tok.matches(Token.TT_COMMA):
                res.register_advancement()
                self.advance()
                
                if not self.current_tok.matches(Token.TT_IDENTIFIER):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))
                args_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
            if not self.current_tok.matches(Token.TT_RPAREN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ')'"
                ))
        else:
            if not self.current_tok.matches(Token.TT_RPAREN):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or ')'"
                ))
        res.register_advancement()
        self.advance()
        if not self.current_tok.matches(Token.TT_LBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))
        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.statements())
        if res.should_return(): return res
        if not self.current_tok.matches(Token.TT_RBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))
        res.register_advancement()
        self.advance()
        return res.success(FuncDefNode(var_name_tok, args_name_toks, node_to_return, False))
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()
        if not self.current_tok.matches(Token.TT_LSQUARE):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))
        res.register_advancement()
        self.advance()
        
        if self.current_tok.matches(Token.TT_RSQUARE):
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.should_return():
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "']', int, float, identifier, 'let', 'if', 'for', 'while', 'function', '+', '-', or '('" + res.error.details
                ))
            while self.current_tok.matches(Token.TT_COMMA):
                res.register_advancement()
                self.advance()
                element_nodes.append(res.register(self.expr()))
                if res.should_return(): return res
            if not self.current_tok.matches(Token.TT_RSQUARE):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))
            res.register_advancement()
            self.advance()
        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end))
    def list_acc_expr(self):
        res = ParseResult()
        if not self.current_tok.matches(Token.TT_IDENTIFIER):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))
        tok = self.current_tok
        res.register_advancement()
        self.advance()
        if self.current_tok.matches(Token.TT_LSQUARE):
            res.register_advancement()
            self.advance()
            pos_expr = res.register(self.expr())
            if res.should_return(): return res
            if not self.current_tok.matches(Token.TT_RSQUARE):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']'"
                ))
            res.register_advancement()
            self.advance()
            return res.success(ListAccessNode(tok, pos_expr))
        elif self.current_tok.matches(Token.TT_DOT):
            res.register_advancement()
            self.advance()
            if not self.current_tok.matches(Token.TT_IDENTIFIER):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))
            access_tok = StringNode(self.current_tok)
            res.register_advancement()
            self.advance()
            return res.success(ListAccessNode(tok, access_tok))
        return res.success(VarAccessNode(tok))
    def dict_expr(self):
        res = ParseResult()
        dictionary = {}
        pos_start = self.current_tok.pos_start.copy()
        if not self.current_tok.matches(Token.TT_LBRAC):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))
        res.register_advancement()
        self.advance()
        
        if self.current_tok.matches(Token.TT_RBRAC):
            res.register_advancement()
            self.advance()
        else:
            while self.current_tok.matches(Token.TT_NEWLINE):
                res.register_advancement()
                self.advance()
            atom = res.register(self.atom())
            if not self.current_tok.matches(Token.TT_COLON):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "':'"
                ))
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.should_return():
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "']', int, float, identifier, 'let', 'if', 'for', 'while', 'function', '+', '-', or '('" + res.error.details
                ))
            dictionary[atom.tok.value] = expr
            while self.current_tok.matches(Token.TT_COMMA):
                res.register_advancement()
                self.advance()
                while self.current_tok.matches(Token.TT_NEWLINE):
                    res.register_advancement()
                    self.advance()
                atom = res.register(self.atom())
                if not self.current_tok.matches(Token.TT_COLON):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "':'"
                    ))
                res.register_advancement()
                self.advance()
                expr = res.register(self.expr())
                if res.should_return():
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "']', int, float, identifier, 'let', 'if', 'for', 'while', 'function', '+', '-', or '('" + res.error.details
                    ))
                dictionary[atom.tok.value] = expr
            while self.current_tok.matches(Token.TT_NEWLINE):
                res.register_advancement()
                self.advance()
            if not self.current_tok.matches(Token.TT_RBRAC):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    " ',' or '}'"
                ))
            res.register_advancement()
            self.advance()
        return res.success(DictNode(dictionary, pos_start, self.current_tok.pos_end))
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type in (Token.TT_INT, Token.TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.matches(Token.TT_STRING):
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))
        elif tok.matches(Token.TT_IDENTIFIER):
            list_acc_expr = res.register(self.list_acc_expr())
            if res.should_return(): return res
            return res.success(list_acc_expr)
        
        
        elif tok.matches(Token.TT_LPAREN):
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.should_return(): return res
            if self.current_tok.matches(Token.TT_RPAREN):
                res.register_advancement()
                self.advance()        
                return res.success(expr)
            else:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'"
                    )
                )
        elif tok.matches(Token.TT_LSQUARE):
            list_expr = res.register(self.list_expr())
            if res.should_return(): return res
            return res.success(list_expr)
        elif tok.matches(Token.TT_LBRAC):
            dict_expr = res.register(self.dict_expr())
            if res.should_return(): return res
            return res.success(dict_expr)
        elif tok.matches(Token.TT_KEYWORD, "if"):
            if_expr = res.register(self.if_expr())
            if res.should_return(): return res
            return res.success(if_expr)
        elif tok.matches(Token.TT_KEYWORD, "for"):
            for_expr = res.register(self.for_expr())
            if res.should_return(): return res
            return res.success(for_expr)
        elif tok.matches(Token.TT_KEYWORD, "while"):
            while_expr = res.register(self.while_expr())
            if res.should_return(): return res
            return res.success(while_expr)
        elif tok.matches(Token.TT_KEYWORD, "function"):
            func_def = res.register(self.func_def())
            if res.should_return(): return res
            return res.success(func_def)
            
        return res.failure(
            InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', or '('"
            )
        )
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.should_return(): return res
        
        if self.current_tok.matches(Token.TT_LPAREN):
            res.register_advancement()
            self.advance()
            arg_nodes = []
            if self.current_tok.matches(Token.TT_RPAREN):
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.should_return():
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "')', int, float, identifier, 'let', 'if', 'for', 'while', 'function', '+', '-', or '('" + res.error.details
                    ))
                while self.current_tok.matches(Token.TT_COMMA):
                    res.register_advancement()
                    self.advance()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
                if not self.current_tok.matches(Token.TT_RPAREN):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "',' or ')'"
                    ))
                res.register_advancement()
                self.advance()
            return res.success(CallFuncNode(atom, arg_nodes))
        return res.success(atom)
                
    def power(self):
        return self.bin_op(self.call, (Token.TT_POW, ), self.factor)
        
    def dice(self):
        res = ParseResult()
        if self.current_tok.matches(Token.TT_DICE):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(self.factor())
            if res.error: return res
            return res.success(BinOpNode(NumberNode(Token(Token.TT_INT, 1, op_tok.pos_start, op_tok.pos_end)), op_tok, right))
        return self.bin_op(self.power, (Token.TT_DICE, ), self.factor)
    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (Token.TT_PLUS, Token.TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        return self.dice()
        
    def term(self):
        return self.bin_op(self.factor, (Token.TT_MUL, Token.TT_DIV, Token.TT_MOD))
    def arith_expr(self):
        return self.bin_op(self.term, (Token.TT_PLUS, Token.TT_MINUS))
    def comp_expr(self):
        res = ParseResult()
        if self.current_tok.matches(Token.TT_KEYWORD, "not"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            
            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        node = res.register(self.bin_op(self.arith_expr, (Token.TT_EE, Token.TT_NE, Token.TT_LT, Token.TT_GT, Token.TT_LTE, Token.TT_GTE)))
        if res.error: 
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "int, float, identifier, '+', '-', '(', or 'not'" + res.error.details
            ))
        return res.success(node)
    def expr(self):
        res = ParseResult()
        if self.current_tok.matches(Token.TT_KEYWORD, "let"):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != Token.TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "an identifier"
                ))
            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            
            if self.current_tok.type != Token.TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "'='"
                ))
            res.register_advancement()
            self.advance()
            
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))
        elif self.current_tok.matches(Token.TT_IDENTIFIER):
            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            access_tok = None
            reverse_count = 1
            #START
            if self.current_tok.matches(Token.TT_LSQUARE):
                res.register_advancement()
                self.advance()
                reverse_count += 1
                save_pos = res.advance_count
                access_tok = res.try_register(self.expr())
                reverse_count += (res.advance_count - save_pos)
                if res.should_return(): return res
                if not self.current_tok.matches(Token.TT_RSQUARE):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ']'"
                    ))
                res.register_advancement()
                self.advance()
                reverse_count += 1
            elif self.current_tok.matches(Token.TT_DOT):
                res.register_advancement()
                self.advance()
                reverse_count += 1
                if not self.current_tok.matches(Token.TT_IDENTIFIER):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))
                access_tok = StringNode(self.current_tok)
                res.register_advancement()
                self.advance()
                reverse_count += 1
            #END
            if self.current_tok.type in (Token.TT_EQ, Token.TT_PLUSEQ):
                op_tok = self.current_tok
                res.register_advancement()
                self.advance()
                
                expr = res.try_register(self.expr())
                if res.error: return res
                if access_tok != None:
                    return res.success(ListReassignNode(var_name, access_tok, op_tok, expr))
                return res.success(VarReassignNode(var_name, op_tok, expr))
            res.register_reverse()
            self.reverse(reverse_count)
        node =  res.register(self.bin_op(self.comp_expr, ((Token.TT_KEYWORD, "and"),(Token.TT_KEYWORD, "or"))))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "int, float, identifier, 'let', 'if', 'for', 'while', 'function', '+', '-', or '('"
            ))
        return res.success(node)
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        if self.current_tok.matches(Token.TT_KEYWORD, "return"):
            res.register_advancement()
            self.advance()
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_end))
        elif self.current_tok.matches(Token.TT_KEYWORD, "continue"):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_end))
        elif self.current_tok.matches(Token.TT_KEYWORD, "break"):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_end))
        expr = res.register(self.expr())
        if res.should_return():
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_start,
                "'Return', " + res.error.details
            ))
        return res.success(expr)
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()
        while self.current_tok.matches(Token.TT_NEWLINE):
            res.register_advancement()
            self.advance()
        statement = res.register(self.statement())
        if res.should_return(): return res
        statements.append(statement)
        more_statements = True
        while True:
            new_line_count = 0
            while self.current_tok.matches(Token.TT_NEWLINE):
                res.register_advancement()
                self.advance()
                new_line_count += 1
            if new_line_count == 0:
                more_statements = False
            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            if statement != Number.null:
                statements.append(statement)
        return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))
    def bin_op(self, func_a, ops, func_b=None):
        if (func_b == None):
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.should_return(): return res
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.should_return(): return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)

class ParseResult():
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0
    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1
    def register_reverse(self):
        self.last_registered_advance_count = -1
        self.advance_count -= 1
    def try_register(self, res):
        if res.error: 
            self.to_reverse_count = res.advance_count
            return None
        else:
            return self.register(res)
    def success(self, node):
        self.node = node
        return self
    def should_return(self):
        return True if self.error else False
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
