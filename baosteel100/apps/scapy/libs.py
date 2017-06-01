from urllib import request
import re
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
import baosteel100.libs.utils as utils

#获取宝武钢铁新闻的主页
def get_baowu_mainpage():
    url=r'http://www.baowugroup.com/channels/5173.html'
    # url = r'http://www.baowugroup.com/'
    try:
        html = request.urlopen(url,timeout=5).read()
        html = html.decode('utf-8')
        return html
    except Exception as e:
        return str(e)

#获取宝武钢铁主页上的宝武新闻
def get_baowunews(html):
    pattern = re.compile(r'<th class="ht"><a href="(.*?)" target="_blank">(.*?)</a></th><th class="ht2">(.*?)</th>')
    # pattern = re.compile(r'<dt>宝武新闻</dt><dd><em>(.*?)</em><a href="(.*?)" title="(.*?)" target="_blank">.*?</a></dd></dl>')
    news = re.findall(pattern,html)
    # print(news)
    return news

#获取宝武新闻详细信息
def get_news_detail(news):
    news_detail=[]
    for i in news:
        # pattern = re.compile(r'<div class="law_text" style="padding-top:7px;">(.*?)</div>',re.S)
        pattern = re.compile(r'<p>(.*?)</p>',re.S)
        detail_html = request.urlopen(i[0]).read()
        detail_html = detail_html.decode('utf-8')
        detail_html = detail_html.replace("&ldquo;","“")
        detail_html = detail_html.replace("&rdquo;", "”")
        detail_html = detail_html.replace("&lsquo;", "‘")
        detail_html = detail_html.replace("&rsquo;", "’")
        detail_html = detail_html.replace("<span>", "<p>")
        detail_html = detail_html.replace("</span>", "</p>")
        detail_news = re.findall(pattern,detail_html)
        detail_news=detail_news[2:]
        news_detail.append(detail_news)
    return news_detail

#直接调用这个方法即可得到宝钢消息详情，不需要传参数
def get_pretty_news():
    pretty_news=[]
    html = get_baowu_mainpage()
    news = get_baowunews(html)
    news_detail=get_news_detail(news)
    for i in range(10):
        pretty_news.append([news[i],news_detail[i]])
    return pretty_news




#获取投资者关系的股价
def get_shareprice():
    url="http://hq.sinajs.cn/list=sh600019,sh600005,sh600581,sh600845,sz000717,sh601968"
    try:
        content = request.urlopen(url,timeout=5).read()
        content = content.decode('gbk')
        items = content.split(";")
        items.remove(items[1])
        return items
    except Exception as e:
        return str(e)

#获取投资者的名称
def get_pricedata():
    url ="http://www.baowugroup.com/channels/4965.html"
    html = request.urlopen(url).read()
    html = html.decode('utf-8')
    pattern = re.compile(r'<td class=".*?"><a href=".*?" target="_blank">(.*?)</a></td>')
    news = re.findall(pattern,html)
    # print(news)
    return news


#整理生成宝钢投资者股票信息
def get_pricetable(data,company):
    replace_name=['600019.SS','600581.SS','600845.SS','000717.SZ','601968.SS']
    table=[]
    i=0
    for i in range(5):
        new = data[i].split(",")
        table.append(
            [company[i],replace_name[i],new[3], float(new[3]) - float(new[2]), (float(new[3]) - float(new[2])) / float(new[2]) * 100, new[1],
             new[4], new[5], new[8], new[31], new[30]])
    return table

#获取首钢首页
def get_shougangmainpage():
    url='http://www.sggf.cn/gfxwen/index.jhtml'
    try:
        html = request.urlopen(url,timeout=5).read()
        html.decode('utf-8')
        return html
    except Exception as e:
        return str(e)


#获取首钢主要新闻
def get_shougang_news(html):
    html = html.decode('utf-8')
    pattern = re.compile(r'<a href="(.*?)" class="gfxwrbotlisttop" target="_blank">(.*?)</a>')
    news = re.findall(pattern,html)
    # print(news)
    return news

def get_detail_shougang_news():
    html = get_shougangmainpage()
    news = get_shougang_news(html)
    detail_news=[]
    for i in news[0:10]:
        url = 'http://www.sggf.cn'+i[0]
        news_page = request.urlopen(url).read()
        news_page = news_page.decode('utf-8')
        pattern = re.compile(r'<div class="xwnrtxt auto">(.*?)</div>',re.S)
        single_detai_news=re.findall(pattern,news_page)
        detail_news.append([i[1],single_detai_news])
    return detail_news

