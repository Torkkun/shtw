import os
import json
import csv

from requests import NullHandler

media = [i for i in os.listdir("投稿画像/")]
icon = [i for i in os.listdir("アイコン画像/")]

data = dict()
with open('test.json', mode='rt', encoding='utf-8') as file:
    data = json.load(file)

checkid = [bioc["id"] for bioc in data["includes"]["users"]]

count = len(data["data"])

def idcheck(id):
    if id in checkid:
        return checkid.index(id)
    else:
        return

def main():
    labels = ['ツイートリンク', 'ツイート内容', 'bio文', '投稿時間', 'アイコン画像のpath', "投稿画像のpath"]
    dct_arr = []
    for i in range(count):
        authorid = data["data"][i]["author_id"]
        lpath =  idcheck(authorid)
        userid = data["includes"]["users"][lpath]["username"]
        TweetLinkid = data["data"][i]["id"]
        Tweet = data["data"][i]["text"]
        Tweet = Tweet.replace('\n', '').replace('\u3000','')
        bio = data["includes"]["users"][lpath]["description"]
        TweetTime = data["data"][i]["created_at"]
        #TweetTime = TweetTime.replace('.000Z', '')
        iconpath =  [ip for ip in icon if userid in ip]
        mediapath = [mp for mp in media if userid in mp]

        format = {'ツイートリンク': "https://twitter.com/{}/status/{}".format(userid, TweetLinkid), 'ツイート内容': "{}".format(Tweet), 'bio文': "{}".format(bio), '投稿時間': "{}".format(TweetTime), 'アイコン画像のpath': "{}".format(iconpath), "投稿画像のpath": "{}".format(mediapath)}
        #print(format)
        dct_arr.append(format)

    
        
    try:
        with open('csv_test.csv', 'wt', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()
            for elem in dct_arr:
                writer.writerow(elem)
    except IOError:
        print("I/O error")


if __name__ == "__main__":
    main()
    