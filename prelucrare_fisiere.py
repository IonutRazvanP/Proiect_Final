import os
import shutil
import csv
import re
import time
import mysql.connector
from datetime import date
from dateutil import parser


class Fisiere():
    def __init__(self):
        self.connect_mysql = mysql.connector.connect(host="", user="", password="", database="")
        self.cursor_mysql = self.connect_mysql.cursor()


class Fisiere_txt(Fisiere):
    def read_txt(self, filename, number):
        continut = []
        with open(filename, "r") as file:
            reader = file.readlines()

            for line in reader:
                line_strip = line.strip("\n ;")
                line_split = line_strip.split(",")
                continut.append(line_split)

            for content in continut:
                ID = content[0]
                DATA_str = content[1]
                SENS = content[2]

                datetime_obj = parser.isoparse(DATA_str)
                formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

                self.cursor_mysql.execute(
                    f"INSERT INTO ACCESS VALUES ('{ID}', '{formatted_datetime}', '{SENS}', '{number}');")
                self.connect_mysql.commit()
            print("Fisierul text a fost prelucrat cu succes")


class Fisiere_csv(Fisiere):
    def read_csv(self, filename, number):
        with open(filename, "r") as file:
            fisier = csv.reader(file)
            next(fisier)
            for line in fisier:
                ID = line[0]
                DATA_str = line[1]
                SENS = line[2]

                datetime_obj = parser.isoparse(DATA_str)
                formatted_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

                self.cursor_mysql.execute(
                    f"INSERT INTO ACCESS VALUES ('{ID}', '{formatted_datetime}', '{SENS}', '{number}');")
                self.connect_mysql.commit()
            print("Fisierul csv a fost prelucrat cu succes.")


def main_function():
    path = 'C:/Users/ponci/Desktop/Proiect_Python/Intrari/'
    backup_path = 'C:/Users/ponci/Desktop/Proiect_Python/backup_intrari/'

    txt_files = [f for f in os.listdir(path) if f.endswith('.txt') and f.startswith('Poarta')]
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv') and f.startswith('Poarta')]

    txt_file = Fisiere_txt("proiect_python")
    csv_file = Fisiere_csv("proiect_python")

    today_date = date.today()

    for txt_filename in txt_files:
        number = re.search(r'Poarta(\d+)\.txt', txt_filename).group(1)
        full_txt_path = os.path.join(path, txt_filename)
        txt_file.read_txt(full_txt_path, number)
        new_txt_name = f"{path}{today_date}-Poarta{number}.txt"
        os.rename(full_txt_path, new_txt_name)
        shutil.move(new_txt_name, backup_path)

    for csv_filename in csv_files:
        number_match = re.search(r'Poarta(\d+)\.csv', csv_filename)
        if number_match:
            number = number_match.group(1)
        else:
            number = "1"

        full_csv_path = os.path.join(path, csv_filename)
        csv_file.read_csv(full_csv_path, number)

        new_csv_name = f"{path}{today_date}-Poarta{number}.csv"
        os.rename(full_csv_path, new_csv_name)
        shutil.move(new_csv_name, backup_path)


if __name__ == "__main__":
    while True:
        time.sleep(5)
