function Nodes() {}

function Node() {
	this.toString = function() {
		return ""+typeof(this)
	}
}
Nodes.NT_IF 			= "NT_IF"
Nodes.NT_NUM 		= "NT_NUM"
Nodes.NT_STRING 		= "NT_STRING"
Nodes.NT_BINOP 		= "NT_BINOP"
Nodes.NT_URINOP 		= "NT_URINOP"
Nodes.NT_LIST 		= "NT_LIST"
Nodes.NT_VarReassign = "NT_VarReassign"
Nodes.NT_VarAssign 	= "NT_VarAssign"
Nodes.NT_VarAccess 	= "NT_VarAccess"

function IfNode(expr, statements) {
	Node.call(this)
	this.type = Nodes.NT_IF
	this.__name__ = "IfNode"
	this.expr = expr
	this.statements = statements
	this.pos_start = this.expr.pos_start
	this.pos_end = this.statements[statements.length-1].pos_end
	this.toString = function() {
		let rtn = this.type_ 
		let arr = this.expr.toString().split("\n")
		rtn += "\n\t\t"+arr[0]
		for (let i = 1; i < arr.length; i++) { 
			rtn += "\n"+arr[i].replace("\t", "\t\t\t")
		}
		
		arr = this.statements.toString().split("\n")
		rtn += "\n\tSTATEMENTS"
		for (let i = 1; i < arr.length; i++) { 
			rtn += "\n"+arr[i].replace("\t", "\t\t")
		}
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.IfNode = IfNode

function NumberNode(tok) {
	Node.call(this)
	this.type = Nodes.NT_NUM
	this.__name__ = "NumberNode"
	this.tok = tok
	this.pos_start = this.tok.pos_start
	this.pos_end = this.tok.pos_end
	this.toString = function() {
		return this.type +":" + this.tok.value_
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.NumberNode = NumberNode

function StringNode(tok) {
	Node.call(this)
	this.type = Nodes.NT_STRING
	this.__name__ = "StringNode"
	this.tok = tok
	this.pos_start = this.tok.pos_start
	this.pos_end = this.tok.pos_end
	this.toString = function() {
		return this.type +":" + this.tok.value_
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.StringNode = StringNode

function VarAssignNode(identifier_tok, tok) {
	Node.call(this)
	this.type = Nodes.NT_VarAssign
	this.__name__ = "VarAssignNode"
	this.identifier_tok = identifier_tok
	this.tok = tok
	this.pos_start = this.identifier_tok.pos_start
	this.pos_end = this.tok.pos_end
	this.toString = function() {
		return this.type +": " +this.identifier_tok + " = " + this.tok
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.VarAssignNode = VarAssignNode

function VarReassignNode(identifier_tok, op_tok, tok) {
	Node.call(this)
	this.type = Nodes.NT_VarReassign
	this.__name__ = "VarReassignNode"
	this.identifier_tok = identifier_tok
	this.op_tok = op_tok
	this.tok = tok
	this.pos_start = identifier_tok.pos_start
	this.pos_end = tok.pos_end
	this.toString = function() {
		return this.type +": " +this.identifier_tok + " - " + this.op_tok +" - " + this.tok
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.VarReassignNode = VarReassignNode

function VarAccessNode(identifier_tok) {
	Node.call(this)
	this.type = Nodes.NT_VarAccess
	this.__name__ = "VarAccessNode"
	this.identifier_tok = identifier_tok
	this.pos_start = identifier_tok.pos_start
	this.pos_end = identifier_tok.pos_end
	this.toString = function() {
		return this.type +": " +this.identifier_tok 
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.VarAccessNode = VarAccessNode

function BinaryOpNode(left_tok, op_tok, right_tok) {
	Node.call(this)
	this.type = Nodes.NT_BINOP
	this.__name__ = "BinaryOpNode"
	this.left_node = left_tok
	this.op_tok = op_tok
	this.right_node = right_tok
	this.pos_start = this.left_node.pos_start
	this.pos_end = this.right_node.pos_end
	this.toString = function() {
		let rtn = this.op_tok.toString()
		if (this.left_node.type == Nodes.NT_BINOP || this.left_node.type == Nodes.NT_URINOP) {
			let arr = this.left_node.toString().split("\n")
			rtn += "\n\t"+arr[0]
			for (let i = 1; i < arr.length; i++) { 
				rtn += "\n"+arr[i].replace("\t", "\t\t")
			}
		} else {
			rtn += "\n\t" + this.left_node.toString()
		}
		if (this.right_node.type == Nodes.NT_BINOP || this.right_node.type == Nodes.NT_URINOP) {
			let arr = this.right_node.toString().split("\n")
			rtn += "\n\t"+arr[0]
			for (let i = 1; i < arr.length; i++) { 
				rtn += "\n"+arr[i].replace("\t", "\t\t")
			}
		} else {
			rtn += "\n\t" + this.right_node.toString()
		}
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.BinaryOpNode = BinaryOpNode

function UrnaryOpNode(op_tok, tok) {
	Node.call(this)
	this.type = Nodes.NT_URINOP
	this.__name__ = "UrnaryOpNode"
	this.tok = tok
	this.op_tok = op_tok
	this.pos_start = this.op_tok.pos_start
	this.pos_end = this.tok.pos_end
	this.toString = function() {
		let rtn = this.op_tok.toString()
		rtn += "\n\t" + this.tok.toString()
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.UrnaryOpNode = UrnaryOpNode

function ListNode(toks) {
	Node.call(this)
	this.type = Nodes.NT_LIST
	this.__name__ = "ListNode"
	this.toks = toks
	this.pos_start = this.toks[0].pos_start
	this.pos_end = this.toks[toks.length-1].pos_end
	this.toString = function() {
		let rtn = this.type
		for (let i = 0; i < this.toks.length; i++) {
			let arr = this.toks[i].toString().split("\n")
			rtn += "\n\t"+arr[0]
			for (let i = 1; i < arr.length; i++) { 
				rtn += "\n"+arr[i].replace("\t", "\t\t")
			}
		}
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.ListNode = ListNode

module.exports = Nodes