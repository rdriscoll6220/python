from py2neo import Node, Graph, Relationship, NodeMatcher
from textblob import TextBlob
import array

# Read in article to TextBlob

def listToDict(tbtags):
    return dict(tbtags)

def readInArticle():
    with open('/home/ron/repos/python/textBlob/inflation.txt', 'r') as text1:
        content = text1.read()
        text1.close()
        blob = TextBlob(content)
        bt = blob.tags
        #tb2dict = listToDict(bt)
        #print(tb2dict)
        
    g = Graph("bolt://192.168.1.17:7687", auth=("neo4j", "Wh@dunn1t"))
    g.delete_all()
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
        #elif (leftNode != None) and (rightNode.properties[pos]) != str(k):
        #    node1 = leftNode
        #    node2 = Node('vPos', pos = str(k))
        #    r1 = Relationship(node1, 'isA', node2)
        #    g.create(r1)
            
                                
    print("Total vWord Nodes: " + str(g.nodes.match("vWord").count()))
    print("Total vPos Nodes: " + str(g.nodes.match("vPos").count()))    
    
def learnReadArticles():
    readInArticle()

def main():
    learnReadArticles()
    
if __name__ == "__main__":
    main()