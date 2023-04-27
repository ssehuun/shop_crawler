import json
import requests

cookies = {
    'NNB': 'RN7EMFYA62RWE',
    'ASID': '798dc239000001867ec5ac6800000058',
    'SHP_BUCKET_ID': '2',
    'nid_inf': '-1107154688',
    'NID_AUT': 'AoQvnWYFT9S3uVGVXO+RyUUMWU6O2pwLmb5xhzW1TkjboQB47aAywEDe2aA88LaA',
    'NID_JKL': 'TpDt+CMfZfv6bFsbVEbo4i0HlEk47/CkxQFaTsmDSU8=',
    'nx_ssl': '2',
    'page_uid': 'iuQS+sp0Jy0ssju/siCssssssIV-021446',
    'spage_uid': 'iuQS%2Bsp0Jy0ssju%2FsiCssssssIV-021446',
    'ncpa': '6844584|lfxlqjeg|599ad2aad5b68b19991edbacafcde7ee2ed1b6a2|s_30aec8d3505be|bfd10bc1d9f035c55aead7b4158621780bf7806c:6877236|lfxlvntc|0fb397515c9c3c62f22a231e1278818834e4a9aa|s_c4e2e0c4754a|1d388fa3f48c24bccce033ca51a9e4a30b401da4:1236626|lfxma3vk|e198145465569e0e596a1c954af8f98427d71be5|s_15bd4c7c1dcb5|e0f8c8eb9443b7c95d15cf4aa6107cdb2d2c54ba:823793|lfxmhsvs|fd070c31106b7eed98ffbff6ca9fbdea14f89495|s_3020ce80b43ba|0e36a1cd82ad97f6f17aabb7cdf87cfc25350227:1127474|lfxmjrvc|6011eb4ac2dce31670cb97f379c20cc73f868488|s_22c3f940d7252|4d01b48472d663e05216ce2837c5f606afe30a7a:6278965|lfxmtqo0|e6e133c47946a266f209ecd98bb5057f8a8a8337|s_1955b1ce015c4|e9db3ec85851cd16bebe793fbc85efdc0b1899b2',
    'NID_SES': 'AAABpeBd4euK/6Ac4lpx8vAP0b6T58aJlsc8ywl7IQmWDC3ppDhdZKhZCkqIK0Ij7I/jr5ZPzL+/ZR+dPf1CdsGPAVPgY7yXL3Q90malAQWnt2ugkv0p16rG3RUWrAdZFcdgdqZzoQxvWR7BFbBnBTpy5tHAoytR50TiVTscceT8EAKVffahFxSjnTjDjKbWi88y0Fsd8ET9yZPFnQl/gb3lzYYHskBhGmIjnjFenafkBdmpaLVMktkGZf2qF928akqH23e2Neou3kSD+TGnUK3vOU6xwZQAO8w6jgT/TCcQYNLfgznnGAVLCDi2xXW7Z/pNBKHAssRZDdTZXaK3E+kK6NGZaHu8MR0R3JigfZz8757lvt/6n0ITIjNGKYFAiuDkvwoEOj7Gw7Dt9/Y7PUJ4+UB7nY/PXUEi3t/5Ye+5H9XCfKCzCvBaAiSoOY9PpiVDboYjOjjDOuW2r7Rawj0GkO26DZELA41keafVdE80N89Sh6UbHF+1Mm1sDHKxITwio0YKMJBIYdPW/2vlAUNXrJ/f4CTfZVqBCV5rPT5F4+KAMntbqaJaYfAbJg7dL3UEXg==',
}

