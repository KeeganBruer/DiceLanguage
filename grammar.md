## Lexar:
```
	NEWLINE 	: \n | ;
	IDENTIFIER	: a-Z (a-Z | 0-9 | .)*
	EE		: ==
	OR		: ||
	AND		: &&
	LT		: \< 
	GT		: \> 
	LTE		: <= 
	GTE		: >= 
	EQ		: = 
	PEQ		: += 
	MEQ 		: -= 
	PLUS		: + 
	MINUS		: - 
	MUL		: * 
	DIV		: / 
	MOD		: % 
	POW 		: ^  
	INT 		: (0-9)+ 
	FLOAT 		: (0-9)* (. (0-9)*) 
	STRING		: " (any characters) " 
```

## Parser:
```	
	statements	: NEWLINE* statement (NEWLINE+ statement) NEWLINE*
	
	statement 	: KEYWORD:return expr
			: KEYWORD:continue
			: KEYWORD:break
			: KEYWORD:let IDENTIFIER EQ expr
			: IDENTIFIER (EQ | PLUSEQ | MINUSEQ) expr
			: expr
	
	expr		: comp-expr ((AND|OR) comp-expr)*
	
	comp-expr	: NOT comp-expr
			: arith-expr ((EE|LT|GT|LTE|GTE) arith-expr)*
				
	arith-expr	: term ((PLUS|MINUS) term)*
	
	term		: factor ((MUL|DIV|MOD) factor)*
	
	factor		: (PLUS|MINUS) factor
			: power
				
	power		: atom (POW factor)*
				
	atom		: INT|FLOAT|STRING|DICE
			: LPAREN expr RPAREN
				  
	if-expr		: KEYWORD:if LPAREN expr RPAREN NEWLINE* LBRAC statements RBRAC
	
	for-expr	: KEYWORD:for LPAREN statement NEWLINE expr NEWLINE statement RPAREN NEWLINE* LBRAC statements RBRAC
```
