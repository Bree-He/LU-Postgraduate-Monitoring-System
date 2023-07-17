# comp639-2023-s1-project2-group16

## Project Details
Project name:	LU Postgraduate Monitoring System

Issue date:	24th April

Group 16:

        Na Bian 

        Yu-Tzu Chang  

        Bree He 

        Yao Su

        Frank Niu 

## Purpose of the Project
The LU Postgraduate Monitoring System project aims to automate the monitoring process for over 100 postgraduate students in the PhD program at the Faculty of Environment, Society, and Design. The current manual system is inefficient and lacks visibility.
The project will develop a web application that allows students, supervisors, convenors, administrators, and the PG Chair to access and manage information. Students can fill out 6-month reports, supervisors can review and complete sections, convenors can update student status, and administrators can track progress and generate reports. The system aims to improve efficiency, provide timely reminders, and facilitate early intervention for struggling students.

## User Stories

Here is a list of all the user stories planned at the beginning of the project and the whether they have been completed. 
### 1. User log in, Priority: 1, Estimated hours: 25 - Completed
As a User
I want to be able to log in to the web application system
So that I can access the system

Acceptance Criteria:

- The login page should be easily accessible from the main page of the web application system.
- The login page should have fields for the user's username and password.
- The system should verify the user's username and password and allow access to the system if the information provided is correct.
- The system should display a dashboard that provides easy navigation to all the features and resources available to the login role in the system.

Additional Criteria:

- The system should provide clear error messages if the user enters incorrect login credentials or if there are other issues with the login process.

### 2. Student register, Priority: 1, Estimated hours: 26 - Completed
As a PG student
I want to register on the web application system
So that I can access the system

Acceptance Criteria:

- The registration page should be easily accessible from the main page of the web application system.
- The registration form should include fields for the user's name, student id, email address, password, and program(DEM/DTSS/SOLA) of study.
- Upon submitting the registration form, the system should check if the information provided is filled with the required format and create a unique account for the user.
- The system will send the new user register request to the PG administrator for approval.

### 3. Student view personal info, Priority: 1, Estimated hours: 2 - Completed
As a PG student
I want to view personal information
So that I can check if my personal information is correct

Acceptance Criteria:

- The personal information page must be accessible only after successful authentication.
- The personal information page should be easily accessible from the PG student main page of the web application system.
- The personal information page should include fields for the user's (name, student id, enrolment date, address, phone, email, part-time/full-time, thesis title, supervisors, scholarship (if any), employment details).
- The page must be easy to understand and navigate so that students can easily review their personal information.

### 4. Student edit personal info, Priority: 1, Estimated hours: 25 - Completed
As a PG student
I want to edit my personal information
So that my personal information can be kept updated

Acceptance Criteria:

- The personal information page should be easily accessible from the PG student main page of the web application system.
- The system should only allow the user to edit some of the personal information fields (address, phone, part-time/full-time, thesis title, employment details) and save the changes if they are valid.
- If the student attempts to save information with an invalid format or missing required fields, an appropriate error message should be displayed and the student should be prompted to correct the errors.
- The system should display a confirmation message to the user after any changes are saved.

### 5. Supervisor view personal info, Priority: 1, Estimated hours: 18 - Completed
 As a PG student supervisor,
I want to be able to view my personal information,
so that I can ensure it is up to date.

Acceptance Criteria:

- I can access my personal information through the system.
- I can view all fields related to my personal information, such as name, email, department, faculty, contact number, and any other relevant information.

### 6. Supervisor update personal info, Priority: 1, Estimated hours: 25 - Completed
As a PG student supervisor,
I want to be able to update my personal information,
so that I can keep it up to date.

Acceptance Criteria:

- I can access my personal information through the system.
- I can edit any field related to my personal information, such as contact number, or any other relevant information.
- Department, faculty, email, and name cannot be changed.
- Once I submit the updated information, it should be reflected in the system.

### 7. Supervisor view supervisee info, Priority: 1, Estimated hours: 18 - Completed
As a PG student supervisor,
I want to be able to view my supervisees' information,
so that I can keep track of their progress.

