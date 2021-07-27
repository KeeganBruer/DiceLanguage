let fs = require("fs")
let DIPLA = require("./DIPLA.js")
let Databases = require("./Databases.js")
let Types = require("./Types.js")



const rl = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout
})
async function run() {
	let database = await new Databases.MongoDB("mongodb://127.0.0.1:27017/")
	//let database = await new Databases.Default()
	let lang = new DIPLA(database)
	//await lang.database.set_database("eca1316b-b1e4-49f1-bfea-19feaaa256a4")
	//await lang.database.set_collection("characters")
	//let character = await lang.database.get_collection_item({"id":0})
	//console.log(character)
	//await lang.database.set_database("test")
	//await lang.database.set_collection("test1")
	//await lang.database.set_table("global.ruck")
	let files = process.argv.slice(2, process.argv.length)
	for (let i = 0; i < files.length; i++ ) {
		let file = fs.readFileSync(files[i])
		file = file.toString().split("\n").join(";").split("\r").join(";")
		file = file.substring(0, file.length-1);
		await lang.evaluate("<stdin>", file)
	}
	while (true) {
		let input = await new Promise((resolve, reject)=> {
			rl.question('>', function(input) {
				resolve(input)
			})
		})
		if (input.includes("add_table")) {
			let table_name = input.split(" ")[1]
			lang.database.add_table(table_name)
			lang.database.set_table(table_name)
		} else {
			let result = await lang.evaluate("<stdin>", input)
			await lang.database.set_var("in", new Types.String(input))
			await lang.database.set_var("out", result)
		}
		let last_in = await lang.database.get_var("in")
		console.log("Input: " + last_in.toString())
		let last_out = await lang.database.get_var("out")
		console.log("Result: " + last_out.toString())
	}
}

run()
