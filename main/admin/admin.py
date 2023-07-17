from flask import (redirect, render_template, request, session, url_for, flash)
from main.admin import admin_bp
from main.config import sendMail
from main.common import getCursor
from datetime import datetime, date
import json

@admin_bp.route("/")
def index():
    username = session.get('username')
    return render_template("admin.html", username=username)

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@admin_bp.route("/studentlist", methods=["GET", "POST"])
def viewStudentList():
    query = """
                SELECT S.student_id, S.fname, S.lname, S.phone, S.email_lu, S.part_full_time, D.dept_name 
                FROM student S
                LEFT JOIN department D ON S.dept_code = D.dept_code
                """
    
    if request.method != "GET":
        student_id = request.form.get('studentID')
        student_name = request.form.get('studentName')
        department_code = request.form.get('departmentCode')
        conditions = []

        if student_id is not None and student_id.isdigit():
            conditions.append(f"S.student_id = {student_id}")

        if student_name is not None and len(student_name.strip()) > 0:
            conditions.append(f"(S.fname LIKE '%{student_name}%' OR S.lname LIKE '%{student_name}%')")

        if department_code is not None and len(department_code.strip()) > 0:
            conditions.append(f"S.dept_code LIKE '%{department_code}%'")

        if conditions:
            query += " WHERE " + " OR ".join(conditions)

    connection = getCursor()
    connection.execute(query)
    studentList = connection.fetchall()
    return render_template("viewStudentList.html", studentList=studentList)

## Delete student and all related information --- Frank ##
@admin_bp.route("/deleteStudent", methods=["POST"])
def deleteStudent():
    student_id = request.form.get('studentid')
    connection = getCursor()
    connection.execute("DELETE FROM supervision WHERE student_id = %s", (student_id,))
    connection.execute("DELETE FROM employment WHERE student_id = %s", (student_id,))
    connection.execute("DELETE FROM scholarship WHERE student_id = %s", (student_id,))
    connection.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
    flash("Student deleted successfully", "success")
    return redirect(url_for('admin.viewStudentList'))

## Edit student information --- Frank ##
@admin_bp.route("/studentdetail/<int:student_id>", methods=["GET", "POST"])
def viewStudentDetail(student_id):
    if  request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        enrollment_date = request.form["enrollment_date"]
        current_address = request.form["current_address"]
        phone = request.form["phone"]
        email_lu = request.form["email_lu"]
        email_other = request.form["email_other"]
        part_full_time = request.form["part_full_time"]
        thesis_title = request.form["thesis_title"]

        update_query = f"""
            UPDATE student
            SET fname = '{fname}', lname = '{lname}', enrollment_date = '{enrollment_date}',
                current_address = '{current_address}', phone = '{phone}', email_lu = '{email_lu}',
                email_other = '{email_other}', part_full_time = '{part_full_time}',
                thesis_title = '{thesis_title}'
            WHERE student_id = {student_id}
        """

        connection = getCursor()
        connection.execute(update_query)

        return redirect(f"/admin/studentdetail/{student_id}")

    query_profile = f"""
        SELECT S.student_id, S.fname, S.lname, S.enrollment_date, S.current_address, S.phone, S.email_lu,
            S.email_other, S.part_full_time, D.dept_name , S.thesis_title
        FROM student S
        LEFT JOIN department D ON S.dept_code = D.dept_code
        WHERE S.student_id = {student_id}
    """

    query_scholarship = f"""
        SELECT student_id, scholarship_name, scholarship_value, scholarship_tenure, scholarship_start_date,
            scholarship_end_date
        FROM SCHOLARSHIP
        WHERE student_id = {student_id}
        ORDER BY scholarship_end_date DESC
    """

    query_employment = f"""
        SELECT student_id, company_name, employment_start_date, employment_end_date
        FROM EMPLOYMENT
        WHERE student_id = {student_id}
        ORDER BY employment_end_date DESC
    """

    query_supervisor = f"""
        SELECT CONCAT(S.fname, ' ', S.lname) AS Name, V.supv_type
        FROM supervision V
        LEFT JOIN staff S ON V.staff_id = S.staff_id
        WHERE V.student_id = {student_id}
    """

    connection = getCursor()

    connection.execute(query_profile)
    studentProfile = connection.fetchone()

    connection.execute(query_scholarship)
    studentScholarship = connection.fetchall()

    connection.execute(query_employment)
    studentEmployment = connection.fetchall()

    connection.execute(query_supervisor)
    studentSupervisor = connection.fetchall()

    return render_template(
        "viewStudentDetail.html",
        studentProfile=studentProfile,
        studentScholarship=studentScholarship,
        studentEmployment=studentEmployment,
        studentSupervisor=studentSupervisor,
    )

@admin_bp.route("/supervisorlist", methods=["GET", "POST"])
def viewSupervisorList():
    query = """
                SELECT S.staff_id, S.fname, S.lname, S.phone, S.email_lu, S.room, D.dept_name 
                FROM staff S
                LEFT JOIN department D ON S.dept_code = D.dept_code
                WHERE S.role = 'Supervisor'
                """
    
    if request.method != "GET":
        staff_id = request.form.get('staffID')
        staff_name = request.form.get('staffName')
        department_code = request.form.get('departmentCode')
        conditions = []

        if staff_id is not None and staff_id.isdigit():
            conditions.append(f"S.staff_id = {staff_id}")

        if staff_name is not None and len(staff_name.strip()) > 0:
            conditions.append(f"(S.fname LIKE '%{staff_name}%' OR S.lname LIKE '%{staff_name}%')")
        
        if department_code is not None and len(department_code.strip()) > 0:
            conditions.append(f"S.dept_code LIKE '%{department_code}%'")

        if conditions:
            query += " AND (" + " OR ".join(conditions) + ")"

    connection = getCursor()
    connection.execute(query)
    supervisorList = connection.fetchall()
    return render_template("viewSupervisorList.html", supervisorList=supervisorList)


## Delete student and all related information --- Frank ##
@admin_bp.route("/deleteSupervisor", methods=["POST"])
def deleteSupervisor():
    staff_id = request.form.get('staffID')
    connection = getCursor()
    connection.execute("DELETE FROM supervision WHERE staff_id = %s", (staff_id,))
    connection.execute("DELETE FROM staff WHERE staff_id = %s", (staff_id,))
    flash("Supervisor deleted successfully.", "success")
    return redirect(url_for('admin.viewSupervisorList'))

