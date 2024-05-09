from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import logging
import os
import atexit
import spacy
nlp = spacy.load('en_core_web_sm')
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
dirname = os.path.dirname(__file__)
#dirname = os.path.dirname(__file__)



# mydb = pymysql.connect(
#     # host="69.216.19.140",
#     host="50.28.107.39",
#     user="narvee",
#     port=3306,
#     password="Atc404$",
#     database="narvee_ATS"
# )

mydb = pymysql.connect(
 
  host="localhost",
  user=		"root",
  password=	"Nadmin123$",
  database=	"usitportal"
)



today = date.today()
Today= today.strftime("%Y-%m-%d")
yesterday = today - timedelta(days = 2)
Yesterday = yesterday.strftime("%Y-%m-%d")

#logging.basicConfig(filename=r'C:\Users\Dell\Documents\NarveeProject\webscrapping\logfiles\log-US-{d}.log'.format(d=Today), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename=os.path.join(dirname, 'logfiles/log-US-{d}.log'.format(d=Today)), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# +
### skills category excel
# df=pd.read_excel(os.path.join(dirname,'IT_skill_category.xlsx'))
# df=pd.read_excel(os.path.join(dirname,'c:\Users\admin\Documents\IT_skill_category_HOT.xlsx'))

startno=0
endno=len('1')

##DateFilter
start_date = Yesterday
end_date = Today

## Job Sites Excel
df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites1.xlsx'))

# +

## Skills from Job_description
df2=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/listofskills.xlsx'))
# -

df2.head()

## import common fields dictionary
from Commonfields import Commonfields

# Create a cursor object
mycursor = mydb.cursor()

import pytz
from datetime import datetime, timedelta
cst_timezone = pytz.timezone('America/Chicago')
now_cst = datetime.now().astimezone(cst_timezone)
today_cst = now_cst.strftime('%Y-%m-%d')
yesterday_cst = now_cst - timedelta(days=2)
#yesterday_cst = yesterday_cst.replace(hour=0, minute=0, second=0)
yesterday_cst_str = yesterday_cst.strftime('%Y-%m-%d')

# Query to retrieve all distinct job sources for today and yesterday
#select_query_all = f"SELECT DISTINCT job_source FROM tbl_rec_requirement WHERE posted_on >= '{yesterday_cst_str}' AND posted_on <= '{today_cst}'"
select_query_all = f"SELECT  job_source FROM tbl_rec_requirement WHERE (posted_on >= '{yesterday_cst_str} 00:00:00' AND posted_on <= '{today_cst} 23:59:59')"

mycursor.execute(select_query_all)

# Fetch all the rows
result_all = mycursor.fetchall() 
print(len(result_all))
start_date_1 = now_cst.strftime("%Y-%m-%d 00:00:00")
end_date_1 = now_cst.strftime("%Y-%m-%d 23:59:00")

select_query_both = f"""SELECT DISTINCT t.technologyarea
    FROM technologies t
    JOIN consultant_info c ON t.id = c.techid
    WHERE c.consultantflg = 'sales'
    AND c.status != 'InActive'
    AND NOT EXISTS (
        SELECT 1
        FROM submission sub
        WHERE sub.consultantid = c.consultantid
        AND sub.flg = 'sales'
        AND sub.createddate BETWEEN '{start_date_1}' AND '{end_date_1}'
    )
    ORDER BY t.technologyarea ASC;

"""
logging.info('Successfully Done ')
# Execute the query
mycursor.execute(select_query_both)


job_titles_strings = [item[0].replace(" ", "%20").strip() for item in mycursor.fetchall()]
#job_titles_strings  = ['.Net', 'AS400%20cobol%20developer', 'Cloud%20Engineer', 'Cyber%20Security', 'Data%20Engineer', 'Devops%20Engineer', 'Embedded%20software%20developer', 'ETL%20Developer', 'Front%20End%20Developer', 'Full%20Stack%20Developer', 'Java%20Full%20Stack%20Developer', 'Kinaxis%20Rapid%20Response', 'Mainframe%20Developer%20with%20COBOL', 'Oracle%20SCM%20Cloud', 'Project%20Manager', 'RPA%20Developer', 'Salesforce%20Developer', 'SAP%20EAM%20Functional%20Lead', 'Scrum%20Master', 'SDET', 'Sr.%20Full%20Stack%20Java%20Developer', 'Test%20Engineer%20with%20QA', 'Workday%20Enhancements%20&%20Support']
print("Unique Tech Count:",len(job_titles_strings))
#job_titles_strings = ['Appian%20bpm%20Developer', 'Camunda%20BPM', 'Oracle%20HCM', 'IBM%20BPM', 'Okta', 'Sailpoint', 'Qualys']
#job_titles_strings = ['Python', 'Java', 'Angular']
mycursor.close()