Acceptance Criteria:

- I can access a list of my supervisees through the system.
- I can view all fields related to my supervisees' information, such as name, email, department, faculty, contact number, and any other relevant information.

### 8. Admin view students/supervisors, Priority: 1, Estimated hours: 20 - Completed
As a PG administrator,
I want to be able to view the students’ and supervisors’ lists,
So that I can efficiently keep track of the postgraduate process.

Acceptance Criteria:

- Admin can view the lists of students and supervisors by searching id/name.
- The page must be easy to understand and navigate so that the administrator can easily review their personal information.

### 9. Admin activate student's account, Priority: 1, Estimated hours: 30 - Completed
As a PG administrator,
I want to have the right to activate the students' accounts,
So that I check if the student is enrolled and give them the authorization to log into the system.

Acceptance Criteria:

- The PG administrator should have the ability to activate or deactivate a student's account by selecting the appropriate option on the student's account page.
- The PG administrator should only be able to activate or deactivate accounts for students who are currently enrolled in the program.
- The system should provide appropriate feedback to the PG administrator after they have activated or deactivated a student's account, such as a confirmation message or an error message if there was an issue with the activation or deactivation process.

### 10. Chair view students, Priority: 1, Estimated hours: 25 - Completed
As a PG Chair,
I want to be able to view a list of all the PG students in the faculty,
so that I can have easy access to their information and monitor their performance status.

Acceptance Criteria:

- Upon logging in, the PG Chair can access a dashboard that displays a list of all the PG students in the faculty.
- The list includes the following information for each PG student: name, student id, enrolment date, address, phone, email, part-time/full-time, thesis title, supervisors, scholarship (if any), employment details, and status (green, orange, red, or two orange ).
- The PG Chair can click on a student's name to view their detailed information, including their 6-month progress reports and any concerns they have raised in Section F.
- The PG Chair can search and filter the list by various criteria, such as department, name, ID, student status (green, orange, red, or two orange), report status (submitted vs overdue), and if Section F is completed.

### 11. Chair view supervisors, Priority: 1, Estimated hours: 30 - Completed
As a PG Chair,
I want to be able to view a list of all the student supervisors in the faculty,
so that I can have easy access to their information.

Acceptance Criteria:

- Upon logging in, the PG Chair can access a dashboard that displays a list of all the PG student supervisors in the faculty.
- The list includes the following information for each supervisor: name, email, department, faculty, email, and contact number.
- The PG Chair can search and filter the list by various criteria, such as department, and name.

### 12. Student view pervious 6MR report, Priority: 2, Estimated hours: 20 - Completed
As a PG student
I want to view previous 6MR reports
So that I can know if my progress is on track

Acceptance Criteria:

- The 6MR report should be easily accessible from the main page of the web application system.
- The 6MR report is only available when the reviews are done.
- The system should provide a list of all previous 6MR reports submitted by the user, sorted by date DESC.
- The system should allow the user to view the contents of each 6MR report.
- The system should provide the convenor's review status (Green/Orange/Two Orange/Red).

Additional Criteria:

- The system should allow the user to download and print their previous 6MR reports for their own records.

### 13. Supervisor search supervisee, Priority: 2, Estimated hours: 28 - Completed
As a PG student supervisor,
I want to be able to search for my supervisees,
so that I can quickly find and access their information.

Acceptance Criteria:

- The search function allows me to enter either the student's name or ID.
- The search results display all relevant students that match the search criteria.
- Clicking on a search result of the student’s name takes me to the student's profile page which shows the scholarship and employment information.
- The search function allows me to enter either the student's name or ID or department

### 14. Supervisor view 6MR report, Priority: 2, Estimated hours: 30 - Completed
As a PG student supervisor,
I want to be able to view the 6MR form,
so that I can provide feedback to my supervisees.

Acceptance Criteria:

- I can access the 6MR form through the system.
- I can view all sections except section F of the form.

### 15. Supervisor complete section E, Priority: 2, Estimated hours: 25 - Completed
As a PG student supervisor,
I want to be able to complete section E of the 6MR form,
so that I can provide feedback to my supervisees.

