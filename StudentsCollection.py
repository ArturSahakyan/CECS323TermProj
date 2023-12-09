from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType


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
                            "bsonType": "ObjectID"
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
        # TO-DO: Handle population of Majors array
        # TO-DO: Handle validation of Sections array
        return [] # This will have stuff in it afterwards lol

    def orphanCleanUp(self, doc):
        pass  # No Return Value Expected :D
