from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(username, password))

def add_node(tx, name, queueLength):
    tx.run("CREATE (n:Node {name: $name, queueLength: $queueLength})", name=name, queueLength=queueLength)

def add_snr_relationship(tx, from_node, to_node, snr):
    tx.run("MATCH (a:Node {name: $from_node}), (b:Node {name: $to_node}) "
           "CREATE (a)-[:SNR {value: $snr}]->(b)", from_node=from_node, to_node=to_node, snr=snr)

with driver.session() as session:
    session.execute_write(add_node, "Node1", 10)
    session.execute_write(add_node, "Node2", 15)
    session.execute_write(add_snr_relationship, "Node1", "Node2", 30)

driver.close()
