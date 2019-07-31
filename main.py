
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import flask_restful
from flask_restful import Resource
from flask import jsonify

# avatar	开发者头像	String	url字符串
# name	拥有者名字	String	/
# full_name	拥有者全名	String	originName(NickName)的形式
# app	applicaion
# app_des applicaion 简介


def getRepoDevelopers(since):
    url = 'https://github.com/trending/developers'
    if not since is None:
        url = url + 'since=' + since
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    devArticles = soup.find_all('article', {'class': 'd-flex'})
    devs = []
    for devArticle in devArticles:
        dev_dic = {}

        img = devArticle.find('img', {'class': 'rounded-1'})
        dev_dic['avatar'] = img.attrs['src']

        full_name = devArticle.find('h1', {'class': 'lh-condensed'})
        dev_dic['full_name'] = full_name.a.text

        name = devArticle.find('p', {'class': 'mb-1'})
        dev_dic['name'] = name.a.text

        app = devArticle.find('a', {'class': 'css-truncate-target'})
        dev_dic['app'] = app.text.replace(
            '\n', '').replace('\r', '').replace(' ', '')

        app_des = devArticle.find('div', {'class': 'f6 text-gray mt-1'})
        if not app_des is None:
            dev_dic['app_des'] = app_des.text.replace(
                '\n', '').replace('\r', '').replace(' ', '')

        devs.append(dev_dic)

    return devs


app = Flask(__name__)
api = flask_restful.Api(app)


class Trending(flask_restful.Resource):
    def get(self):
        since = request.args.get('since')
        data = jsonify(getRepoDevelopers(since))
        return data


api.add_resource(Trending, '/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
