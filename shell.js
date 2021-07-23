
function nocache(module) {
	console.log("[NO CACHE]: \"" + require("path").resolve(module)+"\"")
	require("fs").watchFile(require("path").resolve(module), () => {
		delete require.cache[require.resolve(module)]
	})
}
nocache("./Lexar.js");


const rl = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})

rl.on('line', (input) => {
	let Lexar = require("./Lexar.js")
	let lexar = new Lexar()
	let result = lexar.lex(input);
	console.log(result.toString())
});
