from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType


class CoursesCollection(CollectionBase):

    def initCollection(self):
        self.collName = "courses"

        self.schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["course_number", "course_name", "description", "units"],
                "additionalProperties": False,
                "properties": {
                    "_id": {},
                    "department": {
                        "bsonType": "ObjectID",
                        "description": "The department to which a course belongs"
                    },
                    "course_number": {
                        "bsonType": "number",
                        "minimum": 100,
                        "maximum": 699,
                        "description": "A numerical description identifying a course and its basic features"
                    },
                    "course_name": {
                        "bsonType": "string",
                        "maxLength": 40,
                        "description": "A title given to describe the course"
                    },
                    "description": {
                        "bsonType": "string",
                        "maxLength": 120,
                        "description": "A text string detailing the contents and other details of the course"
                    },
                    "units": {
                        "bsonType": "number",
                        "minimum": 0,
                        "maximum": 5,
                        "description": "A number describing the credit hours required for and fulfilled by the course"
                    }
                }
            }
        }

        self.attributes = [("department", AttrType.FOREIGN), ("course_number", AttrType.INTEGER),
                            ("course_name", AttrType.STRING), ("description", AttrType.STRING),
                            ("units", AttrType.INTEGER)]
        self.uniqueCombos = [[0,1],[0,2]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        # TO-DO: Handle population of department
        return []  # Return Empty Array Since a Return Value is Expected

    def orphanCleanUp(self, doc):
        # TO-DO: Handle cleanup of Sections to which this course belongs
        pass  # No Return Value Expected :D
