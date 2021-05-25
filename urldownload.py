import json
import requests
import json

data = dict()
with open('test.json', mode='rt', encoding='utf-8') as file:
    data = json.load(file)

count = len(data["data"])
iconc = len(data["includes"]["users"])
print(count ,iconc)
med = len(data["includes"]["media"])
print(med)

def idcheck(id):
    c = 0
    for i in data["includes"]["users"]:
        if i["id"] == id:
            return c
            
        c += 1

def mediakeycheck(mediakey):
    c = 0
    for i in data["includes"]["media"]:
        if i["media_key"] == mediakey:
            return c
            
        c += 1


def acountimagedl(i):
    authorid = data["data"][i]["author_id"]
    lpath =  idcheck(authorid)
    #lpath = data["includes"]["users"].index(authorid)
    url = data["includes"]["users"][lpath]["profile_image_url"]
    iconname = data["includes"]["users"][lpath]["username"]
    file_name = "アイコン画像/{}.jpg".format(iconname)
    response = requests.get(url)
    image = response.content
    with open(file_name, mode="wb") as file:
        file.write(image)


def mediadl(i):
    try:
        mediakey = data["data"][i]["attachments"]["media_keys"]
        filenum = 0
        for mkey in mediakey:
            m = mediakeycheck(mkey)
            url = data["includes"]["media"][m]["url"]
            authorid = data["data"][i]["author_id"]
            lpath = idcheck(authorid)
            iconname = data["includes"]["users"][lpath]["username"]
            file_name = "投稿画像/{}image{}.jpg".format(iconname, filenum)
            response = requests.get(url)
            image = response.content
            with open(file_name, mode="wb") as file:
                file.write(image)
        
            filenum += 1
    except KeyError:
        return

    #mediacount += mcount

def main():
    for i in range(count):
        acountimagedl(i)
        mediadl(i)
    #print(data.keys())
    


if __name__ == "__main__":
    main()