headers = {
    'authority': 'search.shopping.naver.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'NNB=RN7EMFYA62RWE; ASID=798dc239000001867ec5ac6800000058; SHP_BUCKET_ID=2; nid_inf=-1107154688; NID_AUT=AoQvnWYFT9S3uVGVXO+RyUUMWU6O2pwLmb5xhzW1TkjboQB47aAywEDe2aA88LaA; NID_JKL=TpDt+CMfZfv6bFsbVEbo4i0HlEk47/CkxQFaTsmDSU8=; nx_ssl=2; page_uid=iuQS+sp0Jy0ssju/siCssssssIV-021446; spage_uid=iuQS%2Bsp0Jy0ssju%2FsiCssssssIV-021446; ncpa=6844584|lfxlqjeg|599ad2aad5b68b19991edbacafcde7ee2ed1b6a2|s_30aec8d3505be|bfd10bc1d9f035c55aead7b4158621780bf7806c:6877236|lfxlvntc|0fb397515c9c3c62f22a231e1278818834e4a9aa|s_c4e2e0c4754a|1d388fa3f48c24bccce033ca51a9e4a30b401da4:1236626|lfxma3vk|e198145465569e0e596a1c954af8f98427d71be5|s_15bd4c7c1dcb5|e0f8c8eb9443b7c95d15cf4aa6107cdb2d2c54ba:823793|lfxmhsvs|fd070c31106b7eed98ffbff6ca9fbdea14f89495|s_3020ce80b43ba|0e36a1cd82ad97f6f17aabb7cdf87cfc25350227:1127474|lfxmjrvc|6011eb4ac2dce31670cb97f379c20cc73f868488|s_22c3f940d7252|4d01b48472d663e05216ce2837c5f606afe30a7a:6278965|lfxmtqo0|e6e133c47946a266f209ecd98bb5057f8a8a8337|s_1955b1ce015c4|e9db3ec85851cd16bebe793fbc85efdc0b1899b2; NID_SES=AAABpeBd4euK/6Ac4lpx8vAP0b6T58aJlsc8ywl7IQmWDC3ppDhdZKhZCkqIK0Ij7I/jr5ZPzL+/ZR+dPf1CdsGPAVPgY7yXL3Q90malAQWnt2ugkv0p16rG3RUWrAdZFcdgdqZzoQxvWR7BFbBnBTpy5tHAoytR50TiVTscceT8EAKVffahFxSjnTjDjKbWi88y0Fsd8ET9yZPFnQl/gb3lzYYHskBhGmIjnjFenafkBdmpaLVMktkGZf2qF928akqH23e2Neou3kSD+TGnUK3vOU6xwZQAO8w6jgT/TCcQYNLfgznnGAVLCDi2xXW7Z/pNBKHAssRZDdTZXaK3E+kK6NGZaHu8MR0R3JigfZz8757lvt/6n0ITIjNGKYFAiuDkvwoEOj7Gw7Dt9/Y7PUJ4+UB7nY/PXUEi3t/5Ye+5H9XCfKCzCvBaAiSoOY9PpiVDboYjOjjDOuW2r7Rawj0GkO26DZELA41keafVdE80N89Sh6UbHF+1Mm1sDHKxITwio0YKMJBIYdPW/2vlAUNXrJ/f4CTfZVqBCV5rPT5F4+KAMntbqaJaYfAbJg7dL3UEXg==',
    'logic': 'PART',
    'referer': 'https://search.shopping.naver.com/search/all?query=%ED%8A%B8%EC%9C%84%EB%93%9C%EC%9E%90%EC%BC%93&prevQuery=%ED%8A%B8%EC%9C%84%EB%93%9C%EC%9E%90%EC%BC%93',
    'sbth': '4231bedc931199611fa09b2600b4c94496fe7e44ca75d8a25488851acb770a4b2e5d19d862b00fb86a2c89e0aec4edca',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

params = {
    'deliveryFee': '',
    'deliveryTypeValue': '',
    'eq': '',
    'iq': '',
    'origQuery': '트위드자켓',
    'pagingIndex': '1',
    'pagingSize': '40',
    'productSet': 'total',
    'query': '트위드자켓',
    'sort': 'rel',
    'viewType': 'list',
    'xq': '',
}

response = requests.get('https://search.shopping.naver.com/api/search/all', params=params, cookies=cookies, headers=headers)
itemsObj = json.loads(response.text)
itemlist = itemsObj['shoppingResult']['products']
for i in itemlist:
    productName = i['productName']
    price = i['price'] # lowPrice
    openDate = i['openDate']
    opDate = openDate[0:4]+'.'+openDate[4:6]
    reviewCount = i['reviewCount']
    purchaseCnt = i['purchaseCnt']
    mallProductUrl = i['mallProductUrl']
    print(productName, price, opDate, reviewCount, purchaseCnt, mallProductUrl)