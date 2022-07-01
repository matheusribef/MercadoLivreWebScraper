from colorama import Cursor
from flask import Flask, render_template, request
import bs4, requests
from matplotlib.pyplot import title

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resultado')
def resultado():
    item = request.args.get('item')
    valor = request.args.get('valor')

    ml_html = requests.get(f"https://lista.mercadolivre.com.br/{item}#D[A:{item}]").content
    soup = bs4.BeautifulSoup(ml_html, 'html.parser')
    links_href = soup.find_all("a", class_="ui-search-result__content ui-search-link")
    titles = soup.find_all("h2", class_="ui-search-item__title ui-search-item__group__element")

    html ="<head><style>tr, th{font-family: sans-serif;font-size: 20px;width:100%;}body{background-color: #FFFFFF;}</style></head>"
    html += "<body><table border=1 frame=hsides rules=rows><tr> <th><b>Nome do Produto</b></th> <th><b>Link</b></th> <th><b>Valor</b></th></tr>"
    index = 1
    for i in range(10):
        link_produto = links_href[i].get('href')
        produto_html = requests.get(link_produto).content
        price_soup = bs4.BeautifulSoup(produto_html, 'html.parser')
        price = price_soup.find("span", class_="andes-money-amount__fraction")
        if int(price.get_text().replace('.', '')) < int(valor):
            html += "<tr>"
            html += f"<td>{titles[i].get_text()}</td>"
            html += f"<td><a href=\"{link_produto}\">Link</a></td>"
            html += f"<td>{price.get_text()}</td>"
            html += "</tr>"

    html += "</table></body>"
    return html

app.run()
