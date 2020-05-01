import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def check2(elem):
	if len(elem)!=0:
		if ',' in elem:
			elem = elem.replace(',','\\,')
			# print(elem)
			return (1,elem)
	if (elem=='-'):
		# print(elem)
		return (1,None)
	if (elem=='30 (Meteorite)255 (Core)'):
		# print(elem)
		return (1,30)
	return (0,elem)

def check_duplicate(r, all_rows):
	t1= r[-2]
	t2= r[-1]
	for row in all_rows:
		tt1= row[-2]
		tt2= row[-1]
		if(tt1==t1 and tt2==t2):
			return True
	return False

def normalize(name):
	if('-' in name):
		name= name.replace('-',' ')
	return name.lower()

def check_moves(name):
	with open('datasets/Allmoves_parsed.csv', "r", encoding='utf-8') as source:
		reader = csv.reader(source)
		for row in reader:
			name1=normalize(row[0])
			name2=normalize(name)
			if(fuzz.ratio(name1, name2)>94):
				print(name1,name2)
				return (1, name1)
		return(0,name2)


writer = csv.writer(open('datasets/pokemon_parsed_temp.csv', 'w', encoding='utf-8'))
rows=[]

with open('datasets/pokemon.csv', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    # print(headers)
    for row in f_csv:
    	temp=[]
    	# print(row)
    	for col in row:
    		(flag,col)=check2(col)
    		# if(flag==1):
    		# 	# print(col)
    		temp.append(col)
    	rows.append(temp)

writer.writerows(rows) 

# writer = csv.writer(open('pokemon_parsed.csv', 'w'))
row_count=0
cols_to_remove = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22,23] # Column indexes to be removed (starts at 0)
cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first

cols_to_remove2 = [0,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,40] # Column indexes to be removed (starts at 0)
cols_to_remove2 = sorted(cols_to_remove2, reverse=True) # Reverse so we remove from the end first

with open('datasets/pokemon_parsed_temp.csv', "r", encoding='utf-8') as source:
    reader = csv.reader(source)
    with open('datasets/pokemon_parsed_main.csv', "w", encoding='utf-8', newline='') as result:
    	writer = csv.writer(result)
    	for row in reader:
        	row_count += 1
        	# print('\r{0}'.format(row_count), end='') # Print rows processed
        	for col_index in cols_to_remove:
        		del row[col_index]
        	writer.writerow(row)
        	# print(len(row))
rows=[]
with open('datasets/pokemon_parsed_temp.csv', "r", encoding='utf-8') as source2:
	reader2 = csv.reader(source2)
	with open('datasets/pokemon_parsed_weakness.csv', "w", encoding='utf-8', newline='') as result:
		writer2 = csv.writer(result)
		for row in reader2:
			row_count += 1
        	# print('\r{0}'.format(row_count), end='') # Print rows processed
			for col_index in cols_to_remove2:
				del row[col_index]
			if (row[-1]==''):
				row[-1]="None"
			if (row[-2]==''):
				row[-2]="None"
			if check_duplicate(row,rows)==False:
				writer2.writerow(row)
				rows.append(row)
	# print(len(rows))


pokemonid_moveid=[]
with open('datasets/pokemon_moves.csv', "r", encoding='utf-8') as source3:
	reader3 = csv.reader(source3)
	firstline = True
	for row in reader3:
		if firstline:    #skip first line
			firstline = False
			continue
		if (row[1]=='18' and row[3]=='1'):
			# print(row)
			temp=[]
			temp.append(row[0])
			temp.append(row[2])	
			pokemonid_moveid.append(temp)

with open('datasets/moves.csv', "r", encoding='utf-8') as source4:
	reader4 = csv.reader(source4)
	firstline = True
	with open('datasets/pokemon_moves_parsed.csv', "w", encoding='utf-8', newline='') as result:
		writer3 = csv.writer(result)
		for row in reader4:
			if firstline:    #skip first line
				firstline = False
				continue
			for pid,mid in pokemonid_moveid:
				if row[0]==mid:
					# print(pid,row[0],row[1])
					(flag, name)=check_moves(row[1])
					if (flag==1):
						temp=[]
						temp.append(pid)
						temp.append(name)
						print(temp)
						writer3.writerow(temp)







