# var DisCountRate = function() {
# 	DisCountRate.prototype.lp00={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp01={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp02={year:"0.0600",month:"0.0060"};
# 	DisCountRate.prototype.lp03={year:"0.0600",month:"0.0060"};
# 	DisCountRate.prototype.lp10={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp11={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp13={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp20={year:"0.1250",month:"0.0090"};
# 	DisCountRate.prototype.lp21={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp23={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp30={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp31={year:"0.1000",month:"0.0110"};
# 	DisCountRate.prototype.lp32={year:"0.1000",month:"0.0060"};
# 	DisCountRate.prototype.lp33={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp40={year:"0.1600",month:"0.0140"};
# 	DisCountRate.prototype.lp41={year:"0.1600",month:"0.0140"};
# 	DisCountRate.prototype.lp43={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp50={year:"0.1250",month:"0.0090"};
# 	DisCountRate.prototype.lp51={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp53={year:"0.1250",month:"0.0090"};
# 	DisCountRate.prototype.lp60={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp61={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp63={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp70={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp71={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp73={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp80={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp81={year:"0.1250",month:"0.0110"};
# 	DisCountRate.prototype.lp82={year:"0.1000",month:"0.0060"};
# 	DisCountRate.prototype.lp83={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp90={year:"0.1000",month:"0.0090"};
# 	DisCountRate.prototype.lp91={year:"0.1000",month:"0.0110"};
# 	DisCountRate.prototype.getDisCountRatebyMonth=function(code){
# 		var fee = 0;
# 		var tmpCode = ["00","01","02","03","10","11","13","20","21","23","30","31","32","33","40","41","43","50","51","53","60","61","63","70","71","73","80","81","82","83","90","91"];
# 		if($.inArray(code,tmpCode)>-1){
# 			return this["lp"+code].month;
# 		}
# 		else{
# 			return fee;
# 		}
# 	}
# 	DisCountRate.prototype.getDisCountRatebyYear=function(code){
# 		var fee = 0;
# 		var tmpCode = ["00","01","02","03","10","11","13","20","21","23","30","31","32","33","40","41","43","50","51","53","60","61","63","70","71","73","80","81","82","83","90","91"];
# 		if($.inArray(code,tmpCode)>-1){
# 			return this["lp"+code].year;
# 		}
# 		else{
# 			return fee;
# 		}
# 	}
# };