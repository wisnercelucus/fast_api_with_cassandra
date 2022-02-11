import pathlib
import os
# from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection
from . import config

settings = config.get_settings()

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR / 'ignored' /'connect.zip')

# load_dotenv()




ASTRA_DB_CLIENT_ID= settings.db_client_id #os.environ.get("ASTRA_DB_CLIENT_ID")
ASTRA_DB_CLIENT_SECRET=  settings.db_client_secret #os.environ.get("ASTRA_DB_CLIENT_SECRET")
#ASTRA_DB_APP_TOKEN= settings. #os.environ.get("ASTRA_DB_APP_TOKEN")

def get_cluster():
    cloud_config= {
        'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster

def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session

# session = get_session()
