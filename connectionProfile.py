from py2neo import Node, Graph, Relationship
from py2neo.bulk import create_nodes
from textblob import TextBlob
import array

# Read in article to TextBlob

def readInArticle():
    with open('/home/ron/repos/python/textBlob/roberts.txt', 'r') as text1:
        content = text1.read()
        text1.close
        blob = TextBlob(content)
        bt = blob.tags
    
def writeNewData():
    lobe1 = Graph("bolt://192.168.1.17:7687", auth=("neo4j", "Wh@dunn1t"))
    keys = ["word", "pos"]
    create_nodes(lobe1.auto(), bt, labels={'vword'} = blob.tags, labels={"vword"}, keys=keys)
    lobe1.nodes.match("vword").count()
        
    

def learnReadArticles():
    readInArticle()
    writeNewData()

   

def main():
    learnReadArticles()
    
if __name__ == "__main__":
    main()