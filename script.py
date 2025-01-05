# it runs everyday at 7am
# if todays date string is the same with the keys of any of the data, it returns the value for that day.

import sqlite3 
from datetime import date
import json
import smtplib
import os
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv
from flask import Flask
app = Flask(__name__)

load_dotenv()

# yy/mm/dd
example_date = date(2025, 12, 2)
# today = date.today()

''' monthly_goals = {
    "2025-01-06": {
        "Brand Development": "Create logo and brand statements",
        "Banana Bliss": "Implement payment section",
        "ServiceTrove": "Finalize MVP criteria and project deliverables",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-01-13": {
        "Brand Development": "Finalize themes, colors, and fonts",
        "Banana Bliss": "Security audit and testing",
        "ServiceTrove": "Begin backend development",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-01-20": {
        "Brand Development": "Set up social media accounts",
        "Banana Bliss": "Deploy to custom domain",
        "ServiceTrove": "Continue backend development",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-01-27": {
        "Brand Development": "Create and post initial content",
        "ServiceTrove": "Start API integration",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-02-03": {
        "Reading": "Complete first book",
        "ServiceTrove": "Continue API integration",
        "Udemy Course": "Begin material collection",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-02-10": {
        "ServiceTrove": "Backend development",
        "Udemy Course": "Organize course materials",
        "Learning": "Start TypeScript journey",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-02-17": {
        "ServiceTrove": "Complete backend features",
        "Udemy Course": "Start creating course outline",
        "Learning": "Continue TypeScript journey",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-02-24": {
        "ServiceTrove": "Finalize API integration",
        "Udemy Course": "Begin note-taking",
        "Learning": "TypeScript practice projects",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-03-03": {
        "ServiceTrove": "Start frontend development",
        "Udemy Course": "Continue note creation",
        "Learning": "Start Docker journey",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-03-10": {
        "ServiceTrove": "Frontend development continues",
        "Udemy Course": "Begin slide creation",
        "Learning": "Docker practice exercises",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-03-17": {
        "ServiceTrove": "Frontend features implementation",
        "Udemy Course": "Complete lesson notes",
        "Learning": "Continue Docker journey",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-03-24": {
        "ServiceTrove": "Begin testing phase",
        "Udemy Course": "Finalize slides",
        "Learning": "Container management practice",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-03-31": {
        "ServiceTrove": "Begin testing phase",
        "Udemy Course": "Finalize slides",
        "Learning": "Container management practice",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-04-07": {
        "Reading": "Complete second book",
        "ServiceTrove": "Final testing",
        "Udemy Course": "Set up recording environment",
        "Learning": "Start AWS journey",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-04-14": {
        "ServiceTrove": "Deployment preparation",
        "Udemy Course": "Begin video recording",
        "Learning": "AWS fundamentals practice",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-04-21": {
        "ServiceTrove": "Launch application",
        "Udemy Course": "Continue recording",
        "Learning": "Explore AWS services",
        "Daily": "Read 3 chapters of gospel"
    },
    "2025-04-28": {
        "ServiceTrove": "Post-launch monitoring",
        "Udemy Course": "Recording progress",
        "Learning": "AWS practical projects",
        "Daily": "Complete gospel reading"
    },
    "2025-05-05": {
        "Udemy Course": "Continue video recording",
        "Learning": "Start basic video editing",
        "Journey": "Begin AI/ML journey"
    },
    "2025-05-12": {
        "Udemy Course": "Complete recordings",
        "Learning": "Progress with video editing",
        "Journey": "Continue AWS and AI/ML learning"
    },
    "2025-05-19": {
        "Udemy Course": "Focus on editing",
        "Video": "Final refinements",
        "Journey": "AI/ML fundamentals study"
    },
    "2025-05-26": {
        "Udemy Course": "Complete all editing",
        "Course": "Final material review",
        "Learning": "Deepen AI/ML knowledge"
    },
    "2025-06-02": {
        "Reading": "Complete third book",
        "Udemy Course": "Final touches",
        "Learning": "Advanced AI/ML concepts"
    },
    "2025-06-09": {
        "Udemy Course": "Platform submission",
        "Learning": "Course launch preparation",
        "Journey": "AI/ML practical applications"
    },
    "2025-06-16": {
        "Monitoring": "Monitor course performance",
        "Feedback": "Gather initial feedback",
        "Project": "AI/ML project work"
    },
    "2025-06-23": {
        "Promotion": "Course promotion activities",
        "Support": "Address student questions",
        "Learning": "Complete AI/ML goals"
    }
}
'''


#! This is where i create my SQLite file and connect to the DB
file = "goals.db"
# connect to SQLite DB
try:
    connection = sqlite3.connect(file)
    print("Connected to SQLite")
except sqlite3.Error as error:
    print("Failed to connect with sqlite3 database", error) 


#! This is where i try to convert what i have in the "monthly_goals" dictionary into sql format and save it into the SQLite DB
# cursor = connection.cursor()

# # Create the table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS weekly_goals (
#         date TEXT PRIMARY KEY,
#         goals TEXT
#     )
# ''')

# # Loop through the monthly_goals dictionary and insert the data
# for dates, goals in monthly_goals.items():
#     # Convert the 'goals' dictionary to a JSON string
#     goals = json.dumps(goals)
    
#     # Use placeholders in the SQL query to safely insert values
#     cursor.execute('''
#         INSERT OR REPLACE INTO weekly_goals (date, goals)
#         VALUES (?, ?)
#     ''', (dates, goals))  # Use the values of 'date' and 'goals' here

# # Commit the transaction
# connection.commit()





# declare the auto goals function. This is the function that will get todays date, get the message if theres a message for today and then send the message via mail.

#! i want split the function to get helper functions

# function to get the message
def get_message():
    try:
        # today = str(date.today())
        today = '2025-01-06'

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
    

# function to send the email
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



# def auto_goals():
#     sender_email = os.getenv("SENDER_EMAIL_ID")
#     sender_password = os.getenv("SENDER_EMAIL_ID_PASSWORD")
#     receiver_email = os.getenv("RECEIVER_EMAIL_ID")

#     try:
#         # get message
#         message = get_message()
#         # print(f"Retrieved message: {message}")

#         # send email
#         if message:
#             send_mail(
#                 sender_email_id=sender_email, 
#                 sender_email_id_password=sender_password, 
#                 receiver_email_id=receiver_email, 
#                 message=message
#                 )
#     except Exception as e:
#         return (f"An error occurred: {e}")
    
    

#  # call the auto goals function
# auto_goals()




@app.route('/')
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


if __name__ == '__main__':
    app.run()

