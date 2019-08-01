
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


def getRepoDevelopers(since=None):
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
                '\n', '').replace('\r', '').strip()

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

# async def getRequest(url, since=None):
#     url = 'https://github.com/trending'
#     if not since is None:
#         url = url + '?since=' + since
#     response = await request(url)
#     return response.text


def getRepo(since=None):
    url = 'https://github.com/trending'
    if not since is None:
        url = url + '?since=' + since
    response = requests.get(url).text
    # response = await getRequest(url,since)
    soup = BeautifulSoup(response, 'html.parser')
    articles = soup.find_all('article', {'class': 'Box-row'})
    trendings = []
    for article in articles:
        dic = {}
        repo = article.find('h1', {'class': 'lh-condensed'})
        if not repo is None:
            repo_a = repo.a
            if not repo_a is None:
                repo_text = replaces(repo_a.text)
                dic['repo'] = repo_text

        desc = article.find('p', {'class': 'col-9'})
        if not desc is None:
            dic['desc'] = desc.text.strip()

        lang = article.find('span', {'itemprop': 'programmingLanguage'})
        if not lang is None:
            dic['lang'] = lang.text.strip()

        lang_color = article.find('span', {'class': 'repo-language-color'})
        if not lang_color is None:
            dic['lang_color'] = lang_color.attrs['style'][-6:]

        fork_starts = article.find_all('a', {'class': 'muted-link'})
        if not fork_starts is None:
            dic['stars'] = fork_starts[0].text.strip()
            dic['forks'] = fork_starts[1].text.strip()

        added_stars = article.find('span', {'class': 'float-sm-right'})
        if not added_stars is None:
            dic['added_stars'] = added_stars.text.strip()

        bs_avatars = article.find_all('img', {'class': 'avatar'})
        avatars = []
        for bs_avatar in bs_avatars:
            avatar = bs_avatar.attrs['src']
            avatars.append(avatar)

        dic['avatars'] = avatars
        trendings.append(dic)

    return trendings


getRepo()

app = Flask(__name__)
api = flask_restful.Api(app)


class Dev(flask_restful.Resource):
    def get(self):
        try:
            since = request.args.get('since')
            data = getRepoDevelopers(since)
            return jsonify({'data': data})
        except Exception as e:
            return e


class Repo(flask_restful.Resource):
    def get(self):
        try:
            since = request.args.get('since')
            data = getRepo(since)
            return jsonify({'data': data})
        except Exception as e:
            return e


api.add_resource(Dev, '/api/dev')
api.add_resource(Repo, '/api/repo')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='5000')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='443', ssl_context=(
        os.environ['HOME']+'/crt/server.pem', os.environ['HOME']+'/crt/server.key'))
