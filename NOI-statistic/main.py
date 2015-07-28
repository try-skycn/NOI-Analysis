from sys import argv

def get_dict(col, info):
	dic = {}
	i = 0
	for ele in col:
		dic[ele] = info[i]
		i += 1
	return dic

gold_line = 0.15
decline_sopeed = 5
total_score = 10
def get_cof(info, total):
	rate = float(info["rank"]) / total
	if rate <= gold_line:
		return total_score
	else:
		return total_score / (1 + decline_sopeed * (rate - gold_line))

def addto_dict(dic, key, val):
	if not dic.get(key):
		dic[key] = val
	else:
		dic[key] += val


folder = "../Data/OI/"
contest_name = "apio"
contest_mode = "Contest_Data/%s%s.csv" % (contest_name, "%d")
output_name = "OI-Analysis/%s.csv" % contest_name
year_list = [2011, 2012, 2013, 2014, 2015]

prov_name = open("name.txt", "r").read().split('\n')
prov_search = get_dict( prov_name, [True] * len(prov_name) )
prov_strength = get_dict( prov_name, [0] * len(prov_name) )

for year in year_list:
	print "Dealing with year %d." % year
	input_info = open(folder + (contest_mode % year), "r").read().split('\n')
	col_info = input_info[0].split(',')
	total = len(input_info) - 1
	rank = 0
	for stu in input_info[1:]:
		rank += 1
		stu_info = get_dict(col_info, stu.split(','))
		stu_info["rank"] = rank
		addto_dict( prov_strength, stu_info["province"], get_cof(stu_info, total) )

outfile = open(folder + output_name, 'w')
outfile.truncate()
for prov, score in prov_strength.items():
	if prov_search.get(prov) != None:
		outfile.write("%s,%s\n" % (prov, score))

outfile.close()
