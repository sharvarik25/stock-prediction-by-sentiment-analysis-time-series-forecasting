from bs4 import BeautifulSoup
import requests, requests.utils
import json
import time
from datetime import datetime, timedelta, date
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
import boto3
import config as cfg
import math
from io import StringIO
csv_buffer = StringIO()

ACCESS_KEY = cfg.aws[0]['access_key']
SECRET_KEY = cfg.aws[0]['secret_key']
BUCKET = cfg.aws[0]['bucket_name']
s3_resource = boto3.resource('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY)
s3 = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY)

def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

#date for which archive link would be generated
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#list of archive links
def urls_list():
    preURL = 'http://www.wsj.com/news/archive/'
    start_date = date(2020, 1, 1)
    end_date = date(2020, 4, 1)
    hrefList = []
    for single_date in daterange(start_date, end_date):
        # with open('log/wsjScrap.log', 'a') as log:
        #     log.write('---{0}\n'.format(single_date.strftime('%Y-%m-%d')))
        hrefList.append(preURL + single_date.strftime('%Y%m%d'))
    return hrefList

#calling the function and storing links in a list
hrefList = urls_list()

####Delta Air Lines####
obj_delta = s3_resource.Object(BUCKET, 'Company_Keywords/DeltaAirLines.txt')
delta = obj_delta.get()['Body'].read().decode().split(',')
delta_list = [item.strip() for item in delta]
####Southwest Airlines####
obj_southwest = s3_resource.Object(BUCKET, 'Company_Keywords/SouthwestAirlines.txt')
southwest = obj_southwest.get()['Body'].read().decode().split(',')
southwest_list = [item.strip() for item in southwest]
####United Airlines Holding####
obj_united = s3_resource.Object(BUCKET, 'Company_Keywords/UnitedAirlinesHoldings.txt')
unitedairline = obj_united.get()['Body'].read().decode().split(',')
unitedairline_list = [item.strip() for item in unitedairline]
####Facebook####
obj_facebook = s3_resource.Object(BUCKET, 'Company_Keywords/Facebook.txt')
facebook = obj_facebook.get()['Body'].read().decode().split(',')
facebook_list = [item.strip() for item in facebook]
####Twitter####
obj_twitter = s3_resource.Object(BUCKET, 'Company_Keywords/Twitter.txt')
twitter = obj_twitter.get()['Body'].read().decode().split(',')
twitter_list = [item.strip() for item in twitter]
####Snapchat####
obj_snapchat = s3_resource.Object(BUCKET, 'Company_Keywords/Snapchat.txt')
snapchat = obj_snapchat.get()['Body'].read().decode().split(',')
snapchat_list = [item.strip() for item in snapchat]
####Johnson & Johnson####
obj_jnj = s3_resource.Object(BUCKET, 'Company_Keywords/Johnson&Johnson.txt')
jnj = obj_jnj.get()['Body'].read().decode().split(',')
jnj_list = [item.strip() for item in jnj]
####Pfizer####
obj_pfizer = s3_resource.Object(BUCKET, 'Company_Keywords/Pfizer.txt')
pfizer = obj_pfizer.get()['Body'].read().decode().split(',')
pfizer_list = [item.strip() for item in pfizer]
####UnitedHealth Group####
obj_unihealth = s3_resource.Object(BUCKET, 'Company_Keywords/UnitedHealthGroup.txt')
unihealth = obj_unihealth.get()['Body'].read().decode().split(',')
unihealth_list = [item.strip() for item in unihealth]
####Amazon####
obj_amazon = s3_resource.Object(BUCKET, 'Company_Keywords/Amazon.txt')
amazon = obj_amazon.get()['Body'].read().decode().split(',')
amazon_list = [item.strip() for item in amazon]
####E-Bay####
obj_ebay = s3_resource.Object(BUCKET, 'Company_Keywords/E-Bay.txt')
ebay = obj_ebay.get()['Body'].read().decode().split(',')
ebay_list = [item.strip() for item in ebay]
####Walmart####
obj_walmart = s3_resource.Object(BUCKET, 'Company_Keywords/Walmart.txt')
walmart = obj_walmart.get()['Body'].read().decode().split(',')
walmart_list = [item.strip() for item in walmart]
####McDonald's####
obj_mcd = s3_resource.Object(BUCKET, 'Company_Keywords/McDonalds.txt')
mcd = obj_mcd.get()['Body'].read().decode().split(',')
mcd_list = [item.strip() for item in mcd]
####Starbucks####
obj_starbucks = s3_resource.Object(BUCKET, 'Company_Keywords/Starbucks.txt')
starbucks = obj_starbucks.get()['Body'].read().decode().split(',')
starbucks_list = [item.strip() for item in starbucks]
####Taco Bell####
obj_taco = s3_resource.Object(BUCKET, 'Company_Keywords/TacoBell.txt')
taco = obj_taco.get()['Body'].read().decode().split(',')
taco_list = [item.strip() for item in taco]

driver = webdriver.Chrome('C:\Python27\Scripts\chromedriver.exe')
driver.get("https://www.wsj.com/")
time.sleep(5)
driver.find_element_by_link_text("Sign In").click()
time.sleep(5)
# driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys("")
# driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("")
driver.find_element_by_css_selector("button.solid-button.basic-login-submit").click()
time.sleep(10)

