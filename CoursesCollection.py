from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType
from CollManager import CollManager


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
                        "bsonType": "objectId",
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

        self.attributes = [("department", AttrType.FOREIGN_DEPT), ("course_number", AttrType.INTEGER),
                           ("course_name", AttrType.STRING), ("description", AttrType.STRING),
                           ("units", AttrType.INTEGER)]
        self.uniqueCombos = [[0, 1], [0, 2]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        return []

    def orphanCleanUp(self, doc) -> bool:
        # Clean Up From Departments
        CollManager.GetCollection("departments").f_removeCourse(doc["department"], doc["_id"])

        # TO-DO: Handle cleanup of Sections to which this course belongs
        return True

    def onValidInsert(self, doc_id):
        dept_id = self.collection.find_one({"_id": doc_id})["department"]

        success = CollManager.GetCollection("departments").f_appendCourse(dept_id, doc_id)
        if not success:
            self.collection.delete_one({"_id": doc_id})
