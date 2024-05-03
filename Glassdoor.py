from bs4 import BeautifulSoup
import pandas as pd
import requests
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import atexit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import os
import spacy
import requests
import pymysql
import pytz
import datetime
from datetime import datetime

# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

# print(today_date)

# mydb = pymysql.connect(
 
#   host="localhost",
#   user=		"root",
#   password=	"Narvee@123$",
#   database=	"50server_db"
# )

# mycursor=mydb.cursor

nlp = spacy.load('en_core_web_sm')
from DataCleaning import extract_skills
driver = webdriver.Chrome()

#driver = webdriver.Chrome('https://www.simplyhired.com')
# Function to release ChromeDriver
def release_chromedriver():
    try:
        # Close the ChromeDriver session
        
        driver.quit()
        print("ChromeDriver released successfully.")
    except Exception as e:
        print(f"Error releasing ChromeDriver: {e}")

# Define CST TimeZone

# Define CST timezone
# cst_timezone = pytz.timezone('America/Chicago')

# now_cst = datetime.now().astimezone(cst_timezone)
# today_cst = now_cst.strftime('%Y-%m-%d %H:%M:%S')

# yesterday_cst = now_cst - timedelta(days=1)
# yesterday_cst = yesterday_cst.replace(hour=0, minute=0, second=0)
# yesterday_cst_str = yesterday_cst.strftime('%Y-%m-%d %H:%M:%S')



# # Function to check if job already exists
# def job_exists(vendor, job_title, job_location):
#     select_query = f"SELECT vendor, job_title, job_location FROM tbl_rec_requirement WHERE vendor = %s AND job_title = %s AND job_location = %s AND posted_on >= %s AND posted_on <= %s"
#     mycursor.execute(select_query, (vendor, job_title, job_location, yesterday_cst_str, today_cst))
#     if mycursor.fetchone():
#         return True
#     return False



# driver= webdriver.Chrome()
# driver.get("https://www.glassdoor.com")




# from urllib3.exceptions import InsecureRequestWarning
from Commonfields import Commonfields

dirname=os.path.dirname(os.path.abspath(__file__))
print("Directory Name - ", dirname)

df=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/test.xlsx'))

df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites.xlsx'))


startno=0
endno=len(df)
a = ['Python']

