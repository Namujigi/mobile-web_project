import requests

HOST = 'http://127.0.0.1:8000'

res = requests.post(HOST + '/api-token-auth/', {
        'username': 'admin',
        'password': '0000',
})

res.raise_for_status()
token = res.json()['token']
print(token)

# 인증이 필요한 요청에 아래의 headers를 붙임
headers = {'Authorization': 'JWT ' + token, 'Accept': 'application/json'}

# Post Create
data = {
    'author': '1',
    'title': '제목 by code',
    'text': 'API내용 by code',
    'created_date': '2025-10-07T18:34:00+09:00',
    'published_date': '2025-10-07T18:34:00+09:00',
}

with open('./google-color.png', 'rb') as f:
    file = {'image': f}
    res = requests.post(HOST + '/api_root/Post/', data=data, files=file, headers= headers)

print(res)
print(res.json())