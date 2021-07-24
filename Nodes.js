function Nodes() {}

function Node() {
	this.toString = function() {
		return ""+typeof(this)
	}
}
Node.NT_NUM 	= "NT_NUM"
Node.NT_BINOP 	= "NT_BINOP"
Node.NT_URINOP 	= "NT_URINOP"
Node.NT_LIST 	= "NT_LIST"

function NumberNode(tok) {
	Node.call(this)
	this.type_ = Node.NT_NUM
	this.tok = tok
	this.toString = function() {
		return this.tok.type_ +":" + this.tok.value_
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.NumberNode = NumberNode

function BinaryOpNode(left_tok, op_tok, right_tok) {
	Node.call(this)
	this.type_ = Node.NT_BINOP
	this.left_tok = left_tok
	this.op_tok = op_tok
	this.right_tok = right_tok
	this.toString = function() {
		let rtn = this.op_tok.toString()
		if (this.left_tok.type_ == Node.NT_BINOP || this.left_tok.type_ == Node.NT_URINOP) {
			let arr = this.left_tok.toString().split("\n")
			rtn += "\n\t"+arr[0]
			for (let i = 1; i < arr.length; i++) { 
				rtn += "\n"+arr[i].replace("\t", "\t\t")
			}
		} else {
			rtn += "\n\t" + this.left_tok.toString()
		}
		if (this.right_tok.type_ == Node.NT_BINOP || this.left_tok.type_ == Node.NT_URINOP) {
			let arr = this.right_tok.toString().split("\n")
			rtn += "\n\t"+arr[0]
			for (let i = 1; i < arr.length; i++) { 
				rtn += "\n"+arr[i].replace("\t", "\t\t")
			}
		} else {
			rtn += "\n\t" + this.right_tok.toString()
		}
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.BinaryOpNode = BinaryOpNode

function UrinaryOpNode(op_tok, tok) {
	Node.call(this)
	this.type_ = Node.NT_URINOP
	this.tok = tok
	this.op_tok = op_tok
	this.toString = function() {
		let rtn = this.op_tok.toString()
		rtn += "\n\t" + this.tok.toString()
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.UrinaryOpNode = UrinaryOpNode

function ListNode(toks) {
	Node.call(this)
	this.type_ = Node.NT_LIST
	this.toks = toks
	this.toString = function() {
		let rtn = ""
		for (let i = 0; i < this.toks.length; i++) {
			rtn += this.toks[i].toString() + ", "
		}
		return rtn
	}
	this.toString = this.toString.bind(this)
	return this
}
Nodes.ListNode = ListNode

module.exports = Nodes