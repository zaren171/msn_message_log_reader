# msn_message_log_reader
html msn messenger log file reader

Start code from: https://codepen.io/SebFrl/pen/WWbYLP

There is a name mapping file, this can be used to map random user names to actual human names, which will be inserted before the user name in parenthesis when matched.

Some emoji's are auto-converted to close/equivalent current emojis.

There is an included python script (chat_parser.py) to help create a few files.  One file is the name_map.txt file.  To create this file, set BUILD_NAME_MAP=True and run.  
This will create a file with the various user names, as well the part of the file name from the chat_logs which represent the email address.  The user names and emails
are separated by ':=:'  Once the file is created you can go through and rename email addresses to the actual names of people to get them prepended in parenthesis to the
chat conversations.  If a name appears in more than one log file, a list of potential email addresses will be given.  If there are a LOT of porential email addresses, it
was likely your own user name.

The chat_parser.py can also produce new chat logs for specific days or months.  To do so, set BUILD_DATE_FILE to true, and set the BUILD_DATE_YEAR, BUILD_DATE_MONTH, and
BUILD_DATE_DAY appropriately.  If you set BUILD_DATE_DAY to 0 the script will instead grab all conversations from the selected year/month, and then sort them in date order
to the output file.

