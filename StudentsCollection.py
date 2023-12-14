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
                            "bsonType": "object",
                            "required": ["section_id", "enrollment"],
                            "properties": {
                                "section_id": {
                                    "bsonType": "objectId",
                                    "description": "Section ID"
                                },

                                "enrollment": {
                                    "oneOf": [
                                        {
                                            "bsonType": "object",
                                            "required": ["type", "min_satisfactory"],
                                            "properties": {
                                                "type": {
                                                    "enum": ["LetterGrade"],
                                                    "description": "LetterGrade type"
                                                },
                                                "min_satisfactory": {
                                                    "enum": ["A", "B", "C"],
                                                    "description": "Minimum satisfactory grade"
                                                }
                                            }
                                        },
                                        {
                                            "bsonType": "object",
                                            "required": ["type", "application_date"],
                                            "properties": {
                                                "type": {
                                                    "enum": ["PassFail"],
                                                    "description": "PassFail type"
                                                },
                                                "application_date": {
                                                    "bsonType": "date",
                                                    "description": "The date on which the student applies to a section as PassFail"
                                                }
                                            }

                                        }
                                    ]
                                }
                            }
                        }
                    }
                    }
                }
            }

        self.attributes = [("last_name", AttrType.STRING), ("first_name", AttrType.STRING),
                           ("email", AttrType.STRING), ("majors", AttrType.FOREIGN_ARR),
                           ("sections", AttrType.FOREIGN_ARR)]
        self.uniqueCombos = [[0, 1], [2]]  # Candidate Keys

    def uniqueAttrAdds(self) -> List[Tuple[str, Any]]:
        return [("majors", []), ("sections", [])]

    def orphanCleanUp(self, doc) -> bool:
        return True

    def onValidInsert(self, doc_id):
        pass

    """ ************ StudentMajor Functionality ***************** """
    def addMajor(self):
        print("Select a Student to Add a Major to!")
        student = self.selectDoc()

        # Get List of Valid Majors
        all_depts = CollManager.GetCollection("departments").collection.find({})
        valid_majors = []
        for dept in all_depts:
            for major in dept['majors']:
                valid_majors.append(major['name'])

        majors = []
        seen = set()

        while True:
            print("Please Select a Major")
            maj_name = input("Name --> ")
            while maj_name not in valid_majors:
                print("Sorry! That's not a valid major!\nTry Again\n\n")
                maj_name = input("Name --> ")

            if maj_name in seen:
                print("Sorry, you've added this before!\nTry Again\n\n")
                continue

            dec_date = None
            while True:
                try:
                    dec_year = int(input("Declaration year --> "))
                    dec_month = int(input("Declaration month (digit) --> "))
                    dec_day = int(input("Declaration day (digit) --> "))
                    print()
                    dec_date = datetime(dec_year, dec_month, dec_day)
                    break
                except:
                    print("Invalid entry. Try again.\n")

            seen.add(maj_name)

            try:
                self.collection.update_one({"_id": student["_id"]}, {'$push': {'majors': {"name": maj_name, "declaration_date": dec_date}}})
                print("Success!!\n")
            except Exception as e:
                print(f"\nError in {self.collName}: {str(e)}")
                print("Failed to add StudentMajor\n")

            print("Add another major?[y/n]")
            y_n_input = input("> ")
            while y_n_input != 'y' and y_n_input != 'n':
                print("\nPlease only enter either 'y' or 'n'")
                y_n_input = input("> ")
            print("")

            if y_n_input == 'n':
                break

    def deleteMajor(self):
        print("Select a student to delete a major from")
        student = self.selectDoc()
        if student is None:
            return

        valid_maj = []
        print("Which major do you want to delete?")
        for majors in student["majors"]:
            valid_maj.append(majors["name"])
            print(majors["name"])

        maj_name = input("Major Name --> ")
        while maj_name not in valid_maj:
            print("That's not a valid major!\nTry Again\n\n")
            maj_name = input("Major Name --> ")

        try:
            self.collection.update_one({}, {"$pull": {"majors": {"name": {"$in": [maj_name]}}}})
        except Exception as e:
            print(f"\nError in {self.collName}: {str(e)}")
            print("Failed to remove major from student")

    """ ****************** Enrollment Functionality ************************* """
    def addEnrollment(self):
        while (True):
            # Get Student
            print("Which Student Do You Want To Enroll?")
            student = self.selectDoc()
            print("")

            # Get Section
            print("Which Section Do You Want To Enroll in?\n")
            section = CollManager.GetCollection("sections").selectDoc()
            if section is None:
                print("Aborting Enrollment..")
                return

            # Do we have a section with the same Course, Semester, Year
            course_id = section["course"]
            semester = section["semester"]
            year = section["section_year"]
            for sect_obj in student["sections"]:
                sect = CollManager.GetCollection("sections").collection.find_one({"_id": sect_obj["section_id"]})
                if course_id == sect["course"] and semester == sect["semester"] and year == sect["section_year"]:
                    print("Sorry you can't enroll in multiple sections of the same course during the same semester!")
                    return

            enrollment = None
            prop_name = ""
            prop_type = ""
            print("\nEnroll with PassFail or LetterGrade?\n\t1. PassFail\n\t2. LetterGrade")
            user_inp = input("> ")
            while user_inp != "1" and user_inp != "2":
                user_inp = input("Try Again. > ")
            if user_inp == "1":
                # Is PassFail
                prop_type = "LetterGrade"
                prop_name = "min_satisfactory"
                while True:
                    try:
                        app_year = int(input("Application year --> "))
                        app_month = int(input("Application month (digit) --> "))
                        app_day = int(input("Application day (digit) --> "))
                        print()
                        enrollment = datetime(app_year, app_month, app_day)
                        break
                    except:
                        print("Invalid entry. Try again.\n")
            else:
                prop_type = "PassFail"
                prop_name = "application_date"
                valid_letters = ['A', 'B', 'C']
                print("Please Select A Minimum Satisfactory Grade From: ", valid_letters)
                user_inp = input("> ")
                while user_inp not in valid_letters:
                    print("\nPlease Input a Valid Grade")
                    user_inp = input("> ")
                enrollment = user_inp

            try:
                self.collection.update_one({"_id": student["_id"]}, {'$push': {'sections': {"section_id":section["_id"], "enrollment": {"type": prop_type, prop_name:enrollment}}}})
                success = CollManager.GetCollection("sections").f_appendStudent(section["_id"], student["_id"])
                if not success:
                    raise Exception
            except Exception as e:
                print(f"\nError in {self.collName}: {str(e)}")
                print("Failed to enroll in section\n")

            print("Add another Enrollment? [y/n]")
            y_n_input = input("> ")
            while y_n_input != 'y' and y_n_input != 'n':
                print("\nPlease only enter either 'y' or 'n'")
                y_n_input = input("> ")
            print("")

            if y_n_input == 'n':
                break

    def deleteEnrollment(self):
        while (True):
            # Get Student
            print("Which Student Do You Want To Un-Enroll?")
            student = self.selectDoc()
            print("")

            # Get Section
            print("Which Section Do You Want To Un-Enroll from?\n")
            section = CollManager.GetCollection("sections").selectDoc()
            if section is None:
                print("Aborting Enrollment..")
                return

            try:
                self.collection.update_one({"_id": student["_id"]}, {"$pull": {"sections": {"section_id":section["_id"]}}})
                success = CollManager.GetCollection("sections").f_removeStudent(section["_id"], student["_id"])
                if not success:
                    raise Exception
            except Exception as e:
                print(f"\nError in {self.collName}: {str(e)}")
                print("Failed to un-enroll in section\n")

            print("Remove an enrollment?")
            y_n_input = input("> ")
            while y_n_input != 'y' and y_n_input != 'n':
                print("\nPlease only enter either 'y' or 'n'")
                y_n_input = input("> ")
            print("")

            if y_n_input == 'n':
                break