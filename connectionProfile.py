from py2neo import Node, Graph, Relationship
import array, time

def wake():
    lobe1 = Graph("bolt://192.168.1.17:7687", auth=("neo4j", "Wh@dunn1t"))
    print(lobe1)
    lobe2 = Graph("bolt://192.168.1.18:7687", auth=("neo4j", "Wh@dunn1t"))
    print(lobe2)
    lobe3 = Graph("bolt://192.168.1.19:7687", auth=("neo4j", "Wh@dunn1t"))
    print(lobe3)
    lobe4 = Graph("bolt://192.168.1.20:7687", auth=("neo4j", "Wh@dunn1t"))
    print(lobe4)
    array=[lobe1, lobe2, lobe3, lobe4]
    print(array)

    wakeEvent = Node("wakeEvent", mark=time.asctime(), Conf=50)

    lobe1.delete_all()
    #ox = lobe1.begin()
    #ox.delete_all()
    #ox.commit()

    #rx = lobe1.begin()
    #rx.create(wakeEvent)
    #rx.commit()

    #sx = lobe2.begin()
    #sx.create(wakeEvent)
    #sx.commit()

    #tx = lobe3.begin()
    #tx.create(wakeEvent)
    #tx.commit()

    #ux = lobe4.begin()
    #ux.create(wakeEvent)
    #ux.commit()
    

def main():
    wake()
    
if __name__ == "__main__":
    main()