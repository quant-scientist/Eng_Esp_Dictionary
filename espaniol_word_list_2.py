from os import listdir
from os.path import isfile, join
import re, string, glob
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
el = browser.find_elements_by_xpath('//*[@id="post-973094"]/table/tbody/tr')
dct = {}
dct[0] = 'null'

for i in range(1, len(el)):
    dct[i] = browser.find_element_by_xpath(f'//*[@id="post-973094"]/table/tbody/tr[{i + 1}]/td[1]/a').text

print(dct)

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

col_names = ['Spanish Term']
for i in range(1, 17):
    col_names.append(f'Result {i}')

file_list = glob.glob('archive-2/esp_collins_dct_*')

for file in file_list:
    print(file)
    df = pd.read_excel(file)
    try:
        word_list = df['Spanish Term'].tolist()
    except:
        word_list = df['Term'].tolist()
    list_dat = []
    for indx, sp_word in enumerate(word_list):
        if check_term(sp_word):
            rw = [sp_word]
            res_l = []
            for j in sp_word:
                if ord(j.lower()) - 96 in range(1, 27):
                    try:
                        res_l.append(ord(j.lower()) - 96)
                    except:
                        continue
                elif ord(j.lower()) == 225:
                    try:
                        res_l.append(1)
                    except:
                        continue
                elif ord(j.lower()) == 233:
                    try:
                        res_l.append(5)
                    except:
                        continue
                elif ord(j.lower()) == 237:
                    try:
                        res_l.append(9)
                    except:
                        continue
                elif ord(j.lower()) == 243:
                    try:
                        res_l.append(15)
                    except:
                        continue
                elif ord(j.lower()) == 250:
                    try:
                        res_l.append(21)
                    except:
                        continue
                elif ord(j.lower()) == 252:
                    try:
                        res_l.append(21)
                    except:
                        continue
                elif ord(j.lower()) == 241:
                    try:
                        res_l.append(14)
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
    # print(letter, df.shape)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=f'esp_{file[-6]}')
    writer.save()