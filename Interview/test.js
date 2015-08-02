
function foo(univ) {
	setTimeout(
		function(){
			console.log(univ);
			console.log(new Date);
		},
		3000
	)
}
console.log(new Date);
setTimeout(
	function(){
		foo("FDU");
	},
	1000
);
foo("SJTU");
