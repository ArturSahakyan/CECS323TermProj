# CECS323TermProj
MongoDB Term Project for Fall 2023 CECS323

Final project for the 2023 Fall Semester of CECS323.
This group was tasked with creating an application using PyMongo that would simulate a database where students can enroll in classes!

How branches are setup:
  -  *main* (*main* release of project, rarely touch pls)
  -  *develop* (Working versions of the project, no bugs/errors)
  -  Feature "{topic}_feat" (Each team member branches off *develop* to work on a specific feature, merge into *develop* after completion)

CREATING A FEATURE:
  1) git checkout develop
  2) git checkout -b {insert_topic_here}_feat
  3) ...do your work, commit to this branch...
  4) Work is finished, feature complete
  5) git checkout develop
  6) Create Pull Request for merging into *develop* branch
  7) Another team member reviews the PR and if it looks good accepts the PR
  8) Your feature is merged!
  9) git branch -d {insert_topic_here}_feat (Delete old feature branch locally)
  10) git push origin --delete {insert_topic_here}_feat (Deletes old feature branch remotely)

INCOMPLETE FEATURES:
- Students orphanCleanUp
- Courses orphanCleanUp
- Sections uniqueAttrAdds
- Sections orphanCleanUp
- Department orphanDelete doesn't warn of deleting child Majors
- StudentMajors (declaration date, add, delete, list)
  - Really this is just adding Update and List functionality to Student
  - See Departments' Major methods
- Enrollments functionality (add, delete, list)
