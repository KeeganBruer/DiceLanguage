function Error( error_name, details, pos_start, pos_end) {
	this.error_name = error_name;
	this.details = details
	this.pos_start = pos_start
	this.pos_end = pos_end
	this.toString = function() {
		let rtn = "=="+this.error_name + "== \n" +this.details+ "\n"
        //rtn += " " * 4 + "File \'{0}\', line {1}\n".format(this.pos_start.fn, this.pos_start.line+1)
        return rtn
	}
}

function IllegalCharError(details, pos_start, pos_end) {
	Error.call(this, "Illegal Character Error", pos_start, pos_end);
	
	return this
}
function InvalidSyntaxError(details, pos_start, pos_end) {
	Error.call(this, "Invalid Syntax Error", pos_start, pos_end);
	
	return this
}
exports.IllegalCharError = IllegalCharError