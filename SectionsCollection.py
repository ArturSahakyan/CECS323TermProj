from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType


class SectionsCollection(CollectionBase):

    def initCollection(self):
        self.collName = "sections"

        self.schema = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["course", "section_number", "semester", "section_year", 
                            "building", "room", "schedule", "start_time", "instructor"],
                "additionalProperties": False,
                "properties": {
                    "_id": {},
                    "course": {
                        "bsonType": "ObjectID",
                        "description": "The course to which a section belongs"
                    },
                    "section_number": {
                        "bsonType": "number",
                        "minimum": 1,
                        "description": "Ordinal identifier for the section"
                    },
                    "semester": {
                        "enum": ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter'],
                        "description": "The period of time during the calendar year during which the section occurs"
                    },
                    "section_year": {
                        "bsonType": "number",
                        "minimum": 1636 # When Harvard, which claims to be the oldest U.S. college, was founded
                    },
                    "building": {
                        "enum": ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        "description": "Name of the structure in which this section will be conducted"
                    },
                    "room": {
                        "bsonType": "number",
                        "minimum": 1,
                        "maximum": 999,
                        "description": "Number identifiyng the room of the building in which the section will be conducted"
                    },
                    "schedule": {
                        "enum": ['MW', 'TuTh', 'MWF', 'F', 'S'],
                        "description": "A string describing the days of the week on which the section is conducted"
                    },
                    "start_time": {
                        "bsonType": "number",
                        "minimum": 800,
                        "maximum": 1930
                        # TO-DO: This is listed as a Time (Timestamp?) type in the documentation, but we don't actually want
                        # a Timestamp... we want a time of day. I think this is better represented as a military-time int
                    },
                    "instructor": {
                        "bsonType": "string",
                        "maxLength": 80
                    },
                    "students": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "ObjectID"
                        }
                    }
                }
            }
        }

        self.attributes = [("course", AttrType.FOREIGN), ("section_number", AttrType.INTEGER),
                            ("semester", AttrType.STRING), ("section_year", AttrType.INTEGER),
                            ("building", AttrType.STRING), ("room", AttrType.INTEGER),
                            ("schedule", AttrType.STRING), ("start_time", AttrType.INTEGER),
                            ("instructor", AttrType.STRING)]
        self.uniqueCombos = [[0,1,2,3],[2,3,4,5,6,7],[2,3,6,7,8]]  # Candidate Keys
        # TO-DO: semester, section_year, department_abbreviation, course_number, student_id
        # should also be a uniqueness constraint, but as of the time of writing this, we do
        # not have a way to access Department or Student. I don't know that it necessarily needs
        # to be enforced here... it seems like more of an Enrollment thing?

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        return []  # Return Empty Array Since a Return Value is Expected

    def orphanCleanUp(self, doc) -> bool:
        return True
