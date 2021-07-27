let Errors = require("./Errors.js")
let ParseResult = require("./ParseResult.js")
let Nodes = require("./Nodes.js")
let Token = require("./Token.js")


function Parser() {
	this.advance = function(amount){
        this.tok_idx += amount != undefined ? amount : 1
        this.update_current_tok()
	}
	this.reverse = function(amount){
        this.tok_idx -= amount != undefined ? amount : 1
        this.update_current_tok()
	}
	this.update_current_tok = function() {
		if (this.tok_idx < this.tokens.length) {
            this.current_tok = this.tokens[this.tok_idx]
		}
	}
	this.parse_tokens = async function(fn, text, tokens) {
		this.fn = fn;
		this.text = text
		this.tok_idx = -1
		this.tokens = tokens
		this.advance()
		let res = this.statements()
		
		return res
	}
	/*
		Binary Operation Helper
	*/
	this.bin_op = function(func, ops, func2) {
		let res = new ParseResult()
		let left = res.register(func())
		if (res.should_return()) {return res}
		while (ops.includes(this.current_tok.type_)) {
			let op_tok = this.current_tok;
			res.register_advancement()
			this.advance()
			let right;
			if (func2 != undefined) {
				right = res.register(func2())
			} else {
				right = res.register(func())
			}
			if (res.should_return()) {return res}
			left = new Nodes.BinaryOpNode(left, op_tok, right)
		}
		return res.success(left)
	}
	this.bin_op = this.bin_op.bind(this)
	/*
		IF EXPR:
			: KEYWORD:if LPAREN expr RPAREN NEWLINE* LBRAC statements RBRAC
	*/
	this.if_expr = function() {
		let res = new ParseResult()
		res.register_advancement()
		this.advance()
		if (!this.current_tok.matches(Token.TT_LPAREN)) {
			return res.failure(Errors.InvalidSyntaxError(this, "Expected \'(\'", this.current_tok.pos_start, this.current_tok.pos_end))
		}
		res.register_advancement()
		this.advance()
		let expr = res.register(this.expr())
		if (res.should_return()) {return res}
		if (!this.current_tok.matches(Token.TT_RPAREN)) {
			return res.failure(Errors.InvalidSyntaxError(this, "Expected \')\'", this.current_tok.pos_start, this.current_tok.pos_end))
		}
		res.register_advancement()
		this.advance()
		while (this.current_tok.matches(Token.TT_NEWLINE)) {
			res.register_advancement()
			this.advance()
		}
		if (!this.current_tok.matches(Token.TT_LBRAC)) {
			return res.failure(Errors.InvalidSyntaxError(this, "Expected \'{\'", this.current_tok.pos_start, this.current_tok.pos_end))
		}
		res.register_advancement()
		this.advance()
		let statements = res.register(this.statements())
		if (res.should_return()) {return res}
		if (!this.current_tok.matches(Token.TT_RBRAC)) {
			return res.failure(Errors.InvalidSyntaxError(this, "Expected \'}\'", this.current_tok.pos_start, this.current_tok.pos_end))
		}
		res.register_advancement()
		this.advance()
		return res.success(new Nodes.IfNode(expr, statements))
	}
	this.if_expr = this.if_expr.bind(this)
	/*
		ATOM:
			: INT|FLOAT|STRING|DICE
			: LPAREN expr RPAREN
			
	*/
	this.atom = function() {
		let res = new ParseResult()
		let tok = this.current_tok
		if ([Token.TT_INT, Token.TT_FLOAT].includes(tok.type_)) {
			res.register_advancement()
			this.advance()
			return res.success(new Nodes.NumberNode(tok))
		} else if ([Token.TT_DICE].includes(tok.type_)) {
			res.register_advancement()
			this.advance()
			return res.success(new Nodes.DiceNode(tok))
		} else if ([Token.TT_STRING].includes(tok.type_)) {
			res.register_advancement()
			this.advance()
			return res.success(new Nodes.StringNode(tok))
		} else if ([Token.TT_LPAREN].includes(tok.type_)) {
			res.register_advancement()
			this.advance()
			let expr = res.register(this.expr())
			if (res.should_return()) {return res}
			if ([Token.TT_RPAREN].includes(this.current_tok.type_)) {
				res.register_advancement()
				this.advance()
				return res.success(expr)
			}
			return res.failure(new Errors.InvalidSyntaxError(this, "Expected \')\'", tok.pos_start, tok.pos_end))
		} else if (tok.matches(Token.TT_KEYWORD, "if")) {
			let if_expr = res.register(this.if_expr())
			if (res.should_return()) {return res}
			return res.success(if_expr)
		}
		return res.failure(new Errors.InvalidSyntaxError(this, "", tok.pos_start, tok.pos_end))
	}
	this.atom = this.atom.bind(this)
	/*
		POWER:
			: atom (POW factor)*
	*/
	this.power = function() {
		let res = this.bin_op(this.atom, [Token.TT_POW], this.factor)
		return res
	}
	this.power = this.power.bind(this)
	/*
		FACTOR: 
			: (PLUS|MINUS) factor
			: power
	*/
	this.factor = function() {
		let res = new ParseResult()
		let tok = this.current_tok
		if ([Token.TT_PLUS, Token.TT_MINUS].includes(tok.type_)) {
			res.register_advancement()
			this.advance()
			let fac = res.register(this.factor())
			return res.success(new Nodes.UrnaryOpNode(tok, fac))
		}
		let power = res.register(this.power())
		if (res.should_return()) {return res}
		return res.success(power)
	}
	this.factor = this.factor.bind(this)
	/*
		TERM:
			: factor ((MUL|DIV|MOD) factor)*
	*/
	this.term = function() {
		let res = this.bin_op(this.factor, [Token.TT_MULT, Token.TT_DIV, Token.TT_MOD])
		return res
	}
	this.term = this.term.bind(this)
	/*
		ARITH EXPR:
			: term ((PLUS|MINUS) term)*
	*/
	this.arith_expr = function() {
		let res = this.bin_op(this.term, [Token.TT_PLUS, Token.TT_MINUS])
		return res
	}
	this.arith_expr = this.arith_expr.bind(this)
	/*
		COMP EXPR:
			: NOT comp-expr
			: arith-expr ((EE|LT|GT|LTE|GTE) arith-expr)*
	*/
	this.comp_expr = function() {
		let res = new ParseResult()
		let tok = this.current_tok
		if ([Token.TT_NOT].includes(tok.type_)) {
			res.register_advancement()
			this.advance()
			let comp_expr = res.register(this.comp_expr())
			return res.success(new Nodes.UrnaryOpNode(tok, comp_expr))
		}
		let arith_expr = res.register(this.arith_expr())
		if (res.should_return()) {return res}
		return res.success(arith_expr)
	}
	this.comp_expr = this.comp_expr.bind(this)
	/*
		EXPR:
			: comp-expr ((AND|OR) comp-expr)*
	*/
	this.expr = function() {
		let res = this.bin_op(this.comp_expr, [Token.TT_AND, Token.TT_OR])
		return res
	}
	this.expr = this.expr.bind(this)
	/*
		STATEMENT:
			: KEYWORD:return expr
			: KEYWORD:continue
			: KEYWORD:break
			: KEYWORD:let IDENTIFIER EQ expr
			: IDENTIFIER (EQ | PLUSEQ | MINUSEQ) expr
			: expr
	*/
	this.statement = function() {
		let res = new ParseResult()
		let tok = this.current_tok
		if (tok.matches(Token.TT_KEYWORD, "return")) {
			res.register_advancement()
			this.advance()
			let expr = res.register(this.expr())
			if (res.should_return()) {return res}
			return res.success(new Nodes.ReturnNode(expr))
		} else if (tok.matches(Token.TT_KEYWORD, "continue")) {
			res.register_advancement()
			this.advance()
			return res.success(new Nodes.ContinueNode())
		} else if (tok.matches(Token.TT_KEYWORD, "break")) {
			res.register_advancement()
			this.advance()
			return res.success(new Nodes.BreakNode())
		} else if (tok.matches(Token.TT_KEYWORD, "let")) {
			res.register_advancement()
			this.advance()
			if (!this.current_tok.matches(Token.TT_IDENTIFIER)) {
				return res.failure(Errors.InvalidSyntaxError(this, "Expected Identifier", tok.pos_start, tok.pos_end))
			}
			let identifier = this.current_tok
			res.register_advancement()
			this.advance()
			if (!this.current_tok.matches(Token.TT_EQ)) {
				return res.failure(Errors.InvalidSyntaxError(this, "Expected EQ", tok.pos_start, tok.pos_end))
			}
			res.register_advancement()
			this.advance()
			let expr = res.register(this.expr())
			if (res.should_return()) {return res}
			return res.success(new Nodes.VarAssignNode(identifier, expr))
		} else if (tok.matches(Token.TT_IDENTIFIER)) {
			let identifier = this.current_tok
			res.register_advancement()
			this.advance()
			if (![Token.TT_EQ, Token.TT_PLUSEQ, Token.TT_MINUSEQ, Token.TT_MULTEQ, Token.TT_DIVEQ, Token.TT_MODEQ].includes(this.current_tok.type_)) {
				return res.success(new Nodes.VarAccessNode(identifier))			
			}
			let op_tok = this.current_tok
			res.register_advancement()
			this.advance()
			let expr = res.register(this.expr())
			if (res.should_return()) {return res}
			return res.success(new Nodes.VarReassignNode(identifier, op_tok, expr))
		}
		let expr = res.register(this.expr())
		if (res.should_return()) {return res}
		return res.success(expr)
	}
	this.statement = this.statement.bind(this)
	/*
		STATEMENTS:
			: NEWLINE* statement (NEWLINE+ statement) NEWLINE*
	*/
	this.statements = function() {
		let res = new ParseResult()
		let statements = []
		let pos_start = this.current_tok.pos_start
		while (this.current_tok.matches(Token.TT_NEWLINE)) {
			res.register_advancement()
			this.advance()
		}
		let statement = res.register(this.statement())
		if (res.should_return()) {return res}
		statements.push(statement)
        more_statements = true
		while (true) {
            let new_line_count = 0
            while (this.current_tok.matches(Token.TT_NEWLINE)) {
                res.register_advancement()
                this.advance()
                new_line_count += 1
			}
            if (new_line_count == 0) {
                more_statements = false
			}
            if (!more_statements) { break}
            statement = res.try_register(this.statement())
            if (statement == undefined){
                this.reverse(res.to_reverse_count)
                more_statements = false
                break
			}
            statements.push(statement)
		}
		return res.success(new Nodes.ListNode(statements))
	}
	this.statements = this.statements.bind(this)
	return this
}

module.exports = Parser