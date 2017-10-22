# coding=utf-8
# filename: re_sora.py

import re

try:
    # Wide UCS-4 build
    re_emoji = re.compile((u'['
                           u'\U0001F300-\U0001F64F'
                           u'\U0001F680-\U0001F6FF'
                           u'\u2600-\u26FF\u2700-\u27BF]+|[\U00010000-\U0010ffff]+'),
                          re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    re_emoji = re.compile(u'('
                          u'\ud83c[\udf00-\udfff]|'
                          u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                          u'[\u2600-\u2B55])+|[\uD800-\uDBFF][\uDC00-\uDFFF]',
                          re.UNICODE)

re_tieba_all_tiezi = re.compile(
    u'<code class="pagelet_html" id="pagelet_html_frs-list\/pagelet\/thread_list" style="display:none;">'
    u'<!--[\S,\s]*?--><\/code>', re.UNICODE)

re_num = re.compile(u'[0-9]+', re.UNICODE)