extra_technologies = [
    "Appian%20BPM%20Developer",
    "Camunda%20BPM",
    "Oracle%20HCM",
    "IBM%20BPM",
    "Okta",
    "Sail%20Point",
    "Qualys",
    "Burp%20Suite",
    "Netsparker",
    "Checkmarx",
    "Sonar%20Qube"
]


job_titles_strings.extend(extra_technologies)

# Convert the time to CST
cst_timezone = pytz.timezone('America/Chicago')  # CST timezone
cst_time = datetime.now().astimezone(cst_timezone).strftime('%Y-%m-%d %H:%M:%S')


# from Simplyhire_Chng import Simplyhire
# simply=pd.DataFrame()

# logging.info('Simplyhire started')
# simply, w2_contracts=Simplyhire(Commonfields(),df,df1.loc[3,'ContractURL'],startno,endno,df1.loc[3,'Domain'], result_all, job_titles_strings)
# #########simply['posted_on'] = simply['posted_on'].apply(lambda x: cst_time)
# logging.info('Simplyhire Execution done')

# from Indeed import Indeed    
# indeed=pd.DataFrame()

# logging.info('indeed started')
# indeed, w2_contracts=Indeed(Commonfields(),df,df1.loc[22,'ContractURL'],startno,endno,df1.loc[3,'Domain'], result_all, job_titles_strings)
# ########indeed['posted_on'] = indeed['posted_on'].apply(lambda x: cst_time)
# logging.info('indeed Execution done') 
# 


#job_titles_strings =['Python', 'Java']

from Techfetch import Techfetch
techfetch=pd.DataFrame()

logging.info('Techfetch started')
techfetch=Techfetch(Commonfields(),df1.loc[3,'ContractURL'],startno,endno,df1.loc[3,'Domain'], result_all, job_titles_strings)

logging.info('Techfetch Execution done')



# from Recruitnet import Recruitnet 
# recruitnet=pd.DataFrame()

# logging.info('Recruitnet started')

# filtered_technology_areas = [area for area in job_titles_strings if area != 'SAP%20BASIS/HANA']
# # ##########filtered_technology_areas = ['Java', 'Python']
# recruitnet, w2_contracts=Recruitnet(Commonfields(),df,df1.loc[34,'ContractURL'],startno,endno,df2, result_all, filtered_technology_areas)
# ###################recruitnet['posted_on'] = recruitnet['posted_on'].apply(lambda x: cst_time)
# logging.info('Recruitnet Execution done')



# from Prodapt import Prodapt
# prodapt=pd.DataFrame()

# logging.info('Prodapt started')
# prodapt=Prodapt(Commonfields(),df,df1.loc[40,'ContractURL'],startno,endno,df1.loc[40,'Domain'], result_all, job_titles_strings)
# prodapt['posted_on']=prodapt['posted_on'].apply(lambda x: Today)
# logging.info('Prodapt Execution done')


# from Experis import Experis
# experis=pd.DataFrame()

# logging.info('Experis started')
# experis=Experis(Commonfields(),df,df1.loc[35,'ContractURL'],startno,endno,df1.loc[35,'Domain'], result_all, job_titles_strings[:8])
# experis['posted_on']=experis['posted_on'].apply(lambda x: Today)
# logging.info('Experis Execution done')


# from Jooble import Jooble
# simply=pd.DataFrame()  

