# -*- coding:utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import csv, os, urllib.request
from .models import Stock, Article, Stocklist
from datetime import datetime
from django.db.models import Max
import pandas as pd
import time
from konlpy.tag import Kkma, Twitter
from collections import Counter
import re, difflib
from itertools import groupby
from operator import itemgetter

TODAY = datetime.now().date()

'''키워드 분석 함수'''
def ngram_counter(article, max_n=3, min_count=1):
    counter={}
    sents = tuple(article.split('.'))
    for sent in sents:
        words = sent.split(' ')
        for word in words:
            for begin in range(len(words) - 1):
                for end in range(begin+2, min(begin+max_n, len(words))):
                    ngram = ' '.join(words[begin:end]).strip()
                    counter[ngram] = counter.get(ngram, 0) + 1
                    
    rtn = {ngram:count for ngram, count in counter.items() if count >= min_count}
    return rtn

def check_word_similarity(s1,s2):
    s1w = re.findall('[ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|W*]', s1.lower())
    s2w = re.findall('[ㄱ-ㅎ|가-힣|a-z|A-Z|0-9|W*]', s2.lower())
                     
    s1cnt = Counter(s1w)
    s2cnt = Counter(s2w)
    
    common = set(s1w).intersection(s2w)
    
    common_ratio = difflib.SequenceMatcher(None, s1w, s2w).ratio()
    return common_ratio
            
def counter_reduce(counter, un_word=['$^$%']):
    new_counter = {}
    examined = []
    word_list = list(counter.keys())
    for idx, word1 in enumerate(word_list):
        for word2 in word_list[idx+1:]:
            if check_word_similarity(word1, word2) > 0.65 and word1 not in examined and word2 not in examined:
                if counter.get(word1,0) > counter.get(word2,0):
                    new_counter[word1] = counter[word1] + counter[word2]
                else:
                    new_counter[word2] = counter[word1] + counter[word2]
                del counter[word1]
                del counter[word2]
                examined.extend([word1,word2])
                break
    result = {**new_counter, **counter}
    return result

def sort_counter(counters, limit=1):
    n = limit * round(len(counters))               
    rtn = sorted(counters.items(), key=lambda x:x[1], reverse=True)[:n]
    return rtn

def noun_extractor(ngrams):
    twitter = Twitter()
    rtn = {}
    for ngram, key in ngrams.items():
        words = twitter.pos(ngram)
        allowed = ['Noun','Alpha','Number','Punctuation']
        not_allowed = ['\"','->','[',']']
        complex_noun=''
              
        for word in words:
            if word[1] in allowed and word[0] not in not_allowed:
                complex_noun += ' ' + word[0]
        complex_noun = complex_noun.strip()
        if len(complex_noun) > 1:
            rtn[complex_noun] = key
    return rtn
''' 끝 '''

def crawl_stock():
    stocklist = pd.read_csv('board/csv/stock_list.csv', delimiter=',', encoding='utf-8', header=0, index_col=1)
    for code in stocklist.index.tolist():
        #starting_date = Stock.objects.filter(stock_id=code).aggregate(Max('date')).get('date__max')
        starting_date = TODAY
        #starting_date = datetime.strptime('2018-11-07','%Y-%m-%d').date()
        print(code)
        for page in [1]:
            for row in [2,3,4,5,6,10,11,12,13,14]:
                URL = 'https://finance.naver.com/item/sise_day.nhn?code={0}&page={1}'.format(code,page)
                source_from_URL = urllib.request.urlopen(URL).read().decode('cp949','ignore')
                soup = BeautifulSoup(source_from_URL, "html.parser")
                result = [ x.get_text(strip=True).replace(',','') for x in soup.findAll('tr')[row].findAll('span')]
                
                try:
                    updown_direction = soup.findAll('tr')[row].findAll('img')[0]['alt']
                except IndexError:
                    pass
                except KeyError:
                    updown_direction = soup.findAll('tr')[row].findAll('img')[0]['src'][-8:-4]
                    if updown_direction == 'wn02':
                        result[2] = '-' + result[2]
                else:
                    if updown_direction == '하락':
                        result[2] = '-' + result[2]

                try:
                    date = datetime.strptime(result[0],"%Y.%m.%d").date()
                    if date < starting_date:
                        break
                except ValueError:
                    break
                else:
                    is_obj = Stock.objects.filter(date=date, stock_id=code).count()
                    
                    if not is_obj:          
                        stock = Stock(
                            date = date,
                            stock = Stocklist.objects.get(stock_id=code),
                            price = result[1],
                            updown = result[2],
                            max_price = result[4],
                            min_price = result[5],
                            sales_amount = result[6],
                            updown_percentage = round(int(result[2]) / int(result[1]) * 100,2)
                        )
                        stock.save()
                    else:
                        break