## Add new supervisors --- Frank ##
@admin_bp.route("/addSupervisor", methods=["GET", "POST"])
def addSupervisor():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        role = request.form.get('role')
        employment_start_date = request.form.get('employment_start_date')
        room = request.form.get('room')
        email_lu = request.form.get('email_lu')
        phone = request.form.get('phone')
        dept_code = request.form.get('dept_code')

        employment_start_date = datetime.strptime(employment_start_date, '%Y-%m-%d') if employment_start_date else datetime.now()

        # Handle other fields that can be None
        fname = fname or ''
        lname = lname or ''
        role = role or ''
        employment_start_date = employment_start_date or ''
        room = room or ''
        email_lu = email_lu or ''
        phone = phone or ''
        dept_code = dept_code or ''


        query = """
            INSERT INTO staff (fname, lname, role, employment_start_date, employment_end_date, room, email_lu, phone, dept_code)
            VALUES (%s, %s, %s, %s, NULL, %s, %s, %s, %s)
        """
        connection = getCursor()
        connection.execute(query, (fname, lname, role, employment_start_date, room, email_lu, phone, dept_code))
        flash("Supervisor added successfully.", "success")
        return redirect(url_for('admin.viewSupervisorList'))
    else:
        return render_template("addSupervisor.html")



## update supervisor details -- Frank ##
@admin_bp.route("/supervisordetail/<int:staff_id>", methods=["GET", "POST"])
def viewSupervisorDetail(staff_id):
    if request.method == "GET":
        connection = getCursor()
        query_supprofile = f"""
            SELECT * FROM staff WHERE staff_id = {staff_id}
        """
        connection.execute(query_supprofile)
        supervisorProfile = connection.fetchone()
        return render_template("viewSupervisorDetail.html", supervisorProfile=supervisorProfile, staff_id=staff_id )
    elif request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        role = request.form.get('role')
        employment_start_date = request.form.get('employment_start_date')
        room = request.form.get('room')
        email_lu = request.form.get('email_lu')
        phone = request.form.get('phone')
        dept_code = request.form.get('dept_code')

        employment_start_date = datetime.strptime(employment_start_date, '%Y-%m-%d') if employment_start_date else datetime.now()

        # Handle other fields that can be None
        fname = fname or ''
        lname = lname or ''
        role = role or ''
        employment_start_date = employment_start_date or ''
        room = room or ''
        email_lu = email_lu or ''
        phone = phone or ''
        dept_code = dept_code or ''

        update_query = f"""
            UPDATE staff
            SET fname = '{fname}', lname = '{lname}', role = '{role}',
                employment_start_date = '{employment_start_date}', phone = '{phone}', email_lu = '{email_lu}',
                room = '{room}', dept_code = '{dept_code}'
            WHERE staff_id = {staff_id}
        """

        connection = getCursor()
        connection.execute(update_query)

        # Re-query the updated supervisor profile
        query_supprofile = f"""
            SELECT * FROM staff WHERE staff_id = {staff_id}
        """
        connection.execute(query_supprofile)
        supervisorProfile = connection.fetchone()
        flash("Supervisor details updated successfully", "success")
        return render_template("viewSupervisorDetail.html", supervisorProfile =supervisorProfile, staff_id=staff_id)


@admin_bp.route("/activatestudentaccount", methods=["GET", "POST"])
def activateStudentAccount():
    connection = getCursor()

    if request.method != "GET":
        studentID = request.args.get('id')
        action = request.args.get('action')
        connection.execute(f'SELECT email_lu FROM student WHERE student_id = {studentID}')
        studentEmail = connection.fetchone()[0]

        if action == 'activate':
            query = f"""
                    UPDATE user 
                    SET admin_flag = '1' 
                    WHERE email_lu = (
                        SELECT email_lu 
                        FROM student 
                        WHERE student_id = {studentID}
                    ) 
                    AND role = 'Student'
                    """
            emailBody = "Your user account has been activated!"
        else:
            query = f"""
                    DELETE FROM user 
                    WHERE email_lu = (
                        SELECT email_lu 
                        FROM student 
                        WHERE student_id = {studentID}
                    ) 
                    AND role = 'Student';
                    """
            emailBody = "Your user account request has been declined!"

        connection.execute(query)
        emailTitle = 'Notification from Lincoln Admin'
        sendMail(emailTitle, studentEmail, emailBody)

    query = """
                SELECT student_id, fname, lname, enrollment_date, dept_code, user.email_lu
                FROM user 
                INNER JOIN student ON user.email_lu = student.email_lu
                WHERE role = 'Student' AND admin_flag = '0'
                """        

    connection.execute(query)
    inactiveStudents = connection.fetchall()
    return render_template("activateStudentAccount.html", inactiveStudents=inactiveStudents)

#### Na
@admin_bp.route("/reminder", methods=["GET", "POST"])
def reminder():
    connection = getCursor()
    # get email addresses!
    connection.execute("SELECT s.email_lu \
                    FROM student AS s \
                    JOIN report AS r ON s.student_id = r.student_id \
                    JOIN report_progress AS rp ON r.report_id = rp.report_id \
                    WHERE r.rept_term = %s AND r.rept_year = %s \
                    AND rp.full_report_completed = 0", ('JUNE', '2023',))
    emailAddress = connection.fetchall()
    connection.execute("SELECT content \
                    FROM email_msg\
                    WHERE email_id = %s ", ('e1',))
    email_msg=connection.fetchone()
    emailTitle = '6MR Report Reminder!'
    emailBody = request.form.get('body')
    if request.method == 'POST':
        for email in emailAddress:
            email = email[0]
            sendMail(emailTitle, email, emailBody)
        msg = "Emails sent successfully" 
        return render_template("admin.html", msg=msg)
    else:
        return render_template("reminder.html",email_msg=email_msg)

def undone_sid():
    connection = getCursor()
    connection.execute("SELECT DISTINCT e.staff_id \
                    FROM report AS r  \
                    JOIN report_progress AS rp ON r.report_id = rp.report_id \
                    JOIN section_e_spvrs as e on r.report_id=e.report_id\
                    WHERE r.rept_term = %s AND r.rept_year = %s \
                    AND student_abcd_completed = %s AND supervisor_approved=%s", ('JUNE', '2023','1','0',))
    staff_id = connection.fetchall()
    return staff_id

# Na 
@admin_bp.route("/send_supervisor", methods=["GET", "POST"])
def send_supervisor():
    connection = getCursor()
    # get undone staff id 
    staff_id= undone_sid()
    # get all the email 
    # Prepare a placeholder string with the same number of '%s' as the length of staff_id
    placeholders = ', '.join(['%s'] * len(staff_id))

    # Get all the emails for the staff_ids
    query = "SELECT email_lu FROM staff WHERE staff_id IN ({})".format(placeholders)

    # Execute the query with staff_id as the parameter values
    connection.execute(query, staff_id)
    staff_email = connection.fetchall()
    emailTitle = '6MR Report Reminder!'
    emailBody = request.form.get('body')
    for email in staff_email:
        email = email[0]
    sendMail(emailTitle, email, emailBody)
    msg = "Emails sent successfully" 
    return render_template("admin.html", msg=msg)