# logging.info('jooble started')
# jooble=Jooble(Commonfields(),df,df1.loc[23,'ContractURL'],startno,endno,df1.loc[3,'Domain'], result_all)
# jooble['posted_on']=jooble['posted_on'].apply(lambda x: Today)
# logging.info('jooble Execution done')

# from Resumelibrary import Resumelibrary
# resumelibrary=pd.DataFrame()
# logging.info('Resumelibrary started')
# resumelibrary=Resumelibrary(Commonfields(),df,df1.loc[7,'ContractURL'],startno,endno,df2)
# resumelibrary['posted_on']=resumelibrary['posted_on'].apply(lambda x: Today)
# logging.info('Resumelibrary Execution done')

# # from Jobcube import Jobcube
# jobcube=pd.DataFrame()

# logging.info('Jobcube started')
# jobcube, w2_contracts=Jobcube(Commonfields(),df,df1.loc[21,'ContractURL'],startno,endno,df1.loc[21,'Domain'], result_all, job_titles_strings)
# #jobcube['posted_on'] = jobcube['posted_on'].apply(lambda x: cst_time)
# logging.info('Jobcube Execution done') 



# from Postjobfree import Postjobfree
# postjobfree=pd.DataFrame()

# logging.info('Postjobfree started')
# postjobfree=Postjobfree(Commonfields(),df,df1.loc[32,'ContractURL'],startno,endno,df1.loc[31,'Domain'], result_all,job_titles_strings)
# simply['posted_on'] = simply['posted_on'].apply(lambda x: cst_time)
# logging.info('Postjobfree Execution done') 




# from Monster import Monster
# monster=pd.DataFrame()
# logging.info('Monster started')
# monster=Monster(Commonfields(),df,df1.loc[20,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# monster['posted_on']=monster['posted_on'].apply(lambda x: Today)
# logging.info('monster Execution done')


# from Careerbuilder import Careerbuilder
# careerbuilder=pd.DataFrame()
# logging.info('careerbuilder started')
# careerbuilder= Careerbuilder(Commonfields(),df,df1.loc[4,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# careerbuilder['posted_on']=careerbuilder['posted_on'].apply(lambda x: Today)
# logging.info('monster Execution done')

# from Timesjobs import Timesjobs             
# timesjobs=pd.DataFrame()

# logging.info('Timesjobs started')
# timesjobs=Timesjobs(Commonfields(),df,df1.loc[1,'ContractURL'],startno,endno,df1.loc[3,'Domain'])
# timesjobs['posted_on']=timesjobs['posted_on'].apply(lambda x: Today)
# logging.info('Timesjobs Execution done')


# from Joblift import Joblift
# joblift=pd.DataFrame()
# logging.info('joblift started')
# joblift=Joblift(Commonfields(),df,df1.loc[26,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# joblift['posted_on']=joblift['posted_on'].apply(lambda x: Today)
# logging.info('joblift Execution done')


# from Linkedin import Linkedin
# linkedin=pd.DataFrame()

# logging.info('Linkedin started')
# linkedin, w2_contracts= Linkedin(Commonfields(),df,df1.loc[24,'ContractURL'],startno,endno,df1.loc[44,'Domain'], result_all, job_titles_strings) #20
# #######################linkedin['posted_on'] = linkedin['posted_on'].apply(lambda x: cst_time)
# logging.info('Linkedin Execution done')


# from Adzuna import Adzuna
# adzuna=pd.DataFrame()
# logging.info('Adzuna started')
# adzuna=Adzuna(Commonfields(),df,df1.loc[27,'ContractURL'],startno,endno,df2, result_all, job_titles_strings[:10])
# simply['posted_on'] = simply['posted_on'].apply(lambda x: cst_time)
# logging.info('Adzuna Execution done')

# from Idealist import Idealist
# idealist=pd.DataFrame()
# logging.info('Idealist started')
# idealist=Idealist(Commonfields(),df,df1.loc[33,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# idealist['posted_on']=idealist['posted_on'].apply(lambda x: Today)
# logging.info('Idealist Execution done')

# from Snaprecruit import Snaprecruit
# snaprecruit=pd.DataFrame()
# logging.info('Snaprecruit started')
# snaprecruit=Snaprecruit(Commonfields(),df,df1.loc[6,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# simply['posted_on'] = simply['posted_on'].apply(lambda x: cst_time)
# logging.info('Snaprecruit Execution done')

