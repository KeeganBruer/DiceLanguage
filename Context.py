class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
class SymbolTable():
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
    def get(self, name, current_ctx_only=False):
        value = self.symbols.get(name, None)
        if value == None and self.parent != None and not current_ctx_only:
            return self.parent.get(name)
        return value
    def set(self, name, value, is_reassign=False):
        if is_reassign:
            cur_value = self.symbols.get(name, None)
            if cur_value == None and self.parent != None:
                self.parent.set(name, value, is_reassign)
                return
        self.symbols[name] = value
    def remove(self, name):
        del self.symbols[name]
