import csv

csv_file = open('chaichai.csv', 'w', encoding="utf-8", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Pardavėjas', 'Produktas', 'Kaina'])