# import pytz
# from datetime import datetime
# # Convert the time to CST
# cst_timezone = pytz.timezone('America/Chicago')  # CST timezone
# cst_time = datetime.now().astimezone(cst_timezone).strftime('%Y-%m-%d %H:%M:%S')





# from Naukri import Naukri
# naukri=pd.DataFrame()
# logging.info('Naukri started')
# naukri=  Naukri(Commonfields(),df,df1.loc[2,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# naukri['posted_on']=naukri['posted_on'].apply(lambda x: Today)
# logging.info('Naukri Execution done')

# from DiceA import Dice
# dice=pd.DataFrame()

# logging.info('Dice1 started')
# dice= Dice(Commonfields(),df,df1.loc[19,'ContractURL'],startno,endno,df2, result_all, job_titles_strings[:3])
# dice['posted_on']=dice['posted_on'].apply(lambda x: Today)
# logging.info('Dice1 Execution done')

# from Juju import Juju
# juju=pd.DataFrame()
# logging.info('Juju started')
# juju=Juju(Commonfields(),df,df1.loc[30,'ContractURL'],startno,endno,df2, result_all, job_titles_strings)
# juju['posted_on']=juju['posted_on'].apply(lambda x: Today)
# logging.info('Juju Execution done')

# # +
# from Monster import Monster
# monster=pd.DataFrame()

# logging.info('Simplyhire started')
# monster= Monster(Commonfields(),df,df1.loc[20,'ContractURL'],startno,endno,df1.loc[20,'Domain'], result_all)
# monster['posted_on']= monster['posted_on'].apply(lambda x: Today)
# logging.info('Simplyhire Execution done')





logging.info('Concatenation of DataFrames started')
dataframes=[techfetch ]#   simply    ,recruitnet  , indeed,    indeed    linkedin  techfetch  timesjobs     adzuna  ,  ,  ,  ,      prodapt  monster  naukri   , ,  careerbuilder experis  snaprecruit   dice   monster   ,postjobfree, ,   randstatUSA,careerbuilder,careerjet, joblift,      juju idealist     , , ,judge  idealist,matrixiers,    ,       , jobboard, resumelibrary       timesjobs   resumelibrary   jooble       apexsystems
data=pd.concat(dataframes,ignore_index=True,sort=False) 

data = data.drop_duplicates(subset=['job_source'])

data = data.drop_duplicates(subset=['job_title', 'vendor', 'job_location'])

# +
dictionary=Commonfields()


logging.info('Extracting Email,Phone')
from DataCleaning import extract_email,extract_mobile_number

data

for c in range(len(data)):
    #print(c)
    dictionary['job_industry'].append('IT industry')
    desc=data.iloc[c,5]
    #desc=data.iloc[c,8]
    #print(desc)
    try:
        email= extract_email(desc)
        dictionary['email'].append(email)
    except:
        dictionary['email'].append('None')
    try:
        phone= extract_mobile_number(desc)
        dictionary['phone'].append(phone)
    except:
        dictionary['phone'].append('None')

data['email']=dictionary['email']
data['phone']=dictionary['phone']
data['job_industry']=dictionary['job_industry']

# +
logging.info('Data Cleaning started')
from DataCleaning import clean_posted,date_format,clean_text,clean_phone

data = data.dropna(axis=0, subset=['posted_on'])
data['posted_on'] = data['posted_on'].apply(lambda x: clean_posted(x))

data['posted_on'] = data['posted_on'].apply(lambda x: date_format(x))

data['job_description'] = data['job_description'].apply(clean_text)

#data=data.drop_duplicates()
logging.info('length of data after dropping the duplicates %s ',len(data))


# -

fd=pd.DataFrame(columns=data.columns)
Technology=list(df2.loc[0:24,'Technology'])
#Technology

data['job_title'] = data['job_title']
#if 'job_title' in data.columns and data['job_title'].dtype == 'O':

for i in range(len(Technology)):
    fd1=data.set_index('job_title')
    fd1=fd1.filter(like=Technology[i],axis=0)
    fd1=fd1.reset_index()
    fd = pd.concat([fd1, fd.dropna(axis=1, how='all')], ignore_index=True, sort=False)

