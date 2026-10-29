import csv

with open('../MetObjects.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for i, row in enumerate(reader):
        if i >= 20:
            break
        print(', '.join(row))