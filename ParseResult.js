function ParseResult() {
    this.error = undefined
    this.node = undefined
    this.last_registered_advance_count = 0
    this.advance_count = 0
    this.to_reverse_count = 0
    this.register = function(res) {
        this.last_registered_advance_count = res.advance_count
        this.advance_count += res.advance_count
        if (res.error) { 
			this.error = res.error
		}
        return res.node
	}
    this.register_advancement = function(){
        this.last_registered_advance_count = 1
        this.advance_count += 1
	}
    this.register_reverse = function() {
        this.last_registered_advance_count = -1
        this.advance_count -= 1
	}
    this.try_register = function(res) {
        if (res.error){
            this.to_reverse_count = res.advance_count
            return None
        } else {
            return this.register(res)
		}
	}
    this.success = function(node) {
        this.node = node
        return this
	}
    this.should_return = function() {
        if (!this.error) {
			return false
		}
		return true
	}
    this.failure = function(error) {
        if (!this.error || this.advance_count == 0) {
            this.error = error
		}
        return this
	}
	this.toString = function() {
		let rtn = this.node.toString()
		return rtn;
	}
}
module.exports = ParseResult