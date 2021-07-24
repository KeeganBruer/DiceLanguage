let Errors = require("./Errors.js")
let ParseResult = require("./ParseResult.js")
let Nodes = require("./Nodes.js")
let Token = require("./Token.js")


function Parser() {
	this.advance = function(amount){
        this.tok_idx += amount != undefined ? amount : 1
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
		let res = await this.expr()
		
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
		}
		return res.failure(new Errors.InvalidSyntaxError(this, "", tok.pos_start, tok.pos_end))
	}
	/*
		POWER:
			: atom (POW factor)*
	*/
	this.power = function() {
		
	}
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
			let fac = res.register(this.atom())
			return res.success(new Nodes.UrinaryOpNode(tok, fac))
		}
		let atom = res.register(this.atom())
		if (res.should_return()) {return res}
		return res.success(atom)
	}
	this.factor = this.factor.bind(this)
	/*
		TERM:
	*/
	this.term = function() {
		let res = this.bin_op(this.factor, [Token.TT_MULT, Token.TT_DIV])
		return res
	}
	this.term = this.term.bind(this)
	/*
		EXPR:
	*/
	this.expr = async function() {
		let res = this.bin_op(this.term, [Token.TT_PLUS, Token.TT_MINUS])
		return res
	}
	this.expr = this.expr.bind(this)

	return this
}

module.exports = Parser