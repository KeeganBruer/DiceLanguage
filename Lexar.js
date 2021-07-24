let Token = require("./Token.js")
let Position = require("./Position.js")
let Errors = require("./Errors.js")

function Lexar() {
	this.DIGITS = "0123456789"
	this.LETTERS = "abcdefghijklmnopqrstwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	this.LETTERS_DIGITS = this.LETTERS + this.DIGITS;
	this.pos = new Position(this)
	this.advance = function() {
		this.pos.increase()
		if (this.pos.idx < this.text.length) {
			this.current_char = this.text[this.pos.idx]
		} else {
			this.current_char = null;
		}
	}
	this.check_next_char = function(inc) {
		if (!inc) {
			inc = 1
		}
		if (this.pos.idx+inc < this.text.length) {
			return this.text[this.pos.idx+inc]
		} else {
			return null;
		}
	}
	
	this.lex = async function(fn, text) {
		this.fn = fn
		this.pos = new Position(this)
		this.text = text
		this.advance()
		let tokens = []
		while (this.current_char != null) {
			if (" \t".includes(this.current_char)) {
				//pass
			} else if ((this.DIGITS+"d").includes(this.current_char)) {
				//if the current character is d and the next value is a number
				if (this.current_char == "d"){
					let i = 1;
					while (this.check_next_char(i) != null && (this.LETTERS_DIGITS+"_.").includes(this.check_next_char(i))) {
						if (this.LETTERS.includes(this.check_next_char(i))) {
							i = -1
							break;
						}
						i +=1
					}
					if (i<0) {
						tokens.push(this.make_identifier())
						continue
					}
				}
				tokens.push(this.make_number())
				continue
			} else if (this.LETTERS.includes(this.current_char)) {
				tokens.push(this.make_identifier())
				continue
			} else if ("\"".includes(this.current_char)) {
				tokens.push(this.make_string())
				continue
			} else if ("+".includes(this.current_char)) {
				tokens.push(this.make_plus())
				continue
			} else if ("-".includes(this.current_char)) {
				tokens.push(this.make_minus())
				continue
			} else if ("*".includes(this.current_char)) {
				tokens.push(this.make_mult())
				continue
			} else if ("/".includes(this.current_char)) {
				tokens.push(this.make_div())
				continue
			} else if ("%".includes(this.current_char)) {
				tokens.push(this.make_mod())
				continue
			} else if ("^".includes(this.current_char)) {
				tokens.push(this.make_pow())
				continue
			} else if ("|".includes(this.current_char)) {
				tokens.push(this.make_or())
				continue
			} else if ("&".includes(this.current_char)) {
				tokens.push(this.make_and())
				continue
			} else if ("(".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_LPAREN, undefined, this.pos, this.pos))
			} else if (")".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_RPAREN, undefined, this.pos, this.pos))
			} else if ("[".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_LSQUARE, undefined, this.pos, this.pos))
			} else if ("]".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_RSQUARE, undefined, this.pos, this.pos))
			} else if ("{".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_LBRAC, undefined, this.pos, this.pos))
			} else if ("}".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_RBRAC, undefined, this.pos, this.pos))
			} else if (",".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_COMMA, undefined, this.pos, this.pos))
			} else if (".".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_DOT, undefined, this.pos, this.pos))
			} else if (":".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_COLON, undefined, this.pos, this.pos))
			} else if ("!".includes(this.current_char)) {
				tokens.push(this.make_not_operator())
				continue
			} else if ("<".includes(this.current_char)) {
				tokens.push(this.make_less_than())
				continue
			} else if (">".includes(this.current_char)) {
				tokens.push(this.make_greater_than())
				continue
			} else if ("=".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_EQ, this.pos, this.pos))
			} else {
				return {"result":tokens, "error":new Errors.IllegalCharError(this, "Illegal Character \'"+ this.current_char+"\'", this.pos, this.pos)}
			}
			this.advance()
		}
		//tokens.push(new Token(Token.TT_EOF))
		return {"tokens":tokens, "error":null}
	}
	this.make_number = function() {
		let num = ""
		let pos_start = this.pos.copy()
		while (this.current_char != null && (this.DIGITS + ".d").includes(this.current_char)) {
			num += this.current_char
			this.advance()
		}
		if (num.includes("d")) {//if the number contains a 'd', it is a dice
			let count = num.split("d")[0]
			let die_val = num.split("d")[1]
			count = parseInt(count)
			let die_type;
			if (!die_val.includes(".") ) {
				die_type = "INT"
				die_val = parseInt(die_val)
			} else {
				die_type = "FLOAT"
				die_val = parseFloat(die_val)
			}
			return new Token(Token.TT_DICE, [!isNaN(count) ? count : 1, die_type, die_val], pos_start, this.pos.copy())
		}
		if (num.includes(".")) {
			return new Token(Token.TT_FLOAT, parseFloat(num), pos_start, this.pos.copy())
		} else {
			return new Token(Token.TT_INT, parseInt(num), pos_start, this.pos.copy())
		}
	}
	this.make_identifier = function() {
		let identifier = ""
		let pos_start = this.pos.copy()
		while (this.current_char != null && (this.LETTERS_DIGITS + "_.").includes(this.current_char)) {
			identifier += this.current_char
			this.advance()
		}
		if (Token.KEYWORDS.includes(identifier)) { //if the found identifier is a keyword.
			return new Token(Token.TT_KEYWORD, identifier, pos_start, this.pos.copy())
		}
		return new Token(Token.TT_IDENTIFIER, identifier, pos_start, this.pos.copy())
	}
	
	this.make_string = function() {
		let str = ""
		let pos_start = this.pos.copy()
		let skip = false;
		str+= this.current_char
		this.advance()
		while (this.current_char != null && (this.current_char != "\"" || skip)) {
			str += this.current_char
			skip = false
			if (this.current_char == "\\") {
				skip = true
			}
			this.advance()
		}
		str+= this.current_char
		this.advance()
		return new Token(Token.TT_STRING, str, pos_start, this.pos.copy())
		
	}
	this.make_or = function() {
		this.advance()
		if (this.current_char == "|") {
			this.advance()
			return new Token(Token.TT_OR)
		}
		return new Token(Token.TT_BITOR)
	}
	this.make_and = function() {
		this.advance()
		if (this.current_char == "&") {
			this.advance()
			return new Token(Token.TT_AND)
		}
		return new Token(Token.TT_BITAND)
	}
	this.make_type_and_equals = function (type_) {
		let pos_start = this.pos.copy()
		this.advance() //advance past <
		let new_type = type_
		if (this.current_char == "=") {
			new_type = Token[type_+"EQ"]
			this.advance()
		}
		return new Token(new_type, undefined, pos_start, this.pos.copy())
	}
	this.make_plus = function() {
		return this.make_type_and_equals(Token.TT_PLUS)
	}
	this.make_minus = function() {
		return this.make_type_and_equals(Token.TT_MINUS)
	}
	this.make_mult = function() {
		return this.make_type_and_equals(Token.TT_MULT)
	}
	this.make_div = function() {
		return this.make_type_and_equals(Token.TT_DIV)
	}
	this.make_mod = function() {
		return this.make_type_and_equals(Token.TT_MOD)
	}
	this.make_pow = function() {
		return this.make_type_and_equals(Token.TT_POW)
	}
	this.make_not_operator = function() {
		return this.make_type_and_equals(Token.TT_NOT)
	}
	this.make_less_than = function() {
		return this.make_type_and_equals(Token.TT_LT)
	}
	
	return this
}

module.exports = Lexar