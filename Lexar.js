import Token

function Position() {
	this.idx = -1
	this.increase = function() {
		this.idx += 1
	}
	return this
}

function Lexar() {
	this.DIGITS = "0123456789"
	this.LETTERS = "abcdefghijklmnopqrstwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	this.LETTERS_DIGITS = this.LETTERS + this.DIGITS;
	this.pos = new Position()
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
	
	this.lex = function(text) {
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
			} else if ("(".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_LPAREN))
			} else if (")".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_RPAREN))
			} else if ("[".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_LSQUARE))
			} else if ("]".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_RSQUARE))
			} else if ("{".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_LBRAC))
			} else if ("}".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_RBRAC))
			} else if (",".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_COMMA))
			} else if (".".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_DOT))
			} else if (":".includes(this.current_char)) {
				tokens.push(new Token(Token.TT_COLON))
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
				tokens.push(new Token(Token.TT_EQ))
			} else {
				//pass
			}
			this.advance()
		}
		return tokens
	}
	this.make_number = function() {
		let num = ""
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
			return new Token(Token.TT_DICE, [!isNaN(count) ? count : 1, die_type, die_val])
		}
		if (num.includes(".")) {
			return new Token(Token.TT_FLOAT, parseFloat(num))
		} else {
			return new Token(Token.TT_INT, parseInt(num))
		}
	}
	this.make_identifier = function() {
		let identifier = ""
		while (this.current_char != null && (this.LETTERS_DIGITS + "_.").includes(this.current_char)) {
			identifier += this.current_char
			this.advance()
		}
		if (Token.KEYWORDS.includes(identifier)) { //if the found identifier is a keyword.
			return new Token(Token.TT_KEYWORD, identifier)
		}
		return new Token(Token.TT_IDENTIFIER, identifier)
	}
	
	this.make_string = function() {
		let str = ""
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
		return new Token(Token.TT_STRING, str)
		
	}
	this.make_type_and_equals = function (type_) {
		this.advance() //advance past <
		let new_type = type_
		if (this.current_char == "=") {
			new_type = Token[type_+"EQ"]
			this.advance()
		}
		return new Token(new_type)
	}
	this.make_plus = function() {
		return this.make_type_and_equals(Token.TT_PLUS)
	}
	this.make_minus = function() {
		return this.make_type_and_equals(Token.TT_PLUS)
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