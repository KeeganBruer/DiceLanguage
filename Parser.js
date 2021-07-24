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
	this.parse_tokens = async function(tokens) {
		this.tok_idx = -1
		this.tokens = tokens
		let res = await this.statements()
		if (!res.error && !this.current_tok.matches(Token.TT_EOF, undefined)) {
			return res.failure(
                Errors.InvalidSyntaxError(
                    "Expected int or float",
					this.current_tok.pos_start,
                    this.current_tok.pos_end
                )
            )
		}
		return res
	}
	this.statements = async function() {
		let res = new ParseResult()
		let statements = []
		res.register_advancement()
		this.advance()
		while (this.current_tok.matches(Token.TT_NEWLINE)) { //skip over any newlines
			res.register_advancement()
			this.advance()
		}
		let statement = res.register(this.statement())
		if (res.should_return()) {return res}
        statements.push(statement)
		while (!this.current_tok.matches(Token.TT_EOF)) { //skip over any newlines
			statement = res.register(this.statement())
			if (res.should_return()) {return res}
			statements.push(statement)
		}
		return res.success(new Nodes.ListNode(statements))
	}
	
	this.statement = function() {
		let res = new ParseResult()
		res.success(new Nodes.NumberNode(this.current_tok))
		if (res.should_return()) {return res}
		res.register_advancement()
		this.advance()
		return res
	}
	return this
}

module.exports = Parser