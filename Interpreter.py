from Nodes import *
from Tokens import Token
from Errors import RTError
from Context import *
import os
import random
class Interpreter():
    def __init__(self):
        self.test_id = 0
    def visit(self, node, context):
        method_name = "visit_{0}".format(type(node).__name__)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception("No Visit_{0} method defined".format(type(node).__name__))

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                "'{0}' is not defined".format(var_name),
                context
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    def visit_ListAccessNode(self, node, context):
        res = RTResult()
        if isinstance(node.var_name_tok, ListAccessNode):
            var_name = res.register(self.visit(node.var_name_tok, context))
        else:
            var_name = node.var_name_tok.value
        if isinstance(var_name, List) or isinstance(var_name, Dict):
            access_pos = res.register(self.visit(node.pos_tok, context))
            value, error = var_name.get(access_pos)
            if error: return res.failure(error)
            value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        else:
            value = context.symbol_table.get(var_name)
            if not value:
                return res.failure(RTError(
                    node.pos_start, node.pos_end,
                    "'{0}' is not defined".format(var_name),
                    context
                ))
            access_pos = res.register(self.visit(node.pos_tok, context))
            value, error = value.get(access_pos)
            if error: return res.failure(error)
            value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    def visit_DictAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                "'{0}' is not defined".format(var_name),
                context
            ))
        access_pos = String(node.access_tok.value)
        value, error = value.get(access_pos)
        if error: return res.failure(error)
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res
        var_exist = context.symbol_table.get(var_name, True)
        if var_exist:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                "{0} has already been defined".format(var_name),
                context
            ))
        context.symbol_table.set(var_name, value)
        return res.success(Number.null)
    def visit_VarReassignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res
        var_exist = context.symbol_table.get(var_name)
        if not var_exist:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                "{0} has not yet been defined".format(var_name),
                context
            ))
        new_value = value
        if node.op_tok.matches(Token.TT_PLUSEQ):
            new_value = var_exist
            new_value.added_to(value)
        context.symbol_table.set(var_name, new_value, True)
        return res.success(Number.null)
    def visit_ListReassignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res
        var_exist = context.symbol_table.get(var_name)
        if not var_exist:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                "{0} has not yet been defined".format(var_name),
                context
            ))
        access_val = res.register(self.visit(node.access_tok, context))
        new_value = var_exist
        if node.op_tok.matches(Token.TT_PLUSEQ):
            old_value = var_exist.get(access_val)
            new_value.set(access_val, old_value[0].added_to(value)[0])
        else:
            new_value.set(access_val, value)
        context.symbol_table.set(var_name, new_value, True)
        return res.success(Number.null)
        
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res
        result, error = None, None
        if node.op_tok.matches(Token.TT_DICE):
            result, error = left.roll_die(right)
        elif node.op_tok.matches(Token.TT_PLUS):
            result, error = left.added_to(right)
        elif node.op_tok.matches(Token.TT_MINUS):
            result, error = left.subbed_by(right)
        elif node.op_tok.matches(Token.TT_MUL):
            result, error = left.multed_by(right)
        elif node.op_tok.matches(Token.TT_DIV):
            result, error = left.dived_by(right)
        elif node.op_tok.matches(Token.TT_MOD):
            result, error = left.modded_by(right)
        elif node.op_tok.matches(Token.TT_POW):
            result, error = left.power_by(right)
        elif node.op_tok.matches(Token.TT_EE):
            result, error = left.comparison_eq(right)
        elif node.op_tok.matches(Token.TT_NE):
            result, error = left.comparison_ne(right)
        elif node.op_tok.matches(Token.TT_LT):
            result, error = left.comparison_lt(right)
        elif node.op_tok.matches(Token.TT_GT):
            result, error = left.comparison_gt(right)
        elif node.op_tok.matches(Token.TT_LTE):
            result, error = left.comparison_lte(right)
        elif node.op_tok.matches(Token.TT_GTE):
            result, error = left.comparison_gte(right)
        elif node.op_tok.matches(Token.TT_KEYWORD, "and"):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(Token.TT_KEYWORD, "or"):
            result, error = left.ored_by(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        error = None
        number = res.register(self.visit(node.node, context))
        if node.op_tok.matches(Token.TT_MINUS):
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(Token.TT_KEYWORD, "not"):
            number, error = number.notted()
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
            
    def visit_IfNode(self, node, context):
        res = RTResult()
        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res
            
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(expr_value)
        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.should_return(): return res
            return res.success(else_value)
        return res.success(None)
    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []
        
        
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res
        
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res
        
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
        else:
            step_value = Number(1)
        i = start_value.value
        
        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value
        
        while condition():
            new_context = Context("<for>", context, node.pos_start)
            new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
            new_context.symbol_table.set(node.var_name.value, Number(i))
            i += step_value.value
            
            value = res.register(self.visit(node.body_node, new_context))
            
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
            
            if res.loop_should_continue:
                continue
            if res.loop_should_break:
                break

            if value != Number.null:
                elements.append(value)

        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []
        while True:
            new_context = Context("<while>", context, node.pos_start)
            new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
            condition = res.register(self.visit(node.condition_node, new_context))
            if res.should_return(): return res
            
            if not condition.is_true(): break
            
            value = res.register(self.visit(node.body_node, new_context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
            
            if res.loop_should_continue:
                continue
            if res.loop_should_break:
                break
            
            elements.append(value)
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
        
    def visit_FuncDefNode(self, node, context):
        res = RTResult()
        if context.parent:
            print(context.symbol_table)
        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.args_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return)
        func_value = func_value.set_context(context)
        func_value = func_value.set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)
        return res.success(func_value)
    def visit_CallFuncNode(self, node, context):
        res = RTResult()
        args = []
        
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res
        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)
    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []
        
        for element_node in node.element_nodes:
            element = res.register(self.visit(element_node, context))
            if res.should_return(): return res
            if element != Number.null:
                elements.append(element)
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_DictNode(self, node, context):
        res = RTResult()
        elements = {}
        
        for key in node.dictionary:
            elements[key] = res.register(self.visit(node.dictionary[key], context))
            if res.should_return(): return res
        return res.success(Dict(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_ReturnNode(self, node, context):
        res = RTResult()
        
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null
            
        return res.success_return(value)
    def visit_ContinueNode(self, node, context):
        res = RTResult()
        return res.success_continue()
    def visit_BreakNode(self, node, context):
        res = RTResult()
        return res.success_break()

class RTResult():
    def __init__(self):
        self.reset()
    def reset(self):
        self.value = None
        self.error = None
        self.func_rtn_value = None
        self.loop_should_continue = False
        self.loop_should_break = False
    def register(self, res):
        self.error = res.error
        self.func_rtn_value = res.func_rtn_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value
    def success(self, value):
        self.reset()
        self.value = value
        return self
    def success_return(self, value):
        self.reset()
        self.func_rtn_value = value
        return self
    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self
    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self
    def failure(self, error):
        self.reset()
        self.error = error
        return self
    def should_return(self):
        return (
            self.error or
            self.func_rtn_value or
            self.loop_should_continue or
            self.loop_should_break
        )

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    def set_context(self, context=None):
        self.context = context
        return self
    def __repr__(self):
        return "{0}".format(self.value)
    
    
    def added_to(self, other):
        return None, self.illegal_operation(other)
    def subbed_by(self, other):
        return None, self.illegal_operation(other)
    def multed_by(self, other):
        return None, self.illegal_operation(other)
    def dived_by(self, other):
        return None, self.illegal_operation(other)
    def modded_by(self, other):
        return None, self.illegal_operation(other)
    def power_by(self, other):
        return None, self.illegal_operation(other)
    def comparison_eq(self, other):
        return None, self.illegal_operation(other)
    def comparison_ne(self, other):
        return None, self.illegal_operation(other)
    def comparison_lt(self, other):
        return None, self.illegal_operation(other)
    def comparison_gt(self, other):
        return None, self.illegal_operation(other)
    def comparison_lte(self, other):
        return None, self.illegal_operation(other)
    def comparison_gte(self, other):
        return None, self.illegal_operation(other)
    def anded_by(self, other):
        return None, self.illegal_operation(other)
    def ored_by(self, other):
        return None, self.illegal_operation(other)
    def notted(self):
        return None, self.illegal_operation(other)
    def is_true(self):
        return None, self.illegal_operation(other)
    def illegal_operation(self, other):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            "Illegal Operation",
            self.context
        )
    
class Null(Value):
    def __init__(self):
        super().__init__()
        self.value = "NULL"
    def copy(self):
        copy = Null()
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def comparison_eq(self, other):
        if isinstance(other, Null):
            return Number.true, None
        else:
            return None, Value.illegal_operation(self, other)
    def __eq__(self, other):
        return type(self) == type(other)
    def __ne__(self, other):
        return type(self) != type(other)
class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        elif isinstance(other, List):
            sum = 0
            for i in range(len(other.elements)):
                if isinstance(other.elements[i], Number):
                    sum += other.elements[i].value
            sum += self.value
            return Number(sum).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    "Division by zero",
                    self.context
                )
            else:
                return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def modded_by(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        return None, self.illegal_operation(other)
    def power_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        elif isinstance(other, Null):
            return Number.false.set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def roll_die(self, other):
        if isinstance(other, Number):
            dice_count = self.value
            die = other.value
            rolled = []
            for i in range(dice_count):
                rolled.append(Number(random.randint(0, die)))
            return List(rolled).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    def is_true(self):
        return self.value != 0
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
Number.null = Null()
Number.false = Number(0)
Number.true = Number(1)
class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        elif isinstance(other, Number):
            return String(self.value + str(other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        elif isinstance(self, String):
            return String(self.value + " * " + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_eq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        elif isinstance(other, Null):
            return Number.false.set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def is_true(self):
        return len(self.value) > 0
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def __str__(self):
        return "{0}".format(self.value)
    def __repr__(self):
        return "\"{0}\"".format(self.value)
class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
    
    def added_to(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        elif isinstance(other, Number):
            sum = 0
            for i in range(len(self.elements)):
                if isinstance(self.elements[i], Number):
                    sum += self.elements[i].value
            sum += other.value
            return Number(sum).set_context(self.context), None
        return None, Value.illegal_operation(self, other)
    def comparison_gt(self, other):
        if isinstance(other, Number):
            bool_arr = []
            for i in range(len(self.elements)):
                if self.elements[i].value > other.value:
                    bool_arr.append(Number.true)
                else:
                    bool_arr.append(Number.false)
            return List(bool_arr).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def comparison_eq(self, other):
        if isinstance(other, Null):
            return Number.false.set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get(self, other):
        if isinstance(other, Number):
            element = self.elements[other.value]
            return element.set_context(self.context), None
        return None, Value.illegal_operation(self, other)
    def set(self, other, value):
        if isinstance(other, Number):
            self.elements[other.value] = value
            return self.copy(), None
        return None, Value.illegal_operation(self, other)
    def is_true(self):
        return len(self.elements) > 0
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def __str__(self):
        return "[{0}]".format(", ".join([str(x) for x in self.elements]))
    def __repr__(self):
        return "[{0}]".format(", ".join([str(x) for x in self.elements]))

class Dict(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
    
    def added_to(self, other):
        if isinstance(other, Dict):
            pass
        return None, Value.illegal_operation(self, other)
    def comparison_gt(self, other):
        if isinstance(other, Dict):
            pass
        return None, Value.illegal_operation(self, other)
    def comparison_eq(self, other):
        if isinstance(other, Null):
            return Number.false.set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get(self, other):
        if isinstance(other, Number) or isinstance(other, String):
            element = self.elements[other.value]
            return element.set_context(self.context), None
        return None, Value.illegal_operation(self, other)
    def set(self, other, value):
        if isinstance(other, Number):
            self.elements[other.value] = value
            return self.copy(), None
        if isinstance(other, String):
            self.elements[other.value] = value
            return self.copy(), None
        return None, Value.illegal_operation(self, other)
    def is_true(self):
        return len(self.elements) > 0
    def copy(self):
        copy = Dict(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def __repr__(self):
        res = ""
        i = 0
        last_key_index = len(self.elements)-1
        for key in self.elements:
            res += "\""+str(key)+"\""
            res += ": "
            res += str(self.elements[key])
            if i != last_key_index:
               res += ", " 
            i+=1
            
        return "{" + res + "}"
    

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"
        self.is_anonymous = self.name == "<anonymous>"
    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context
    def check_args(self, arg_names, args):
        res = RTResult()
        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                "Too many arguments",
                self.context
            ))
        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                "Too few arguments",
                self.context
            ))
        return res.success(None)
    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(arg_names)):
            arg_name = arg_names[i]
            arg_value = args[i] if i < len(args) else Number.null
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)
    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        #res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)
    def __eq__(self, other):
        return type(self).__name__ == other
    def __ne__(self, other):
        return type(self).__name__ != other
       
class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return, parent=None):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return
        self.parent_context = parent
        print(parent)
    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
       
        exec_context = self.generate_new_context()
        
        #print("START {} END".format(self.context.symbol_table.get("this")))
        if not self.is_anonymous:
            exec_context.symbol_table.set("this", Dict({"context":self.parent_context}))
        self.check_and_populate_args(self.arg_names, args, exec_context)
        
        value = res.register(interpreter.visit(self.body_node, exec_context))
        if res.should_return() and res.func_rtn_value == None: return res
        ret_value = (value if self.should_auto_return else None) or res.func_rtn_value or (exec_context.symbol_table.get("this") if exec_context.symbol_table.get("this").elements != {} else Number.null)
        print("wow")
        print(exec_context.symbol_table.get("this"))
        return res.success(ret_value)
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return "<function {0}>".format(self.name)

class BuiltinFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    def execute(self, args):
        res = RTResult()
       
        exec_context = self.generate_new_context()
        method_name = "execute_{0}".format(self.name)
        method = getattr(self, method_name, self.no_execute_method)
        
        res.register(self.check_and_populate_args(method.arg_names, args, exec_context))
        if res.should_return(): return res
        
        return_value = res.register(method(exec_context))
        if res.should_return(): return res
        
        return res.success(return_value)
    def no_execute_method(self, node, context):
        method_name = "execute_{0}".format(self.name)
        raise Exception("No {0} method".format(method_name))
    def copy(self):
        copy = BuiltinFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return "<builtin function {0}>".format(self.name)
        
    def execute_print(self, exec_ctx):
        print(exec_ctx.symbol_table.get("value"), end="")
        return RTResult().success(Number.null)
    execute_print.arg_names = ['value']
    def execute_println(self, exec_ctx):
        print(exec_ctx.symbol_table.get("value"))
        return RTResult().success(Number.null)
    execute_println.arg_names = ['value']
    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else "clear")
        return RTResult().success(Number.null)
    execute_clear.arg_names = []
    def execute_len(self, exec_ctx):
        arr = exec_ctx.symbol_table.get("array")
        return RTResult().success(Number(len(arr.elements)))
    execute_len.arg_names = ["array"]
    def execute_true_indexs(self, exec_ctx):
        arr = exec_ctx.symbol_table.get("array")
        inds = []
        for i in range(len(arr.elements)):
            if arr.elements[i] == Number.true:
                inds.append(i)
        return RTResult().success(List(inds))
    execute_true_indexs.arg_names = ["array"]
    def execute_exit(self, exec_ctx):
        exit()
        #return RTResult().success(Number.null)
    execute_exit.arg_names = []
    
BuiltinFunction.print           = BuiltinFunction("print")
BuiltinFunction.true_indexs     = BuiltinFunction("true_indexs")
BuiltinFunction.println         = BuiltinFunction("println")
BuiltinFunction.clear           = BuiltinFunction("clear")
BuiltinFunction.exit            = BuiltinFunction("exit")
BuiltinFunction.len             = BuiltinFunction("len")
