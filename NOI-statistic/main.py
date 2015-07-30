from sys import argv

def get_dict(col, info):
	dic = {}
	i = 0
	for ele in col:
		dic[ele] = info[i]
		i += 1
	return dic

def dict_init(lst, val):
	dic = {}
	for ele in lst:
		dic[ele] = val
	return dic

gold_line = 0.15
decline_sopeed = 5.0
total_score = 10.0
def get_cof(info, total):
	rate = float(info["rank"]) / float(total)
	if rate <= gold_line:
		return total_score
	else:
		return total_score / (1.0 + decline_sopeed * (rate - gold_line))

def addto_dict(dic, key, val):
	if not dic.get(key):
		dic[key] = val
	else:
		dic[key] += val

def calc_strength(filename, name_list):
	res = dict_init(name_list, 0.0)
	content = open(filename).read().split('\n')
	col_info = content[0].split(',')
	total = len(content) - 1
	rank = 0
	for stu in content[1:]:
		rank += 1
		stu_info = get_dict( col_info, stu.split(',') )
		stu_info["rank"] = rank
		if res.get( stu_info["province"] ) != None:
			res[stu_info["province"]] += get_cof(stu_info, total)
	return res

prov_list = open("name.txt").read().split('\n')
root_folder = "../Data/"
input_file = root_folder + "OI/Contest_Data/%s%d.csv"
output_file = root_folder + "Time_Dependency/Output/%s.csv"
contest_info = {
	"wc" : [2012, 2013, 2015],
	"noi" : [2011, 2012, 2013, 2014],
	"apio" : [2011, 2012, 2013, 2014],
	"ctsc" : [2011, 2012, 2013, 2014]
}
contest_result = {}

for contest, year_list in contest_info.items():
	contest_result[contest] = {}
	for year in year_list:
		contest_result[contest][year] = calc_strength(input_file % (contest, year), prov_list)

for contest, year_list in contest_info.items():
	output = open(output_file % contest, "w")
	output.truncate()
	for prov in prov_list:
		output.write(prov)
		for year in year_list:
			output.write( ",%lf" % contest_result[contest][year][prov] )
		output.write("\n")
	output.close()