Acceptance Criteria:

- I can access the 6MR form through the system.
- I can complete section E of the form for each of my supervisees.
- Once I submit the completed form, it should be saved in the system and accessible to my supervisees.
- Once I submit the completed form, the PG convenor will receive the notice of completion.

### 16. Supervisor can reject the 6MR report, Priority: 2, Estimated hours: 30 - Completed
As a PG student supervisor,
I want to be able to reject a supervisee's 6MR report,
so that I can ensure that only accurate and complete reports are passed on to the next supervisor or convenor.

Acceptance Criteria:

- The PG student's main supervisor can either approve or reject the report.
- When a report is rejected, the supervisor must provide a reason for rejection.

Additional Criteria: 

- Students can receive the email for rejection reasons.

### 17. Admin manage students/supervisors, Priority: 2, Estimated hours: 25 - Completed
As a PG administrator,
I want to be able to manage the students’ and supervisors’ lists,
So that I can ensure that all necessary parties are registered in the system and are up to date.

Acceptance Criteria:

- Admin can add, edit, or delete student and supervisor information as needed.
- The system automatically sends an email to both the student and supervisor when a new student is added or when their information is updated.

### 18. Convenor view 6MR form, Priority: 2, Estimated hours: 15 - Completed
As a PG Convenor
I want to be able to view the 6MR form
So that I can check the student’s status

Acceptance Criteria:

- The system allows convenor to access the 6MR form for each student in their department
- The 6MR form should display in a clear way for viewing

### 19. Convenor view supervisor's profile, Priority: 2, Estimated hours: 15 - Completed
As a PG Convenor
I want to be able to view supervisors’ profiles
So that I can manage supervisors

Acceptance Criteria:

- The system allows convenor to view a list of supervisors in their department
- The supervisor can be searched by ID or name from the list.
- For each supervisor, the convenor can view their name, supervisor ID, and progress status.

### 20. Convenor view student's profile, Priority: 2, Estimated hours: 15 - Completed
As a PG Convenor
I want to be able to view student profiles
So that I can manage students

Acceptance Criteria:

- The system allows the convenor to view a list of students in their department
- The student can be searched by ID or name from the list.
- For each student, the convenor can view their name, student ID, and progress status.

### 21. Convenor edit 6MR form, Priority: 2, Estimated hours: 30 - Completed
As a PG Convenor
I want to be able to edit the 6MR form
So that I can complete 6MR and update the student’s status

Acceptance Criteria:

- The system allows the convenor to leave comments on the specific area
- The system allows the convenor to choose one of the colours (green/orange/ two orange/red) for each student
- The system will notify the PG administrator after the form completing

### 22. Chair view 6MR report, Priority: 2, Estimated hours: 25 - Completed
As a PG Chair,
I want to be able to view the 6-month report (6MR),
so that I can monitor their performance and identify any concerns or issues raised by the student.

Acceptance Criteria:

- The PG Chair can view the student's previous 6MR reports, including any comments or ratings provided by the supervisor and department Convenor.
- The PG Chair can view the student's current 6MR form, including the sections filled out by the student, supervisor, and department Convenor.
- The PG Chair can view the status of each report, including whether it has been completed, is overdue, and has been marked as Green, Orange, or Red by the PG Convenor.
- The PG Chair can view a summary of all the students' statuses and an analysis of the faculty's performance based on the 6MR reports.

### 23. Chair complete 6MR and update student status, Priority: 2, Estimated hours: 30 - Completed
As a PG Chair,
I want to be able to complete 6MR and update student status (if the Convenor is a supervisor),
so that the report can highlight any areas that might need closer consideration and indicate the status of their performance.

Acceptance Criteria:

- The PG Chair can access the list of students whose convenor is a supervisor, and view their 6MR reports that require him to complete the 6MR and update the student status.
- The PG Chair can complete the 6MR and update the student’s status (Green, Orange, or Red) based on the student's performance.
- The PG Chair should be able to leave comments or feedback for the student, supervisor or convenor.
- After completing the 6MR and updating the student status, the report status and student status get updated in the system.

