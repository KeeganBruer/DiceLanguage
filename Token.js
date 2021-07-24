function Token(type_, value_, pos_start, pos_end) {
	this.type_ = type_
	this.value_ = value_
	this.pos_start = pos_start
	this.pos_end = pos_end
	this.toString = function(obj) {
		if (this.value_) {
			return "" +this.type_ + ":" + this.value_ + "";
		}
		return ""+this.type_+""
	}
	this.matches = function(type_, value_) {
		if (type_ == this.type_ && value_ == this.value_) {
			return true
		}
		return false
	}
	return this
}
Token.TT_IDENTIFIER = "TT_IDENTIFIER"
Token.TT_KEYWORD	= "TT_KEYWORD"
Token.TT_FLOAT   	= "TT_FLOAT"
Token.TT_STRING   	= "TT_STRING"
Token.TT_INT 		= "TT_INT"
Token.TT_EQ 		= "TT_EQ"
Token.TT_COMMA 		= "TT_COMMA"
Token.TT_DOT 		= "TT_DOT"
Token.TT_COLON 		= "TT_COLON"
Token.TT_LPAREN 	= "TT_LPAREN"
Token.TT_RPAREN 	= "TT_RPAREN"
Token.TT_LSQUARE 	= "TT_LSQUARE"
Token.TT_RSQUARE 	= "TT_RSQUARE"
Token.TT_LBRAC 		= "TT_LBRAC"
Token.TT_RBRAC 		= "TT_RBRAC"
Token.TT_PLUS 		= "TT_PLUS"
Token.TT_PLUSEQ 	= Token.TT_PLUS+"EQ"
Token.TT_MINUS 		= "TT_MINUS"
Token.TT_MINUSEQ 	= Token.TT_MINUS+"EQ"
Token.TT_MULT 		= "TT_MULT"
Token.TT_MULTEQ 	= Token.TT_MULT+"EQ"
Token.TT_DIV 		= "TT_DIV"
Token.TT_DIVEQ 		= Token.TT_DIV+"EQ"
Token.TT_MOD		= "TT_MOD"
Token.TT_MODEQ		= Token.TT_MOD+"EQ"
Token.TT_POW		= "TT_POW"
Token.TT_POWEQ		= Token.TT_POW+"EQ"
Token.TT_NOT		= "TT_NOT"
Token.TT_NOTEQ		= Token.TT_NOT+"EQ"
Token.TT_DICE		= "TT_DICE"
Token.TT_EOF		= "TT_EOF"

Token.KEYWORDS 		= [
	"if",
	"else",
	"while",
	"function",
	"d"
]

module.exports = Token