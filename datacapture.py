# coding: utf-8
# author: xujipm

import requests
import time
import json
import random
from bs4 import BeautifulSoup


proxies = []
agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0']
testUrl = 'https://fuwu.taobao.com/ser/list.html?tracelog=category&listType=0&isMultiList=0&primary_sort=user_count&primary_sort_desc=true&currentPage=1'
testUrl = 'https://fuwu.taobao.com/ser/list.html?spm=a1z13.1113643.0.0.8JbHZi&listType=0&isMultiList=0&primary_sort=default_sort_tag&primary_sort_desc=true'
testItems = {'name': 'div > p:nth-child(1) > span',
             'is_official': 'div > p:nth-child(2) > span',
             'company': 'div > p:nth-child(2) > a',
             'is_tp': 'div > p:nth-child(2) > a.flag-tp',
             'tp_img': 'div > p:nth-child(2) > a.flag-tp',
             'wangwang': 'div > p:nth-child(2) > span > a',
             'price': 'div > div.content-list-users > span.content-list-price',
             'users-amount': 'div > div.content-list-users > span.users-amount',
             'rate': 'div > div.content-list-users > span.ui-no-rate',
             'img': 'a > img',
             'link': 'a',
             }
testItem = {
    'easy': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.dimension > li:nth-child(1) > span.high.per',
    'service': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.dimension > li:nth-child(2) > span.high.per',
    'stable': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.dimension > li:nth-child(3) > span.high.per',
    'security': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.use-state > li:nth-child(1) > span.count',
    'paying-users': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.use-state > li:nth-child(2) > span.count',
    '30days': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.use-state > li:nth-child(2) > span.color-gray',
    'repay': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.use-state > li:nth-child(3) > span.count',
    'refund': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.use-state > li:nth-child(4) > span.count',
    'open-rate': '#apc-detail > div.content > div.meta-wrap.clearfix > div.col-sub.col-sub-right > div > ul.use-state > li:nth-child(5) > span.count',
    'comments': '#J_ItemTab > div > ul > li:nth-child(4) > a > span',
    'orders': '#J_ItemTab > div > ul > li:nth-child(5) > a > span',
    'authenticate': '#apc-detail > div.service-detail > div > div > p:nth-child(2) > img',
    'son-title': '#J_SKUForm > div.service-intro > p',
    'PC-able': '#J_SKUForm > div.service-intro > h2 > i.ico-exter.ico-exter-pc',
    'MB-able': '#J_SKUForm > div.service-intro > h2 > i.ico-exter.ico-exter-mb'

    }
localOfNext = '#apc-list > div.content-wrap.clearfix > div.col-main > div > div.tbl-service-attach > div > div > a.page-next'


def getProxy():
    global proxies
    proxyUrl = 'http://proxy.mimvp.com/api/fetch.php?' \
               'orderid=860160504214312199&' \
               'num=100&' \
               'country_group=1&http_type=2&' \
               'anonymous=5&' \
               'isp=5&' \
               'ping_time=0.3&' \
               'result_format=json'

    while len(proxies) == 0:
        print('获取Proxy. . .')
        try:
            proxyData = json.loads(requests.get(proxyUrl).text)['result']
            for p in range(len(proxyData)):
                proxies.append({'http': 'http://' + proxyData[p]['ip:port'], 'https': 'http://' + proxyData[p]['ip:port'], })
            time.sleep(1)
            #print(time.ctime())
        except:
            print('获取proxy失败')
    result = proxies[random.randrange(len(proxies))]
    print('使用代理： ', result)
    return result


def getItems(_request_url, _items, _header, _proxies=None, _list='html'):
    global proxies
    result = []
    flag = 1
    while flag:
        try:
            webData = requests.get(_request_url, headers=_header, proxies=_proxies, timeout = 30)
            flag = 0
        except BaseException as Argument:
            print('代理失效: ',_proxies,' + ',Argument)
            proxies.remove(_proxies)
            _proxies = getProxy()

    soup = BeautifulSoup(webData.text, 'lxml')
    try:
        print('https:' + soup.select(localOfNext)[0].get('href'))
    except:
        pass
    itemNum = len(soup.select(_list))
    if _list == 'html':
        localHead = ''
        itemNum = 1
    for i in range(itemNum):
        # for i in range(1):
        item = {}
        for (name, local) in _items.items():
            if _list != 'html':
                localHead = _list + ':nth-of-type(' + str(i + 1) + ') > '
            local = localHead + local.replace('nth-child', 'nth-of-type')
            # print(name,local)
            try:
                if name == 'is_tp':
                    item[name] = soup.select(local)[0].get('title')
                elif name == 'tp_img':
                    item[name] = soup.select(local)[0].get('style')
                elif name == 'wangwang':
                    # 还有问题
                    # content-list > li:nth-child(6) > div > p:nth-child(2) > span > a
                    item[name] = soup.select(local)[0].get('href')
                elif name == 'rate':
                    item[name] = soup.select(local)[0].get('title')
                elif name == 'img':
                    item[name] = soup.select(local)[0].get('src')
                elif name == 'link':
                    item[name] = 'https:' + soup.select(local)[0].get('href')
                    #print(name, item[name])
                    detail = getItems(item[name], testItem, _header)[0]
                    # print('--logout--',item,detail,sep='\n\r==')
                    item = dict(item, **detail)
                elif name == 'authenticate':
                    item[name] = soup.select(local)[0].get('title')
                elif name == 'PC-able':
                    item[name] = soup.select(local)[0].get('title')
                elif name == 'MB-able':
                    item[name] = soup.select(local)[0].get('title')
                else:
                    # print(local)
                    item[name] = soup.select(local)[0].get_text(strip=True)
            except:
                item[name] = ''
            # print(name,item[name])
        result.append(item)
        # print(item)
    # print(result)
    return result


print('Start Time:', time.ctime())
print(getItems(testUrl, testItems, {'User-Agent': agents[0]}, getProxy(), '#content-list > li'))
testUrl = 'https://fuwu.taobao.com/ser/detail.html?service_code=appstore-22384'
print('End   Time:', time.ctime())
#print(getItems(testUrl, testItem, {'User-Agent': agents[0]}))

# content-list > li:nth-child(1)
# content-list > li:nth-child(2)
# content-list > li:nth-child(1) > div > p:nth-child(1) > span
# content-list > li:nth-child(3) > div > p:nth-child(2) > a.flag-offical