# need to find date, link, header, content, keywords
# for one archive link: http://www.wsj.com/news/archive/20180728
final_json_dict = []
for archive_url_list in hrefList:
    links = []
    date = archive_url_list[-8::]  # 20180728
    driver.get(archive_url_list)  # http://www.wsj.com/news/archive/20180728
    time.sleep(10)
    elements = driver.find_elements_by_xpath("//div[contains(@class, 'WSJTheme--headline--7VCzo7Ay ')]")
    for element in elements:  # selenium information
        urls = element.find_elements_by_tag_name("a")
        for url in urls:  # selenium information
            # date_list.append([archive_url_list[-8:],url.get_attribute("href")])
            links.append(url.get_attribute("href"))  # list of links in http://www.wsj.com/news/archive/20180728

    for link in links:  # list of links in http://www.wsj.com/news/archive/20180728
        time.sleep(5)
        article_content = []
        header = ''

        prev_window = driver.current_window_handle
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(link)
        main_window = driver.current_window_handle

        # header
        header_elements = driver.find_elements_by_xpath(
            "//div[contains(@class, 'wsj-article-headline-wrap')]/h1")  # selenium information
        if header_elements == []:
            header = 'Article'

        for element in header_elements:
            # print(element.text)
            if element.text != '':
                header = element.text
            else:
                header = 'Article'

        if 'What’s News' in header:
            continue

        # content
        some_list = ['Customer Service', 'Ads', 'WSJ Membership', 'Tools & Features', 'More']
        content_elements = driver.find_elements_by_tag_name('p')
        for element in content_elements:
            article_content.append(element.text)

        for words in article_content:
            if words in some_list:
                article_content.remove(words)

        article_content_duplicate = article_content
        article_content_duplicate = list(filter(None, article_content_duplicate))
        article_content_duplicate = article_content_duplicate[1:-3]

        if len(article_content_duplicate) <= 5:
            continue

        number_of_words = 0
        number_of_chartot = 0
        for name in article_content_duplicate:
            number_of_words = number_of_words + len(name.split())
            number_of_chartot = number_of_chartot + len(name)
        number_of_char = number_of_chartot
        while number_of_char > 5000:
            middle_index = math.ceil(len(article_content_duplicate) / 2)
            article_content_duplicate.pop(middle_index)
            number_of_char = 0
            number_of_words = 0
            for name in article_content_duplicate:
                number_of_words = number_of_words + len(name.split())
                number_of_char = number_of_char + len(name)
        # keywords
        try:
            keywords = driver.find_element_by_xpath("//meta[contains(@name, 'keywords')]").get_attribute('content')
            keyword_list = list(keywords.split(","))
            strip_keyword_list = [item.strip() for item in keyword_list]
        except:
            continue

        driver.switch_to.window(prev_window)
        driver.close()
        driver.switch_to.window(main_window)

        for word in delta_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('#####Delta####')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'Airline/' + 'DeltaAirline/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Airline', 'Company': 'Delta Air Lines', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in southwest_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####southwest####')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'Airline/' + 'Southwest/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Airline', 'Company': 'Southwest Airlines', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in unitedhealth_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####unitairline####')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'Airline/' + 'UnitedAirline/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Airline', 'Company': 'United Airlines Holdings', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in facebook_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####facebook')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'SocialMedia/' + 'Facebook/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Social Media', 'Company': 'Facebook', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in twitter_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####twitter')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'SocialMedia/' + 'Twitter/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Social Media', 'Company': 'Twitter', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in snapchat_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####snapchat')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'SocialMedia/' + 'Snapchat/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Social Media', 'Company': 'Snapchat', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in jnj_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####jnj')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'Healthcare/' + 'JNJ/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Healthcare', 'Company': 'Johnson and Johnson', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in pfizer_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####pfizer')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'Healthcare/' + 'Pfizer/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Healthcare', 'Company': 'Pfizer', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in unihealth_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####unihealth')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'Healthcare/' + 'UnitedHealth/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Healthcare', 'Company': 'UnitedHealth Group', 'date': date, 'link': link,
                         'header': header, 'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in amazon_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####amazon')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'E-commerce/' + 'Amazon/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'E-commerce', 'Company': 'Amazon', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in ebay_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####ebay')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'E-commerce/' + 'Ebay/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'E-commerce', 'Company': 'E-Bay', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in walmart_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####walmart')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'E-commerce/' + 'Walmart/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'E-commerce', 'Company': 'Walmart', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in mcd_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####mcd')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'FastFood/' + 'McDonalds/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Fast Food', 'Company': 'Mc Donalds', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in starbucks_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####starbucks')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'FastFood/' + 'Starbucks/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Fast Food', 'Company': 'Starbucks', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

        for word in taco_list:
            for keyword in strip_keyword_list:
                if word.lower() in keyword.lower():
                    print('####tacobell')
                    print(word.lower())
                    # s3.put_object(Body = json.dumps(article_content_duplicate), Bucket = BUCKET, Key = 'ScrapedContent_Companywise/' + 'FastFood/' + 'TacoBell/' + date + '/' + link.split('/')[-1] + '.txt')
                    final_json_dict.append(
                        {'Category': 'Fast Food', 'Company': 'Taco Bell', 'date': date, 'link': link, 'header': header,
                         'keywords': strip_keyword_list, 'content': article_content_duplicate})
                    break

df = pd.DataFrame(final_json_dict)
df.to_csv(csv_buffer)
s3_resource.Object(BUCKET, 'Final_content/' + 'Year/' + '2018/' + '0302_0305.csv').put(Body=csv_buffer.getvalue())