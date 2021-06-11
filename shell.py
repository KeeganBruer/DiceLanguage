import argparse
from Lexer import Lexer
from Parser import Parser
from Interpreter import *
from Context import Context, SymbolTable

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("print", BuiltinFunction.print)
global_symbol_table.set("println", BuiltinFunction.println)
global_symbol_table.set("true_indexs", BuiltinFunction.true_indexs)
global_symbol_table.set("len", BuiltinFunction.len)
global_symbol_table.set("clear", BuiltinFunction.clear)
global_symbol_table.set("exit", BuiltinFunction.exit)

def main(args):
    for file_path in args.file_path:
        text = "" 
        with open(file_path, 'r') as file:
            text = file.read()
        res, error = run(file_path, text)
        print_out(res, error, True)
        
    if args.is_interactive:
        while True:
            text = input("")
            res, error = run("<stdin>", text)
            if error: print(error)
            print_out(res, error)
            
def print_out(res, error, is_file=False):
    if error: print(error)
    elif res: 
        if len(res.elements) == 1:
            if type(res.elements[0]) != type(Number.null):
                print(res.elements[0])
        elif (is_file):
            for i in range(len(res.elements)):
                if (res.elements[i] != "Function"):
                    end = "" if i != len(res.elements)-1 else "\n"
                    print(res.elements[i], end="\n" )
        else:
            print(repr(res))

def run(fn, text):
    if text.strip() == "":
        return None, None
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    #print(tokens)
    if error: return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    #print(ast)
    if ast.error: return None, ast.error
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    res = interpreter.visit(ast.node, context)
    
    return res.value, res.error

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('file_path', metavar='FILE', nargs="*", default=None, help='')
    parser.add_argument('-i', dest='is_interactive', action='store_true', default=False, help='')
    parser.add_argument('-s', dest='program_string', action='store_true', default=False, help='')

    args = parser.parse_args()
    main(args)
