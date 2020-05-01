import csv

def check1(elem):
	if len(elem)!=0:
		if ',' in elem:
			elem = elem.replace(',','\\,')
			# print(elem)
			return (1,elem)
	if (elem=='-'):
		print(elem)
		return (1,None)
	if (elem=='∞'):
		return (1,999)
	return (0,elem)

writer = csv.writer(open('datasets/AllMoves_parsed.csv', 'w'))
rows=[]
with open('datasets/All_Moves.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    print(headers)
    for row in f_csv:
    	temp=[]
    	for col in row:
    		(flag,col)=check1(col)
    		if(flag==1):
    			print(col)
    		temp.append(col)
    	rows.append(temp)

writer.writerows(rows)    	


