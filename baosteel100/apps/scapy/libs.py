from urllib import request
import re

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





