# This is a script that is triggered by a cron job to send weekly goals(tasks) to an email.

import sqlite3 
from datetime import date
import json
import smtplib
import os
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv

# load environment variables
load_dotenv()


#! This is where i create my SQLite file and connect to the DB
# connect to SQLite DB
file = "goals.db"
try:
    connection = sqlite3.connect(file, check_same_thread=False)
    print("Connected to SQLite")
except sqlite3.Error as error:
    print("Failed to connect with sqlite3 database", error) 
 

# ! This is the function that will get todays date, and get the message if theres a message for today
def get_message():
    try:
        today = str(date.today())
        # today = '2025-01-06'

        #! fetch the message from SQLite
        cursor = connection.cursor()

        query = "SELECT * FROM weekly_goals WHERE date = ?"

        cursor.execute(query, (today,))

        results = cursor.fetchall()

        for row in results:
            # Extract the JSON string (second item in tuple)
            json_data = row[1]
            # Parse JSON string to dictionary
            goals = json.loads(json_data)
            # Format the dictionary into a readable string
            formatted_message = "Weekly Goals:\n\n"
            for category, task in goals.items():
                formatted_message += f"- {category}: {task}\n"
            return formatted_message
        
    except Exception as e:
        return (f"An error occurred: {e}")
    

# !function to send the email
def send_mail(sender_email_id, sender_email_id_password,receiver_email_id, message):
    try:

        subject = "Goals for the week"
        body = message

        em = EmailMessage()
        em['From'] = sender_email_id
        em['To'] = receiver_email_id
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender_email_id, sender_email_id_password)
            # smtp.send_message(em)
            smtp.sendmail(sender_email_id, receiver_email_id, em.as_string())
            print("Email sent successfully!")
    except Exception as e:
        return print(f"An error occurred: {e}")



def auto_goals():
    sender_email = os.getenv("SENDER_EMAIL_ID")
    sender_password = os.getenv("SENDER_EMAIL_ID_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL_ID")

    try:
        # get message
        message = get_message()
        # print(f"Retrieved message: {message}")

        # send email
        if message:
            send_mail(
                sender_email_id=sender_email, 
                sender_email_id_password=sender_password, 
                receiver_email_id=receiver_email, 
                message=message
                )
        return "Script executed successfully!", 200 
    except Exception as e:
        return (f"An error occurred: {e}")


# call the auto_goals function
auto_goals()