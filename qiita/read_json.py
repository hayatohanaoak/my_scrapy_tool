import json

with open('./test.json', encoding='utf-8') as f:
    data   = json.load(f)
    titles = data[0]['titles']
    urls   = data[0]['urls']
    for title, url in zip(titles, urls):
        print(title, url)