#  Na
@admin_bp.route("/super_check/<int:report_id>", methods=["GET", "POST"])
def super_check(report_id):
    # check who did not finish the form
    report_id=report_id
    connection = getCursor()
    connection.execute("SELECT r.student_id, CONCAT(s.fname, ' ', s.lname) AS name, rp.report_id, student_abcd_completed, student_f_completed, supervisors_completed, convenor_completed, full_report_completed \
                    FROM report_progress rp \
                    JOIN report r ON rp.report_id = r.report_id \
                    JOIN student s ON r.student_id = s.student_id \
                    WHERE r.rept_term = %s AND r.rept_year = %s and rp.report_id=%s", ('JUNE', '2023',report_id,))
    status=connection.fetchall()
    # get undone staff id
    # get student id
    connection.execute("SELECT student_id  \
                    From report \
                    WHERE rept_term = %s AND rept_year = %s and report_id=%s", ('JUNE', '2023',report_id,))
    student_id=connection.fetchone()

    connection.execute("SELECT n.staff_id \
                        FROM staff s left join supervision n on s.staff_id = n.staff_id \
                        WHERE n.student_id = %s",(student_id[0],))
    super_all=connection.fetchall()
    connection.execute("SELECT staff_id \
                        FROM section_e_spvrs \
                        WHERE student_id = %s and report_id=%s",(student_id[0],report_id,))
    super_done=connection.fetchall()
    #  `super_all` and `super_done` are lists of staff_id values

    # Convert the lists to sets
    super_all_set = set(super_all)
    super_done_set = set(super_done)

    # Calculate the difference between the sets
    difference_set = super_all_set - super_done_set

    # Convert the result back to a list
    difference_list = list(difference_set)
    # this list is not none!
    # Create an empty list to store the staff names
    staff_names = []

    # Iterate over the staff_id values in difference_list
    for staff_id in difference_list:
        connection.execute("SELECT concat(s.fname, ' ', s.lname) as main_name \
                        FROM staff s \
                        WHERE s.staff_id = %s", (staff_id[0],))
        staff_name = connection.fetchall()

    # Check if staff_name is not None and append the names to the list
        if staff_name is not None:
            for item in staff_name:
                name = item[0]  # Assuming main_name is in the first position of each tuple
                staff_names.append(name)
                # Convert the staff_names list into a single string separated by a comma
        # Convert the staff_names list into a single string separated by a comma
    staff_names_str = ', '.join(staff_names)
        
    return render_template("super_check.html",status=status, names=staff_names_str)

@admin_bp.route("/checkstatus", methods=["GET", "POST"])
def checkstatus():
    connection = getCursor()
    query = """SELECT r.student_id, CONCAT(s.fname, ' ', s.lname) AS name, rp.report_id, student_abcd_completed, student_f_completed, supervisors_completed, convenor_completed, full_report_completed \
                    FROM report_progress rp \
                    JOIN report r ON rp.report_id = r.report_id \
                    JOIN student s ON r.student_id = s.student_id  """
    
    if request.method != "GET":
        student_id = request.form.get('student_id')
        studentName = request.form.get('studentName')
        department = request.form.get('department')
        r_status = request.form.get('r_status')
        rept_term=request.form.get('rept_term')
        rept_year=request.form.get('rept_year')

        conditions = []
        if rept_term is not None:
            conditions.append(f"r.rept_term = '{rept_term}'")
        if rept_year  is not None:
            conditions.append(f"r.rept_year = '{rept_year}'")
        if student_id is not None and student_id.isdigit():
            conditions.append(f"s.student_id = {student_id}")
        if r_status is not None:
            if r_status == "incomplete":
                r_status = 0
            else:
                r_status = 1
            conditions.append(f"rp.full_report_completed = {r_status}")
        if studentName is not None and len(studentName.strip()) > 0:
            conditions.append(f"(s.fname LIKE '%{studentName}%' OR s.lname LIKE '%{studentName}%')")
        if department is not None:
            conditions.append(f"s.dept_code = '{department}'")
        if conditions:
            query += " WHERE (" + " AND ".join(conditions) + ") ORDER BY s.student_id"
            connection.execute(query)
            status = connection.fetchall()
        return render_template("checkstatus.html", status=status,student_id=student_id,r_status=r_status,studentName=studentName,department=department)
    else: 
        connection.execute("SELECT r.student_id, CONCAT(s.fname, ' ', s.lname) AS name, rp.report_id, student_abcd_completed, student_f_completed, supervisors_completed, convenor_completed, full_report_completed \
                FROM report_progress rp \
                JOIN report r ON rp.report_id = r.report_id \
                JOIN student s ON r.student_id = s.student_id \
                WHERE r.rept_term = %s AND r.rept_year = %s", ('JUNE', '2023',))
        status=connection.fetchall()
        return render_template("checkstatus.html", status=status)

@admin_bp.route("/ad_check/<int:report_id>")
def ad_check(report_id):
    connection = getCursor()
    # update fullreport to 1
    connection.execute("UPDATE report_progress set full_report_completed = %s where report_id=%s ;",('1',report_id,))
    connection.execute("SELECT r.student_id, CONCAT(s.fname, ' ', s.lname) AS name, rp.report_id, student_abcd_completed, student_f_completed, supervisors_completed, convenor_completed, full_report_completed \
                    FROM report_progress rp \
                    JOIN report r ON rp.report_id = r.report_id \
                    JOIN student s ON r.student_id = s.student_id \
                    WHERE r.rept_term = %s AND r.rept_year = %s", ('JUNE', '2023'))
    status=connection.fetchall()
    return render_template("checkstatus.html", status=status)

 
@admin_bp.route("/checkall")
def checkall():
    connection = getCursor()
    # get all the id then for
    connection.execute("SELECT rp.report_id \
                    FROM report_progress rp \
                    JOIN report r ON rp.report_id = r.report_id \
                    WHERE r.rept_term = %s AND r.rept_year = %s and rp.convenor_completed=%s and rp.full_report_completed=%s", ('JUNE', '2023','1','0',))
    report_ids=connection.fetchall()
    for report_id in report_ids:
        connection.execute("UPDATE report_progress set full_report_completed = %s where report_id=%s ;",('1',report_id[0],))
    
    connection.execute("SELECT r.student_id, CONCAT(s.fname, ' ', s.lname) AS name, rp.report_id, student_abcd_completed, student_f_completed, supervisors_completed, convenor_completed, full_report_completed \
                    FROM report_progress rp \
                    JOIN report r ON rp.report_id = r.report_id \
                    JOIN student s ON r.student_id = s.student_id \
                    WHERE r.rept_term = %s AND r.rept_year = %s", ('JUNE', '2023'))
    status=connection.fetchall()
    return render_template("checkstatus.html", status=status)



### 17#  admin add/update/delete students and supervisors

## Add new student and assign supervisor ##

