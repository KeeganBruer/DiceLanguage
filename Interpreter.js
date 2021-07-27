let Token = require("./Token.js")
let Errors = require("./Errors.js")
let Types = require("./Types.js")


function Interpreter(database) {
	this.database = database
	this.visit = async function(node) {
		return await this["visit_"+node.__name__](node)
	}.bind(this)
	this.visit_BinaryOpNode = async function(node) {
		let left_value = await this.visit(node.left_node)
		let right_value = await this.visit(node.right_node)
		if (node.op_tok == Token.TT_PLUS) {
			let new_node = left_value.added_to(right_value);
			return new_node
		} else if (node.op_tok == Token.TT_MINUS) {
			let new_node = left_value.subtracted_by(right_value);
			return new_node
		} else if (node.op_tok == Token.TT_MULT) {
			let new_node = left_value.multiplied_by(right_value);
			return new_node
		} else if (node.op_tok == Token.TT_DIV) {
			let new_node = left_value.divided_by(right_value);
			return new_node
		}
	}.bind(this)
	this.visit_UrnaryOpNode = async function(node) {
		let op_tok = node.op_tok
		let value_ = await this.visit(node.tok)
		if (node.op_tok == Token.TT_PLUS) {
			return value_
		} else if (node.op_tok == Token.TT_MINUS) {
			let new_node = value_.multiplied_by(new Types.Number(-1));
			return new_node
		}
	}.bind(this)
	this.visit_NumberNode = async function(node) {
		return new Types.Number(node.tok.value_)
	}.bind(this)
	this.visit_VarAssignNode = async function(node) {
		let value_node = await this.visit(node.tok)
		await this.database.set_var(node.identifier_tok.value_, value_node)
		return
	}.bind(this)
	this.visit_VarReassignNode = async function(node) {
		let new_var = await this.database.get_var(node.identifier_tok.value_)
		if (new_var.type_ == Types.T_Number) {
			new_var =  new Types.Number(new_var.val)
		}
		
		let value_node = await this.visit(node.tok)
		if (node.op_tok == Token.TT_EQ) {
			await this.database.set_var(node.identifier_tok.value_, value_node)
			return value_node
		} else if (node.op_tok == Token.TT_PLUSEQ) {
			new_var.added_to(value_node)
			await this.database.set_var(node.identifier_tok.value_, new_var)
			return new_var
		} else if (node.op_tok == Token.TT_MINUSEQ) {
			new_var.subtracted_by(value_node)
			await this.database.set_var(node.identifier_tok.value_, new_var)
			return new_var
		} else if (node.op_tok == Token.TT_MULTEQ) {
			new_var.multiplied_by(value_node)
			await this.database.set_var(node.identifier_tok.value_, new_var)
			return new_var
		} else if (node.op_tok == Token.TT_DIVEQ) {
			new_var.divided_by(value_node)
			await this.database.set_var(node.identifier_tok.value_, new_var)
			return new_var
		}
		
	}.bind(this)
	this.visit_VarAccessNode = async function(node) {
		return await this.database.get_var(node.identifier_tok.value_)
	}.bind(this)
	this.visit_ListNode = async function(node) {
		let statements = node.toks;
		let results = []
		for (let i = 0; i < statements.length; i++) {
			let statement = await this.visit(statements[i])
			results.push(statement)
		}
		return new Types.List(results)
	}.bind(this)
	return this
}
module.exports = Interpreter