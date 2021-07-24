function Error(system, error_name, details, pos_start, pos_end) {
	this.fn = system.fn
	this.text = system.text
	this.error_name = error_name;
	this.details = details
	this.pos_start = pos_start
	this.pos_end = pos_end
	this.toString = function() {
		let rtn = this.text.split("\n").slice(this.pos_start.line, this.pos_end.line+1) + "\n"
		let arr = []
		for (let i = 0; i < this.pos_start.col-1; i++) {
			rtn += " "
		}
		for (let i = this.pos_start.col; i < this.pos_end.col+1; i++) {
			rtn += "^"
		}
		rtn+="\n"
		rtn += this.error_name + ": " +this.details+ "\n"
		rtn += "\ton line "+(this.pos_start.line+1)+" of \'"+this.fn+"\'\n"
		
        return rtn
	}
}

function IllegalCharError(system, details, pos_start, pos_end) {
	Error.call(this, system, "Illegal Character Error", details, pos_start, pos_end);
	
	return this
}
exports.IllegalCharError = IllegalCharError


function InvalidSyntaxError(system, details, pos_start, pos_end) {
	Error.call(this, system, "Invalid Syntax Error", details, pos_start, pos_end);
	
	return this
}
exports.InvalidSyntaxError = InvalidSyntaxError