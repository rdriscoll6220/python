from py2neo import Node, Graph, Relationship, NodeMatcher
from textblob import TextBlob
from nltk import punkt
#import array
import newspaper
from newspaper import Article

#building news sources

def buildNewsSources():
    print('building news sources...')
    global cnbc_paper
    cnbc_paper = newspaper.build('http://cnbc.com', memoize_articles=False)
    #global bloomberg_paper
    #bloomberg_paper = newspaper.build('http://www.bloomberg.com', memoize_articles=False)
    #global foxnews_paper
    #foxnews_paper = newspaper.build('http://foxnews.com', memoize_articles=False)
    #global cnn_paper
    #cnn_paper = newspaper.build('http://cnn.com', memoize_articles=False)
    print('CNBC paper size is ', cnbc_paper.size())
    #print('Bloomberg paper size is ', bloomberg_paper.size())
    #print('Fox News  paper size is ', foxnews_paper.size())
    #print('CNN paper size is ', cnn_paper.size())

def downloadArticles():
    print("downloading CNBC articles...")
    cnbc_paper.download_articles()
    #print('downloading Bloomberg articles')
    #bloomberg_paper.download_articles()
    #print("downloading Fox News articles...")
    #foxnews_paper.download_articles()
    #print('downloading CNN articles...')
    #cnn_paper.download_articles()

def parseArticles():
    print("parsing articles...")
    cnbc_paper.parse_articles()
    #bloomberg_paper.parse_articles()
    #foxnews_paper.parse_articles()
    #cnn_paper.parse_articles()

def conditionallyProcessArticle():
    g = Graph("bolt://192.168.1.17:7687", auth=("neo4j", "Wh@dunn1t"))
    g.delete_all()
    for article in cnbc_paper.articles:
       
        if 'Ukraine' in article.text:
            print('Search term "Ukraine" found...extracting features with newspaper3k...')
            article.nlp()
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

def main():
    buildNewsSources()
    downloadArticles()
    parseArticles()
    conditionallyProcessArticle()
    
if __name__ == "__main__":
    main()