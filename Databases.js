let Types = require("./Types.js")

function Database() {
	this.tables = {"global":{}}
	this.current_table = ["global"]
	this.set_table = async function(name) {
		let table_path = name.split(".")
		this.current_table = table_path
	}
	this.set_var = async function(name, val) {
		//get the current table
		let table = this.tables;
		let var_path = name.split(".")
		for (let i = 0; i < this.current_table.length; i++) {
			if (table[this.current_table[i]] == undefined) {
				table[this.current_table[i]] = {}
			} 
			table =table[this.current_table[i]]
		}
		//find the variable in the current table
		let variable = table
		for (let i = 0; i < var_path.length; i++) {
			
			if (i == var_path.length-1) {
				variable[var_path[i]] = val
				return;
			} else if (variable[var_path[i]] == undefined) {
				variable[var_path[i]] = {}
				variable = variable[var_path[i]]
			} else {
				variable = variable[var_path[i]]
			}
		}
	}.bind(this)
	this.get_var = async function(name, val) {
		let table = this.tables;
		let var_path = name.split(".")
		for (let i = 0; i < this.current_table.length; i++) {
			table =table[this.current_table[i]]
		}
		//find the variable in the current table
		let variable = table
		for (let i = 0; i < var_path.length; i++) {
			variable = variable[var_path[i]]
			if (variable == undefined) {
				break;
			}
		}
		return variable
	}.bind(this)
	return this
}
exports.Default = Database

function MongoDB(URL, database_name, collection_name) {
	Database.call(this)
	const mongodb = require('mongodb');
	this.client = mongodb.MongoClient;
	this.mongo_url = URL
	this.database_name = database_name != undefined ? database_name : "test"
	this.collection_name = collection_name != undefined ? collection_name : "test1"
	this.table_name = ["global"]
	this.is_connected = false
	this.setup = async function(db_name, coll_name, table_name) {
		if (db_name) {
			await this.set_database(db_name)
		}
		if (coll_name) {
			await this.set_collection(coll_name)
		}
		if (table_name) {
			await this.set_table(table_name)
		}
	}.bind(this)
	this.set_database = async function(name) {
		this.database_name = name
		this.database_obj = this.db_manager.db(this.database_name);
	}.bind(this)
	this.set_collection = async function(name) {
		this.collection_name = name
		this.collection_obj = this.database_obj.collection(this.collection_name)
		let all_tables = await this.collection_obj.find({}).toArray()
		this.all_tables = all_tables != undefined ? all_tables : []
	}.bind(this)
	this.set_table = function(name) {
		let table_path = name.split(".")
		this.table_name = table_path
	}.bind(this)
	this.set_var = async function(name, val) {
		let var_path = name.split(".")
		let table_obj = await this.collection_obj.findOne({"name":this.table_name[0]})
		if (table_obj == undefined) {
			await this.collection_obj.insertOne({"name":this.table_name[0]});
			table_obj = await this.collection_obj.findOne({"name":this.table_name[0]})
		}
		let table = table_obj
		for (let i = 1; i < this.table_name.length; i++) {
			if (table[this.table_name[i]] == undefined) {
				table[this.table_name[i]] = {}
			} 
			table = table[this.table_name[i]]
		}
		for (let i = 0; i < var_path.length; i++) {
			if (i == var_path.length-1) {
				table[var_path[i]] = {}
				table[var_path[i]].type_ = val.type_
				table[var_path[i]].val = val.toString()
			} else if (table[var_path[i]] == undefined) {
				table[var_path[i]] = {}
				table = table[var_path[i]]
			} else {
				table = table[var_path[i]]
			}
		}
		await this.collection_obj.findOneAndReplace({"name":this.table_name[0]}, table_obj);		
	}.bind(this)
	this.get_var = async function(name) {
		let var_path = name.split(".")
		let table_obj = await this.collection_obj.findOne({"name":this.table_name[0]})
		let table = table_obj
		for (let i = 1; i < this.table_name.length; i++) {
			if (table[this.table_name[i]] == undefined) {
				table[this.table_name[i]] = {}
			} 
			table = table[this.table_name[i]]
		}
		let variable = table
		for (let i = 0; i < var_path.length; i++) {
			
			if (variable[var_path[i]] == undefined) {
				variable[var_path[i]] = {}
				variable = variable[var_path[i]]
			} else {
				variable = variable[var_path[i]]
			}
		}
		if (variable.type_ == Types.T_Number) {
			return new Types.Number(parseFloat(variable.val))
		} else if (variable.type_ == Types.T_String) {
			return new Types.String(variable.val)
		} else if (variable.type_ == Types.T_List) {
			return new Types.List(variable.val.replace("[", "").replace("]", "").split(","))
		}
		return variable
	}.bind(this)
	this.get_collection_item = async function(name) {
		let table_obj = await this.collection_obj.findOne(name)
		return table_obj
	}.bind(this)
	let promise = new Promise((resolve, reject) => {
		this.client.connect(this.mongo_url, function(err, db) {
			if (err) throw err;
			this.db_manager = db
			this.is_connected = true
			this.setup(this.database_name, this.collection_name).then(() => {
				console.log("Connected To Database")
				resolve(this)
			})
		}.bind(this));
	})
	return promise
}
exports.MongoDB = MongoDB