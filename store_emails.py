import json 

#predefined emails
emails = { 
    'myself': 'shubharthaksangharsha@gmail.com', 
    'mummy': 'usharani20jan@gmail.com', 
    'bro': 'siddhant3s@gmail.com', 
    'bhabhi':'ahuja.chaks@gmail.com', 
    'pranchal': 'pranchal018@gmail.com', 
    'pranjal': 'pranchal018@gmail.com', 
    'vinita': 'vinitarai948@gmail.com'
}

smtp_servers = {
    'gmail': ('smtp.gmail.com', 465),
    'outlook': ('smtp.office365.com', 587),
    'yahoo': ('smtp.mail.yahoo.com', 465),
    'cuchd' : ('smtp.office365.com', 587)
}

def storeEmails(emails):
    with open('all_emails.json', 'w') as f:
        json.dump(emails, f)

def readEmails():
    with open('all_emails.json', 'r') as f:
        emails = json.load(f)
    return emails

if __name__ == '__main__':
    pass

