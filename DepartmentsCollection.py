from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType


class DepartmentsCollection(CollectionBase):

    """
        Base Class Will Call All of These Functions When Necessary
        No Need to Call Any of These Manually :D

        Just Set Them Up Like So!
    """

    def initCollection(self):
        self.collName = "departments"

        self.schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["name", "abbreviation", "chair_name", "building", "office", "description"],
                "properties": {
                    "building": {
                        "enum": ['NAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        "description": "Name of the structure that houses most of this department's work"
                    },
                    "office": {
                        "bsonType": "number",
                        "description": "Number identifying the room where the chair does work for the department"
                    },
                    "name": {
                        "bsonType": "string",
                        "minLength": 10,
                        "maxLength": 50,
                        "description": "Title identifying the department"
                    },
                    "abbreviation": {
                        "bsonType": "string",
                        "maxLength": 6,
                        "description": "Short Acronym Identifying the Department"
                    },
                    "chair_name": {
                        "bsonType": "string",
                        "maxLength":  80,
                        "description": "Name of the head of the department"
                    },
                    "description": {
                        "bsonType": "string",
                        "minLength": 10,
                        "maxLength": 80,
                        "description": "Short to medium length text describing the department"
                    },

                    "majors": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "object",
                            "required": ["name", "description"],
                            "properties": {
                                "name": {
                                    "bsonType": "string",
                                    "minLength": 5,
                                    "maxLength": 50,
                                    "description": "Name of the major"
                                },
                                "description": {
                                    "bsonType": "string",
                                    "minLength": 10,
                                    "maxLength": 80,
                                    "description": "Description of the major"
                                }
                            }
                        },
                        "description": "List of majors offered by the department"
                    }
                }
            }
        }

        self.attributes = [("building", AttrType.STRING), ("office", AttrType.INTEGER), ("name", AttrType.STRING),
                           ("abbreviation", AttrType.STRING), ("chair_name", AttrType.STRING),
                           ("description", AttrType.STRING), ("majors", AttrType.FOREIGN)]
        self.uniqueCombos = [[2], [3], [4], [0, 1]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        maj_list = []

        user_inp = ""
        while user_inp != "n":
            print("Do you want to add a major to this department? [y/n]")
            user_inp = input("> ")

            if user_inp == "y":
                print("What's the name of the major?")
                maj_name = input("> ")

                print("\nWhat's the description of that major?")
                maj_desc = input("> ")

                maj_list.append({"name":maj_name, "description":maj_desc})
                print("")

        return [("majors", maj_list)]

    def orphanCleanUp(self, doc):
        pass  # No Return Value Expected :D
