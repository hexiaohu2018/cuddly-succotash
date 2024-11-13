import requests
from bs4 import BeautifulSoup
import time

# 小说地址
book_url = 'http://www.xbiquge.la/10/10489/'

# 模拟浏览器请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
}

# 发送请求并获取响应
response = requests.get(book_url, headers=headers)
response.encoding = 'utf-8'

# 使用 BeautifulSoup 解析 HTML 内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到章节目录所在的标签
chapter_list = soup.find_all('dd')

# 保存小说的文件路径
save_path = '三寸人间.txt'

# 定义计数器
count = 0

# 逐个处理每个章节
for chapter in chapter_list:
    # 获取章节标题和链接
    chapter_title = chapter.a.text
    chapter_link = chapter.a['href']

    # 拼接章节链接
    chapter_url = 'http://www.xbiquge.la' + chapter_link

    # 发送请求获取章节内容
    response_chapter = requests.get(chapter_url, headers=headers)
    response_chapter.encoding = 'utf-8'

    # 使用 BeautifulSoup 解析章节内容
    soup_chapter = BeautifulSoup(response_chapter.text, 'html.parser')

    # 找到章节正文内容所在的标签
    content_tag = soup_chapter.find('div', id='content')

    # 获取章节正文内容
    chapter_content = content_tag.text.strip()

    # 将章节标题和内容写入文件
    with open(save_path, 'a+', encoding='utf-8') as f:
        f.write('--------' + chapter_title + '--------\n')
        f.write(chapter_content + '\n')

    # 计数器加一
    count += 1

    # 打印爬取信息
    print('第{}章 标题 : {} 爬取完毕！'.format(count, chapter_title))

    # 防止爬取速度过快被封IP，可以加上间隔
    time.sleep(1)
