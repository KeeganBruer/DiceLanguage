function Position(lexar, idx, line, col) {
	this.idx = idx != undefined ? idx : -1
	this.line = line != undefined ? line : 0
	this.col = col != undefined ? col : 0
	this.lexar = lexar != undefined ? lexar : null
	this.fn = lexar.fn != undefined ? lexar.fn : ""
	this.increase = function() {
		this.idx += 1
		this.col += 1
		if (this.lexar.current_char == "\n") {
			this.line += 1
			this.col = 0
		}
	}
	this.copy = function() {
		return new Position(this.lexar, this.idx, this.line, this.col)
	}
	return this
}

module.exports = Position