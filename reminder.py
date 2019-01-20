import csv
import sys
import smtplib
from datetime import datetime

# Message variable left at the top for easy editing access for users
message = "Subject: Birthday Reminder: %s's birthday on %s.\n\nHi %s,\nThis is a reminder that %s will be " \
                  "celebrating their birthday on %s.\nThere are 7 days left to get a present!"


def not_null(ind, cell, head):
    # Check if cell has any data, if not, inform user where the data is missing, exit the script
    if cell:  # Since the task does not ask us to validate name and email data, we only check if it's available
        return cell
    else:
        print("Error in row", ind+2, "- missing", head)
        f.close()
        sys.exit()


def generate_birthday_rows():
    # Generate and return a list of row indexes that will have a birthday in 7 days
    today = datetime.today()
    needed_rows = []  # A list of birthday rows we'll be returning
    for i, list_date in enumerate(dates):
        birthday = list_date
        birthday = birthday.replace(year=today.year)  # Replacing original birthday year to current year
        if birthday < today:
            # If the birthday has already passed this year, we increase the year by 1 so we would always count positive
            birthday = birthday.replace(year=today.year+1)
        time_to_birthday = birthday - today
        if time_to_birthday.days == 6:  # 7 days will always be represented as 6 days + some hours, hence == to 6
            needed_rows.append(i)
    return needed_rows


def send_emails(index_list):
    # Sender log in information and email smtp server information
    from_email = "dvcodingemail@gmail.com"
    password = "learningpython"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Security function, needed to connect to the Gmail server
    server.login(from_email, password)  # Loging to the server
    # Preparing bd variable, which will show the birthday date for our emails (we know it will be in 7 days from today)
    today = datetime.today()
    bd = today.replace(day=today.day + 7)
    # Looping through our birthday index list in case there are more than one birthday in a week
    for ind in index_list:
        # Creating temporary copies to modify the lists as needed without affecting the original data
        temp_names = names.copy()
        temp_emails = emails.copy()
        # Removing birthday person information from the temporary mailing lists
        del temp_names[ind]
        del temp_emails[ind]
        print("\nSending emails to notice of %s's birthday:\n" % names[ind])
        # Adding another loop, because the task requires to address each recipient by name. Otherwise could do without
        for name, email in zip(temp_names, temp_emails):
            # All the custom variables from the emails message template are assigned here
            server.sendmail(from_email, email, message % (names[ind], str(bd.date()), name, names[ind], str(bd.date())))
            print("Email send to %s (%s)." % (name, email))
    server.quit()  # Log off from the Gmail server once all the emails are sent for today


filename = 'data.csv'
try:
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        names, emails, dates = [], [], []
        for ind, row in enumerate(reader):
            # Data is checked while added to the column lists
            name = not_null(ind, row[0], header_row[0])
            names.append(name)
            email = not_null(ind, row[1], header_row[1])
            emails.append(email)
            # No need to create a date check function, as datetime.strptime() does that for us
            date = datetime.strptime(row[2], "%Y-%m-%d")  # Choose date format you wish to use here
            dates.append(date)

except FileNotFoundError:
    print("'data.csv' file is missing or named incorrectly.")
except ValueError:
    # This except will only trigger on date variable, as name and email are strings that get value even from empty cells
    print("Error in row", ind+2, "- missing or wrong date (", row[2], "). A reminder to use YYYY-MM-DD date format.")
    f.close()
else:
    f.close()
    # Once all the data is successfully extracted, we check which data rows will have birthdays in seven days
    week_to_birthday_rows = generate_birthday_rows()
    if not week_to_birthday_rows:  # If the list is empty, can also use <if len(list) == 0> to be more anal
        print("No birthday notifications today.")
    else:
        send_emails(week_to_birthday_rows)
