import mysql.connector
from datetime import timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time


def send_email(subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''

    from_email = ""
    to_email = ""

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())


def calculate_time_difference(intrari, iesiri):
    time_diffs = []
    for intrare, iesire in zip(intrari, iesiri):
        diff = iesire - intrare
        time_diffs.append(diff)
    return time_diffs


def format_hours_and_minutes(delta):
    total_minutes = delta.total_seconds() / 60
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return f"{hours} ore și {minutes} minute"


def main_ore_email():
    try:
        connection = mysql.connector.connect(
            host="", user="", password="", database="")

        if connection.is_connected():
            print("Conexiunea la baza de date a fost realizată.")

            cursor = connection.cursor()

            query = "SELECT id, data, sens FROM access ORDER BY id, data"
            cursor.execute(query)

            rows = cursor.fetchall()
            current_id = None
            intrari = []
            iesiri = []

            insufficient_hours = {}

            for row in rows:
                id, data, sens = row
                if current_id is None:
                    current_id = id

                if id != current_id:
                    if intrari and iesiri:
                        time_diffs = calculate_time_difference(intrari, iesiri)
                        total_time = sum(time_diffs, timedelta())
                        if total_time.total_seconds() < 8 * 60 * 60:  # 8 ore in secunde
                            if current_id not in insufficient_hours:
                                insufficient_hours[current_id] = []
                            insufficient_hours[current_id].append(
                                (total_time, data))
                    current_id = id
                    intrari = []
                    iesiri = []

                if sens == "in":
                    intrari.append(data)
                elif sens == "out":
                    iesiri.append(data)

            #ultimul calcul pt id.
            if intrari and iesiri:
                time_diffs = calculate_time_difference(intrari, iesiri)
                total_time = sum(time_diffs, timedelta())
                if total_time.total_seconds() < 8 * 60 * 60:  # 8 ore in secunde
                    if current_id not in insufficient_hours:
                        insufficient_hours[current_id] = []
                    insufficient_hours[current_id].append((total_time, data))

            if insufficient_hours:
                email_message = "ID-urile utilizatorilor care au lucrat sub 8 ore:\n"
                for id, records in insufficient_hours.items():
                    for total_time, date in records:
                        formatted_time = format_hours_and_minutes(total_time)
                        formatted_date = date.strftime('%d.%m.%Y')
                        email_message += f"id {id}: {formatted_time} in data de {formatted_date}\n"

                send_email("Raport Ore Insuficiente", email_message)
                print("Email trimis cu ID-uri cu ore insuficiente:\n", email_message)

    except mysql.connector.Error as error:
        print("Eroare MySQL:", error)
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Conexiunea la baza de date a fost inchisă.")


schedule.every().day.at("12:07").do(main_ore_email)
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)