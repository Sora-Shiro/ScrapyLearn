# coding=utf-8
# filename: tieba_post_spider.py
import json

import scrapy
import sys
from scrapy.http import HtmlResponse
from constant.china_constant import *
from tools.re_sora import *

sys.path.append('D:/Work/PythonProject/ScrapyLearn/ScrapyTieba/ScrapyTieba')
from items import AskScoreToUniversityItem

UNIVERSITY = u'南京师范大学'

class TiebaPostSpider(scrapy.spiders.Spider):
    name = "tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        # "https://tieba.baidu.com/p/3821636267"
        "http://tieba.baidu.com/f?kw=%E5%8D%97%E4%BA%AC%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=59950"
    ]

    # Custom head
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
        }
    }

    # 这个爬虫用来保存每个出现了数字和省份的主题帖，见 AskScoreToUniversityItem
    def parse(self, response):
        content = response.body
        if re_tieba_all_tiezi.search(content):
            list_page = re_tieba_all_tiezi.findall(content)
            page_pre = list_page[0]
            # Parse ajax code
            page = page_pre.replace(
                '<code class="pagelet_html" id="pagelet_html_frs-list/pagelet/thread_list" style="display:none;"><!--',
                '').replace('--></code>', '')
            html_page = HtmlResponse(url="All Tiezi", body=page)
            list_tiezi = html_page.css("div[class^='col2_right j_threadlist_li_right ']")
            # Check every tiezi title
            for tiezi in list_tiezi:
                a = tiezi.css("div[class^='threadlist_title pull_left j_th_tit '] > a[class^='j_th_tit ']")
                title = a.css("::text").extract()[0].strip()
                href = "http://tieba.baidu.com" + a.css("::attr(href)").extract()[0].strip()
                list_content_emoji = []
                if re_emoji.search(title):
                    list_content_emoji.append(re_emoji.findall(title))
                    title = re_emoji.sub('[Emoji]', title)
                # try:
                #     print title
                # except:
                #     print "error print title"
                # print href
                bool_province = False
                pro = ""
                for PROVINCE in CHINA_PROVINCE:
                    bool_province |= PROVINCE in title
                    if bool_province:
                        pro = PROVINCE
                        # Save into SQL
                        if re_num.search(title):
                            author_n_time = tiezi.css("div[class^='threadlist_author pull_right']")
                            author = author_n_time.css("span[class^='frs-author-name-wrap'] > a::text").extract()[0].strip()
                            item = {
                                'title': title,
                                'province': pro,
                                'author': author,
                            }
                            yield scrapy.Request(href, callback=self.parse_tiezi_time_1, meta={'item': item})
                        break

            return
            # Parse next page
            next_page = html_page.css("a[class^='next pagination-item ']")
            if len(next_page) != 0:
                next_href = next_page[0].css("::attr(href)").extract()[0]
                yield scrapy.Request("http:" + next_href, callback=self.parse)
        else:
            # Baidu against spider solution: request again
            yield scrapy.Request(response.urljoin(''), callback=self.parse)

    # 解析主题帖创建时间
    def parse_tiezi_time_1(self, response):
        posts = response.css("div[class^='p_postlist'] > div")
        if len(posts) == 0:
            print 'parse_time_1_false_1'
            self.parse_tiezi_time_2(response)
        post = posts[0]
        data = post.css("::attr(data-field)").extract()
        if len(data) == 0:
            print 'parse_time_1_false_2'
            self.parse_tiezi_time_2(response)
        json_data = json.loads(data[0])
        date = str(json_data['content']['date'])
        item = response.meta['item']
        item['date'] = date.strip()+":00"
        # go to item pipeline
        item_info = AskScoreToUniversityItem()
        item_info['title'] = item['title']
        item_info['href'] = response.urljoin('')
        item_info['province'] = item['province']
        item_info['university'] = UNIVERSITY
        item_info['author'] = item['author']
        item_info['date'] = item['date']
        yield item_info

    # 虽然也是解析创建时间，但是这个解析函数针对（部分）个人贴吧
    def parse_tiezi_time_2(self, response):
        posts = response.css("div[class^='l_post l_post_bright j_l_post clearfix']")
        if len(posts) == 0:
            print 'parse_time_2_false_1'
        post = posts[0]
        date = post.css("span[class='tail-info']::text").extract()
        if len(date) == 0:
            print 'parse_time_2_false_2'
        date = date[-1].strip()
        item = response.meta['item']
        item['date'] = date
        # go to item pipeline
        item_info = AskScoreToUniversityItem()
        item_info['title'] = item['title']
        item_info['province'] = item['province']
        item_info['university'] = UNIVERSITY
        item_info['author'] = item['author']
        item_info['date'] = item['date']
        yield item_info

    # 解析主题帖的每个帖子
    def parse_tiezi(self, response):
        # filename = response.url.split("/")[-1]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        posts = response.css("div[class^='l_post l_post_bright j_l_post clearfix']")
        for post in posts:
            pre_content = post.css("div[class^='d_post_content j_d_post_content']").extract()
            if len(pre_content) == 0:
                continue

            json_name = post.css("a[class^='p_author_name']::attr(data-field)").extract()[0]
            name = json.loads(json_name)['un']

            content = post.css("div[class^='d_post_content j_d_post_content']").extract()[0].strip()
            list_content_emoji = []
            if re_emoji.search(content):
                list_content_emoji.append(re_emoji.findall(content))
                content = re_emoji.sub('[Emoji]', content)

            floor = post.css("span[class='tail-info']::text").extract()[-2].strip()
            time = post.css("span[class='tail-info']::text").extract()[-1].strip()

            print name.encode('gbk')
            print content.encode('gbk', 'replace').decode('gbk')
            print list_content_emoji
            print floor
            print time

            # Parse lzl
            json_pd = json.loads(post.css("::attr(data-field)").extract()[0])
            pid = str(json_pd['content']['post_id'])
            tid = str(json_pd['content']['thread_id'])
            lzl_url = "https://tieba.baidu.com/p/comment?tid=" + tid + "&pid=" + pid + "&pn=1"
            response.urljoin(lzl_url)
            print lzl_url
            yield scrapy.Request(lzl_url,
                                 callback=lambda response, out_floor=floor: self.parse_lzl(response, out_floor))

        # If post has next page, request next page and parse it
        next_href = response.css('li[class="l_pager pager_theme_4 pb_list_pager"] a')
        print next_href
        for h in next_href:
            href = h.xpath('@href').extract()
            text = h.xpath('./text()').extract()
            if text[0] == u'下一页':
                next_page = response.urljoin(href[0].encode('GB18030'))
                yield scrapy.Request(next_page, callback=self.parse_tiezi)

    # 解析每个楼层的楼中楼
    def parse_lzl(self, response, out_floor, main_url):

        # Collect this page's all users' words and print them
        lzl_content = response.css("li[class^='lzl_single_post j_lzl_s_p']")
        if len(lzl_content) != 0:
            for i in range(0, len(lzl_content)):
                single_post = lzl_content[i]
                content = single_post.css("div.lzl_cnt")
                username = content.css("a::attr(username)").extract()[0].strip()
                words_list = content.css("span::text").extract()
                words = ""
                for word in words_list[:-1]:
                    words += word.strip()
                time = words_list[-1:][0].strip()
                list_words_emoji = []
                if re_emoji.search(words):
                    list_words_emoji.append(re_emoji.findall(words))
                    words = re_emoji.sub('[Emoji]', words)
                print username + ":" + words.encode('gbk', 'replace').decode('gbk')
                print list_words_emoji
                print time
                print u'外层数' + out_floor
                print u'楼中楼层数' + str(i + 1)

        # If lzl has next page, request next page and parse it
        lzl_next = response.css("li.lzl_li_pager.j_lzl_l_p.lzl_li_pager_s p a")
        if len(lzl_next) != 0:
            for h in lzl_next:
                href = h.xpath("@href").extract_first().strip()
                text = h.xpath("./text()").extract_first().strip()

                if text == u'下一页':
                    index = response.url.find("&pn=")
                    next_url = response.url[:index + 4] + href[1:]
                    yield scrapy.Request(next_url, callback=self.parse_lzl)