### 24. Chair view section F submissions, Priority: 3, Estimated hours: 30 - Completed
As a PG Chair,
I want to be able to view Section F submissions,
So that take appropriate actions to address any issues or concerns raised by the student promptly and effectively.

Acceptance Criteria:

- The web application system should have a section that displays all the Section F forms submitted by the students.
- The PG Chair can access the section and view the Section F form, as well as the student information and 6MR reports.
- The PG Chair can decide what action to take and leave comments to address the unsatisfactory comments made by the student.

### 25. Admin sends automatic reminder to student/supervisor, Priority: 3, Estimated hours: 40 - Completed
As a PG administrator,
I want to send automated reminders to students and supervisors to complete the 6MR form before the due date.
So that I can ensure that all students and supervisors are aware of the upcoming deadline and encourage them to submit their forms on time.

Acceptance Criteria:

- The system should send automated reminders to all students and supervisors who have not completed the 6MR form by the due date. The reminders should be sent 1 week before the due date, and then again on the day of the due date.
- The reminders should be sent via email and include a link to the form.
- The PG administrator should be able to customize the email message that is sent with the reminders.
- The system should keep a record of all the reminders that have been sent to each student and supervisor.
- The system should notify the PG administrator when all students and supervisors have completed the form or if there are any outstanding forms.

### 26. Admin confirm report completed, Priority: 3, Estimated hours: 20 - Completed
As a PG administrator,
I want to be able to confirm that a student's 6-month progress report form has been completed,
So that I can ensure that all students have submitted their forms and follow up with those who haven't.

Acceptance Criteria:

- The system should allow the PG administrator to view the status of all the 6MR forms for each student, including the status of the student, supervisor, or convenor.
- The PG administrator should be able to search by id/name for a specific student's form and view its status.
- The PG administrator should be able to filter the list of students by department, supervisor, or status of the 6MR form (i.e., Green, Orange, or Red).
- The system should notify the PG administrator when a student submits a form and when a supervisor completes the rating of the form.

### 27. Admin check overdue reports, Priority: 3, Estimated hours: 25 - Completed
As a PG administrator,
I want to check for overdue reports,
So that I can know all the overdue reports and take further action.

Acceptance Criteria:

- The system should display a list of all the 6MR forms that are overdue.
- The list should include the student name, supervisor name, due date, and current status of the form.
- The PG administrator should be able to filter the list by department, supervisor, and status.
Change:
- In the third criteria, the PG administrator should be able to filter the list by department, student name, and supervisor name.(as the status of the overdue report is always incomplete)

### 28. Admin report 6MR status, Priority: 3, Estimated hours: 30 - Completed
As a PG administrator,
I want to report the 6MR status for the faculty,
So that I can monitor the progress of the PG students.

Acceptance Criteria:

- The report should include the status of each student's 6MR (Green, Orange, or Red) and any comments or notes made by the Convenor or supervisors.
- The reports should be easily accessible to the PG administrator and the PG Chair of the faculty.
- The system should generate a summary report of all the students' 6MR status for the faculty.
- The PG administrator should have the ability to select a specific faculty member and view the corresponding 6-month report (6MR) status for each of their assigned PG students.

### 29. Admin report faculty's performance analysis, Priority: 3, Estimated hours: 30 - Completed
As a PG administrator,
I want to report on the faculty’s performance analysis,
So that I can identify areas of improvement for the faculty's postgraduate program.

Acceptance Criteria:

- The system should also generate an analysis of the faculty's performance based on the 6MRs submitted.
- The reports should be easily accessible to the PG administrator and the PG Chair of the faculty and only for them to view.
- The PG administrator should have the ability to select a specific faculty member and view their corresponding performance analysis report for the postgraduate program.

### 30. Admin identify student who have issues, Priority: 3, Estimated hours: 25 - Completed
As a PG administrator,
I want to identify students that have issues,
So that I take necessary actions to address their concerns and ensure that they are making progress toward completing their PhD program.

Acceptance Criteria:

