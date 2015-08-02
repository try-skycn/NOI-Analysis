import random
import types
filename = "students.json"

total_students = 50

rank_line = {
	"SJTU" : 15,
	"FDU" : 25
}

prob_cof = {
	"SJTU" : 0.975,
	"FDU" : 0.985
}

profile_prob = {
	"SJTU" : 0.3,
	"FDU" : 0.1
}

def calc_prob(univ, stulist):
	for i in range(0, rank_line[univ]):
		stulist[i][univ + "_competence"] = True
		stulist[i][univ + "_profile"] = True

	prob = 1
	for i in range(rank_line[univ], total_students):
		prob *= prob_cof[univ]
		stulist[i][univ + "_competence"] = random.random() < prob
		if stulist[i][univ + "_competence"]:
			stulist[i][univ + "_profile"] = random.random() < profile_prob[univ]
		else:
			stulist[i][univ + "_profile"] = False

def union_dict(dic, rank):
	ret = ""
	ret += "\t{\n"

	lst = []
	for name, val in dic.items():
		STR = "\t\t\"%s\" : " % name
		if val:
			STR += "true"
		else:
			STR += "false"
		lst.append(STR)
	lst.append("\t\t\"rank\" : %d" % rank)

	ret += ",\n".join(lst)
	ret += "\n\t}"
	return ret

stulist = []
for i in range(0, total_students):
	stulist.append({})

calc_prob("SJTU", stulist)
calc_prob("FDU", stulist)


stu_object_list = []
for i in range(0, total_students):
	stu_object_list.append(union_dict(stulist[i], i + 1))

#print stu_object_list
output_file = open(filename, "w")
output_file.write("[\n" + ",\n".join(stu_object_list) + "\n]\n")
output_file.close()