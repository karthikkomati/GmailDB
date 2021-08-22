# GmailDB

Connect to a gmail and store its information in a database.

This python program uses Google API to connect to a user's gmail account. This requires the user to login to their gmail instead of inputting their credentials in the program which  are then stored locally so they can be used again the next time without needing the user to login.

A number of emails form the accessed emails are read and certain parts of each email is stored in a MySQL database. The number of emails read is specified in at the start of the program (5) and the part of the email stored are the mail_id, thread_id and the snippet.
