
function nocache(modules) {
	for (let i = 0; i < modules.length;i++) {
		console.log("[NO CACHE]: \"" + require("path").resolve(modules[i])+"\"")
		require("fs").watchFile(require("path").resolve(modules[i]), () => {
			delete require.cache[require.resolve(modules[i])]
		})
	}
}
nocache([
	"./Lexar.js", 
	"./Position.js", 
	"./Token.js", 
	"./Errors.js"
]);


const rl = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})

rl.on('line', (input) => {
	let Lexar = require("./Lexar.js")
	let Parser = require("./Parser.js")
	let lexar = new Lexar()
	lexar.lex("<stdin>",input).then((result) => {
		if (result.error) {
			console.log(result.error.toString())
			return;
		}
		console.log(result.tokens.toString())
		
		let parser = new Parser()
		parser.parse_tokens(result.tokens).then((res) => {
			console.log(res.node.toString())
		})
	});
});