- The system should send an automated notification to the department Convenor and the Faculty PG Chair if a student has received a Red status in their 6MR form.
- The PG administrator should be able to add notes to the student's record to keep track of any actions taken to address the issues.
- The system should allow the PG administrator to filter the list by department, supervisor, and status.
- The system should highlight any students who have received an Orange or Red status in their 6-month progress report form.

### 31. Student fill in 6mr, Priority 2, Estimated hours: 50
 As a PG student
I want to fill in 6mr, 
So that I can save my study progress

Acceptance Criteria:

- The 6MR form should be easily accessible from the main page of the web application system.
- The student must complete the 6MR form including (A)Student record, (B)Milestones, (C)Evaluation of faculty(or centre) performance, (D)Progress and Achievement, incl. the optional section (F)Student Assessment of Supervision, Technical and Administrative Support.
- The system should allow the user to submit the 6MR form after all the required fields are filled in.
- The system should provide a confirmation message to the user after the 6MR form is successfully submitted.
- The system should prompt the complete form to the main supervisor for review.

Additional Criteria:

- The system should provide a save function if the form is only partially filled and students can carry on when they want to edit it again.
- The system should provide reminders to the user when it is time to fill in the 6MR form or an unfinished form in save, such as login notifications with a popup window.

## Solution

### Data Model: ERD
![ Data Model: ERD](main/static/img/ERD1.png)

### GUI Design
### 1.	Introduction
The LU Postgraduate Monitoring System is a software application designed to streamline and enhance the monitoring process for postgraduate students at Lincoln University. This GUI design report aims to present a comprehensive overview of the graphical user interface (GUI) design for the LU Postgraduate Monitoring System. The GUI design for the LU Postgraduate Monitoring System consists of five distinct interfaces tailored to different user roles: admin staff, convenors, supervisors, students, and chairs. Each interface provides specific functionalities and features based on the needs and responsibilities of the respective user.

### 2.	User interface design
The GUI design for the LU Postgraduate Monitoring System consists of five distinct interfaces tailored to different user roles: admin staff, convenors, supervisors, students, and chairs. Each interface provides specific functionalities and features based on the needs and responsibilities of the respective user.

Admin Staff Interface:

The admin staff interface is designed to facilitate administrative tasks related to the monitoring system.
It includes features such as user management, program management, report generation, and system configuration.
The interface is intuitive and user-friendly, allowing admin staff to efficiently navigate and perform their duties.

Convenor Interface:

The convenor interface is created for convenors who oversee the academic programs and ensure their smooth operation.
It provides features such as report viewing, checking student and supervisor lists, filling up section E, and monitoring report progress.
The interface focuses on providing convenors with the necessary tools and information to effectively manage the program.

Supervisor Interface:

The supervisor interface caters to faculty members who supervise postgraduate students.
It offers features such as report sections to fill up, progress tracking, and check students’ information.
The interface emphasizes clear communication and efficient supervision of students' academic progress.

Student Interface:

The student interface is designed for postgraduate students to access their personal monitoring information.
It provides features such as 6mr sections’ submission, profile management and account registration.
The interface focuses on simplicity and accessibility, enabling students to easily interact with the system and stay updated on their progress.

Chair Interface:

The chair interface caters to the department chairs who oversee the postgraduate programs.
It offers features such as checking student and supervisor lists, report status, performance evaluation, and checking overdue.
The interface aims to provide chairs with a comprehensive view of the program's status and facilitate effective decision-making.

At the forefront of the application is the dashboard, serving as the initial landing page adorned with the Lincoln University logo prominently displayed at the top. The dashboard design is meticulously crafted to deliver an aesthetically pleasing and effortlessly navigable experience, enabling students to swiftly grasp the report system. The user interface incorporates a predominantly blue color scheme, with buttons and interactive elements thoughtfully adorned in shades of blue, fostering a cohesive and visually engaging design.

### 3.	Navigation and layout
The navigation and layout are carefully crafted to provide a clear and intuitive user experience. Key considerations are given to ensure easy access to different sections and functionalities, consistent placement of navigation elements, and a responsive design that adapts to various screen sizes and devices.