def Glassdoor(commonfields,df,URL,startnum,endnum, pagestart, pageend):
    job=commonfields
    w2_contracts=[]
    for i in a:
        for j in range(pagestart, pageend):
            # skillname=df.loc[i, 'SkillName'] 
            url=URL.format(a=i)
            
            print('url:', url)
            
            driver.get(url)

            time.sleep(5)
            # print(driver.page_source)
            
            # html = requests.get(url, verify=True).text
            # soup = BeautifulSoup(html,'html.parser')
            	

            # job_elem= driver.find_elements(By.CLASS_NAME, "JobCard_jobCardContainer___hKKI")
            # job_elem= driver.find_elements(By.CLASS_NAME, "JobCard_jobCardWrapper__lyvNS")
            job_elem= driver.find_elements(By.CLASS_NAME, "jobCard ")
            # job_elem= driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv") 
            # job_elem= driver.find_elements(By.CLASS_NAME, "EmployerProfile_profileContainer__VjVBX EmployerProfile_compact__nP9vu")  #0
            print("Job Elements:  ",len(job_elem))
            # driver.quit()
            for e in job_elem:
                driver.implicitly_wait(10)
                try:
                 role = e.find_element(By.CLASS_NAME, "JobCard_jobTitle___7I6y")
                 print('Role:  ', role.text)
                except:
                    print("No job Role")  
                link=role.get_attribute('href')
                print("Link: ",link)  
                company_elem = e.find_element(By.CLASS_NAME, "EmployerProfile_compactEmployerName__LE242")
                company = company_elem.text
                print("Company:" , company) 
                location = e.find_element(By.CLASS_NAME,"JobCard_location__rCz3x").text 
                print("Location:",location)
                wait = WebDriverWait(driver, 10)
                # time.sleep(5)

                try:
                    salary_element = e.find_element(By.CLASS_NAME, "JobCard_salaryEstimate__arV5J")
                    job_salary= salary_element.text           
                    print("Job_salary:", job_salary)
                except:
                    print("Salary Element Not Fetched")

                posted_on_element =e.find_element(By.CLASS_NAME, "JobCard_listingAge__Ny_nG")
                posted_on = posted_on_element.text
                if posted_on == '24h':
                
                 print("posted_on:", today_date)


                
                # html = requests.get(url, verify=True).text
                # soup = BeautifulSoup(html, 'html.parser')
                driver.get(link)
                                # Find the "See more" button
                see_more_button = driver.find_element(By.XPATH, "//button[contains(@class, 'JobDetails_showMore___Le6L')]")

                # Click the "See more" button
                see_more_button.click()

                # Wait for the job description to expand
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'JobDetails_showMoreWrapper__ja2_y')))

                # Find the <div> element with the job description
                job_description_div = driver.find_element(By.CLASS_NAME, 'JobDetails_jobDescription__uW_fK')

                # Extract the text content of the <div> element
                job_description = job_description_div.text

                print("Job Description:", job_description)

                
                print("---------------------------")
                time.sleep(5)

                                

                # headers = {
                #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                #         }

                # response = requests.get(link, headers=headers)
                # print(response.status_code)
                # # break

                # #     # Check if the request was successful
                # if response.status_code == 200:
                #     html_content = response.text
                #     soup = BeautifulSoup(html_content, 'html.parser')
                #     print(soup.text)
                # break
                    
                


                

                # job_type_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "JobCard_location__N_iYE")))
                # job_type = job_type_element.text
                # print("JobType:", job_type)
                
                # try:
                    
                #     job['posted_on'].append(posted_on.text)        
                # except:
                #     job['posted_on'].append(' ')
    
                # job['category_skill'].append(skillname)
                # job['job_description'].append(' ')
                # job['job_title'].append(role.text)
                # job['vendor'].append(company)
                # job['job_location'].append(location)
                # # job['Employment_type'].append(job_type)
                # job['job_source'].append(link)
                        




                # try:
                            
                #             # job['job_salary'].append(job_salary)
                # except:     
                #     # job['job_salary'].append('None')
                # try:
                            
                #     job['posted_on'].append(posted_on.text)        
                # except:
                #     job['posted_on'].append(' ')
			
                #     job['category_skill'].append(skillname)
                #     job['job_description'].append(' ')
                #     job['job_title'].append(role.text)
                #     job['vendor'].append(company)
                #     job['job_location'].append(location)
                #     job['Employment_type'].append(job_type)
                #     job['job_source'].append(link)


                # job_type_element = wait.until(EC.visibility_of_element_located((By.XPATH, 'JobCard_location__N_iYE')))
                # job_type = job_type_element.text
                # print("JobType:", job_type)  
                                  
                    
                # posted_on=e.find('span',class_='pdate pull-right')
                # posted_on=posted_on.text.strip().split('Posted\n',1)[1]
                # posted_on.strip()
                # job['posted_on'].append(posted_on.strip())
                # details=e.find('div',class_='col-12 p-0')
                # job_title=details.find('h4')
                # job_title.text
                # job['job_title'].append(job_title.text.strip())
                # location=details.find('span',class_='locca')
                # location.text
                # job['job_location'].append(location.text)
                # job_type=details.find('span',class_='pdate')
                # job_type.text
                # job['Employment_type'].append(job_type.text)
                # link=e.find('a').get('href')
                # link
                # html1 = requests.get(link)
                # soup1 = BeautifulSoup(html1.text,'html.parser')
                # job_desc=soup1.find('ul',class_='mb-4')
                # job_desc.text
                # job['job_description'].append(job_desc.text)
                # company='JudgeGroup'
                # job['vendor'].append(company)
                # job['job_source'].append(link)
                # try:
                #     nlp1 = nlp(job_desc.text)
                #     noun_chunks = list(nlp1.noun_chunks)
                #     tokens = [token.text for token in nlp1 if not token.is_stop]
                #     skills=list(df2['Skill'])
                #     skillset = []
                #     # check for one-grams
                #     for token in tokens:
                #         if token.lower() in skills:
                #             skillset.append(token)
                #     # check for bi-grams and tri-grams
                #     for token in noun_chunks:
                #         token = token.text.lower().strip()
                #         if token in skills:
                #             skillset.append(token)
                #     skills1= [v.capitalize() for v in set([v.lower() for v in skillset])]
                #     skills1=",".join(skills1)
                #     skills1
                #     job['job_skills'].append(skills1)
                # except:
                #     job['job_skills'].append('None')
                # job['category_skill'].append(skillname)
             
                
    # for r in range(len(job['job_title'])):
    #     job['job_country'].append('United States')
        #job['job_source'].append('Judge')
                    
    # print("len(job['job_title']),len(job['vendor']),len(job['job_location']),len(job['posted_on']),len(job['Employment_type']) len,(job['posted_on_element']),len(job['job_salary']),len(job['job_description'])")
    
    glassdoor=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in job.items() ]))
    #logging.info('no. of jobs in resumelibrary: %s', len(Careerjet))
    
    return(glassdoor)


glassdoor=Glassdoor(Commonfields(), df, df1.loc[45, 'ContractURL'], startno, endno,1,2)
# print(glassdoor)



# dataframes=[Glassdoor]
# print(dataframes)

# data = pd.DataFrame(Commonfields())

# # for dice in dataframes:
# #     data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
# # data=data.drop_duplicates()


