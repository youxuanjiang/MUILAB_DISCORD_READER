# """
# BeautifulSoup Tutorial:
# https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/
# """

def parse_ubereats_url(url):
    import urllib.request as req

    # create a Request object with Request Header
    request=req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    # analysis html code
    import bs4
    root = bs4.BeautifulSoup(data, "html.parser")
    # print(root.prettify())
    return root.title.string


def parse_ubereats_receipt():
    from telnetlib import NAOCRD
    import textract

    text = textract.process("Receipt/ubereats-receipt.pdf").decode("utf-8")

    restaurant = text.split('以下是您在')[1].split('訂購的電子明細。')[0]
    name_order = text.split('總計\n\n')[1].split('\n\n小計')[0].split('\n')[1:] # 從PDF parse出名字跟餐點的部分

    redundent_info = []
    for element in name_order:
        if element == '':
            redundent_info.append(element)

    for redundent in redundent_info:
        name_order.remove(redundent)

    one_order = -1
    total_order = []

    # 把名字、餐點，以及價位一起存成list
    for index in range(len(name_order)):
        if name_order[index].isdigit():
            if name_order[index-1].find('$') == -1:
                if one_order != -1:
                    total_order.append(one_order)
                one_order = {'name': name_order[index-1], 'order': []}

            if name_order[index+2][0] == '$':
                one_order['order'].append({'number': name_order[index], 'food':name_order[index+1].split(' ')[0], 'price': name_order[index+2].split('$')[1].split('.')[0]})
            else:
                one_order['order'].append({'number': name_order[index], 'food':name_order[index-3].split(' ')[0], 'price': name_order[index-2].split('$')[1].split('.')[0]})

    total_order.append(one_order)

    # 單純print list
    my_text = 'UberEats\n' + restaurant + '\n-----\n'
    for order in total_order:
        my_text += order['name'] + '\n'
        for food in order['order']:
            my_text += '。' + food['food'] + 'x' + food['number'] + ' ' + food['price'] + '元\n'
        my_text += '-----\n'

    return {'restaurant': restaurant, 'message': my_text}

#  有些情況可能需要用這個版本的code

# import textract

# def parse_ubereats_receipt():
#     text = textract.process("Receipt/ubereats-receipt.pdf").decode("utf-8")
#     restaurant = text.split('以下是您在')[1].split('訂購的電子明細。')[0]
#     name_order = text.split('總計\n\n')[1].split('\n\n小計')[0].split('\n') # 從PDF parse出名字跟餐點的部分
#     redundent_info = []
#     for element in name_order:
#         if element.find('  ') != -1:
#             redundent_info.append(element)

#     for redundent in redundent_info:
#         name_order.remove(redundent)

#     pay = text.split('日\n\n')[1].split('如需詳細資訊')[0].split('\n\n')
#     pay = pay[1:len(pay)-3] # 從PDF中parse出嫁前的部分

#     one_order = -1
#     total_order = []

#     # 把名字、餐點，以及價位一起存成list
#     for element in name_order:
#         if element.split(' ')[0].isdigit():
#             one_order['order'].append({'number': element.split(' ')[0], 'food':element.split(' ')[1], 'price': pay.pop(0).split('$')[1].split('.')[0]})
#         else:
#             if one_order != -1:
#                 total_order.append(one_order)
#             # 有時名字不知道為什麼會重複顯示，這是刪除多餘部分的文字
#             temp = (element + element).find(element, 1, -1)
#             if temp != -1:
#                 element = element[:temp]
#             one_order = {'name': element, 'order': []}
#     total_order.append(one_order)

#     # 單純print list
#     my_text = 'UberEats\n' + restaurant + '\n-----\n'
#     for order in total_order:
#         my_text += order['name'] + '\n'
#         for food in order['order']:
#             my_text += '。' + food['food'] + 'x' + food['number'] + ' ' + food['price'] + '元\n'
#         my_text += '-----\n'

#     return {'restaurant': restaurant, 'message': my_text}