### 4.	Color scheme and graphics
For the GUI design of the LU Postgraduate Monitoring System, a blue gradient color scheme has been chosen. The use of a blue gradient color palette creates a visually appealing and professional interface. The gradient effect adds depth and dimension to the design, making it visually engaging for users.

The color blue is often associated with trust, reliability, and professionalism, which are important qualities for a monitoring system. Additionally, blue has a calming effect and is easy on the eyes, ensuring a comfortable user experience.

### 5.	Functionality and Features

User Roles and Authentication:

- User registration and login for students, department Convenors, PG administrator, and Faculty PG Chair.
- Role-based access control to ensure appropriate permissions and access levels for each user category.
Student Profile and Progress Tracking:
- Student profile creation and management, including personal information and program details.
- Progress tracking features, allowing students to update their forms, and evaluation of faculty performance in the 6-month report.
- Notifications and reminders for report submission deadlines.

Supervisor Evaluation and Feedback:

- Supervisor interface to evaluate and rate students' performance in the 6-month report.
- Ability for supervisors to provide feedback and suggestions for improvement.
- Automatic notification to supervisors for pending evaluations and submission deadlines.

Department Convenor Actions:

- Dashboard for department Convenors to monitor the progress of students in their respective departments.
- Ability to review and assess the 6-month reports, highlighting areas needing closer consideration.
- Status indication (Green, Orange, Red) to identify the overall performance of each student.

PG Administrator's Administrative Tasks:

- Administrative interface for the PG administrator to manage administrative aspects of the postgraduate program.
- Student registration and enrollment management.
- Sending reminders to students and supervisors for report submissions.
- Monitoring the status of the reporting process and identifying delays or missing reports.

Faculty PG Chair's Oversight:

- Dashboard for the Faculty PG Chair to oversee the entire postgraduate monitoring process.
- Access to student reports, summaries of student statuses, and faculty performance analysis.
- Addressing student concerns raised in Section F of the report, viewed only by the PG Chair.
- Ability to schedule immediate meetings between students and Convenors for red-flagged reports.

Reporting and Analytics:

- Generation of reports summarizing student statuses and faculty performance.
- Comparison of current and previous 6-month reports to monitor student progress over time.
- Data visualization and analytics to identify trends, areas for improvement, and actionable insights.

Notifications and Communication:

- Email notifications and reminders for report deadlines, evaluation tasks, and meeting scheduling.
- Announcement board for important updates, guidelines, and notifications.

System Administration and Security:

- System administration privileges for the PG administrator, allowing for user management and system configuration.
- Secure data storage and encryption to protect sensitive information.
- Regular backups and data integrity measures.

### 6.	User Experience
The user experience of the LU Postgraduate Monitoring System will prioritize clarity, ease of use, and efficient navigation, ensuring that students, convenors, supervisors, administrators, and chairs can seamlessly interact with the system to monitor and manage the postgraduate monitoring process effectively.

### 7.	Conclusion
The GUI design of the LU Postgraduate Monitoring System will prioritize clarity, ease of use, and efficient navigation. The interfaces for students, Convenors, the PG administrator, and the Faculty PG Chair will be tailored to their specific roles and responsibilities. The design will focus on providing a user-friendly and intuitive experience, ensuring that users can easily access and interact with the system to monitor and manage the postgraduate monitoring process effectively.

## 	PythonAnywhere URL and Login Details


- PythonAnywhere URL: [comp639grp16.pythonanywhere.com](https://comp639grp16.pythonanywhere.com)


- Login Username for Admin:	    yu-tzu.chang&#8203;@lincolnuni.ac.nz
- Login Username for Student:	    na.bian&#8203;@lincolnuni.ac.nz
- Login Username for Convenor:	    frank.niu&#8203;@lincolnuni.ac.nz
- Login Username for Chair:	    yao.su&#8203;@lincolnuni.ac.nz
- Login Username for Supervisor:	bree.he&#8203;@lincolnuni.ac.nz

- All Password:                   MyPass123
