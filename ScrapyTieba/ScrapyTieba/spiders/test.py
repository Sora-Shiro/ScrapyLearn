# coding=utf-8
# filename: tieba_post_spider.py

# double-deck(in Chinese, named 'Lou Zhong Lou'(楼中楼), abbr.->lzl)
import scrapy

from tools.re_sora import re_emoji


class TiebaPostSpider(scrapy.spiders.Spider):
    name = "tbPost"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        # 1. Has lzl, don't have re_emoji
        # "https://tieba.baidu.com/p/comment?tid=3886007864&pid=71342182567&pn=3"
        # 2. Has lzl, has re_emoji
        "https://tieba.baidu.com/p/comment?tid=5301206923&pid=111379725038&pn=1",
        # 3. Don't have lzl
        #  "https://tieba.baidu.com/p/comment?tid=5301206923&pid=111390028140&pn=1",
    ]
    # I tried to change header to fix it but I failed :(
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
        }
    }

    # Parse lzl, if there isn't lzl then print nothing, or print username and his/her words
    def parse(self, response):

        # Collect this page's all users' words and print them
        lzl_content = response.css("li[class^='lzl_single_post j_lzl_s_p']")
        if len(lzl_content) != 0:
            for single_post in lzl_content:
                content = single_post.css("div.lzl_cnt")
                username = content.css("a::attr(username)").extract()[0].strip()
                words_list = content.css("span::text").extract()
                words = ""
                for word in words_list[:-1]:
                    words += word.strip()
                time = words_list[-1:]
                list_words_emoji = []
                if re_emoji.search(words):
                    list_words_emoji.append(re_emoji.findall(words))
                    words = re_emoji.sub('[Emoji]', words)
                print username + ":" + words
                print list_words_emoji
                print time[0]

        # If lzl has next page, request next page and parse it
        lzl_next = response.css("li.lzl_li_pager.j_lzl_l_p.lzl_li_pager_s p a")
        if len(lzl_next) != 0:
            for h in lzl_next:
                href = h.xpath("@href").extract_first().strip()
                text = h.xpath("./text()").extract_first().strip()

                if text == u'下一页':
                    index = response.url.find("&pn=")
                    next_url = response.url[:index + 4] + href[1:]
                    yield scrapy.Request(next_url, callback=self.parse)
