from py2neo import Node, Graph, Relationship, NodeMatcher
from textblob import TextBlob
from nltk import punkt
#import array
import newspaper
from newspaper import Article
import time

#building news sources

def buildNewsSources():
    print('building news sources...')
    global papers, paper, pCount, papersBuilt 
    
    papers = [('http://cnbc.com', 'bolt://192.168.1.17'), ('http://www.bloomburg.com', 'bolt://192.168.1.18'), ('http://foxnews.com', 'bolt://192.168.1.19'), ('http://cnn.com', 'bolt://192.168.1.20')]
    papersBuilt = [newspaper, newspaper, newspaper, newspaper]
    paper = 0
    i = 0
    for paper in papers:
        print (i)
        print('building ' + paper[0])
        papersBuilt[i] = newspaper.build(paper[0], memoize_articles=True)
        print(paper[0] + ' paper size is ', papersBuilt[i].size())
        i += 1

    #global bloomberg_paper
    #bloomberg_paper = newspaper.build('http://www.bloomberg.com', memoize_articles=False)
    #global foxnews_paper
    #foxnews_paper = newspaper.build('http://foxnews.com', memoize_articles=False)
    #global cnn_paper
    #cnn_paper = newspaper.build('http://cnn.com', memoize_articles=False)
    #print('CNBC paper size is ', cnbc_paper.size())
    #print('Bloomberg paper size is ', bloomberg_paper.size())
    #print('Fox News  paper size is ', foxnews_paper.size())
    #print('CNN paper size is ', cnn_paper.size())

def downloadArticles():
    print("downloading articles...")
    for i in papersBuilt:
        print('downloading newspaper ')
        i.download_articles()
    #print('downloading Bloomberg articles')
    #bloomberg_paper.download_articles()
    #print("downloading Fox News articles...")
    #foxnews_paper.download_articles()
    #print('downloading CNN articles...')
    #cnn_paper.download_articles()

def parseArticles():
    print("parsing articles...")
    for i in papersBuilt:
        i.parse_articles()
    #bloomberg_paper.parse_articles()
    #foxnews_paper.parse_articles()
    #cnn_paper.parse_articles()

def conditionallyProcessArticle():
    db_url0 = 'bolt://192.168.1.17'
    db_url1 = 'bolt://192.168.1.18'
    db_url2 = 'bolt://192.168.1.19'
    db_url3 = 'bolt://192.168.1.20'
    db_urls = [db_url0, db_url1, db_url2, db_url3]
    x = 0 
    while x < len(db_urls):
        print('Opening connection to graph...')
        g = Graph(db_urls[x], auth=("neo4j", "Wh@dunn1t"))
        #g.delete_all()
        for article in papersBuilt[x].articles: 
            article.nlp()
            if 'Ukraine' in article.text:
                print('Search term "economy" found...extracting features with newspaper3k...')
                tbat = TextBlob(article.text)
                print('     Publish Date: ', article.publish_date)
                print('     Title: ', article.title)
                print('     Authors: ', article.authors)
                print('     Sentiment: ', tbat.polarity)
                print('     Subjectivity: ', tbat.subjectivity)
                print('     Summary: ', article.summary)
                print('     Key Words: ', article.keywords)

            tbs = TextBlob(article.summary)
            print("Extracting tags...")
            tbst = tbs.tags
        
            print("Extracting noun_phrases...")
            tbnf = tbs.noun_phrases  

            # for loop
            for i in tbst:
                j = i[0]
                k = i[1]
                
                #existsVword = g.exists("vWord", key="wordImage", property_value=str(j))
                #existsVpos = g.exists("vPos", key="pos", property_value=str(j))
                nodes = NodeMatcher(g)
                leftNode = nodes.match("vWord", wordImage = str(j)).first()
                rightNode = nodes.match("vPos", pos = str(k)).first()
                
                #print(leftNode, ' ', rightNode)
                if (leftNode == None) and (rightNode == None):
                    node1 = Node('vWord', wordImage = str(j))
                    #g.create(node1)
                    node2 = Node('vPos', pos = str(k))
                    #g.create(node2)
                    r1 = Relationship(node1, 'isA', node2)
                    g.create(r1)
                    print("New vWord New vPOS:", str(j) + ' ', r1)
                elif (leftNode == None) and (rightNode != None):
                    node1 = Node('vWord', wordImage = str(j))
                    node2 = rightNode
                    r1 = Relationship(node1, 'isA', node2) 
                    g.create(r1) 
                    print("New vWord Existing vPos:", str(j) + ' ', r1)  
            
        print("Total vWord Nodes: " + str(g.nodes.match("vWord").count()))
        print("Total vPos Nodes: " + str(g.nodes.match("vPos").count())) 
        x += 1

def main():
    i = 0
    while i == 0:
        buildNewsSources()
        downloadArticles()
        parseArticles()
        conditionallyProcessArticle()
        print('Waiting 10 minutes...')
        time.sleep(600)
    
if __name__ == "__main__":
    main()