# 获取宣化和张家口天气
def get_weather():
    url = "http://www.weather.com.cn/weather/101090302.shtml"
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    content_html = soup.find("ul",{"class":"t clearfix"})
    detail_day = content_html.findAll("h1")
    detail_wea = content_html.findAll("p",{"class":"wea"})
    pattern = re.compile(r'<span>(.*?)</span>/<i>(.*?)℃</i>')
    html = html.decode('utf-8')
    detail_tem_pretty = re.findall(pattern,html)
    detail_wins=content_html.findAll("i")
    today_tem = content_html.findAll("i",limit=1)
    weather=[]
    weather.append([detail_day[0].text,detail_wea[0].text,today_tem[0].text,detail_wins[1].text])
    for i in range(1,7):
        weather.append([detail_day[i].text,detail_wea[i].text,detail_tem_pretty[i-1],detail_wins[2*i+1].text])
        #返回的分别是日期、天气、气温、风力

    z_url = "http://www.weather.com.cn/weather/101090301.shtml"
    z_html = request.urlopen(z_url).read()
    z_soup = BeautifulSoup(z_html, 'html.parser')
    z_content_html = z_soup.find("ul", {"class": "t clearfix"})
    z_detail_day = z_content_html.findAll("h1")
    z_detail_wea = z_content_html.findAll("p", {"class": "wea"})
    z_pattern = re.compile(r'<span>(.*?)</span>/<i>(.*?)℃</i>')
    z_html = z_html.decode('utf-8')
    z_detail_tem_pretty = re.findall(z_pattern, z_html)
    z_detail_wins = z_content_html.findAll("i")
    z_today_tem = content_html.findAll("i", limit=1)
    z_weather = []
    z_weather.append([z_detail_day[0].text, z_detail_wea[0].text, z_today_tem[0].text, z_detail_wins[1].text])
    for j in range(1, 7):
        z_weather.append([z_detail_day[j].text, z_detail_wea[j].text, z_detail_tem_pretty[j-1], z_detail_wins[2 * j + 1].text])

    return weather,z_weather

get_weather()

# 获取央视网主页banner图新闻，信息依次为标题，图片，详情
def get_cctv_mainnews():
    url ='http://news.cctv.com/'
    html = request.urlopen(url).read()
    html = html.decode('utf-8')
    soup = BeautifulSoup(html,'html.parser')
    content_html = soup.find("div",{"id":"pics_show"})
    img= content_html.findAll("img")
    title = content_html.findAll("h3")
    banner_news=[]
    for i in range(len(title)):
        banner_news.append([title[i].contents[0].text,img[i].attrs["class"],title[i].contents[0].attrs["href"]])
    return banner_news


# 获取央视网食疗养生新闻
def get_yangsheng_news():
    url='http://food.cctv.com/yangsheng/index.shtml'
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    news = soup.find_all("li",{"class":""},limit=5)
    yangsheng_news=[]
    for i in range(len(news)):
        yangsheng_news.append([news[i].contents[1].text.replace("\r\n",""),news[i].contents[0].text,news[i].contents[1].attrs["href"]])
    return yangsheng_news


# 获取央视网减肥瘦身新闻
def get_jianfei_news():
    url = 'http://food.cctv.com/jianfei/index.shtml'
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    news = soup.find_all("li",{"class":""},limit=5)
    jianfei_news =[]
    for i in range(len(news)):
        jianfei_news.append([news[i].contents[1].text.replace("\r\n",""),news[i].contents[0].text,news[i].contents[1].attrs["href"]])
    return jianfei_news


# 获取央视网厨房小百科新闻
def get_chufang_news():
    url = 'http://food.cctv.com/baike/index.shtml'
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all("li", {"class": ""}, limit=5)
    chufang_news = []
    for i in range(len(news)):
        chufang_news.append(
            [news[i].contents[1].text.replace("\r\n", ""), news[i].contents[0].text, news[i].contents[1].attrs["href"]])
    return chufang_news

#获取新闻详细消息

def get_detail_news(url):
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    origin_news=soup.find("div",{"class":"cnt_bd"})
    # news = origin_news.findAll("p",{"class":"","align":""})
    # img = origin_news.findAll("p",{"align":"center"})
    # text_news =[]
    # for i in range(len(news)):
    #     text_news.append(news[i].text)
    # img_news=[]
    # for j in range(len(img)):
    #     img_news.append(img[j].contents[0].attrs["src"])
    # return text_news,img_news

    tem_news = origin_news.findAll("p", {"classs": ""})
    del tem_news[0]
    final_news=[]
    for i in range(len(tem_news)):
        final_news.append(str(tem_news[i]))
    return final_news

# print(get_detail_news("http://food.cctv.com/2017/05/29/ARTIejIhGha1t77gKDVLWBZP170529.shtml"))














