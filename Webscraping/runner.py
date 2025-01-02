import subprocess


subprocess.run(['python', './Webscraping/webscraper.py'])

subprocess.run(['python', './Webscraping/add_to_database.py'])

# alternatively archived:

# with open('webscraper.py') as file1:
#     exec(file1.read())

# with open('add_to_databaser.py') as file2:
#     exec(file2.read())