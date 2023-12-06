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
                        "maxLength": 80,
                        "description": "Name of the head of the department"
                    },
                    "description": {
                        "bsonType": "string",
                        "minLength": 10,
                        "maxLength": 80,
                        "description": "Short to medium length text describing the department"
                    }
                }
            }
        }

        self.attributes = [("building", AttrType.STRING), ("office", AttrType.INTEGER), ("name", AttrType.STRING),
                           ("abbreviation", AttrType.STRING), ("chair_name", AttrType.STRING),
                           ("description", AttrType.STRING)]
        self.uniqueCombos = [[2], [3], [4], [0, 1]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        return []  # Return Empty Array Since a Return Value is Expected

    def orphanCleanUp(self, doc):
        pass  # No Return Value Expected :D
