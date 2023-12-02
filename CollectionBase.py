import pymongo
from pprint import pprint
from abc import ABC, abstractmethod
from enum import Enum
from datetime import time
from typing import Tuple, Any, List


class AttrType(Enum):
    STRING = 1
    INTEGER = 2
    TIME = 3


class CollectionBase(ABC):
    def __init__(self, db):
        # Collection
        self.collName = "Invalid Collection"  # REASSIGN IN CHILD !!!
        self.collection = None
        self.m_db = db

        # Collection Attributes (REASSIGN ALL OF THESE IN CHILD !!!)
        self.schema = "{invalid}"
        self.attributes = []  # Array of Tuples (col_name, AttrType)
        self.uniqueCombos = []  # Array of arrays, indices representing the indices from self.attributes to make up a candidate key

    def setupCollection(self):
        # Create Collection or Use Existing
        try:
            self.db.create_collection(self.collName)
        except Exception as e:
            print(f'Using Previous "{self.collName}" Collection')

        # Assign Schema
        mod_results = self.db.command("collMod", self.collName, validator=self.schema)

        # Create Indices
        for combo in self.uniqueCombos:
            gen_tuple_list = []
            for index in combo:
                attr = self.attributes[index]
                gen_tuple_list.append((attr[0], pymongo.ASCENDING))

            self.collection.create_index(gen_tuple_list, unique=True)

    def addDoc(self):
        successful: bool = False

        while not successful:
            try:
                new_doc = {}

                # General Attributes to Add
                for attr in self.attributes:
                    match attr[1]:
                        case AttrType.STRING:
                            new_doc[attr[0]] = input(f"Input {attr[0]} --> ")
                        case AttrType.INTEGER:
                            new_doc[attr[0]] = int(input(f"Input Integer {attr[0]} --> "))
                        case AttrType.TIME:
                            hour = int(input(f"Input Hour(Int 0-23) for {attr[0]} --> "))
                            minutes = int(input(f"Input Minutes(Int 0-59) for {attr[0]} --> "))
                            new_doc[attr[0]] = time(hour, minutes)

                # Handle Any ForeignKeys/Relationships
                new_attrs = self.uniqueAttrAdds()
                for attr in new_attrs:
                    new_doc[attr[0]] = attr[1]

                self.collection.insert_one(new_doc)

            except Exception as e:
                print(f"Error in {self.collName}: {str(e)}")
                print("\n\nTry Again!!")
                continue

            successful = True

    # Implement this function to add in foreign keys or create relationships
    @abstractmethod
    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        pass

    def deleteDoc(self):
        old_doc = self.selectOne()
        deleted = self.collection.delete_one({"_id": old_doc["_id"]})
        print(f"We just deleted: {deleted.deleted_count} document(s).")

    def listAll(self):
        doc_list = self.collection.find({})
        for doc in doc_list:
            pprint(doc)

    def selectOne(self) -> {}:
        new_doc = None

        num_ways = len(self.uniqueCombos)
        print("How Would You Like to Select One?")
        for i in range(num_ways):
            print(f"{i + 1}. {self.uniqueCombos[i]}")

        user_input = int(input(f"(Int 1-{num_ways})> ")) - 1
        while user_input < 0 or user_input > (num_ways - 1):
            print("Invalid. Please Try Again")
            user_input = int(input(f"(Int 1-{num_ways})> ")) - 1
        print("")

        combo = self.uniqueCombos[user_input]
        doc_filter = {}
        found: bool = False
        while not found:
            for index in combo:
                attr = self.attributes[index]
                match attr[1]:
                    case AttrType.STRING:
                        doc_filter[attr[0]] = input(f"Input {attr[0]} --> ")
                    case AttrType.INTEGER:
                        doc_filter[attr[0]] = int(input(f"Input Integer {attr[0]} --> "))
                    case AttrType.TIME:
                        hour = int(input(f"Input Hour(Int 0-23) for {attr[0]} --> "))
                        minutes = int(input(f"Input Minutes(Int 0-59) for {attr[0]} --> "))
                        doc_filter[attr[0]] = time(hour, minutes)

            if self.collection.count_documents(doc_filter) != 1:
                found = True
            else:
                print("Couldn't Find A Document With Attributes: " + str(doc_filter) + "!")

        return self.collection.find_one(doc_filter)

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
    def collName(self, val: str):
        """ Setter for collName; Regens self.collection """
        self.collName = val
        self.collection = self.db[self.collName]
