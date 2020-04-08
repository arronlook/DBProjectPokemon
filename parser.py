import csv

def check(elem):
	if len(elem)!=0:
		if ',' in elem:
			elem = elem.replace(',','\\,')
			# print(elem)
			return (1,elem)
	return (0,elem)

writer = csv.writer(open('AllMoves_parsed.csv', 'w'))
rows=[]
with open('AllMoves.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    print(headers)
    for row in f_csv:
    	temp=[]
    	for col in row:
    		(flag,col)=check(col)
    		if(flag==1):
    			print(col)
    		temp.append(col)
    	rows.append(temp)

writer.writerows(rows)    	


