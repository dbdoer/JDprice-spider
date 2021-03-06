from datetime import date, timedelta, datetime  #分别表示日期的类、时间间隔的类、日期时间的类
import time
from urllib.parse import urlencode  #urllib.parase定义了url的标准接口，实现Url的各种抽取，包括解析、合并、编码、解码   而urlencode()则将字典构形式的参数序列化为url编码后的字符串（常用来构造get请求和post请求的参数）k1=v1&k2=v2
import xlwt         #xlrd模块实现对excel文件内容读取
import xlrd         #xlwt模块实现对excel文件的写入
import requests     #requests库
import re           #正则表达式，用来处理字符串，最常用到三个函数的是match，search，findall
from requests import RequestException   #异常化处理
import  tokenGet

def get_one_page(url, token):                                                # 获取要爬取的网页
    group = {'DA': 1, 'action': 'gethistory', 'url': url, 'bjid': '',        # url是输入进来的京东url
             'spbh': '', 'cxid': '', 'zkid': '', 'w': 951, 'token': token    # token需要手动记录，与url对应
             }
    url = "http://tool.manmanbuy.com/history.aspx?" + urlencode(group)       # 网址格式，url从京东链接变为request的网址
    try:
        kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
        res = requests.get(url, headers=kv)
        if res.status_code == 200:
            return res.text
        else:
            return None
    except RequestException:
        print('请求失败！！')
        return None

def parse_one_page(html):
    pattern = re.compile(r'\[(.*?),(.*?),\\"(.*?)\\"\],', re.S)    #如果不使用re.S参数，则只在每一行内进行匹配，如果一行没有，就换下一行重新开始，不会跨行。
                                                                #而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，将“\n”当做一个普通的字符加入到这个字符串中，在整体中进行匹配。
    items = re.findall(pattern, html)   #找到所有的日期和价格
    for item in items:                  #存入item
        yield {
            'date': time.strftime("%Y-%m-%d",time.localtime(int(item[0])/1000)),   #日期格式xxxx-xx-xx
            'price': item[1],
            'discount':item[2]
        }
def main():
    f1 = open('url.txt', 'r')
    index = 1
    while True:
      url = f1.readline()  # 一行行读取url
      print(url)
      if url == '':  # 直到没有url
          break
      token = str(tokenGet.getToken('https:'+url))
      print('第' + str(index) + '件商品: ' + 'https:'+url + ' ' + token)  # 输出第几件商品 和对应的url、token
      html = get_one_page("https:"+url, token)
      print(html)
      workbook = xlwt.Workbook(encoding='utf-8')  # 新建一个excel文件
      worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)  # 如果对一个单元格重复操作，会引发错误，所以加上cell_overwrite_ok=True
      worksheet.write(0, 0, label='date')  # 1行1列写日期
      worksheet.write(0, 1, label='price')  # 1行2列写价格
      worksheet.write(0, 2, label='discount')

      i = 1
      for item in parse_one_page(html):
        worksheet.write(i, 0, str(item['date']))
        worksheet.write(i, 1, float(item.get('price')))
        worksheet.write(i,2,str(item['discount']))
        i = i+1

      workbook.save('E:\零食_' + str(index) + '.xls')
      index = index + 1
    print('*****')
if __name__ =='__main__':
    main()