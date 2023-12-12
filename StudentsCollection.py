from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType
from CollManager import CollManager


class StudentsCollection(CollectionBase):

    def initCollection(self):
        self.collName = "students"

        self.schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["last_name", "first_name", "email", "major"],
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
                            "bsonType": "string"
                        }
                    },
                    "sections": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "objectId"
                        }
                    }
                }
            }
        }

        self.attributes = [("last_name", AttrType.STRING), ("first_name", AttrType.STRING),
                            ("email", AttrType.STRING), ("majors", AttrType.FOREIGN),
                            ("sections", AttrType.FOREIGN)]
        self.uniqueCombos = [[0,1], [2]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        

        # TO-DO: in theory we should handle possibility of no dept collection

        ret_list = []

        dept_collection = CollManager.GetCollection("departments")
        dept_list = dept_collection.find({})
        valid_majors_set = set()
        for dept in dept_list:
            for major in dept['majors']:
                valid_majors_set.add(major['name'])
        valid_majors = list(valid_majors_set)
        major_set = set()

        print(f"Requires:\n{str(self.schema['$jsonSchema']['properties']['majors'])}")
        while(True):
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
                counter = 1
                for maj in valid_majors:
                    print(f"{counter}: {maj}")

                try:
                    new_maj_index = int(input("Input major name --> "))
                    if new_maj_index <= 0 or new_maj_index > len(valid_majors):
                        raise ValueError
                except Exception as e:
                    print("Invalid selection. Try again.")
                    continue

                major_set.add(valid_majors[new_maj_index - 1])

        major_list = list(major_set)
        ret_list.append(("majors", major_list))

        # TO-DO: in theory we should handle possibility of no sect collection

        sect_collection = CollManager.GetCollection("sections")
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
                doc = sect_collection.selectDoc()
                if doc is not None:
                    sect_set.add(doc["_id"])
        sect_list = list(sect_set)
        ret_list.append(("sections", sect_list))

        return ret_list

    def orphanCleanUp(self, doc) -> bool:
        return True
