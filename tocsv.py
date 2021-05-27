import os
import json
import csv

media = [i for i in os.listdir("投稿画像1/")]
icon = [i for i in os.listdir("アイコン画像1/")]

data = dict()
with open('test1.json', mode='rt', encoding='utf-8') as file:
    data = json.load(file)

medianum = len(data["includes"]["media"])

checkid = [bioc["id"] for bioc in data["includes"]["users"]] #useridcheck用のリスト

userlist = set([uid["username"] for uid in data["includes"]["users"]])#usernameのリスト
umlist = {username: 0 for username in userlist}#それぞれのユーザーのメディア数

count = len(data["data"])#取得データ個数

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
        #Tweet = Tweet.replace('\n', '').replace('\u3000','')
        Tweet = Tweet.replace('\u3000','')
        bio = data["includes"]["users"][lpath]["description"]
        TweetTime = data["data"][i]["created_at"]
        #TweetTime = TweetTime.replace('.000Z', '')
        iconpath =  [ip for ip in icon if userid in ip]
        mediapath = []
        if "attachments" in data["data"][i].keys():
            newnum = len(data["data"][i]["attachments"]["media_keys"])
            for i in range(umlist[userid], newnum):
                filename = userid + "image{}.jpg".format(i)
                if filename in media:
                    mediapath.append(filename)
                    umlist[userid] += newnum    #mediakeyの個数を更新
                else:
                    continue

        format = {'ツイートリンク': "https://twitter.com/{}/status/{}".format(userid, TweetLinkid), 'ツイート内容': "{}".format(Tweet), 'bio文': "{}".format(bio), '投稿時間': "{}".format(TweetTime), 'アイコン画像のpath': "{}".format(iconpath), "投稿画像のpath": "{}".format(mediapath)}
        #print(format)
        dct_arr.append(format)

    
        
    try:
        with open('csv_test1.csv', 'wt', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=labels)
            writer.writeheader()
            for elem in dct_arr:
                writer.writerow(elem)
    except IOError:
        print("I/O error")


if __name__ == "__main__":
    main()
    