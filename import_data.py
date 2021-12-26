from py2neo import Graph, Node, Relationship
import json

# laod entity
with open("halo_entity.json") as f:
    data = json.load(f)
    entity_list = data['entity']

# laod dependency
with open("halo_dependency.json") as f:
    data = json.load(f)
    dep_list = data['dependency']

g = Graph("http://49.232.25.208:7474", user="neo4j", password="aduiduidui")
tx = g.begin()


for e in entity_list:
    n = Node("Entity", **e)
    tx.create(n)

g.commit(tx)

tx = g.begin()

for d in dep_list:
    n_src = g.nodes.match('Entity', entityID=d['dependencySrcID']).first()
    n_dest = g.nodes.match('Entity', entityID=d['dependencydestID']).first()
    if n_src is None or n_dest is None:
        print("Node not find")
        continue
    dr = Relationship(n_src, d['dependencyType'], n_dest, **d)
    tx.create(dr)

g.commit(tx)