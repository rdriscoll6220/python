from py2neo import Graph, Node, Relationship


def deleteAll():
    g = Graph("bolt://192.168.1.17:7687", auth=("neo4j", "Wh@dunn1t"))
    a = g.delete_all()
    
def main():
    deleteAll()
    
if __name__ == "__main__":
    main()