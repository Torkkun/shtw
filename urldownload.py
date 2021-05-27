import json
import requests
import json

data = dict()
with open('test1.json', mode='rt', encoding='utf-8') as file:
    data = json.load(file)


#dataの個数を表示
count = len(data["data"])
iconc = len(data["includes"]["users"])
med = len(data["includes"]["media"])
print("データの個数は" + str(count))
print("アイコンのデータは" + str(iconc))
print("メディアの個数は" + str(med))

userlist = set([uid["username"] for uid in data["includes"]["users"]])#usernameのリスト
umlist = {username: 0 for username in userlist}#それぞれのユーザーのメディア数
checkid = [bioc["id"] for bioc in data["includes"]["users"]]

def idcheck(id):
    if id in checkid:
        return checkid.index(id)

def mediakeycheck(mediakey):
    c = 0
    for i in data["includes"]["media"]:
        if i["media_key"] == mediakey:
            return c
            
        c += 1


def acountimagedl(i):
    authorid = data["data"][i]["author_id"]
    lpath =  idcheck(authorid)
    url = data["includes"]["users"][lpath]["profile_image_url"]
    iconname = data["includes"]["users"][lpath]["username"]
    file_name = "アイコン画像1/{}.jpg".format(iconname)
    response = requests.get(url)
    image = response.content
    with open(file_name, mode="wb") as file:
        file.write(image)


def mediadl(i):
    try:
        mediakey = data["data"][i]["attachments"]["media_keys"]
        for mkey in mediakey:
            m = mediakeycheck(mkey)
            if data["includes"]["media"][m]["type"] == "photo":
                url = data["includes"]["media"][m]["url"]
                authorid = data["data"][i]["author_id"]
                lpath = idcheck(authorid)
                iconname = data["includes"]["users"][lpath]["username"]
                filenum = umlist[iconname]
                file_name = "投稿画像1/{}image{}.jpg".format(iconname, filenum)
                response = requests.get(url)
                image = response.content
                with open(file_name, mode="wb") as file:
                    file.write(image)
        
                umlist[iconname] += 1
    except KeyError:
        return

def countjpg():
    count = 0
    for i in userlist:
        count += umlist[i]

    return count


def main():
    for i in range(count):
        acountimagedl(i)
        mediadl(i)
        
    print("jpg画像の合計は" + str(countjpg()))
    #print(data.keys())
    


if __name__ == "__main__":
    main()