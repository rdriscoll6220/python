from py2neo import Node, Graph, Relationship, NodeMatcher
import newspaper
from newspaper import Article
from nltk import punkt
from textblob import TextBlob


cnbc_paper = newspaper.build('http://cnbc.com')
bloomberg_paper = newspaper.build('http://www.bloomberg.com')
print('CNBC paper size is ', cnbc_paper.size())
print('Bloomberg paper size is ', bloomberg_paper.size())

print("downloading CNBC articles...")
cnbc_paper.download_articles()
print('downloading Bloomberg articles')
bloomberg_paper.download_articles()
print("parsing articles...")
cnbc_paper.parse_articles()
bloomberg_paper.parse_articles()

#print(sina_paper.size())

#for article in msnbc_paper.articles:
#    article.download()
#    print(msnbc_paper. )

#for article in msnbc_paper.articles:
#    article.parse()
#

for article in cnbc_paper.articles:
    if 'Apple' in article.text:
        article.nlp()
        tb = TextBlob(article.summary)
        print('Publish Date: ', article.publish_date)
        print('Title: ', article.title)
        print('Authors: ', article.authors)
        print('Sentiment: ', tb.polarity)
        print('Subjectivity: ', tb.subjectivity)
        print('Summary: ', article.summary)

for article in bloomberg_paper.articles:
    if 'Apple' in article.text:
        article.nlp()
        tb = TextBlob(article.summary)
        print(article.publish_date)
        print(article.title)
        print(article.authors)
        print(tb.polarity)
        print(tb.subjectivity)
        print(article.summary)





