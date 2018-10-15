import requests
import re
import csv
import time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def get_index(url):
    try:
        content = requests.get(url)
        if content.status_code == 200:
            return content.text
        return None
    except RequestException:
        return None


def parse_region(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    region = soup.select('.mp-sidebar-list')[0]
    hotcitys = region.select('li')
    link_list = []
    for hotcity in hotcitys:
        city = hotcity.get_text().strip()
        link = url + hotcity.select('a')[0]['href'].replace('®ion','&region') + '&page='
        link_list.append(link)
    #         print(city)
    return link_list


def parse_sight(html):
    soup = BeautifulSoup(html, 'html.parser')
    result_list = soup.select('.result_list')[0]
    sight_item = result_list.select('.sight_item')
    sight_list = []
    num = 0
    for item in sight_item:
        #替换掉错误编码的字符
        name = item.select('.sight_item_caption')[0].get_text()
        name = name.replace('\u2219','').replace('\u2022','').replace('\u200b','')
        info = item.select('.sight_item_info')[0]
        area = info.select('.area')[0].get_text().replace('[', '').replace(']', '')
        hot = info.select('.product_star_level')[0].get_text()
        hot_num = re.compile('(\d+\.\d)').search(hot).group(1)
        sale = item.select('.hot_num')
        if len(sale) == 0:
            sale = '免费'
        else:
            sale = sale[0].get_text()
        num += 1
        list = [num,name, area, hot_num, sale]
        print(list)
        sight_list.append(list)
    return sight_list


def write_to_csv(itemlist):
    # 加上encoding = 'utf-8'所写入的文件中会出现乱码，但是不会出现报错
    # 加上encoding = 'gbk'文件中不会出现乱码，但是会报错
    with open('ChinaHotCity2.csv', 'w+', newline='',encoding = 'gbk') as f:
        writer = csv.writer(f)
        writer.writerow(['序号','景区', '地址', '热度', '销量'])
        for item in itemlist:
            writer.writerow(item)

def main():
    url = 'http://piao.qunar.com/'
    html1 = get_index(url)
    link_list = parse_region(html1, url)
    hotcity = []
    for link in link_list:
        sight_list = []
        for i in range(1,11):
            href = link + str(i)
            print(href)
            html2 = get_index(href)
            list = parse_sight(html2)
            sight_list.append(list)
        item_list = [list for sight in sight_list for list in sight]
        hotcity.append(item_list)
        time.sleep(10)
    onehot = [item for city in hotcity for item in city]
    print('爬取记录数:',len(onehot))
    write_to_csv(onehot)

    # print(sight_list)


if __name__ == '__main__':
        main()
