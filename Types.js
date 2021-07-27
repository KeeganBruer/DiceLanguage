function Type(type_) {
	this.type_ = type_
}
module.exports = Type
Type.T_Number = "Number"
Type.T_List = "List"
Type.T_String = "String"

function Number(val) {
	Type.call(this, Type.T_Number)
	this.val = val
	this.added_to = function(node) {
		if (node.type_ == "Number") {
			this.val += node.val
			return this
		}
	}.bind(this)
	this.subtracted_by = function(node) {
		if (node.type_ == "Number") {
			this.val -= node.val
			return this
		}
		
	}.bind(this)
	this.multiplied_by = function(node) {
		if (node.type_ == "Number") {
			this.val *= node.val
			return this
		}
		
	}.bind(this)
	this.divided_by = function(node) {
		if (node.type_ == "Number") {
			this.val /= node.val
			return this
		}
		
	}.bind(this)
	this.toString = function() {
		return ""+this.val + "";
	}.bind(this)
}
Type.Number = Number

function String(val) {
	Type.call(this, Type.T_String)
	this.val = val
	this.added_to = function(node) {
		if (node.type_ == "Number") {
			this.val += node.val
			return this
		}
	}.bind(this)
	this.subtracted_by = function(node) {
		if (node.type_ == "Number") {
			this.val -= node.val
			return this
		}
		
	}.bind(this)
	this.multiplied_by = function(node) {
		if (node.type_ == "Number") {
			this.val *= node.val
			return this
		}
		
	}.bind(this)
	this.divided_by = function(node) {
		if (node.type_ == "Number") {
			this.val /= node.val
			return this
		}
		
	}.bind(this)
	this.toString = function() {
		return ""+this.val + "";
	}.bind(this)
}
Type.String = String

function List(items) {
	Type.call(this, Type.T_List)
	this.items = items
	this.added_to = function(node) {
		if (node.type_ == "Number") {
			return this
		}
	}.bind(this)
	this.subtracted_by = function(node) {
		if (node.type_ == "Number") {
			return this
		}
		
	}.bind(this)
	this.multiplied_by = function(node) {
		if (node.type_ == "Number") {
			return this
		}
		
	}.bind(this)
	this.divided_by = function(node) {
		if (node.type_ == "Number") {
			return this
		}
		
	}.bind(this)
	this.toString = function() {
		return "["+this.items.toString() + "]";
	}.bind(this)
}
Type.List = List