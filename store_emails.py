import json 

emails = { 
    'myself': 'shubharthaksangharsha@gmail.com', 
    'mummy': 'usharani20jan@gmail.com', 
    'bro': 'siddhant3s@gmail.com', 
    'bhabhi':'ahuja.chaks@gmail.com', 
    'pranchal': 'pranchal018@gmail.com', 
    'pranjal': 'pranchal018@gmail.com', 
    'vinita': 'vinitarai948@gmail.com'
}

with open('all_emails.json', 'w') as f:
    json.dump(emails, f)

with open('all_emails.json', 'r') as f:
    emails = json.load(f)



