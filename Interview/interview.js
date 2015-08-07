
students = require('./students.json');
constant = require('./constant.json');

another = {
	SJTU : "FDU",
	FDU : "SJTU"
};

accept_list = {
	SJTU : [],
	FDU : []
};

order_list = {
	SJTU : {
		now : 0,
		queue : []
	},
	FDU : {
		now : 0,
		queue : []
	}
};

function willing(univ, stu) {
	if (stu.state !== "free")
		return false;
	if (stu[univ + "_rejected"] === true)
		return false;
	if (univ === "FDU")
		return Math.random() > constant.SJTU_LOYALTY;
	else return true;
}

function ask(univ) {
	while ( order_list[univ].now < order_list[univ].queue.length && 
		!willing( univ, order_list[univ].queue[ order_list[univ].now ] ) ) {

		//console.log(univ + " is searching for " + order_list[univ].queue[ order_list[univ].now ].rank + " without result. =_=");
		order_list[univ].now++;
	}
	if (order_list[univ].now === order_list[univ].queue.length)
		return "over";
	else return order_list[univ].queue[ order_list[univ].now ];
}

function start_interview(univ, stu) {
	stu.state = univ + "_interviewing";
	console.log(univ + " is interviewing " + stu.rank);
}

function interview_time(univ, stu) {
	if (stu.rank >= constant[univ + "_LINE"])
		return constant[univ + "_TIME_SHORT"];
	else if(stu[univ + "_profile"])
		return constant[univ + "_TIME_MID"];
	else return constant[univ + "_TIME_LONG"];
}

function end_interview(univ, stu) {
	console.log(univ + " has now end the interview of " + stu.rank)
	if (stu[univ + "_competence"]) {
		stu.state = univ + "_accepted";
		accept_list[univ].push(stu);
		console.log(stu.rank + " is accepted by " + univ);
	} else {
		stu.state = "free";
		stu[univ + "_rejected"] = true;
		console.log(stu.rank + " is rejected by " + univ);
	}
}

function interview(univ) {
	if (accept_list[univ].length === constant[univ + "_TOTAL"]) {
		end_of_interview(univ)
		return;
	}
	var stu = ask(univ);
	if (stu === "over") {
		end_of_interview(univ)
		return;
	}
	start_interview(univ, stu);
	setTimeout(function (){
			end_interview(univ, stu);
			interview(univ);
		},
		interview_time(univ, stu)
	);
}

function SJTU_initialize(para) {
	if (para === "NOI_ORDER") {
		for (var i = 0; i < students.length; ++i) {
			if (students[i].SJTU_profile)
				order_list["SJTU"].queue.push(students[i]);
		}
		for (var i = 0; i < students.length; ++i) {
			if (students[i].SJTU_profile === false)
				order_list["SJTU"].queue.push(students[i]);
		}
	} else if (para === "PROFILE_PREFER") {
		for (var i = 0; i < students.length; ++i) {
			order_list["SJTU"].queue.push(students[i]);
		}
	}
}

function FDU_initialize() {
	for (var i = 0; i < students.length; ++i) {
		//order_list["SJTU"].queue.push(students[i]);
		order_list["FDU"].queue.push(students[i]);
		students[i].state = "free";
	}
}

function end_of_interview(univ) {
	console.log("\t" + univ + "\'s interview is over! Here is the accepting list.");
	console.log("\t" + accept_list[univ].length);
	for (var i = 0; i < accept_list[univ].length; ++i) {
		console.log("\t\t" + accept_list[univ][i].rank);
	}
}

SJTU_initialize("PROFILE_PREFER");
FDU_initialize();

interview("SJTU");
interview("FDU");