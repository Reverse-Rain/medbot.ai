
import telebot
import datetime
import mysql.connector
import threading
import time

bot_token= "6254586187:AAGOdBfyQyk6UMoowW494xuOXM2VYrldkF4"
bot = telebot.TeleBot(bot_token)

reminder_data = {}
print("reminder file starting...")

# Connect to the MySQL database
cnx = None
cursor = None

try:
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mes20ad048",
        database="reminders"
    )

    cursor = cnx.cursor()

    # Create the reminders table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                      (chat_id INT, medicine_name VARCHAR(255), reminder_datetime DATETIME)''')
    cnx.commit()

    print("Database connection successful")

except mysql.connector.Error as err:
    print("Database connection error:", err)
    exit()


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Welcome to Medicine Reminder Bot!\n\n"
                              "Please enter what you want to remind ")


@bot.message_handler(func=lambda message: True)
def set_reminder(message):
    chat_id = message.chat.id
    user_input = message.text

    if chat_id not in reminder_data:
        # Expecting medicine name
        reminder_data[chat_id] = {'medicine_name': user_input}
        bot.send_message(chat_id, "Please enter the time to remind (in HH:MM AM/PM format).")
        print(reminder_data[chat_id])
    elif 'reminder_time' not in reminder_data[chat_id]:
        # Expecting reminder time
        try:
            reminder_time = datetime.datetime.strptime(user_input, '%I:%M %p').time()
            reminder_data[chat_id]['reminder_time'] = reminder_time
            bot.send_message(chat_id, "Please enter the date to remind (in DD-MM-YYYY format).")
        except ValueError:
            bot.send_message(chat_id, "Please enter the time in HH:MM AM/PM format.")
    # Rest of the code remains the same
    else:
        # Expecting reminder date
        try:
            reminder_date = datetime.datetime.strptime(user_input, '%d-%m-%Y').date()
            reminder_time = reminder_data[chat_id]['reminder_time']
            reminder_datetime = datetime.datetime.combine(reminder_date, reminder_time)

            if reminder_datetime <= datetime.datetime.now():
                bot.send_message(chat_id, "Invalid reminder date or time. Please provide a future date and time.")
            else:
                reminder_data[chat_id]['reminder_datetime'] = reminder_datetime

                # Insert reminder data into the database
                query = "INSERT INTO reminders (chat_id, medicine_name, reminder_datetime) VALUES (%s, %s, %s)"
                values = (chat_id, reminder_data[chat_id]['medicine_name'], reminder_datetime)
                cursor.execute(query, values)
                cnx.commit()

                bot.send_message(chat_id, "Reminder set successfully!")

        except ValueError:
            bot.send_message(chat_id, "Please enter the date in DD-MM-YYYY format.")
            bot.send_message(chat_id, "Please enter the date to take the medicine (in DD-MM-YYYY format).")


def check_reminders():
    while True:
        # Retrieve reminders from the database
        current_time = datetime.datetime.now()
        cursor.execute("SELECT chat_id, medicine_name FROM reminders WHERE reminder_datetime <= %s", (current_time,))
        reminders = cursor.fetchall()

        for reminder in reminders:
            chat_id, medicine_name = reminder
            bot.send_message(chat_id, f"It's time for  {medicine_name}!")

        # Remove expired reminders from the database
        cursor.execute("DELETE FROM reminders WHERE reminder_datetime <= %s", (current_time,))
        cnx.commit()

        # Sleep for 1 minute before checking reminders again
        time.sleep(60)


if __name__ == "__main__":
    # Start the reminders checking loop in a separate thread
    reminders_thread = threading.Thread(target=check_reminders)
    reminders_thread.start()
    print("reminder file running...")

    bot.polling()
