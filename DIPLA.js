let Lexar = require("./Lexar.js")
let Parser = require("./Parser.js")
let Interpreter = require("./Interpreter.js")
let Databases = require("./Databases.js")
function DIPLA(database) {
	this.lexar = new Lexar()
	this.parser = new Parser()
	this.database = database != undefined ? database : Databases.Default()
	this.interpreter = new Interpreter(this.database)
	this.evaluate = async function(fn, text) {
		let result = await this.lexar.lex(fn,text)
		if (result.error) {
			console.print_obj(result.error)
			return;
		}
		//console.log(result)
		let res = await this.parser.parse_tokens(fn,text, result.tokens)
		if (res.error) {
			console.print_obj(res.error)
			return;
		}
		console.print_obj(res)
		result = await this.interpreter.visit(res.node)
		return result
	}
	return this
}
console.print_obj = function(obj){
	if (obj.toString) {
		console.log(obj.toString())
	} else {
		console.log(obj)
	}
}

DIPLA.Lexar = Lexar
DIPLA.Parser = Parser
module.exports = DIPLA