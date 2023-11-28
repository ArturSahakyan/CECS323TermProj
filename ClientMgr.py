# API Imports
from pymongo import MongoClient
import certifi

""" Just a class to keep things organized! """
class ClientMgr:
    def __init__(self):
        self.m_clusterLink: str = ""
        self.m_client = None

    def genClusterLink(self):
        # Get Information For Cluster Link
        username = input("Username--> ")
        password = input("Password--> ")
        cluster_name = input("Cluster Name(eg. cecs-323-spring-2023)--> ")
        cluster_hash = input("Cluster hash--> ")

        # Link to Database Cluster in Atlas
        self.m_clusterLink = f"mongodb+srv://" + username + ":" + password + "@" + cluster_name + "." + cluster_hash + ".mongodb.net/?retryWrites=true&w=majority"

    def connectClient(self):
        self.m_client = MongoClient(self.m_clusterLink, tlsCAFile=certifi.where())

    @property
    def client(self):
        """Getter Method (Just in Case)"""
        return self.m_client

    @client.setter
    def client(self, value):
        """Setter Method (Avoid Setting this value"""
        print("umm, why are you trying to set the client value?")
