from bs4 import BeautifulSoup
import pandas as pd
import requests
import logging
from datetime import datetime, timedelta
import pymysql
import re
import time
# Establish connection parameters
mydb = pymysql.connect(
    # host="69.216.19.140",
    host="50.28.107.39",
    user="narvee",
    port=3306,
    password="Atc404$",
    database="narvee_ATS"
)
# Create a cursor object
mycursor = mydb.cursor()

# Define date and time parameters for filtering
now = datetime.now()
today = now.strftime('%Y-%m-%d 00:00:00')
yesterday = now - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d 23:59:59')


# Function to check if job already exists
def job_exists(vendor, job_title, job_location):
    select_query = f"SELECT vendor, job_title, job_location FROM tbl_rec_requirement WHERE vendor = %s AND job_title = %s AND job_location = %s AND posted_on BETWEEN %s AND  %s"
    mycursor.execute(select_query, (vendor, job_title, job_location, yesterday_str, today))
    if mycursor.fetchone():
        return True
    return False


def Linkedin(commonfields, df, URL, startnum, endnum, df2, result_all, job_titles_strings):
    job = commonfields 
    w2_contracts = []
    for i in job_titles_strings:
        for j in range(1, 2):
            url = URL.format(a=i, b=j)
            print(url)  # For debugging
            logging.info(url)

            html = requests.get(url, verify=True).text
            soup = BeautifulSoup(html, 'html.parser')
            job_elem = soup.find_all('div', class_='base-card')
            print(len(job_elem))

            for e in job_elem:
                details = e.find('div', class_='base-search-card__info')
                job_title_element = details.find('h3', class_='base-search-card__title')
                job_title = job_title_element.text.strip() if job_title_element else 'None'

                company_element = e.find('h4', class_='base-search-card__subtitle')
                company_name = company_element.text.strip() if company_element else 'None'

                link_element = e.find('a')
                link = link_element['href'] if link_element else 'None'
                response = requests.get(link)
                location_element = e.find('span', class_='job-search-card__location')
                location = location_element.text.strip() if location_element else 'None'
                if (link,) not in result_all:
                    def extract_city_state(location):
                        # Define regex pattern to match city and state
                        pattern = r'(?i)(?:Remote|Hybrid remote|On-Site|Hybrid)\s*in\s*([^0-9,\(\)]+),\s*([A-Za-z\s]+)|([^0-9,\(\)]+),\s*([A-Za-z\s]+)'

                        # Search for the pattern in the location string
                        match = re.search(pattern, location)

                        if match:
                            # Extract city and state
                            city = match.group(1) or match.group(3)
                            state = match.group(2) or match.group(4)
                            return f"{city.strip()}, {state.strip()}"
                        else:
                            # If "Dallas" is encountered, return "Dallas, TX"
                            if "Dallas" in location:
                                return "Dallas, TX"
                            else:
                                return location.strip()
                        
                    
                    location = extract_city_state(location)

                    print(location)

                    job_type_element = e.find('div', class_='result-benefits__text')
                    job_type = job_type_element.text.strip() if job_type_element else 'Contract'
                    print("Link:", link)
                    time.sleep(3)
                    html1 = requests.get(link, verify=True).text
                    soup1 = BeautifulSoup(html1, 'html.parser')
                    time.sleep(2)
                    try:
                        job_discrption = soup1.find('div', class_='show-more-less-html__markup').text
                        #print("Job Discrption:", job_discrption) 
                    except :
                        job_discrption = ' ' 
                        #print("555555555")


                    # response = requests.get(link)
                    # html_content = response.text

                    # # Regular expression pattern to match email addresses
                    # email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

                    # # Find all email addresses in the HTML content
                    # emails_found = re.findall(email_pattern, html_content)
                    # print("Email:", emails_found)
                    # if emails_found: 
                    #     emails = emails_found[0]
                    # else :
                    #     emails = ''
                    # Check if the request was successful
                    if response.status_code == 200:
                        # Parse the HTML content
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # Find all text within the HTML
                        all_text = soup.get_text().lower()
                        #print(all_text)
                        if "w2" in all_text or 'no c2c' in all_text or 'no 3rd parties' in all_text or 'only w2' in all_text or 'full-time' in all_text:
                            print("YES W2 Position........")
                            w2_contracts.append({
                                    'job_title': job_title,
                                    'vendor': company_name,
                                    'job_location': location,
                                    'posted_on': today,
                                    'Employment_type': job_type,
                                    'job_description': job_discrption,
                                    'job_source': link,                                    
                                    # 'email': emails,
                                    'job_country': "United States",
                                    'category_skill':(i.replace("%20", " ")),
                                    'source': "LinkedIn"
                                    
                                })
                            
                        else:                            
                                

                            if not job_exists(company_name, job_title, location) :

                                job['vendor'].append(company_name)
                                job['job_title'].append(job_title)
                                job['job_location'].append(location)
                                job['Employment_type'].append(job_type)
                                job['job_description'].append(all_text)
                                job['job_source'].append(link)
                                job['category_skill'].append(i.replace("%20", " "))
                                job['posted_on'].append(today)
                            else :
                                print("Same Vendor, Location and Job Title already In our Database")

    for r in range(len(job['job_title'])):
        job['job_country'].append('United States')
        job['source'].append('Linkedin')

    print(len(job['job_title']), len(job['vendor']), len(job['job_location']), len(job['Employment_type']),
          len(job['job_salary']), len(job['job_description']))

    linkedin = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in job.items()]))
    mydb.close()
    mycursor.close()
    return linkedin, w2_contracts






