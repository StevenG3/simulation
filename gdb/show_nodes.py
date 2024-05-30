from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# 连接Neo4j数据库
uri = "bolt://localhost:7687"  # 或者你的数据库URI
username = "neo4j"             # 默认用户名
password = "password"          # 替换为你的密码

driver = GraphDatabase.driver(uri, auth=(username, password))

def fetch_data():
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT 50
    """
    with driver.session() as session:
        result = session.run(query)
        return [(record["n"], record["m"], record["r"]) for record in result]

# 获取数据
data = fetch_data()

G = nx.Graph()

for n, m, r in data:
    node_start = n["name"]  # 假设每个节点有一个'name'属性
    node_end = m["name"]
    G.add_node(node_start)
    G.add_node(node_end)
    G.add_edge(node_start, node_end, label=r.type)  # 假设我们关心的是关系的类型

# 画图
pos = nx.spring_layout(G)  # 节点的布局
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'label'))
plt.show()

