import csv
easy_words=[]
medium_words=[]
hard_words=[]

with open("easy.csv","r") as file:
	reader = csv.reader(file)
	for row in reader:
		# txt= str(row).lower()
		easy_words.append(row[0])
	file.close()

with open("medium.csv","r") as file:
	reader = csv.reader(file)
	for row in reader:
		medium_words.append(row[0])
	file.close()

with open("hard.csv","r") as file:
	reader = csv.reader(file)
	for row in reader:
		hard_words.append(row[0])
	file.close()


