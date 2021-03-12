import os
import random
from bs4 import BeautifulSoup


with open('assets/url_base.txt', 'r') as f:
    url_base = f.read()

with open('assets/layout.html', 'r') as f:
    layout = f.read()

layout = layout.replace('<url_base/>', url_base)




def load_article(path, id):
    with open(path, 'r') as f:
        text = f.read()

    soup = BeautifulSoup(text, 'html.parser')

    attributes = {'text': text}

    attributes['id'] = int(soup.find(id='id').contents[0])
    attributes['title'] = soup.find(id='title').contents[0]
    attributes['link'] = url_base + 'articles/' + '_'.join(attributes['title'].split()).lower() + '.html'
    attributes['description'] = soup.find(id='description').contents[0]
    attributes['time'] = soup.find(id='time').contents[0]
    attributes['categories'] = soup.find(id='categories').contents[0].lower().split(', ')

    return attributes

def load_articles():
    articles = []
    for id, article in enumerate(os.listdir('docs/articles')):
        path = os.path.join('docs/articles', article)
        attributes = load_article(path, id)
        articles.append(attributes)

    return sorted(articles, key=lambda x: x['id'])


articles = load_articles()


def generate_index():
    with open('assets/index.html', 'r') as f:
        index = f.read()

    with open('assets/featured.txt', 'r') as f:
        featured = f.read()

    featured = featured.split(', ')

    article_list = []

    for f in featured:
        id = int(f)
        article = articles[id]

        title = article['title']
        description = article['description'][:300]
        link = article['link']

        text = f'''
        <a class="article-preview">
            <a href="{link}"> <h2>{title} </h2> </a>
            <p>{description}</p>
        </a>
        '''
        article_list.append(text)

    index = index.replace('<featured/>', ''.join(article_list))

    index = layout.replace('<content/>', index)

    with open('docs/index.html', 'w+') as f:
        f.write(index)


def generate_articles():
    for article in os.listdir('articles'):
        path = os.path.join('articles', article)
        with open(path) as f:
            text = f.read()

        soup = BeautifulSoup(text, 'html.parser')
        title = soup.find(id='title').contents[0]
        title = '_'.join(title.split()).lower() + '.html'

        page = layout.replace('<content/>', text)

        with open(f'docs/articles/{title}', 'w+') as f:
            f.write(page)


if __name__ == '__main__':
    generate_articles()
    generate_index()