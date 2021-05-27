import requests
import config
import json

bearer_token = config.Bearer_Token

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params = {'query': '(プレゼント企画 OR 配布企画) -is:retweet -is:reply',   #検索クエリリツイートとリプライを含まない
                'tweet.fields': 'author_id,created_at',             #ツイートの作成日時
                'media.fields': 'url',                              #ツイートの添付画像のurl
                'expansions': 'author_id,attachments.media_keys',   #includesのmedia
                'user.fields': 'description,profile_image_url',                       #bio
                'max_results': 100                                 #持ってくる数１００まで可能
                }



def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(search_url, headers, query_params)
    
    file = json.dumps(json_response, indent=4, ensure_ascii=False, sort_keys=True) #プレゼント企画のツイートを拾う
    #file = profile.main()
    #print(file)
    with open('test1.json', mode='wt', encoding='utf-8') as file:
        json.dump(json_response, file, indent=4, ensure_ascii=False, sort_keys=True)
    



if __name__ == "__main__":
    main()
