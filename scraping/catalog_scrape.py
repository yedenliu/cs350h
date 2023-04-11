# -*- coding: utf-8 -*-
'''
CS304 Course Catalog Scraping

INSTALL:
pip install bs4 --> NEED TO UPDATE OR ELSE FIND FUNCTIONS DON'T WORK
pip install soupsieve
'''
########################################################################################################
#   IMPORT MODULES
########################################################################################################
from bs4 import BeautifulSoup as BS 
import csv, os
from scrape_helpers import *

########################################################################################################
#   FUNCTIONS TO COMPILE DATA
########################################################################################################

fields=['Department', 
        'Course Number', 
        'Course Name',
        'Units', 
        'Max Enrollment', 
        'Prerequisites', 
        'Instructor', 
        'Distribution Requirements', 
        'Typical Periods Offered', 
        'Semesters Offered this Academic Year']

def create_tsv(url):
    soup = html_object(url)
    sections = find_sections(soup)
    data = all_courses(sections)
    cwd = os.getcwd()
    pd = os.path.abspath(os.path.join(cwd, os.pardir))
    with open(os.path.join(pd, 'DDL', 'all_courses.tsv'), 'a', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
        # write the data
        writer.writerows(data)

########################################################################################################
#   DATA IMPORT + EXPORT
########################################################################################################
def parse_majors():
    # iterate through the catalog_urls.tsv file for (1) dept num (2) catalog page URL
    import pandas as pd
    cwd = os.getcwd()
    file_path = os.path.join(cwd, 'catalog_urls.tsv')
    col_list = ['abbrev', 'cat_url']
    df = pd.read_csv(file_path, delimiter='\t', usecols=col_list,)
    for i in range(len(df.index)):
        #abbrev = df.iat[i, 0]
        cat_url = df.iat[i, 1]
        create_tsv(cat_url)

parse_majors()