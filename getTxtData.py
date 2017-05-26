import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
movie = input('请输入要抓取的豆瓣电影网址：')
# movie = 'https://movie.douban.com/subject/11611021'
start_url = movie +'/comments'

#创建文件保存数据
table = input('请输入要插入的文件名：')
path = './' + table+'.txt'
file = open(path,'w')

max = input('请选择要抓取前几页的数据(最多10页)：')

def getContent(start_url):
    #获得url开始抓取
    print('正在抓取'+start_url)
    res = requests.get(start_url,headers = headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')

        #开始分析文档内容
    comments = soup.select('.comment-item')
    for comment in comments:
        username = comment.find('a')['title'] and comment.find('a')['title'] or ''
        try:
            rating = comment.find('span',class_='rating')['title'] and comment.find('span',class_='rating')['title'] or ''
        except:
            continue
        time = comment.find('span',class_='comment-time').text.strip() and comment.find('span',class_='comment-time').text.strip() or ''
        content = comment.find('p').text.strip() and comment.find('p').text.strip() or ''
        vote = comment.find('span',class_='votes').text and comment.find('span',class_='votes').text or ''

            #写入数据
        data = '用户：'+username+'   推荐度：'+rating+'   发表时间：'+time+'  赞同数：'+vote+'\n\n'+content+'\n\n'
        line = '-----------------------------------------------------\n\n'
        try:
            file.write(data)
        except:
            continue
        file.write(line)



getContent(start_url)

for i in range(1,int(max)):
    num = i*20
    nextPage = '?start='+str(num)+'&limit=20&sort=new_score&status=P'
    nextUrl = movie+'/comments'+nextPage
    getContent(nextUrl)


file.close()
print('数据写入完成')