@admin_bp.route("/studentlist/add/profile", methods=["GET", "POST"])
def addStudentProfile():
    if request.method == "POST":
        fname = request.form.get('fname') or ''
        lname = request.form.get('lname') or ''
        phone = request.form.get('phone') or ''
        enrollment_date = request.form.get('enrollment_date')
        current_address = request.form.get('current_address') or ''
        email_lu = request.form.get('email_lu') or ''
        email_other = request.form.get('email_other') or ''
        part_full_time = request.form.get('part_full_time') or ''
        dept_code = request.form.get('dept_code') or ''
        thesis_title = request.form.get('thesis_title') or ''

        enrollment_date = datetime.strptime(enrollment_date, '%Y-%m-%d') if enrollment_date else datetime.now()

        connection = getCursor()

        query1 = """
            INSERT INTO student (fname, lname, phone, enrollment_date, current_address, email_lu, email_other, part_full_time, dept_code, thesis_title)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        connection.execute(query1, (fname, lname, phone, enrollment_date, current_address, email_lu, email_other, part_full_time, dept_code, thesis_title))
        connection.execute("SELECT LAST_INSERT_ID()")
        student_id = connection.fetchone()[0]
        session['dept_code'] = dept_code
        flash("Student added in the system successfully, please select the student's supervisors.", "success")
        return redirect(url_for('admin.addStudentSupervisors', student_id=student_id))
    else:
        return render_template("addStudentProfile.html")




def addsupervisorsforStudent(student_id, dept_code):
    connection = getCursor()
    query5 = """
        SELECT CONCAT(staff.fname, ' ', staff.lname) staff_name
        FROM staff
        WHERE (staff.role = 'Supervisor' OR staff.role = 'Convenor')
        AND staff.dept_code = %s
        AND staff.staff_id NOT IN (
            SELECT staff_id
            FROM supervision
            WHERE student_id = %s
        )
        ORDER BY staff.staff_id ASC
    """
    connection.execute(query5, (dept_code, student_id))
    supervisor_names = connection.fetchall()
    return supervisor_names


  
@admin_bp.route("/studentlist/add/supervisors", methods=["GET", "POST"])
def addStudentSupervisors():
    if request.method == "POST":
        student_id = request.form.get('student_id')
        dept_code = session.get('dept_code')
        supervisor_names = addsupervisorsforStudent(student_id, dept_code)
        supervisor_name = request.form.get('supervisor_name')
        supv_type = request.form.get('supv_type')
        connection = getCursor()
        query4 = "SELECT staff_id FROM staff WHERE CONCAT(fname, ' ', lname) = %s"
        connection.execute(query4, (supervisor_name,))
        staff_id = connection.fetchone()[0]

        query3 = """
            INSERT INTO supervision (student_id, staff_id, supv_type)
            VALUES (%s, %s, %s)
        """
        connection.execute(query3, (student_id, staff_id, supv_type))

        query6 = """
            SELECT supv_type FROM supervision WHERE student_id = %s
        """
        connection.execute(query6, (student_id,))
        existing_supervisor_types = [row[0] for row in connection.fetchall()]

        flash("Supervisor added successfully, please continue adding remaining supervisors or click Back to finish adding student", "success")
        return redirect(url_for('admin.addStudentSupervisors', student_id=student_id, existing_supervisor_types=existing_supervisor_types, supervisor_names=supervisor_names))
       
    else:
        dept_code = session.get('dept_code')
        student_id = request.args.get('student_id')
        supervisor_names = addsupervisorsforStudent(student_id, dept_code)

        # Get the existing supervisor types for the student
        connection = getCursor()
        query6 = """
            SELECT supv_type FROM supervision WHERE student_id = %s
        """
        connection.execute(query6, (student_id,))
        existing_supervisor_types = [row[0] for row in connection.fetchall()]

        return render_template("addStudentSupervisors.html", supervisor_names=supervisor_names, student_id=student_id, dept_code=dept_code, existing_supervisor_types=existing_supervisor_types)





@admin_bp.route("/issues", methods=["GET", "POST"])
def issues():
    connection = getCursor()
    query = """SELECT
            s.student_id,
            CONCAT(s.fname, ' ', s.lname) AS Name,
            r.report_id,
            r.rept_year,
            r.rept_term,
            rp.full_report_completed,
            sec.student_status,
            (
                SELECT sec_prev.student_status
                FROM report r_prev
                LEFT JOIN section_e_convenor sec_prev ON r_prev.report_id = sec_prev.report_id
                WHERE r_prev.student_id = s.student_id
                    AND r_prev.rept_year < r.rept_year
                ORDER BY r_prev.rept_year DESC
                LIMIT 1
            ) AS previous_student_status,
            s.dept_code
            FROM student s
            LEFT JOIN report r ON s.student_id = r.student_id
            LEFT JOIN report_progress rp ON r.report_id = rp.report_id
            LEFT JOIN section_e_convenor sec ON r.report_id = sec.report_id"""

    if request.method == "POST":
        student_id = request.form.get('student_id')
        reportYear = request.form.get('reportYear')
        reportTerm = request.form.get('reportTerm')
        studentName = request.form.get('studentName')
        department = request.form.get('department')
        s_status = request.form.get('s_status')
        conditions = []

        if student_id is not None and student_id.isdigit():
            conditions.append(f"s.student_id = {student_id}")
            
        if reportYear is not None:
            conditions.append(f"r.rept_year = {reportYear}")
        
        if reportTerm is not None:
            conditions.append(f"r.rept_term = '{reportTerm}'")
        
        if studentName is not None and len(studentName.strip()) > 0:
            conditions.append(f"(s.fname LIKE '%{studentName}%' OR s.lname LIKE '%{studentName}%')")
        
        if department is not None:
            conditions.append(f"s.dept_code = '{department}'")
        if s_status is not None:
            conditions.append(f"sec.student_status = '{s_status}'")

        if conditions:
            query += " WHERE (" + " AND ".join(conditions) + ") ORDER BY s.student_id"
            connection.execute(query)
            result = connection.fetchall()
            if s_status == 'G':
                s_status='Green'
            elif s_status == 'O':
                s_status='Orange'
            elif s_status == 'R':
                s_status = 'Red'
            else:
                s_status=None
            return render_template("issues.html", result=result,s_status=s_status,student_id=student_id,reportYear=reportYear,reportTerm=reportTerm,studentName=studentName,department=department)
        else:
            query += " WHERE r.rept_year = '2023' ORDER BY s.student_id"
            connection.execute(query)
            result = connection.fetchall()
            return render_template("issues.html",result=result)
    
    else:
        # complete ones!!
        query += " WHERE r.rept_year = '2023' ORDER BY s.student_id"
        connection.execute(query)
        result = connection.fetchall()
        return render_template("issues.html",result=result)

@admin_bp.route("/notes/<int:report_id>", methods=["GET", "POST"])
def notes(report_id):
    report_id=report_id
    connection = getCursor()
    connection.execute("SELECT s.student_id, CONCAT(s.fname, ' ', s.lname) AS Name,\
            r.report_id,\
            r.rept_year,\
            r.rept_term,\
            rp.full_report_completed,\
            sec.student_status,\
            (\
                SELECT sec_prev.student_status\
                FROM report r_prev\
                LEFT JOIN section_e_convenor sec_prev ON r_prev.report_id = sec_prev.report_id\
                WHERE r_prev.student_id = s.student_id\
                    AND r_prev.rept_year < r.rept_year\
                ORDER BY r_prev.rept_year DESC\
                LIMIT 1\
            ) AS previous_student_status,\
            s.dept_code\
            FROM student s\
            LEFT JOIN report r ON s.student_id = r.student_id\
            LEFT JOIN report_progress rp ON r.report_id = rp.report_id\
            LEFT JOIN section_e_convenor sec ON r.report_id = sec.report_id WHERE r.rept_year = '2023'and r.report_id=%s",(report_id,))
    result = connection.fetchall()
    connection = getCursor()
    connection.execute("SELECT * \
                        FROM admin_note \
                        WHERE report_id = %s",(report_id,))
    notes=connection.fetchone()
    if request.method == "POST":
        note = request.form.get('note')
        today = date.today()
        if notes is None:
        # insert
        # date
            
            
            connection.execute("INSERT INTO admin_note (report_id,note, note_date) VALUES (%s,%s,%s)",(report_id,note,today,))
            connection.execute("SELECT * FROM admin_note where report_id=%s",(report_id,))
            notes=connection.fetchall()
            return render_template("issues.html",notes=notes,result=result)
        else:
            connection.execute("UPDATE admin_note set note=%s, note_date=%s where report_id=%s;",(note,today,report_id,))
            connection.execute("SELECT * FROM admin_note where report_id=%s",(report_id,))
            notes=connection.fetchall()
            return render_template("issues.html",notes=notes,result=result)


    else:
        return render_template("notes.html",notes=notes,result=result)


@admin_bp.route("/view6MR/<int:report_id>", methods=["GET", "POST"])
def view6MR(report_id):
    report_id=report_id
    connection = getCursor()
    
    # get supervisor
    connection.execute("SELECT student_id \
                        FROM report \
                        WHERE report_id = %s",(report_id,))
    student_id = connection.fetchone()
    
    # get all the super name
    super1, super2, super3= None, None, None
    connection.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                        FROM staff s left join supervision n on s.staff_id = n.staff_id \
                        WHERE n.student_id = %s AND n.supv_type = 'Main Supervisor'",(student_id[0],))
    super1=connection.fetchone()
    
    connection.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                        FROM staff s left join supervision n on s.staff_id = n.staff_id\
                        WHERE n.student_id = %s AND n.supv_type = 'Associate Supervisor'",(student_id[0],))
    super2=connection.fetchone()
    
    connection.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                        FROM staff s left join supervision n on s.staff_id = n.staff_id\
                        WHERE n.student_id = %s AND n.supv_type = 'Other Supervisor'",(student_id[0],))
    super3=connection.fetchall()
    
    # get basic profile which can not be edited
    connection.execute("SELECT * \
                        FROM student s \
                        WHERE s.student_id = %s",(student_id[0],))
    profile = connection.fetchall()
    
    # get scholalrship 
    connection.execute("SELECT * \
                            FROM scholarship \
                            WHERE student_id = %s",(profile[0][0],))
    scholarship= connection.fetchall()
    # get employment
    connection.execute("SELECT * \
                            FROM employment \
                            WHERE student_id = %s",(profile[0][0],))
    employment= connection.fetchall()
    # view b history
    connection.execute("SELECT * FROM section_b WHERE report_id = %s",(report_id,))
    section_b = connection.fetchall()

    # view c
    connection.execute("SELECT * FROM section_c WHERE report_id = %s",(report_id,))
    section_c = connection.fetchall()
    connection.execute("SELECT * FROM section_d WHERE report_id = %s",(report_id,))
    section_d = connection.fetchall()
    # # parse JSON string into Python objects
    t1 = json.loads(section_d[0][1])
    t2 = json.loads(section_d[0][3])
    t3 = json.loads(section_d[0][4])
    t4 = json.loads(section_d[0][5])
    t5 = json.loads(section_d[0][6])
    # convert Python objects into a list
    t1_list = list(t1)
    t2_list = list(t2)
    t3_list = list(t3)
    t4_list = list(t4)
    t5_list = list(t5)
    total_expenditure = 0
    for t5 in t5:
        total_expenditure += float(t5['amount'])
    total_expenditure = '{:.0f}'.format(total_expenditure) #formatted the amount without decimal
    connection.execute("SELECT * FROM section_e_spvrs WHERE report_id = %s",(report_id,))
    section_e = connection.fetchall()
    connection.execute("SELECT CONCAT(s.fname, ' ', s.lname) AS Name, e.date, e.comments, e.student_status FROM section_e_convenor e JOIN staff s ON s.staff_id = e.staff_id WHERE report_id = %s",(report_id,))
    section_e_convenor = connection.fetchall()
    return render_template("view6MR.html", profile=profile,super1=super1,super2=super2,super3=super3,scholarship=scholarship, employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e,section_e_convenor=section_e_convenor)
    
############## admin check overdue reports--Bree
@admin_bp.route("/overdueList", methods=["GET", "POST"])
def overdueList():
    connection = getCursor()    
    query = """SELECT
                R.report_id,
                R.student_id,
                CONCAT(S.fname, ' ', S.lname) AS student_name,
                S.dept_code,
                CONCAT(SU.fname, ' ', SU.lname) AS supervisor_name,
                SV.supv_type,
                R.due_date,
                CASE
                    WHEN RP.full_report_completed = 1 THEN 'Completed'
                    ELSE 'Pending'
                END AS current_status
                FROM
                (
                    SELECT
                    MAX(report_id) AS report_id,
                    student_id
                    FROM
                    report
                    WHERE
                    due_date < CURDATE()
                    GROUP BY
                    student_id
                ) AS MR
                INNER JOIN report R ON MR.report_id = R.report_id
                INNER JOIN student S ON R.student_id = S.student_id
                LEFT JOIN (
                    SELECT
                    report_id,
                    MAX(full_report_completed) AS full_report_completed
                    FROM
                    report_progress
                    GROUP BY
                    report_id
                ) RP ON R.report_id = RP.report_id
                INNER JOIN supervision SV ON R.student_id = SV.student_id
                INNER JOIN staff SU ON SV.staff_id = SU.staff_id
                WHERE R.due_date < CURDATE() AND (RP.full_report_completed = 0 OR RP.full_report_completed IS NULL) and SV.supv_type ='Main Supervisor'"""
    connection.execute(query)
    overduelist = connection.fetchall()
    if request.method != "GET":
        student_id = request.form.get('student_id')
        studentName = request.form.get('studentName')
        department = request.form.get('dept_code')
        staff_id = request.form.get('staff_id')
        supervisorName = request.form.get('supervisorName')
        conditions = []
        if studentName:
            query += " AND (s.fname LIKE %s OR s.lname LIKE %s)"
            conditions.append(f"%{studentName}%")
            conditions.append(f"%{studentName}%")
        if department:
            query += " AND s.dept_code LIKE %s"
            conditions.append(f"%{department}%")
        if supervisorName:
            query += " AND (su.fname LIKE %s OR su.lname LIKE %s)"
            conditions.append(f"%{supervisorName}%")
            conditions.append(f"%{supervisorName}%")
        # Execute the query with the parameters
        connection.execute(query, tuple(conditions))
        overduelist = connection.fetchall()

        if not overduelist:
            no_results_message = "No results found."
            return render_template("overdueList.html", overduelist=overduelist, no_results_message=no_results_message)
        return render_template("overdueList.html", overduelist=overduelist, student_id=student_id, studentName=studentName, department=department, staff_id=staff_id, supervisorName=supervisorName)
    return render_template("overdueList.html", overduelist=overduelist)

############## admin check overdue reports' status--Bree
@admin_bp.route("/overdueCheck", methods=["GET", "POST"])
def overdueCheck():
    report_id = request.args.get('report_id')
    student_id = request.args.get("student_id")   
    connection = getCursor()
    query = """SELECT
                    RP.report_id,
                    RP.student_abcd_completed,
                    RP.student_f_completed,
                    RP.supervisor_approved,
                    RP.supervisors_completed,
                    RP.convenor_completed,
                    RP.full_report_completed,
                    S.student_id
                FROM
                    report_progress RP
                    INNER JOIN report R ON RP.report_id = R.report_id
                    LEFT JOIN supervision S ON R.student_id = S.student_id
                WHERE RP.report_id = %s """
    query += " GROUP BY RP.report_id;"
    connection.execute(query, (report_id,))
    overduelist = connection.fetchall()
    report_ids = []
    for row in overduelist:
        report_ids.append(row[0]) 

    staff_counts = []
    for report_id in report_ids:
        connection.execute("""SELECT COUNT(DISTINCT su.staff_id) 
                FROM supervision su 
                JOIN report r ON su.student_id = r.student_id 
                WHERE r.report_id = %s""", (report_id,))
        staff_count = connection.fetchone()[0]
        staff_counts.append(staff_count)

        
    return render_template("overdueCheck.html", overduelist=overduelist,report_id=report_id, student_id=student_id, staff_counts=staff_counts)

############## admin check overdue reports' supervisor who need to complete seciton E--Bree
@admin_bp.route("/checkSupervisor", methods=["GET", "POST"])
def checkSupervisor():
    report_id = request.args.get('report_id')
    success_message = request.args.get('success_message')
    connection = getCursor()
    query = """SELECT DISTINCT S.staff_id, CONCAT(S.fname, ' ', S.lname) AS staff_name, s.room, s.email_lu, s.phone
            FROM staff S
            LEFT JOIN supervision SV ON S.staff_id = SV.staff_id
            LEFT JOIN report R ON SV.student_id = R.student_id
            LEFT JOIN report_progress RP ON R.report_id = RP.report_id
            LEFT JOIN SECTION_E_SPVRS SE ON R.report_id = SE.report_id AND S.staff_id = SE.staff_id
            WHERE r. report_id = %s AND SE.report_id IS NULL;"""  
    connection.execute(query, (report_id,))
    supervisorlist = connection.fetchall()
    return render_template("checkSupervisor.html", supervisorlist=supervisorlist,report_id=report_id,success_message=success_message)

    
############## admin check overdue reports' convenor who need to complete seciton E--Bree
@admin_bp.route("/checkConvenor", methods=["GET", "POST"])
def checkConvenor():
    student_id = request.args.get("student_id")
    report_id = request.args.get('report_id')
    success_message = request.args.get('success_message')
    connection = getCursor()
    query = """SELECT DISTINCT S.staff_id, CONCAT(S.fname, ' ', S.lname) AS staff_name, s.room, s.email_lu, s.phone, ST.student_id
                FROM staff S
                LEFT JOIN student ST ON S.dept_code = ST.dept_code
                LEFT JOIN report R ON ST.student_id = R.student_id
                LEFT JOIN report_progress RP ON R.report_id = RP.report_id
                WHERE ST. student_id = %s AND S.role = 'Convenor';"""  
    connection.execute(query, (student_id,))
    convenorlist = connection.fetchall()
    return render_template("checkConvenor.html", convenorlist=convenorlist,student_id=student_id,report_id=report_id,success_message=success_message)

############## admin check overdue reports' supervisor who need to approve 6mr--Bree
@admin_bp.route("/checkMainsuper", methods=["GET", "POST"])
def checkMainsuper():
    report_id = request.args.get('report_id')
    success_message = request.args.get('success_message')
    connection = getCursor()
    query = """SELECT DISTINCT S.staff_id, CONCAT(S.fname, ' ', S.lname) AS staff_name, s.room, s.email_lu, s.phone
                FROM staff S
                LEFT JOIN supervision SV ON S.staff_id = SV.staff_id
                LEFT JOIN report R ON SV.student_id = R.student_id
                LEFT JOIN report_progress RP ON R.report_id = RP.report_id
                WHERE r. report_id = %s AND RP.supervisor_approved != '1' AND SV.supv_type = 'Main Supervisor';"""  
    connection.execute(query, (report_id,))
    supervisorlist = connection.fetchall()
    return render_template("checkMainsuper.html", supervisorlist=supervisorlist,report_id=report_id,success_message=success_message)

############## admin check overdue reports' student who need to complate seciton F--Bree
@admin_bp.route("/checkStudentF", methods=["GET", "POST"])
def checkStudentF():
    report_id = request.args.get('report_id')
    success_message = request.args.get('success_message')
    connection = getCursor()
    query = """SELECT DISTINCT S.student_id, CONCAT(S.fname, ' ', S.lname) AS student_name, s.current_address, s.email_lu, s.phone
                FROM student S
                LEFT JOIN report R ON S.student_id = R.student_id
                LEFT JOIN report_progress RP ON R.report_id = RP.report_id
                WHERE r. report_id = %s AND RP.student_f_completed != '1';"""  
    connection.execute(query, (report_id,))
    studentlist = connection.fetchall()
    return render_template("checkStudentF.html", studentlist=studentlist,report_id=report_id,success_message=success_message)

############## admin check overdue reports' student who need to complate seciton ABCD--Bree
@admin_bp.route("/checkStudentABCD", methods=["GET", "POST"])
def checkStudentABCD():
    report_id = request.args.get('report_id')
    success_message = request.args.get('success_message')
    connection = getCursor()
    query = """SELECT DISTINCT S.student_id, CONCAT(S.fname, ' ', S.lname) AS student_name, s.current_address, s.email_lu, s.phone
                FROM student S
                LEFT JOIN report R ON S.student_id = R.student_id
                LEFT JOIN report_progress RP ON R.report_id = RP.report_id
                WHERE r. report_id = %s AND RP.student_abcd_completed != '1';"""  
    connection.execute(query, (report_id,))
    studentlist = connection.fetchall()
    return render_template("checkStudentABCD.html", studentlist=studentlist,report_id=report_id,success_message=success_message)

#########all reminder for overdue-Bree####
@admin_bp.route("/sendRemindersu", methods=["GET", "POST"])
def sendRemindersu():
    report_id = request.args.get('report_id')
    email_lu = request.args.get('email_lu')
    emailTitle = '6MR Overdue'
    emailBody = 'Please complete 6MR' 
    sendMail(emailTitle, email_lu, emailBody)
    success_message = "Successfully Reminder Overdue Report."
    return redirect (url_for('admin.checkSupervisor',report_id =report_id, email_lu = email_lu,success_message=success_message))

@admin_bp.route("/sendReminderABCD", methods=["GET", "POST"])
def sendReminderABCD():
    report_id = request.args.get('report_id')
    email_lu = request.args.get('email_lu')
    emailTitle = '6MR Overdue'
    emailBody = 'Please complete 6MR' 
    sendMail(emailTitle, email_lu, emailBody)
    success_message = "Successfully Reminder Overdue Report."
    return redirect (url_for('admin.checkStudentABCD',report_id =report_id, email_lu = email_lu,success_message=success_message))

@admin_bp.route("/sendReminderF", methods=["GET", "POST"])
def sendReminderF():
    report_id = request.args.get('report_id')
    email_lu = request.args.get('email_lu')
    emailTitle = '6MR Overdue'
    emailBody = 'Please complete 6MR' 
    sendMail(emailTitle, email_lu, emailBody)
    success_message = "Successfully Reminder Overdue Report."
    return redirect (url_for('admin.checkStudentF',report_id =report_id, email_lu = email_lu,success_message=success_message))

@admin_bp.route("/sendReminderMain", methods=["GET", "POST"])
def sendReminderMain():
    report_id = request.args.get('report_id')
    email_lu = request.args.get('email_lu')
    emailTitle = '6MR Overdue'
    emailBody = 'Please complete 6MR' 
    sendMail(emailTitle, email_lu, emailBody)
    success_message = "Successfully Reminder Overdue Report."
    return redirect (url_for('admin.checkMainsuper',report_id =report_id, email_lu = email_lu,success_message=success_message))

@admin_bp.route("/sendReminderCon", methods=["GET", "POST"])
def sendReminderCon():
    report_id = request.args.get('report_id')
    student_id = request.args.get("student_id")
    email_lu = request.args.get('email_lu')
    emailTitle = '6MR Overdue'
    emailBody = 'Please complete 6MR' 
    sendMail(emailTitle, email_lu, emailBody)
    success_message = "Successfully Reminder Overdue Report."
    return redirect (url_for('admin.checkConvenor',report_id =report_id, email_lu = email_lu,student_id=student_id,success_message=success_message))

#####↓↓↓↓↓ Yu-Tzu Chang ↓↓↓↓↓#####
@admin_bp.route("/status_report", methods=["GET", "POST"])
def status_report():
    cur = getCursor()
    cur.execute("SELECT * FROM report_dem_status")
    dem = cur.fetchall()
    dem_supvr_max_length = max(len(dem[2].split(',')) for dem in dem) if dem else 0 # find the max length of student's supervisor list
    cur.execute("SELECT * FROM report_dtss_status")
    dtss = cur.fetchall()
    dtss_supvr_max_length = max(len(dtss[2].split(',')) for dtss in dtss) if dtss else 0
    cur.execute("SELECT * FROM report_sola_status")
    sola = cur.fetchall()
    sola_supvr_max_length = max(len(sola[2].split(',')) for sola in sola) if sola else 0
    return render_template("admin_status_report.html", dem = dem, dem_supvr_max_length = dem_supvr_max_length, dtss = dtss, dtss_supvr_max_length = dtss_supvr_max_length, sola = sola, sola_supvr_max_length = sola_supvr_max_length)

### Admin check faculty performance analysis report -- Frank ###
@admin_bp.route("/facultyperformancereport", methods=["GET", "POST"])
def facultyperformancereport():
    connection = getCursor()
  
    query1 = """SELECT all_categories.category, all_ratings.rating, COUNT(t.category) AS count
               FROM (
               SELECT 'access_principal' AS category
               UNION ALL SELECT 'access_asst_other'
               UNION ALL SELECT 'expertise_principal'
               UNION ALL SELECT 'expertise_asst_other'
               UNION ALL SELECT 'quality_principal'
               UNION ALL SELECT 'quality_asst_other'
               UNION ALL SELECT 'timeless_principal'
               UNION ALL SELECT 'timeless_asst_other'
               UNION ALL SELECT 'courses_available'
               UNION ALL SELECT 'workspace'
               UNION ALL SELECT 'computer_facilities'
               UNION ALL SELECT 'its_supt'
               UNION ALL SELECT 'research_software'
               UNION ALL SELECT 'library_facilities'
               UNION ALL SELECT 'teach_Learn_supt'
               UNION ALL SELECT 'statistical_supt'
               UNION ALL SELECT 'research_equip'
               UNION ALL SELECT 'technical_supt'
               UNION ALL SELECT 'financial_resource'
               ) all_categories
               CROSS JOIN (
               SELECT 'very good' AS rating
               UNION ALL SELECT 'good'
               UNION ALL SELECT 'satisfactory'
               UNION ALL SELECT 'unsatisfactory'
               UNION ALL SELECT 'not relevant'
               ) all_ratings
               LEFT JOIN (
               SELECT category, rating
               FROM (
               SELECT 'access_principal' AS category, access_principal AS rating
               FROM section_c
               UNION ALL
               SELECT 'access_asst_other', access_asst_other
               FROM section_c
               UNION ALL
               SELECT 'expertise_principal', expertise_principal
               FROM section_c
               UNION ALL
               SELECT 'expertise_asst_other', expertise_asst_other
               FROM section_c
               UNION ALL
               SELECT 'quality_principal', quality_principal
               FROM section_c
               UNION ALL
               SELECT 'quality_asst_other', quality_asst_other
               FROM section_c
               UNION ALL
               SELECT 'timeless_principal', timeless_principal
               FROM section_c
               UNION ALL
               SELECT 'timeless_asst_other', timeless_asst_other
               FROM section_c
               UNION ALL
               SELECT 'courses_available', courses_available
               FROM section_c
               UNION ALL
               SELECT 'workspace', workspace
               FROM section_c
               UNION ALL
               SELECT 'computer_facilities', computer_facilities
               FROM section_c
               UNION ALL
               SELECT 'its_supt', its_supt
               FROM section_c
               UNION ALL
               SELECT 'research_software', research_software
               FROM section_c
               UNION ALL
               SELECT 'library_facilities', library_facilities
               FROM section_c
               UNION ALL
               SELECT 'teach_Learn_supt', teach_Learn_supt
               FROM section_c
               UNION ALL
               SELECT 'statistical_supt', statistical_supt
               FROM section_c
               UNION ALL
               SELECT 'research_equip', research_equip
               FROM section_c
               UNION ALL
               SELECT 'technical_supt', technical_supt
               FROM section_c
               UNION ALL
               SELECT 'financial_resource', financial_resource
               FROM section_c
               ) t
               WHERE rating IN ('very good', 'good', 'satisfactory', 'unsatisfactory', 'not relevant')
               ) t ON all_categories.category = t.category AND all_ratings.rating = t.rating
               GROUP BY all_categories.category, all_ratings.rating;
               """

    connection.execute(query1)
    alldata = connection.fetchall()

    query2="""SELECT 
                results.rating,
                SUM(results.count) AS rating_sum
            FROM (
                SELECT all_categories.category, all_ratings.rating, COUNT(t.category) AS count
                FROM (
                    SELECT 'access_principal' AS category
                    UNION ALL SELECT 'access_asst_other'
                    UNION ALL SELECT 'expertise_principal'
                    UNION ALL SELECT 'expertise_asst_other'
                    UNION ALL SELECT 'quality_principal'
                    UNION ALL SELECT 'quality_asst_other'
                    UNION ALL SELECT 'timeless_principal'
                    UNION ALL SELECT 'timeless_asst_other'
                    UNION ALL SELECT 'courses_available'
                    UNION ALL SELECT 'workspace'
                    UNION ALL SELECT 'computer_facilities'
                    UNION ALL SELECT 'its_supt'
                    UNION ALL SELECT 'research_software'
                    UNION ALL SELECT 'library_facilities'
                    UNION ALL SELECT 'teach_Learn_supt'
                    UNION ALL SELECT 'statistical_supt'
                    UNION ALL SELECT 'research_equip'
                    UNION ALL SELECT 'technical_supt'
                    UNION ALL SELECT 'financial_resource'
                ) all_categories
                CROSS JOIN (
                    SELECT 'very good' AS rating
                    UNION ALL SELECT 'good'
                    UNION ALL SELECT 'satisfactory'
                    UNION ALL SELECT 'unsatisfactory'
                    UNION ALL SELECT 'not relevant'
                ) all_ratings
                LEFT JOIN (
                    SELECT category, rating
                    FROM (
                        SELECT 'access_principal' AS category, access_principal AS rating
                        FROM section_c
                        UNION ALL
                        SELECT 'access_asst_other', access_asst_other
                        FROM section_c
                        UNION ALL
                        SELECT 'expertise_principal', expertise_principal
                        FROM section_c
                        UNION ALL
                        SELECT 'expertise_asst_other', expertise_asst_other
                        FROM section_c
                        UNION ALL
                        SELECT 'quality_principal', quality_principal
                        FROM section_c
                        UNION ALL
                        SELECT 'quality_asst_other', quality_asst_other
                        FROM section_c
                        UNION ALL
                        SELECT 'timeless_principal', timeless_principal
                        FROM section_c
                        UNION ALL
                        SELECT 'timeless_asst_other', timeless_asst_other
                        FROM section_c
                        UNION ALL
                        SELECT 'courses_available', courses_available
                        FROM section_c
                        UNION ALL
                        SELECT 'workspace', workspace
                        FROM section_c
                        UNION ALL
                        SELECT 'computer_facilities', computer_facilities
                        FROM section_c
                        UNION ALL
                        SELECT 'its_supt', its_supt
                        FROM section_c
                        UNION ALL
                        SELECT 'research_software', research_software
                        FROM section_c
                        UNION ALL
                        SELECT 'library_facilities', library_facilities
                        FROM section_c
                        UNION ALL
                        SELECT 'teach_Learn_supt', teach_Learn_supt
                        FROM section_c
                        UNION ALL
                        SELECT 'statistical_supt', statistical_supt
                        FROM section_c
                        UNION ALL
                        SELECT 'research_equip', research_equip
                        FROM section_c
                        UNION ALL
                        SELECT 'technical_supt', technical_supt
                        FROM section_c
                        UNION ALL
                        SELECT 'financial_resource', financial_resource
                        FROM section_c
                    ) t
                    WHERE rating IN ('very good', 'good', 'satisfactory', 'unsatisfactory', 'not relevant')
                ) t ON all_categories.category = t.category AND all_ratings.rating = t.rating
                GROUP BY all_categories.category, all_ratings.rating
                ORDER BY CASE 
                    WHEN all_ratings.rating = 'very good' THEN 1
                    WHEN all_ratings.rating = 'good' THEN 2
                    WHEN all_ratings.rating = 'satisfactory' THEN 3
                    WHEN all_ratings.rating = 'unsatisfactory' THEN 4
                    WHEN all_ratings.rating = 'not relevant' THEN 5
                END
            ) results
            GROUP BY results.rating
            WITH ROLLUP;
            """
    connection.execute(query2)
    totaldata = connection.fetchall()
    return render_template("facultyperformancereport.html", alldata=alldata,totaldata=totaldata)

@admin_bp.route("/issues/sendAlertEmail", methods=["GET", "POST"])
def sendAlertEmail():
    report_id = request.args.get('report_id')
    current_status =  request.args.get('current')
    previous_status =  request.args.get('previous')
    dept = request.args.get('dept')
    cur = getCursor()
    if (current_status == 'O' and previous_status == 'O') or current_status == 'R': # if the status is 2 oranges(current + previous) or 1 red(current), send email to convenor and student
        query = """SELECT s.student_id, CONCAT(s.fname, ' ', s.lname) AS student_name, s.email_lu AS student_email, c.email_lu AS convenor_email
                FROM report r
                JOIN student s ON r.student_id = s.student_id
                JOIN staff c ON c.staff_id = (
                    SELECT staff_id
                    FROM staff
                    WHERE dept_code = %s AND role = 'Convenor'
                )
                WHERE r.report_id = %s;"""
        cur.execute(query, (dept, report_id))
        result = cur.fetchall()
        emailTitle = '6MR Report Alert!'
        student_emailBody = 'Your 6MR is not performing well, the convenor will contact you to discuss it.'
        student_email = result[0][2]
        sendMail(emailTitle, student_email, student_emailBody)
        convenor_email_body = "Student ID: " + str(result[0][0]) + " Student Name: " + str(result[0][1]) + " is not performing well, please contact " + str(student_email) + " to discuss."
        convenor_email = result[0][3]
        sendMail(emailTitle, convenor_email, convenor_email_body)
    elif current_status == 'O' and previous_status != 'O': # if the status is 1 orange(current), send email to convenor and supervisor
        query = """SELECT s.student_id, CONCAT(s.fname, ' ', s.lname) AS student_name, c.email_lu AS convenor_email, st.email_lu AS main_supervisor_email
                FROM report r
                JOIN student s ON r.student_id = s.student_id
                JOIN staff c ON c.staff_id = (
                    SELECT staff_id
                    FROM staff
                    WHERE dept_code = %s AND role = 'Convenor'
                )
                JOIN supervision sv ON sv.student_id = s.student_id AND sv.supv_type = 'Main Supervisor'
                JOIN staff st ON st.staff_id = sv.staff_id
                WHERE r.report_id = %s;"""
        cur.execute(query, (dept, report_id))
        result = cur.fetchall()
        emailTitle = '6MR Report Alert!'
        supervisor_emailBody = "One of your supervisee Student ID: " + str(result[0][0]) + " Student Name: " + str(result[0][1]) + " is not performing well, the convenor will contact you to discuss it."
        supervisor_email = result[0][3]
        sendMail(emailTitle, supervisor_email, supervisor_emailBody)
        email_body = "Student ID: " + str(result[0][0]) + " Student Name: " + str(result[0][1]) + " is not performing well, please contact the student's main supervisor " + str(supervisor_email) + " to discuss."
        convenor_email = result[0][2]
        sendMail(emailTitle, convenor_email, email_body)
    flash('Alert email sent successfully', 'success')
    return redirect (url_for('admin.issues'))