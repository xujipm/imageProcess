# encoding: utf-8
# author: xujipm

import requests
import json
import diff

sid = '0-2967884-dc9160de56581d2dc267cea8ccfb2242'
#sid = '0-244089-3-42b535ba435b03a7deec4a08d59922c1'
headers = {
    'Host': 'tbgr.huanleguang.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,es;q=0.4,zh-TW;q=0.2,ja;q=0.2',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,es;q=0.4,zh-TW;q=0.2,ja;q=0.2',
    'Cookie': 'gr_user_id=ee85e7f1-fde2-480f-a0b4-5231df7d978a; Hm_lvt_5766daecaea803ec4e53ece43223db47=1459760632,1459776905,1459941653,1460193386; Hm_lpvt_5766daecaea803ec4e53ece43223db47=1460195947; mobiledesc_guider=1; _umdata=ED82BDCEC1AA6EB9D6D58F882CEBC530EAFE08399D7705876C420FF9C2BF353B0E5982ACB956A1AFD076406DA868586FACEC286A13CBE0C750F7FD97F2CB4739FD79E715F2B6743C6759CAB6D6B3A72744F7D4AFE5EBECBD553F1A2A57494C5A0A6225010E2CCA26; CNZZDATA1256695076=1872665485-1459340262-%7C1460210328; hlg_0_0=0-2967884-dc9160de56581d2dc267cea8ccfb2242; gr_session_id_816681834742aea8=0434c10a-9f19-4d53-8d19-e83e97b86ea0; _ati=1000002967884'
}
homeUrl = 'http://tbgr.huanleguang.com/?hpm=1&sid=' + sid
pageSize = 10
DEEP = 5


def link_items_url(_sid, q='', cid='0', local='1', status='0', page_size=20, page_num=1):
    return 'http://tbgr.huanleguang.com/itemlibrary/mobiledesc/loadTbItems/?hpm=1' \
        '&sid=' + _sid + '&q=' + q + '&cid=' + cid + '&type=' + local + '&status=' + status +\
        '&page_size=' + str(page_size) + '&page_num=' + str(page_num)


def get_items(_sid):
    items = []
    page = requests.get(link_items_url(_sid, page_size=1), headers=headers)
    #headers['Cookie'] = page.cookies
    print(page)
    data = json.loads(page.content.decode('utf-8'))
    total_records = int(data['payload']['total_records'])
    for pageNum in range(1, total_records // pageSize + 2):
        page = requests.get(link_items_url(_sid, page_size=pageSize, page_num=pageNum), headers=headers)
        data = json.loads(page.content.decode('utf-8'))
        for i in range(len(data['payload']['list'])):
            items.append(data['payload']['list'][i]['num_iid'])
    return items


def get_wireless_desc(_sid, _item_id):
    url = 'http://tbgr.huanleguang.com/itemlibrary/mobiledesc/loadWapDesc/?hpm=1&sid='\
          + _sid + '&num_iid=' + str(_item_id) + '&is_preview=1'
    lists = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))['payload']['list']
    img_urls = []
    for i in range(len(lists)):
        img_urls.append(lists[i]['src'])
    return img_urls


img_0_url = 'https://img.alicdn.com/imgextra/i2/505981619/TB2.zvGmFXXXXbkXXXXXXXXXXXX_!!505981619.jpg'
diff.set_img_0(img_0_url)

results = {}
for item in get_items(sid):
    images = get_wireless_desc(sid, item)
    result = []
    for i in range(min(DEEP, len(images))):
        result.append({
            'src': images[i],
            'diff': diff.match(images[i])
        })
    results[item] = result

print(results)
