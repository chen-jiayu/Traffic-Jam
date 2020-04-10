import csv
with open('train.csv' , newline='') as csvFile:
    rows = csv.DictReader(csvFile)
    # for row in rows:
    # 	print(row)


with open('newfile.csv' , 'w' , newline='') as csvFile1:
	writer = csv.writer(csvFile1)
	writer.writerow(['acqic'])
	# writer = csv.DictWriter(csvFile, fieldNames)
	# writer.writeheader()

	for row in rows:
		if row['fraud_ind'] == 1:
			writer.writerow(row['acqic'])

csvFile.close()
print("end")
