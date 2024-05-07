# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
import dateutil.parser as parser
import time
import re
import spacy

# nlp1= spacy.load('en_core_web_sm')

def date_format(posted_on):
    import re
    try:
        matches = re.search(r"(\d+ weeks?,? )?(\d+ days?,? )?(\d+ hours?,? )?(\d+ mins?,? )?(\d+ secs? )?ago", posted_on)
        date_pieces = {'week': 0, 'day': 0, 'hour': 0, 'min': 0, 'sec': 0}

        for i in range(1, len(date_pieces) + 1):
            if matches.group(i):
                value_unit = matches.group(i).rstrip(', ')
                if len(value_unit.split()) == 2:
                    value, unit = value_unit.split()
                    date_pieces[unit.rstrip('s')] = int(value)

        d2 = datetime.today() - timedelta(
            weeks=date_pieces['week'],
            days=date_pieces['day'],
            hours=date_pieces['hour'],
            minutes=date_pieces['min'],
            seconds=date_pieces['sec']
        )
        d1=d2.strftime("%Y-%m-%d")
    except:
        try:
            d2=parser.parse(posted_on)
            d1=d2.strftime("%Y-%m-%d")
        except:
            d1=posted_on
    return(d1)

def clean_posted(date):
    date=date.lower()
    date=date.replace('today','0 days ago').replace('yesterday','1 days ago').replace('just now','0 days ago')
    date=date.replace("+","")
    return date

def clean_text(text):
        if isinstance(text, str):
            '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
            and remove words containing numbers.'''
            #text = re.sub('\n', '', text)
            #text = re.sub('\t', '', text)
            text = re.sub('₹', '', text)
            return re.sub(r'\[.*?\]', '', text)
        else:
            return text

def clean_phone(text):
    try:
        clean_phone_number = re.sub('[^0-9]+', '', text)
        formatted_phone_number = re.sub(r"(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone_number[:-1])) + clean_phone_number[-1]

        return formatted_phone_number
    except:
        return text
    


def extract_email(text):
    email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
    else:
        number =" "
        return number


def extract_mobile_number(text):
   
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                    [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    mob_num_regex1 = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)[-\.\s]*\d{3}[-\.\s]??\d{4}|([(]?(\d{3})?[)]?(\s|-|\.)?(\d{3})(\s|-|\.)(\d{4})))'''
    phone = re.findall(re.compile(mob_num_regex1), text)

    if phone:
        number = ''.join(phone[0])
        return number
    else:
        number =" "
        return number


# def extract_skills(skillslist):

#     tokens = [token.text for token in nlp1 if not token.is_stop]
#     skills=list(skillslist['Skill'])
#     skillset = []
#     # check for one-grams
#     for token in tokens:
#         if token.lower() in skills:
#             skillset.append(token)
#     # check for bi-grams and tri-grams
#     for token in "noun_chunks":
#         token = token.text.lower().strip()
#         if token in skills:
#             skillset.append(token)
#     return [i.capitalize() for i in set([i.lower() for i in skillset])]




