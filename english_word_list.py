# import nltk
# nltk.download('wordnet')
import string
import time
import tarfile

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from itertools import chain

from nltk.corpus import wordnet as wn

c = 0
# wl = [i for i in wn.words()]
# for i in wl[::-1]:
#     if c<20:
#         print(i)
#     c+=1
# c=0
# with open('wordnet_dict.txt','w+') as f:
#     for ss in wn.all_synsets():
#         f.write(str(ss)[8:-2]+'\n')
#         for i in ss.lemma_names():
#             c+=1
#             f.write(i+'\n')
# print(c)
# c=0
# with open('words_alpha.txt','r') as f:
#     for line in f:
#         for word in line:
#             if not len(wn.synsets(word)):
#                 c+=1
# print(c)

# tar = tarfile.open("aspell6-en-2020.12.07-0.tar.bz2", "r:bz2")
# tar.extractall()
# tar.close()

# r = requests.get('https://www.merriam-webster.com/browse/dictionary/a')
# soup = bs(r.content, 'lxml')
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# browser = webdriver.Chrome(executable_path=
#                            '/Users/aryaroy/PycharmProjects/WonDerivation/chromedriver',options=options)
# with open('words_mariam_1.txt','w+') as f:
#     for i in string.ascii_lowercase[-3:]:
#         pg=1
#         browser.get(f'https://www.merriam-webster.com/browse/dictionary/{i}/{pg}')
#         if i=='x':
#             a=browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/div[2]/div[1]/div/div[2]/div/ul/li[6]/a')
#         else:
#             a = browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/div[2]/div[1]/div/div[2]/div/ul/li[7]/a')
#         pg = int(a.get_attribute('href').split('/')[-1])
#         for m in range(1,pg+1):
#             browser.get(f'https://www.merriam-webster.com/browse/dictionary/{i}/{m}')
#             time.sleep(2)
#             for j,k in enumerate(browser.find_elements_by_xpath('/html/body/div[1]/div/div[6]/div[2]/div[1]/div/div[3]/ul/li')):
#                 for l in browser.find_elements_by_xpath(f'/html/body/div[1]/div/div[6]/div[2]/div[1]/div/div[3]/ul/li[{j+1}]/a'):
#                     f. write(l.text+'\n')
######
s1, s2 = set(), set()

with open('words_alpha.txt', 'r') as f:
    for line in f:
        s1.add(line)

with open('words_mariam.txt', 'r') as f:
    for line in f:
        s2.add(line)

s3 = s1.union(s2)
lst_wrds = list(s3)
lst_wrds.sort()
s = 0
# for i in range(5):
    # print(s3.pop(),s2.pop(),s1.pop())
    # print(lst_wrds[i])


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


list_dat = []
for i in lst_wrds:
    rw = [i[:-1]]
    res_l = []
    for j in i:
        if j in string.ascii_lowercase or j in string.ascii_uppercase:
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
            rw.append(str(s)+'_'+dct[s])
        else:
            rw.append(dct[s])
        while s>9:
            s=pyth_sum(s)
            if s:
                rw.append(str(s)+'_'+dct[s])
            else:
                rw.append(dct[s])
            c+=1
        c+=1
    for x in range(16-c):
        # l.append('null')
        rw.append('null')
    list_dat.append(tuple(rw))
    # print(tuple(rw))
col_names= ['Term']
for i in range(1,17):
    col_names.append(f'Result {i}')
df = pd.DataFrame(list_dat,columns=col_names)

writer = pd.ExcelWriter(f'eng_dct_1.xlsx', engine='xlsxwriter')
for i in range(0,df.shape[0],50000):
    if i > 0 and not i%150000:
        writer.save()
        writer = pd.ExcelWriter(f'eng_dct_{i // 150000 + 1}.xlsx', engine='xlsxwriter')
    # print(i+50000,df.shape[0])
    df.iloc[i:min(i+50000,df.shape[0]),:].to_excel(writer, sheet_name=f'eng_{i//50000+1}')
writer.save()
# df.to_excel('eng_dct_4.xlsx',sheet_name='Eng_Dictionary')

df = pd.read_excel('eng_dct_4.xlsx')
print(df.shape)

