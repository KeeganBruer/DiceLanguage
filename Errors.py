class Error():
    def __init__(self, pos_start, pos_end, error_name, details):
        self.error_name = error_name
        self.details = details
        self.pre_pend = ""
        self.pos_start = pos_start
        self.pos_end = pos_end
    def as_string(self):
        rtn = "{0}: {1}{2}\n".format(self.error_name,self.pre_pend, self.details)
        rtn += " " * 4 + "File \'{0}\', line {1}\n".format(self.pos_start.fn, self.pos_start.line+1)
        rtn += string_with_arrow(self.pos_start.ftext, self.pos_start, self.pos_end)
        return rtn
    def __repr__(self):
        return self.as_string()

def string_with_arrow(text, start, end):
    result = ""
    idx_start = max(text.rfind("\n", 0, start.idx), 0)
    idx_end = text.find("\n", idx_start+1)
    if idx_end < 0: idx_end = len(text)
    line_count = end.line - start.line + 1
    for i in range(line_count):
        line = text[idx_start:idx_end]
        col_start = start.col if i == 0 else 0
        col_end = end.col if i == line_count-1 else len(line) - 1
        result += " " * 8 + line.replace("\n", "") + "\n"
        result += " " * 8 + " " * col_start + "^" * (col_end - col_start)

        idx_start = idx_end+1
        idx_end = text.find("\n", idx_start+1)
        if idx_end < 0: idx_end = len(text)
    return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)
        self.details = self.details.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t").replace(" ", "[space]")
        #self.pre_pend = "Expected "
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)
        self.pre_pend = "Expected "
class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, "Expected Character", details)
        self.pre_pend = "Expected "
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "RunTime Error", details)
        self.context = context
    def as_string(self):
        rtn = self.generate_traceback()
        rtn += "{0}: {1}\n".format(self.error_name, self.details)
        rtn += "\n" +string_with_arrow(self.pos_start.ftext, self.pos_start, self.pos_end)
        return rtn
    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context
        while ctx:
            rtn = " " * 4 + "File \'{0}\', line {1}, in {2}\n".format(pos.fn, pos.line+1, ctx.display_name) + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return "Traceback (most recent call last):\n" + result


    
