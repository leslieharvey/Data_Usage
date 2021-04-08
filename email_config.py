import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_info import server_email, server_email_password
from datetime import datetime

# Note: Email config must be in email_info.py file
def messageConfig(sender_email, receiver_email, text_content, html_content):
  """
  This function will generate a MIMEText object to send as an email attachement
  
  Args:
    sender_email (str): The email address of the sender of the email.
    receiver_email (str): The email address of the reciever of the email.
    text_content (str): The text content of the email.
    html_content (str): The HTML content of the email.

  Returns:
    MIMEText: A MIMEText object to send as an email attachment
  
  """
  current_day = datetime.today().strftime('%Y-%m-%d')

  message = MIMEMultipart("alternative")
  message["Subject"] = "Renne Lab: Data Usage " + current_day
  message["From"] = sender_email

  # Configure "To" portion of message
  message["To"] = receiver_email

  # Turn message into plain/html MIMEText objects
  plain_part = MIMEText(text_content, "plain")
  html_part = MIMEText(html_content, "html")

  # Add HTML/plain-text parts to MIMEMultipart message
  # The email client will try to render the last part first
  message.attach(plain_part)
  message.attach(html_part)

  return message


def emailSender():
  """
  This function will email the HTML results to the specified users
  """

  # File name of the CSV file with user email information
  email_csv_name = "email_info.csv"

  # File name of the HTML result file for the group data usage
  group_html_result_name = "result.html"
  sender_email = server_email
  password = server_email_password

  # Create the plain-text version of the message
  text = """\
  HTML email containing the data usage information
  """

  # Group HTML Result
  try:
    with open(group_html_result_name, 'r') as group_html_file:
      group_html_content = group_html_file.read()
  except (FileNotFoundError):
    raise Exception("Group HTML file not found")

  # Create secure connection with server and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      # Log in with server email
      server.login(sender_email, password)

      # Open the csv file with user data
      with open(email_csv_name, 'r', encoding='utf-8-sig') as csv_file:
        for _, line in enumerate(csv_file):
          current_line = line.rstrip().split(',')
      
          # Store user information
          user_name = current_line[0]
          user_email = current_line[1]

          # Open the corresponding result html file
          try:
            with open(user_name + '_result.html', 'r') as html_file:
              html_content = html_file.read()
          except (FileNotFoundError):
            print("HTML file for " + user_name + " not found")
            continue

          # Generate user MIMEMultipart message
          user_message = messageConfig(sender_email, user_email, text, html_content)

          server.sendmail(
              sender_email, user_email, user_message.as_string()
          )

          # Personal HTML result sent, must send group result to specified user
          group_message = messageConfig(sender_email, user_email, text, group_html_content)

          server.sendmail(
              sender_email, user_email, group_message.as_string()
          )
