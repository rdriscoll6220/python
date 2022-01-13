import newspaper
from newspaper import Article

url = 'http://www.magickeys.com/books/gingerbread/index.html'
article = Article(url)
article.download()
article.parse()
print("Printing article title...")
print(article.title)
print("Printing article publish date...")
print(article.publish_date)
print("Printing article text...")
print(article.text)
print("Printing article images...")
print(article.images)
print("Printing article movies...")
print(article.movies)
article.nlp()
print("Printing article keywords...")
print(article.keywords)
print("Printing article summary...")
print(article.summary)
print("Google top trending terms...")


