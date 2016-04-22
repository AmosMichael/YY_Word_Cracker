# -*- coding: utf-8 -*-
from __future__ import division
import urllib
import urllib2
import cookielib
import re

import sys,time
from progressbar import *

print(u"yy_word_cracker.一个为了解释大量英语单词而生的程序.")
print("From now, you don't need to consult any dictionary by hand!!!Do a few， Think much.")
print(u"注意：程序使用说明已经存在于你的Ｄ盘")
note = open("D:\\yy_word_cracker_userbook.txt", "w")
note.write("你需要做:把需要解释的大量单词放在D盘根目录名为yy_freshword.txt文件里（每行放置一个单词），然后运行yy_word_cracker.单词解释会自动从网上下载到D盘名为yy_wordcracker.txt文件里*!*")
note.close()
print(u"你可以使用此程序，但不可分发。This written by Amos. Fork me on GitHub.")
time.sleep(0)
print("Please waite. I'm busing....")
#filename = 'F:\\save.txt'
cookie = cookielib.MozillaCookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)


def_block_pattern = re.compile(r'<!-- End of DIV def-block-->', re.S)

word_pattern = re.compile(r'<span class="hw">(.*?)</span>', re.S)
pron_pattern = re.compile(r'<span class="uk"><span class="pron">.*?</span></span>', re.S)

pos_pattern = re.compile(r'<span class="pos" title=.*?>(.*?)</span>', re.S)
guideword_pattern = re.compile(r'<span class="guideword".*?>(.*?)</span>', re.S)
rent_pattern = re.compile(r'<span .*?class="epp-xref.*?>(.*?)</span>', re.S)
definition_pattern = re.compile(r'<span class="def"(.*?)/span></span>', re.S)
example_pattern = re.compile(r'<span class="examp"><span title="Example" class="eg"(.*?)</span></spa', re.S)
each_word_pattern = re.compile(r'>(.*?)<', re.S)

freshword = open("D:\\yy_freshword.txt", "r")
t_word = 0
target_file = "D:\\YY_WORD_CRACKER.txt"
tempfile = open(target_file, "w")
check = 0
while True:
    check = check + 1
    print check
    store_word = t_word
    t_word = freshword.readline()
    if store_word == t_word:
        break
    url = 'http://dictionary.cambridge.org/dictionary/english/' + t_word
    #print url
    response = opener.open(url)
    content = response.read().decode('utf-8')
    content_pattern = re.compile(r'Cambridge University Press\)', re.S)
    content = re.split(content_pattern, content)
    content = content[0]

    SenseBlock = re.split('<!-- End of DIV sense-block-->', content)

    tempfile.close()
    for i in range(len(SenseBlock)):
        tempfile = open(target_file, 'a')
        word = re.findall(word_pattern, SenseBlock[i])
        if len(word) == 0:
            #print('no world find i = ', i)
            pass
        else:
            word = word[0]
            tempfile.write(word.encode('utf-8'))
            tempfile.write(':')
            pron = re.findall(pron_pattern, SenseBlock[i])
            if len(pron) == 0:
                #print('no pron found at ', i)
                pass
            else:
                pron = pron[0]
                pron_word = re.findall(each_word_pattern, pron)
                for t in range(len(pron_word)):
                    tempfile.write(pron_word[t].encode('utf-8'))

            guideword = re.findall(guideword_pattern, SenseBlock[i])
            if len(guideword) == 0:
                #print('no guide word found at ', i)
                pass
            else:
                guideword = guideword[0]
                guideword = re.sub('\t{1,5}', ' ', guideword)
                guideword = re.sub('\n{1,2}', ' ', guideword)
                guideword = re.sub('\b{1,3}', ' ', guideword)
                guideword = re.sub('\s+', ' ', guideword)
                tempfile.write(guideword.encode('utf-8'))


            pos = re.findall(pos_pattern, SenseBlock[i])
            if len(pos) == 0:
                #print('no pos found at ', i)
                pass
            else:
                pos = pos[0]
                tempfile.write('[' + pos.encode('utf-8') + ']'+'\n\t')

            rent = re.findall(rent_pattern, SenseBlock[i])
            if len(rent) == 0:
                #print('no rent found at ', i)
                pass
            else:
                rent = rent[0]
                tempfile.write('['+rent.encode('utf-8')+']')

            definition = re.findall(definition_pattern, SenseBlock[i])
            if len(definition) == 0:
                #print('no definiton found at ', i)
                pass
            else:
                tempfile.write('def:')
                definition = definition[0]
                def_word = re.findall(each_word_pattern, definition)
                for t in range(len(def_word)):
                    tempfile.write(def_word[t].encode('utf-8'))
                tempfile.write('\n')
                example = re.findall(example_pattern, SenseBlock[i])
                if len(example) == 0:
                    #print('no example found at ', i)
                    pass
                else:
                    tempfile.write('\t\t')
                    for t in range(min(len(example), 5)):
                        example_word = re.findall(each_word_pattern, example[t])
                        for word_i in range(len(example_word)):
                            tempfile.write(example_word[word_i].encode('utf-8'))
                        if t != len(example)-1:
                            tempfile.write('\n\t\t')
                        else:
                            tempfile.write('\n')

        tempfile.close()
        time.sleep(0.5)

tempfile.close()
total = 1000
progress = ProgressBar()
for i in progress(range(total)):
  time.sleep(0.01)

pbar = ProgressBar().start()
for i in range(1,1000):
    pbar.update(int((i/(total-1))*100))
    time.sleep(0.01)
pbar.finish()
