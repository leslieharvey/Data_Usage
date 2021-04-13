# Data Usage Email Reporter

This project aims to automate the data usage report generation of shared folder. The overall end result will send an HTML email to specified users that give information relevant to their largest folders as well as the storage usage of other users on the designated folder.

## How To Use

1. Populate _email_info.csv_ with intended email users. The format is: **COMPUTER_USERNAME,EMAIL_ADDRESS**
2. Create _email_info.py_ and store the sender email address login information in the relevant variables.
   - server_email
   - server_email_password
3. Run intended commands via _data_usage.csv_
