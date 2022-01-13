from py2neo import Node, Graph, Relationship, NodeMatcher
from textblob import TextBlob
import array
import newspaper
from newspaper import Article

# Read in article to TextBlob

def readInArticle():
    print("Reading article...")
    print("Creating newpaper3k Article") 
    article = Article('https://lite.cnn.com/en/article/h_4ea51f73190023916dde1c4fbae0adf1')
    print("Parsing article")
    article.download()
    article.parse()
    article.nlp()
    print(article.title)
    print(article.publish_date)
    print(article.authors)
    print(article.summary)
    print(article.text)
    print("Instanstiating TextBlob...")
    blob = TextBlob(article.text)
    print(blob)
    print("Extracting tags...")
    bt = blob.tags
    print("Extracting noun_phrases...")
    bn = blob.noun_phrases
    print(bn)
    print("Analysing sentiment...")
    bs = blob.sentiment
    print(bs)    
        
    g = Graph("bolt://192.168.1.17:7687", auth=("neo4j", "Wh@dunn1t"))
    #g.delete_all()
    # for loop
    for i in bt:
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
            print("New Pair:", r1)
        elif (leftNode == None) and (rightNode != None):
            node1 = Node('vWord', wordImage = str(j))
            node2 = rightNode
            r1 = Relationship(node1, 'isA', node2) 
            g.create(r1) 
            print("New vWord Existing vPos:", r1)  
            
    print("Total vWord Nodes: " + str(g.nodes.match("vWord").count()))
    print("Total vPos Nodes: " + str(g.nodes.match("vPos").count()))    
    
def learnReadArticles():
    readInArticle()

def main():
    learnReadArticles()
    
if __name__ == "__main__":
    main()