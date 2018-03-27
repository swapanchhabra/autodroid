import os

comment_list = []
count = 0

out_f = open('testcase.command', 'w')

with open("action.command") as f:
    for line in f:
    	if line.startswith('sleep'):
    		out_f.write(line)
    		continue
    	count = count + 1
        os.system(line)
        get_comment = raw_input('Input Command and press enter: ')
        comment_list.append(get_comment)
        out_f.write(line)
        if get_comment != "":
        	out_f.write(get_comment)
        	out_f.write("\n")
#print comment_list