fd['job_title'] = fd['job_title']   # .str.title()

# fd

fd=fd.drop_duplicates()

fd['Employment_type']=fd['Employment_type'].apply(lambda x: 'Contract')
fd['phone']=fd['phone'].apply(lambda x: clean_phone(x))

API_ENDPOINT = "http://narveetech.com/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=lekhana.pmk@gmail.com&password=Lekhana123$"


logging.info('Execution End')


#data1=data[['job_title','vendor','job_location','posted_on','job_description','Employment_type','job_skills','job_source','email','phone','category_skill','source', 'isexist']]

#data1 =data1.fillna('')

# Create a cursor object
mycursor = mydb.cursor()

# Query to retrieve all distinct vendors from the 'vendor' table
select_query_all = "SELECT DISTINCT company FROM vendor;"
mycursor.execute(select_query_all)

# Fetch all the distinct vendors
distinct_vendors = set([row[0].lower() for row in mycursor.fetchall()])



# Initialize the 'isexist' column in the DataFrame with the default value '0'
data['isexist'] = 0

# Loop through vendors and update 'isexist' column
for i, row in data.iterrows():
    vendor_lower = str(row['vendor']).lower()  # Convert to lowercase for case-insensitive comparison

    # Check if the vendor name is a substring of any vendor name from the database
    isexist_value = 0
    for db_vendor in distinct_vendors:
        if vendor_lower in db_vendor.lower():
            isexist_value = 1
            break
    
    data.at[i, 'isexist'] = isexist_value


data1=data[['job_title','vendor','job_location','posted_on','job_description','Employment_type','job_skills','job_source','email','phone','category_skill','source', 'isexist']]

data1 =data1.fillna('')


# Create the directory if it does not exist
output_directory = os.path.join(dirname, 'Alljobsscraped')
os.makedirs(output_directory, exist_ok=True)

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

data1.to_excel(os.path.join(output_directory, 'HL-Main_US-{d}.xlsx'.format(d=current_datetime)), index=False)


sql = "INSERT INTO tbl_rec_requirement (job_title,vendor,job_location,posted_on,job_description,Employment_type,job_skills,job_source,email,phone,category_skill,source, isexist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for i, row in data1.iterrows():
    # Ensure 'isexist' is a valid integer value
    isexist_value = int(row['isexist']) if pd.notna(row['isexist']) and str(row['isexist']).strip() != '' else 0

    # Handle NaN values in the entire row before inserting into MySQL
    row = row.apply(lambda x: '' if pd.isna(x) else x)

    # Convert 'isexist' to integer before inserting into MySQL
    row['isexist'] = isexist_value

    mycursor.execute(sql, tuple(row))

    # The connection is not autocommitted by default, so we must commit to save our changes
    mydb.commit() 
# for contract in w2_contracts:
#     # Insert each contract into the table    
#     insert_query = """
#         INSERT INTO tbl_rec_fulltime (job_title, vendor, job_location, posted_on, Employment_type, source, job_source, category_skill)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#     """  #         tbl_dice_recs
#     values = (
#         contract['job_title'],
#         contract['vendor'],
#         contract['job_location'],
#         contract['posted_on'],
#         contract['Employment_type'],
#         contract['source'],
#         contract['job_source'],
#         contract['category_skill']
#     )

#     mycursor.execute(insert_query, values)
#     mydb.commit()



# Close the database connection
mydb.close()
mycursor.close()






def print_success_with_stars():
    name = "SUCCESS"
    characters = {
        'S': [' ****', '*    ', ' *** ', '    *', '*   *', '**** '],
        'U': ['*   *', '*   *', '*   *', '*   *', '*   *', ' *** '],
        'C': [' *** ', '*   *', '*    ', '*    ', '*   *', ' *** '],
        'E': ['**** ', '*    ', '***  ', '*    ', '*    ', '**** ']
    }

    for i in range(6):
        for char in name:
            print(characters.get(char, ['     '])[i], end='   ')
        print()


if __name__ == "__main__":
    print_success_with_stars()



