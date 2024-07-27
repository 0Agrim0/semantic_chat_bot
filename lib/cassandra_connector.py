from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
auth_provider = PlainTextAuthProvider(username='cassandra', password='password')
cluster = Cluster(['0.0.0.0'], port=9042,auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("SELECT * FROM chat.chhat").one()
if row:
    print(row[0])