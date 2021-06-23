from os import listdir
from os.path import isfile, join
import re, string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from google_trans_new import google_translator
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
browser = webdriver.Chrome(executable_path=
                           '/Users/aryaroy/PycharmProjects/WonDerivation/chromedriver', options=options)

browser.get('https://byjus.com/chemistry/118-elements-their-symbols-atomic-numbers/')
el = browser.find_elements_by_xpath('//*[@id="post-973094"]/div[1]/table/tbody/tr')
dct = {}
dct[0] = 'null'

for i in range(1, len(el)):
    dct[i] = browser.find_element_by_xpath(f'//*[@id="post-973094"]/div[1]/table/tbody/tr[{i + 1}]/td[1]/a').text


def pyth_sum(s):
    sm = 0
    while s:
        sm += (s % 10)
        s = s // 10
    return sm


def check_term(w):
    for i in w:
        if i.isnumeric():
            return False
    return True


col_names = ['Spanish Term', 'English Translation']
for i in range(1, 17):
    col_names.append(f'Result {i}')
count_no_en = []
for letter in string.ascii_lowercase:
    word_list = []
    word_list_en = []
    browser.get(f'https://www.collinsdictionary.com/us/browse/spanish-english/spanish-words-starting-with-{letter}')
    el = browser.find_elements_by_xpath('//*[@id="main_content"]/div[1]/div/div/ul[2]/li')
    # //*[@id="main_content"]/div[1]/div/div/ul[2]/li[3]/a
    for i in range(len(el)):
        browser.get(f'https://www.collinsdictionary.com/us/browse/spanish-english/spanish-words-starting-with-{letter}')
        a = browser.find_element_by_xpath(f'//*[@id="main_content"]/div[1]/div/div/ul[2]/li[{i + 1}]/a').get_attribute(
            'href')
        browser.get(a)
        el_1 = browser.find_elements_by_xpath(f'//*[@id="main_content"]/div[1]/div/div/ul[2]/li')
        for j in range(len(el_1)):
            browser.get(a)
            link = browser.find_element_by_xpath(f'//*[@id="main_content"]/div[1]/div/div/ul[2]/li[{j + 1}]/a')
            browser.get(link.get_attribute('href'))
            word_list.append(browser.find_element_by_class_name('orth').text)
            # print(browser.find_element_by_class_name('orth').text)
            try:
                word_list_en.append(browser.find_element_by_class_name('cit.type-translation.quote').text)
            except:
                if browser.find_elements_by_class_name('form.type-expan.orth'):
                    word_list_en.append(browser.find_element_by_class_name('form.type-expan.orth').text)
                elif browser.find_elements_by_class_name('ref'):
                    browser.get(browser.find_element_by_class_name('ref').get_attribute('href'))
                    if browser.find_elements_by_class_name('cit.type-translation.quote'):
                        word_list_en.append(browser.find_element_by_class_name('cit.type-translation.quote').text)
                    else:
                        word_list_en.append(browser.find_element_by_class_name('orth').text)
                else:
                    word_list_en.append(browser.find_element_by_class_name('orth').text)
    list_dat = []
    for indx, sp_word in enumerate(word_list):
        if check_term(sp_word):
            rw = [sp_word]
            rw.append(word_list_en[indx])
            res_l = []
            for j in sp_word:
                if ord(j.lower()) - 96 in range(1, 27):
                    try:
                        res_l.append(ord(j.lower()) - 96)
                    except:
                        continue
            # print(res_l)
            l, c = [], 0
            go = True
            while go:
                s = 0
                go = False
                for k in range(len(res_l)):
                    if res_l[k] > 9:
                        go = True
                    s += res_l[k]
                    res_l[k] = pyth_sum(res_l[k])
                # print(res_l)
                while s > 118:
                    s = pyth_sum(s)
                # l.append(dct[s])
                if s:
                    rw.append(str(s) + '_' + dct[s])
                else:
                    rw.append(dct[s])
                while s > 9:
                    s = pyth_sum(s)
                    if s:
                        rw.append(str(s) + '_' + dct[s])
                    else:
                        rw.append(dct[s])
                    c += 1
                c += 1
            for x in range(16 - c):
                # l.append('null')
                rw.append('null')
            list_dat.append(tuple(rw))
        # print(tuple(rw))
    df = pd.DataFrame(list_dat, columns=col_names)
    print(letter,df.shape)
    writer = pd.ExcelWriter(f'esp_collins_dct_{letter}.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name=f'esp_{letter}')
    writer.save()
# print(count_no_en)
# print(df.shape)

# browser.get('https://spanishforyourjob.com/commonwords/')
#
# el = browser.find_elements_by_xpath('//*[@id="post-1262"]/div/table/tbody/tr')
# esp_wrds = []
# for i in range(1, len(el)):
#     esp_wrds.append(browser.find_element_by_xpath(f'//*[@id="post-1262"]/div/table/tbody/tr[{i + 1}]/td[2]').text)
#
# l_l = []
# for i in esp_wrds:
#     if not df['Term'].eq(i).any():
#         print(i)
#     else:
#         l_l.append([i, df.index[df['Term'] == i].tolist()[0] // 150000 + 1,
#                     (df.index[df['Term'] == i].tolist()[0] % 150000) // 50000 + 1])
#
# df_1 = pd.DataFrame(l_l, columns=['Term', 'File', 'Tab'])
#
# df_1.to_csv('common_esp_terms.csv', index=False)
#
