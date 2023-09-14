import requests
import json

tag = {}
difficultyMap = {"无选择": -1, "暂无评定": 0, "入门": 1, "普及-": 2, "普及/提高-": 3, "普及+/提高": 4, "提高+/省选-": 5, "省选/NOI-": 6, "NOI/NOI+/CTSC": 7}

reqUrl = "https://www.luogu.com.cn/problem/list"
userAgent01 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 " \
            "Safari/537.36 Edg/116.0.1938.76 "
userAgent02 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/103"
cookie = "__client_id=d670d45cce0e21ad3e7f30f352487ddb8028277b; _uid=1086745"
headers = {
    "user-agent": userAgent02,
    "cookie": cookie
}
tagUrl = "https://www.luogu.com.cn/_lfe/tags?_version=1694484943"
_contentOnly = 1


import json
import requests

def getPids(difficulty, tags, keyword):
    initTag()
    # 爬取json数据
    params = {"_contentOnly": _contentOnly}
    difficulty = difficultyMap[difficulty]
    if difficulty != -1:
        params["difficulty"] = difficulty
    if len(tags) != 0:
        accessibleTags = []
        for item in tags:
            # 判断标签是否存在
            if item not in tag.keys():
                return "invalid tag", ""
            else:
                accessibleTags.append(tag[item])
        if len(accessibleTags) != 0:
            params["tag"] = accessibleTags
    if keyword != '':
        params["keyword"] = keyword
    resp = requests.get(reqUrl, headers=headers, params=params)
    jsonTxt = resp.text
    map1 = json.loads(jsonTxt)
    map2 = map1["currentData"]["problems"]
    totalCount = map2["count"]
    problems = map2["result"]
    return totalCount, problems

import json
import requests

def initTag():
    if len(tag) != 0:
        return

    res = requests.get(tagUrl, headers=headers)
    if "Exception" in res.text:
        print("爬取Tag列表失败...")
        return "error"

    jsonTxt = res.text.encode("utf-8").decode("unicode_escape")
    map = json.loads(jsonTxt)
    tagList = map["tags"]
    for item in tagList:
        tagName = item['name']
        tagId = item['id']
        tag[tagName] = tagId

if __name__ == "__main__":
    totalCount, problems = getPids("入门", [], '')
    print("共发现{}道题目".format(totalCount))
    print(problems)
    print(len(problems))
