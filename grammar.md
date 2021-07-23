**Lexar:
	NEWLINE 	: \n | ;<br>
	IDENTIFIER	: a-Z (a-Z | 0-9 | .)*<br>
	EE			: ==<br>
	LT			: \< <br>
	GT			: \> <br>
	LTE			: <= <br>
	GTE			: >= <br>
	EQ			: = <br>
	PEQ			: += <br>
	MEQ 		: -= <br>
	PLUS		: + <br>
	MINUS		: - <br>
	MUL			: * <br>
	DIV			: / <br>
	MOD			: % <br>
	POW 		: ^ <br> 
	INT 		: (0-9)+ <br>
	FLOAT 		: (0-9)* (. (0-9)*) <br>
	STRING		: " (any characters) " <br>


**Parser:
	program 	: statements
	
	statements	: NEWLINE* statement (NEWLINE+ statement) NEWLINE*
	
	statement 	: KEYWORD:return expr
				: KEYWORD:continue
				: KEYWORD:break
				: KEYWORD:let IDENTIFIER EQ expr
				: IDENTIFIER (EQ | PEQ | MEQ) expr
				: expr
	
	expr		: comp-expr ((KEYWORD:and|KEYWORD:or) comp-expr)*
	
	comp-expr	: KEYWORD:not comp-expr
				: arith-expr ((EE|LT|GT|LTE|GTE) arith-expr)*
				
	arith-expr	: term ((PLUS|MINUS) term)*
	
	term		: factor ((MUL|DIV|MOD) factor)*
	
	factor		: (PLUS|MINUS) factor
				: power
				
	power		: atom (POW factor)*
				
	atom		: INT (IDENTIFIER:d INT)
				: FLOAT|STRING
				  LPAREN expr RPAREN
				  
	if-expr		: KEYWORD:if LPAREN expr RPARENT NEWLINE* LBRAC statements RBRAC
	
	for-expr	: KEYWORD:for LPAREN (statement NEWLINE expr NEWLINE statement )