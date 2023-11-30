import pymongo
from pprint import pprint
from abc import ABC, abstractmethod

class CollectionBase(ABC):
    def __init__(self, db):
        # Collection
        self.collName = "Invalid Collection"
        self.collection = None
        self.m_db = db

        # Collection Attributes
        self.schema = "{invalid}"
        self.uniqueCombos = []

    # TODO: Finish Deciding Abstract Methods & Methods Base Will Implement
    @abstractmethod
    def addDoc(self):
        pass

    def deleteDoc(self):
        pass

    def listAll(self):
        pass

    """ **************** Getters & Setters ******************* """
    @property
    def db(self):
        """ Getter for Database; For Convention Purposes :p """
        return self.m_db
    @db.setter
    def db(self, val):
        """ Setter for Database; Regens collection as well """
        self.m_db = val
        self.collection = self.db[self.collName]

    @property
    def collName(self) -> str:
        """ Getter for collName """
        return self.collName
    @collName.setter
    def collName(self, val:str):
        """ Setter for collName; Regens self.collection """
        self.collName = val
        self.collection = self.db[self.collName]