from Tokens import Token
class Node:
    def __init__(self):
        pass
    def __repr__(self):
        return "(<{0}>)".format(type(self).__name__)

class NumberNode(Node):
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self):
        return "({0})".format(self.tok)
class StringNode(Node):
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self):
        return "({0})".format(self.tok)
        
class ListNode(Node):
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
        return "([{0}])".format(", ".join([str(x) for x in self.element_nodes]))
        
class DictNode(Node):
    def __init__(self, dictionary, pos_start, pos_end):
        self.dictionary = dictionary
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
        res = ""
        for key in self.dictionary:
            res += str(key)
            res += " : "
            res += str(self.dictionary[key]) 
        return "({" + res + "})"
  
class ListAccessNode(Node):
    def __init__(self, var_name_tok, pos_tok):
        self.var_name_tok = var_name_tok
        self.pos_tok = pos_tok
        
        self.pos_start = var_name_tok.pos_start
        self.pos_end = var_name_tok.pos_end
        
class VarAccessNode(Node):
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        
        self.pos_start = var_name_tok.pos_start
        self.pos_end = var_name_tok.pos_end
class VarAssignNode(Node):
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.pos_start = var_name_tok.pos_start
        self.pos_end = value_node.pos_end
class VarReassignNode(Node):
    def __init__(self, var_name_tok, op_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.op_tok = op_tok
        self.pos_start = var_name_tok.pos_start
        self.pos_end = value_node.pos_end

class BinOpNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.right_node = right_node
        self.op_tok = op_tok
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end
    def __repr__(self):
        return "({0} {1} {2})".format(self.left_node, self.op_tok, self.right_node)
class UnaryOpNode(Node):
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end
    def __repr__(self):
        return "({0} {1})".format(self.op_tok, self.node)
        
class IfNode(Node):
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = cases[0][0].pos_start
        self.pos_end = (else_case or cases[len(cases)-1][0]).pos_end
    
class ForNode(Node):
    def __init__(self, var_name, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name = var_name
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        
        self.pos_start = self.var_name.pos_start
        self.pos_end = self.body_node.pos_end
class WhileNode(Node):
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.pos_start = condition_node.pos_start
        self.pos_end = body_node.pos_end
        
class FuncDefNode(Node):
    def __init__(self, var_name_tok, args_name_toks, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.args_name_toks = args_name_toks
        self.body_node = body_node
        self.should_auto_return = should_auto_return
        
        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.args_name_toks) > 0:
            self.pos_start = self.args_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start
        self.pos_end = self.body_node.pos_end
        
class CallFuncNode(Node):
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
        
        self.pos_start = self.node_to_call.pos_start
        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes)-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
class ReturnNode(Node):
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return
        self.pos_start = pos_start
        self.pos_end = pos_end
class ContinueNode(Node):
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end
class BreakNode(Node):
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end


















