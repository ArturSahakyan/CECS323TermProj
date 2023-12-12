from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType
from SectionsCollection import SectionsCollection
from CollManager import CollManager
from datetime import datetime
from bson.objectid import ObjectId

class StudentsCollection(CollectionBase):

    def initCollection(self):
        self.collName = "students"

        self.schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["last_name", "first_name", "email", "majors"],
                "additionalProperties": False,
                "properties": {
                    "_id": {},
                    "last_name": {
                        "bsonType": "string",
                        "maxLength": 40,
                        "description": "The student's surname"
                    },
                    "first_name": {
                        "bsonType": "string",
                        "maxLength": 40,
                        "description": "The student's given name"
                    },
                    "email": {
                        "bsonType": "string",
                        "maxLength": 100,
                        "description": "The text of the address used to send digital mail to the student"
                    },
                    "majors": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["name", "declaration_date"],
                            "properties": {
                                "name": {
                                    "bsonType": "string",
                                    "minLength": 5,
                                    "maxLength": 50,
                                    "description": "Name of the major"
                                },
                                "declaration_date": {
                                    "bsonType": "date",
                                    "description": "The calendar day on which the student joined the major"
                                }
                            }
                        },
                        "description": "List of majors offered by the department"
                    },
                    "sections": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "objectId",
                            "description": "The course offering that a student has enrolled in"
                        }
                    }
                }
            }
        }

        self.attributes = [("last_name", AttrType.STRING), ("first_name", AttrType.STRING),
                            ("email", AttrType.STRING), ("majors", AttrType.FOREIGN_ARR),
                            ("sections", AttrType.FOREIGN_ARR)]
        self.uniqueCombos = [[0,1], [2]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        
        # TO-DO: in theory we should handle possibility of no dept collection
        
        ret_list = []
        
        all_depts = CollManager.GetCollection("departments").collection.find({})
        valid_majors = []
        for dept in all_depts:
            for major in dept['majors']:
                valid_majors.append(major['name'])

        majors = []
        seen = set()
        
        while(True):
            dec_year = 0
            dec_month = 0
            dec_day = 0

            print("Add a major? [y/n]")
            y_n_input = input("> ")
            while y_n_input != 'y' and y_n_input != 'n':
                print("\nPlease only enter either 'y' or 'n'")
                y_n_input = input("> ")
            print("")

            if y_n_input == 'n':
                break

            else:
                print("Select a major to add:")
                for number, major in enumerate(valid_majors):
                    print(number + 1, major)
                print()

                try:
                    new_maj_index = int(input("Selection --> "))
                    print()
                    if new_maj_index <= 0 or new_maj_index > len(valid_majors):
                        raise ValueError
                    if valid_majors[new_maj_index - 1] in seen:
                        print("Student already has that major. Try again.\n")
                        continue
                except:
                    print("Invalid selection. Try again.\n")
                    continue
                
                while(True):
                    try:
                        dec_year = int(input("Declaration year --> "))
                        dec_month = int(input("Declaration month (digit) --> "))
                        dec_day = int(input("Declaration day (digit) --> "))
                        print()
                        dec_date = datetime(dec_year, dec_month, dec_day)
                        break
                    except:
                        print("Invalid entry. Try again.")

                seen.add(valid_majors[new_maj_index - 1])
                majors.append({'name': valid_majors[new_maj_index - 1], 'declaration_date': dec_date})

        ret_list.append(("majors", majors))

        # TO-DO: in theory we should handle possibility of no sect collection

        sect_set = set()
        while(True):
            print("Add a section?")
            y_n_input = input("> ")
            while y_n_input != 'y' and y_n_input != 'n':
                print("\nPlease only enter either 'y' or 'n'")
                y_n_input = input("> ")
            print("")

            if y_n_input == 'n':
                break

            else:
                doc = CollManager.GetCollection("sections").selectDoc()
                if doc is not None:
                    sect_set.add(ObjectId(doc["_id"]))
        
        sect_list = list(sect_set)
        ret_list.append(("sections", sect_list))

        return ret_list

    def orphanCleanUp(self, doc) -> bool:
        return True

    def onValidInsert(self, doc_id):
        pass