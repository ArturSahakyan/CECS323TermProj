import pymongo
from pprint import pprint
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import Tuple, Any, List

from CollManager import CollManager

class AttrType(Enum):
    STRING = 1
    INTEGER = 2
    TIME = 3
    FOREIGN_ARR = 4

    FOREIGN_DEPT = "departments"
    FOREIGN_COURSE = "courses"

class CollectionBase(ABC):

    """
        Base Class For All Collection Managers
        Simplifies Redundant Code As All Collections Will Have: (Add Delete List and Select) functions

        ABSTRACT METHODS TO IMPLEMENT
            -   initCollection(self)
                    This is where you reassign: collName, schema, attributes, uniqueCombos
                    CollectionBase will handle the initialization of everything from these attributes

            -   uniqueAttrAdds(self)->List[Tuple[str, Any]]
                    This is where you can call the select functions of other collections
                    Use in case of any relationships

            -   orphanCleanUp(self, doc)
                    This is where you clean up any relationships created from uniqueAttrAdds Upon Deletion
                    Leave No Child Left Behind!!!

            -   onValidInsert(self, doc_id)
                    This gets called once a document is inserted and it's valid.
                    Use this if you need to do anything immediately after creation
    """

    def __init__(self, db):
        # Collection
        self.m_collName = "Invalid Collection"  # REASSIGN IN CHILD !!!
        self.m_collection = None
        self.m_db = db

        # Collection Attributes (REASSIGN ALL OF THESE IN CHILD !!!)
        self.schema = {"invalid"}
        self.attributes = []  # Array of Tuples (col_name, AttrType)
        self.uniqueCombos = []  # Array of arrays, indices representing the indices from self.attributes to make up a candidate key

        # Initialize Collection
        self.initCollection()
        self.setupCollection()

    @abstractmethod
    def initCollection(self):
        """
            ReAssign Collection Attributes for Specific Child
            collName, schema, attributes, uniqueCombos
        """
        pass

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
        new_doc_id = None

        while not successful:
            try:
                new_doc = {}

                # General Attributes to Add
                for attr in self.attributes:
                    print("")
                    match attr[1]:
                        case AttrType.STRING:
                            new_doc[attr[0]] = input(f"Requires:\n{str(self.schema['$jsonSchema']['properties'][attr[0]])}\nInput {attr[0]} --> ")
                        case AttrType.INTEGER:
                            new_doc[attr[0]] = int(input(f"Requires:\n{str(self.schema['$jsonSchema']['properties'][attr[0]])}\nInput Integer {attr[0]} --> "))
                        case AttrType.TIME:
                            hour = int(input(f"Requires:\n{str(self.schema['$jsonSchema']['properties'][attr[0]])}\nInput Hour(Int 0-23) for {attr[0]} --> "))
                            minutes = int(input(f"Input Minutes(Int 0-59) for {attr[0]} --> "))
                            new_doc[attr[0]] = datetime(2000, 1, 1, hour, minutes, 0)
                        case _:
                            # Error checking
                            if not isinstance(attr[1], AttrType):
                                print("\nPlease make sure you are using the AttrType enumeration when creating attributes!!")
                                return

                            if attr[1] == AttrType.FOREIGN_ARR:
                                continue

                            print(f"We will need values from {attr[1].value}")
                            new_doc[attr[0]] = CollManager.GetCollection(attr[1].value).selectDoc()["_id"]

                # Handle Any ForeignKeys/Relationships
                new_attrs = self.uniqueAttrAdds()
                if len(new_attrs) > 0:
                    for attr in new_attrs:
                        new_doc[attr[0]] = attr[1]

                new_doc_id = self.collection.insert_one(new_doc).inserted_id

            except Exception as e:
                print(f"\nError in {self.collName}: {str(e)}") # Print Error

                # Ask to Try Again
                print("Try Again? [y/n]")
                user_inp = input("> ")
                while user_inp != 'y' and user_inp != 'n':
                    print("\nPlease Only Enter Either 'y' or 'n'")
                    user_inp = input("> ")
                print("")

                # Break Loop if User Doesn't Want to Try Again
                if user_inp == 'n':
                    break

                continue # Start Back From Top

            successful = True
        self.onValidInsert(new_doc_id)

    # Implement this function to add in foreign keys or create relationships
    @abstractmethod
    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        """ Add Any Attributes That Require Selects (i.e. Foreign Keys) """
        pass

    @abstractmethod
    def onValidInsert(self, doc_id):
        pass

    def deleteDoc(self):
        # Select Doc & Error Handling
        old_doc = self.selectDoc()
        if old_doc == None:
            print("Failed Document Selection, Aborting Delete..\n")
            return

        # Can't Leave Parent-less Children!!
        success = self.orphanCleanUp(old_doc)
        if not success:
            print(f"Orphan CleanUp Failed in {self.collName} collection!")
            return

        # Continue With Deletion :D
        deleted = self.collection.delete_one({"_id": old_doc["_id"]})
        print(f"We just deleted: {deleted.deleted_count} document(s).")

    @abstractmethod
    def orphanCleanUp(self, doc) -> bool:
        """ Clean Up Any ToBe Orphans before doc gets deleted, returns either success or fail """
        pass

    def listAll(self) -> List:
        doc_list = self.collection.find({})
        for doc in doc_list:
            pprint(doc)
        return doc_list

    def getAll(self) -> List:
        return self.collection.find({})

    def selectDoc(self) -> {}:
        new_doc = None

        # List possible ways to select a document, using any of the candidate keys specified in self.uniqueCombos
        num_ways = len(self.uniqueCombos)
        print("How Would You Like to Select One?")
        for i in range(num_ways):
            print(f"{i+1}. [", end="")
            for j in range(len(self.uniqueCombos[i])-1):
                print(f"{self.attributes[self.uniqueCombos[i][j]][0]}, ", end="")

            print(f"{self.attributes[self.uniqueCombos[i][-1]][0]}", end="")
            print("]")

        # Make Sure User Picks a Valid Selection
        user_input = int(input(f"(Int 1-{num_ways})> ")) - 1
        while user_input < 0 or user_input > (num_ways - 1):
            print("Invalid. Please Try Again")
            user_input = int(input(f"(Int 1-{num_ways})> ")) - 1
        print("")

        # Collect Data Required From Candidate Key to Select Doc
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
                        doc_filter[attr[0]] = datetime(2000, 1, 1, hour, minutes, 0)
                    case _:
                        # Error checking
                        if not isinstance(attr[1], AttrType):
                            print(
                                "\nPlease make sure you are using the AttrType enumeration when creating attributes!!")
                            return

                        # Grab Foreign Key!
                        if attr[1] == AttrType.FOREIGN_ARR:
                            print("\nThis application is not prepared to handle selecting using arrays!")
                            continue

                        print(f"We will need values from {attr[1].value}")
                        doc_filter[attr[0]] = CollManager.GetCollection(attr[1].value).selectDoc()["_id"]

            # Attempt Selection
            if self.collection.count_documents(doc_filter) != 0:
                found = True
            else:
                print("Couldn't Find A Document With Attributes: " + str(doc_filter) + "!")

                # Ask to Try Again
                print("Try Again? [y/n]")
                user_inp = input("> ")
                while user_inp != 'y' and user_inp != 'n':
                    print("\nPlease Only Enter Either 'y' or 'n'")
                    user_inp = input("> ")
                print("")

                if user_inp == 'n':
                    return None  # Possibility of NoneType Return Means We Have to Be Cautious When We Call This Function

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
        return self.m_collName

    @collName.setter
    def collName(self, val: str):
        """ Setter for collName; Regens self.collection """
        self.m_collName = val
        self.collection = self.db[self.m_collName]

    @property
    def collection(self):
        """ Getter for PyMongo Collection; For Unique Use Cases"""
        return self.m_collection

    @collection.setter
    def collection(self, val):
        """ Setter for PyMongo Collection; Should Never Be Used Except in setupCollection """
        self.m_collection = val
