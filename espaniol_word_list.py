from os import listdir
from os.path import isfile, join
import re, string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xlsxwriter

mypath = '/Users/aryaroy/PycharmProjects/WonDerivation/archive-2/spanish_corpus/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
text_dat_s = set()
for i in onlyfiles:
    with open(f"/Users/aryaroy/PycharmProjects/WonDerivation/archive-2/spanish_corpus/{i}", "r",
              encoding='latin-1') as file:
        text = file.read()

    # check to make sure the file read in alright; let's print out the first 1000 characters
    text = re.sub('<.*>', '', text)

    # get rid of the "ENDOFARTICLE." text
    text = re.sub('ENDOFARTICLE.', '', text)

    # get rid of punctuation (except periods!)
    punctuationNoPeriod = "[" + re.sub("\.", "", string.punctuation) + "]"
    text = re.sub(punctuationNoPeriod, "", text)
    text_dat = text.split()
    text_dat_s = text_dat_s.union(set(text_dat))
text_dat_s = list(text_dat_s)
text_dat_s.sort()

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


list_dat = []
for i in text_dat_s:
    if check_term(i):
        rw = [i]
        translate_text = translator.translate('a caballo entre', lang_tgt='en')
        rw.append(translate_text)
        res_l = []
        for j in i:
            if ord(j.lower()) - 96 in range(1,27):
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

col_names = ['Term']
for i in range(1, 17):
    col_names.append(f'Result {i}')
df = pd.DataFrame(list_dat, columns=col_names)

browser.get('https://spanishforyourjob.com/commonwords/')

el = browser.find_elements_by_xpath('//*[@id="post-1262"]/div/table/tbody/tr')
esp_wrds = []
for i in range(1, len(el)):
    esp_wrds.append(browser.find_element_by_xpath(f'//*[@id="post-1262"]/div/table/tbody/tr[{i + 1}]/td[2]').text)

l_l = []
for i in esp_wrds:
    if not df['Term'].eq(i).any():
        print(i)
    else:
        l_l.append([i, df.index[df['Term'] == i].tolist()[0] // 150000 + 1,
                    (df.index[df['Term'] == i].tolist()[0] % 150000) // 50000 + 1])

df_1 = pd.DataFrame(l_l, columns=['Term', 'File', 'Tab'])

df_1.to_csv('common_esp_terms.csv', index=False)

writer = pd.ExcelWriter(f'esp_dct_1.xlsx', engine='xlsxwriter')
for i in range(0,df.shape[0],50000):
    if i > 0 and not i%150000:
        writer.save()
        writer = pd.ExcelWriter(f'esp_dct_{i // 150000 + 1}.xlsx', engine='xlsxwriter')
    df.iloc[i:min(i+50000,df.shape[0]),:].to_excel(writer, sheet_name=f'esp_{i//50000+1}')
writer.save()
