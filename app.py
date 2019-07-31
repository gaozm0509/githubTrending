
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import flask_restful
from flask_restful import Resource
from flask import jsonify
import os


def replaces(str):
    return str.replace('\n', '').replace('\r', '').replace(' ', '')

# avatar	开发者头像	String	url字符串
# name	拥有者名字	String	/
# full_name	拥有者全名	String	originName(NickName)的形式
# app	applicaion
# app_des applicaion 简介


def getRepoDevelopers(since):
    url = 'https://github.com/trending/developers'
    if not since is None:
        url = url + '?since=' + since
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    dev_articles = soup.find_all('article', {'class': 'd-flex'})
    devs = []
    for dev_article in dev_articles:
        dev_dic = {}

        img = dev_article.find('img', {'class': 'rounded-1'})
        dev_dic['avatar'] = img.attrs['src']

        full_name = dev_article.find('h1', {'class': 'lh-condensed'})
        if not full_name is None:
            dev_dic['full_name'] = full_name.a.text

        name = dev_article.find('p', {'class': 'mb-1'})
        if not name is None:
            dev_dic['name'] = name.a.text

        app = dev_article.find('a', {'class': 'css-truncate-target'})
        dev_dic['app'] = app.text.replace(
            '\n', '').replace('\r', '').replace(' ', '')

        app_des = dev_article.find('div', {'class': 'f6 text-gray mt-1'})
        if not app_des is None:
            dev_dic['app_des'] = app_des.text.replace(
                '\n', '').replace('\r', '').replace(' ', '')

        devs.append(dev_dic)

    return devs


#       added_stars: "116 stars today"
#       avatars: (5) ["https://avatars0.githubusercontent.com/u/23621655?s=40&v=4", "https://avatars3.githubusercontent.com/u/43715439?s=40&v=4", "https://avatars2.githubusercontent.com/u/23149796?s=40&v=4", "https://avatars3.githubusercontent.com/u/47393639?s=40&v=4", "https://avatars1.githubusercontent.com/u/43502196?s=40&v=4"]
#       desc: "This is an attempt to modify Dive into Deep Learning, Berkeley STAT 157 (Spring 2019) textbook's code into PyTorch."
#       forks: "65"
#       lang: "Jupyter Notebook"
#       repo: "dsgiitr/d2l-pytorch"
#       repo_link: "https://github.com/dsgiitr/d2l-pytorch"
#       stars: "301"
# def getRepo(since):
#     url = 'https://github.com/trending/trending'
#     if not since is None:
#         url = url + '?since=' + since

#     response = requests.get(url).text
#     print(response)
#     soup = BeautifulSoup(response, 'lxml')
#     articles = soup.find_all('article', {'class': 'Box-row'})
#     print(articles)
#     trendings = []
#     for article in articles:
#         dic = {}
#         repo = article.find('h1', {'class': 'lh-condensed'})
#         print(repo)
#         if not repo is None:
#             repo_a = repo.a
#             if not repo_a is not None:
#                 repo_text = replaces(repo_a.span.text) + replaces(repo_a.text)
#                 dic['repo'] = repo_text
#                 print(repo_text)


# getRepo(None)

app = Flask(__name__)
api = flask_restful.Api(app)


class Trending(flask_restful.Resource):
    def get(self):
        since = request.args.get('since')
        data = jsonify(getRepoDevelopers(since))
        return data


api.add_resource(Trending, '/')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port = '5000',ssl_context=(
        os.environ['HOME']+'/crt/server.crt', os.environ['HOME']+'/crt/server.key'))
