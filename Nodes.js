function Nodes() {}

function Node() {
	this.toString = function() {
		return ""+typeof(this)
	}
}

function NumberNode(tok) {
	Node.call(this)
	this.tok = tok
	this.toString = function() {
		return "num " + this.tok.value_
	}
}
Nodes.NumberNode = NumberNode
function ListNode(toks) {
	Node.call(this)
	this.toks = toks
	this.toString = function() {
		let rtn = ""
		for (let i = 0; i < this.toks.length; i++) {
			rtn += this.toks[i].toString() + ", "
		}
		return rtn
	}
}
Nodes.ListNode = ListNode

module.exports = Nodes