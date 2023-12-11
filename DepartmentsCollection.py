from typing import List, Tuple, Any
from CollectionBase import CollectionBase, AttrType
from CollManager import CollManager
from bson.objectid import ObjectId

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

    def orphanCleanUp(self, doc) -> bool:

        # students_coll = CollManager.GetCollection("students")
        
        course_coll = CollManager.GetCollection("courses")
        courses_cnt = course_coll.count_documents({"department": ObjectID(doc["_id"])})
        
        if courses.cnt > 0:
            print(f"{courses_cnt} courses belonging to this department must be deleted first.")
            return False
        
        for major in doc["majors"]:
            if(students_coll.count_documents({"majors.name": {"$in":[major["name"]]}}) > 0):  # I'm VERY iffy about this
                print("There are majors that belong to this department.")
                print("Delete these majors? The deleted Majors will also be removed")
                print("from any students who have declared those Majors [y/n]")
                user_inp = input("> ")
                while user_inp != 'y' and user_inp != 'n':
                    print("\nPlease Only Enter Either 'y' or 'n'")
                    user_inp = input("> ")
                print("")

                # Break Loop if User Doesn't Want to Try Again
                if user_inp == 'n':
                    return False
                """
                else:
                    for major in doc["majors"]:
                        students_coll.update_many({"majors": {"$pull":[major["name"]]}})
                """
        return True
    
    def addMajor(self):
        print("Select a department to add the major to.\n")
        doc = self.selectDoc()
        
        new_maj = {}

        while(True):
            while(True):
                new_maj_name = input("Enter a name for the major --> ")
                major_count = self.collection.count_documents({"majors.name": {"$in":[new_maj_name]}})
                if(major_count > 0):
                    print("\nA major with that name already exists. Try again.\n")
                else:
                    new_maj_desc = input("Enter a description for the major --> ")
                    break
            
            try:
                new_maj['name'] = new_maj_name
                new_maj['description'] = new_maj_desc
                doc_id = ObjectId(doc["_id"])
                self.collection.update_one({"_id": doc_id}, {'$push': {'majors': new_maj}})
                print(f"\n{new_maj_name} added to {doc['name']}")
                return

            except Exception as e:
                print(f"\nError in {self.collName}: {str(e)}") # Print Error
                new_maj = {}

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

                else:
                    continue

    def deleteMajor(self):
        
        # students_coll = CollManager.GetCollection("students")

        major_to_del = input("Name of the major to delete --> ")
        
        if self.collection.count_documents({"majors.name": {"$in":[major_to_del]}}) == 0:
            print("No majors with that name.")
            return
        """
        num_declared = students_coll.count_documents({"majors.name": {"$in":[major_to_del]}}) # this feels fake

        if(num_declared > 0):
            print(f"There are {num_declared} students who have declared that major.")
            print("Remove those major declarations before proceeding.")
        
        # else:
        """
        self.collection.update_one({}, {"$pull": {"majors": {"name": {"$in":[major_to_del]}}}})
        print(f"{major_to_del} deleted.")

    def listMajors(self):
        all_depts = self.collection.find({})
        for dept in all_depts:
            print(dept["name"])
            print()
            for major in dept["majors"]:
                print(major["name"])
                print(major["description"])
                print()