def crawl_article_url():
    stocklist = pd.read_csv('board/csv/stock_list.csv', delimiter=',', encoding='utf-8', header=0, index_col=1)
    
    file_name = 'board/csv/news_url.csv'
    header = ['종목코드','종목명','제목','날짜','주소']
    mode = 'w'
        
    with open(file_name, mode, encoding='utf-8', newline='') as f:
        count2 = 0
        wr = csv.writer(f)
        if mode == 'w':
            wr.writerow(header)
    
        for code in stocklist.index.tolist()[546:]:
            #starting_date = Article.objects.filter(stock_id=code).aggregate(Max('date')).get('date__max')
            #starting_date = datetime.strptime('2018-11-07','%Y-%m-%d').date()
            starting_date = TODAY
            stock_name = stocklist.loc[code].종목명
            print(stock_name)
            page = 1

            while page > 0:
                URL = 'http://search.chosun.com/search/news.search?query={0}&pageno={1}&orderby=docdatetime&naviarraystr=&kind=&cont1=&cont2=&cont5=&categoryname=&categoryd2=&c_scope=&sdate=&edate=&premium='.format(code,page)
                source_from_URL = urllib.request.urlopen(URL).read().decode('utf-8','ignore')
                soup = BeautifulSoup(source_from_URL, "html.parser")
                page += 1
                
                for i in range(0,10):
                    try:
                        title = soup.find_all("dl", class_="search_news")[i].find('dt').a.get_text()
                        date = soup.find_all("dl", class_="search_news")[i].find('span', class_="date").get_text()[:-4]
                        url = soup.find_all("dl", class_="search_news")[i].find('dt').a['href']
                    except (IndexError, AttributeError):
                        page = 0
                    else:
                        date = datetime.strptime(date, "%Y. %m. %d").date()
                        if (date and starting_date):
                            if date >= starting_date:                       
                                result = [title, date, url]
                                result.insert(0,stock_name)
                                result.insert(0,code)
                                wr.writerow(result)
                            else:
                                page = 0
                                print('없음')
                                break
                        
def crawl_article():
    data = pd.read_csv('board/csv/news_url.csv', delimiter=',', encoding='utf-8',  dtype={'종목코드':str})

    for idx in data.index.tolist():
        URL = data.주소[idx]
        source_from_URL = urllib.request.urlopen(URL).read()
        soup = BeautifulSoup(source_from_URL, "html.parser")
        
        stock = Stocklist.objects.get(stock_id=data.종목코드[idx])
        
        article = Article(
            stock = stock,
            title = data.제목[idx],
            url = data.주소[idx],                
            date = datetime.strptime(data.날짜[idx],'%Y-%m-%d')###
        )
        article.save()
        content = ''.join([x.get_text() for x in soup.findAll("div", class_="par")])
        cnt = sort_counter(counter_reduce(noun_extractor(ngram_counter(content))))[:10]
        keyword = '\n'.join([x[0] for x in cnt])
        article.keyword = keyword
        article.save()
        
                
def csv_stock():
    stockprice = pd.read_csv('board/csv/stock_price.csv', delimiter=',', encoding='utf-8', header=0, dtype={'종목코드':'str'})
    
    for idx in stockprice.index.tolist():
        item = stockprice.loc[idx]
        print(item.날짜)
        
        stock = Stock.objects.create(
            date = datetime.strptime(item.날짜,"%Y-%m-%d").date(),
            stock = Stocklist.objects.get(stock_id=item.종목코드),
            price = item.종가,
            max_price = item.고가,
            min_price = item.저가,
            sales_amount = item.거래량,
            updown = item.전일비,
            updown_percentage = item.전일비퍼센트,
        )
        stock.save()
        
def csv_article():
    articlelist = pd.read_csv('board/csv/article_list.csv', delimiter=',', encoding='utf-8', header=0, dtype={'종목코드': 'str'})
    
    for idx in articlelist.index.tolist():
        item = articlelist.loc[idx]
        print(idx)
        stock=Stocklist.objects.get(stock_id=item.종목코드)
        
        article = Article(
            date = datetime.strptime(item.날짜,"%Y-%m-%d").date(),
            stock = stock,
            title = item.제목,
            url = item.주소,
            keyword = item.키워드
        )
        article.save()
        
