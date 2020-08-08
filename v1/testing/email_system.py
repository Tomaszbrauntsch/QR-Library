import email
import imaplib

username = 'xxxx@gmail.com'
password = 'xxxx'

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

mail.select("inbox")
result, data = mail.uid('search', None, 'ALL')
inbox = data[0].split()

#initializes the inbox
computer_inbox = inbox[-1]
user_inbox = inbox[-2]

result, computer_type = mail.uid('fetch', computer_inbox, '(RFC822)')
result, user_type = mail.uid('fetch', user_inbox, '(RFC822)')

raw_user = user_type[0][1]
raw_computer = computer_type[0][1]

user_email = email.message_from_string(raw_user)
computer_email = email.message_from_string(raw_computer)

user_value = user_email['subject']
computer_value = computer_email['subject']

user_value = user_value.split()
name = user_value[0] + " " + user_value[1]
grade = user_value[2]
