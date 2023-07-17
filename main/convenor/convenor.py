import json
from main.common import getCursor
from flask import (redirect, render_template, request, session, url_for, flash)
from main.config import sendMail
from main.convenor import convenor_bp

@convenor_bp.route("/")
def index():
    username = session.get('username')
    return render_template("convenor.html", username=username)

@convenor_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def getprofile():
    username = session.get('username')
    # get basic profile which can not be edited
    query = f"SELECT * FROM staff WHERE email_lu = '{username}'"
    connection = getCursor()
    connection.execute(query)
    profile = connection.fetchone()
    return profile

@convenor_bp.route("/studentlist", methods=["GET", "POST"])
def viewStudentList():
    convenorProfile = getprofile()
    convenorDeptCode = convenorProfile[9]

    query = f"""
                SELECT S.student_id, S.fname, S.lname, S.phone, S.email_lu, S.part_full_time, D.dept_name 
                FROM student S
                LEFT JOIN department D ON S.dept_code = D.dept_code
                WHERE S.dept_code = "{convenorDeptCode}"
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

        if conditions:
            query += " AND " + " OR ".join(conditions)
    
    print(query)

    connection = getCursor()
    connection.execute(query)
    studentList = connection.fetchall()
    return render_template("convenor_viewStudentList.html", studentList=studentList)

@convenor_bp.route("/studentdetail/<int:student_id>", methods=["GET", "POST"])
def viewStudengDetail(student_id):
    query_profile = f"""
                SELECT S.student_id, S.fname, S.lname, S.enrollment_date, S.current_address, S.phone, S.email_lu, S.email_other, S.part_full_time, D.dept_name , S.thesis_title
                FROM student S
                LEFT JOIN department D ON S.dept_code = D.dept_code
                WHERE S.student_id = {student_id}
                """

    query_scholarship = f"""
                SELECT student_id, scholarship_name, scholarship_value, scholarship_tenure, scholarship_start_date, scholarship_end_date
                FROM scholarship
                WHERE student_id = {student_id}
                ORDER BY scholarship_end_date DESC
                """

    query_employment = f"""
                SELECT student_id, company_name, employment_start_date, employment_end_date
                FROM employment
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

    return render_template("convenor_viewStudentDetail.html", studentProfile=studentProfile, studentScholarship=studentScholarship, studentEmployment=studentEmployment, studentSupervisor=studentSupervisor)

@convenor_bp.route("/supervisorlist", methods=["GET", "POST"])
def viewSupervisorList():
    convenorProfile = getprofile()
    convenorDeptCode = convenorProfile[9]

    query = f"""
                SELECT S.staff_id, S.fname, S.lname, S.phone, S.email_lu, S.room, D.dept_name 
                FROM staff S
                LEFT JOIN department D ON S.dept_code = D.dept_code
                WHERE S.role = 'Supervisor' AND S.dept_code = "{convenorDeptCode}"
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

        if conditions:
            query += " AND (" + " OR ".join(conditions) + ")"

    connection = getCursor()
    connection.execute(query)
    supervisorList = connection.fetchall()
    return render_template("convenor_viewSupervisorList.html", supervisorList=supervisorList) 

# This feature is fill section_e for convenor as convenor role
@convenor_bp.route("/section_e/<int:report_id>", methods=["GET", "POST"])
def sectionE(report_id):  
    connection = getCursor()

    profile = getprofile()

    studentQuery = f"SELECT * FROM student WHERE student_id = (select student_id from report where report_id = {report_id})"
    connection.execute(studentQuery)
    student = connection.fetchone()

    if request.method != "GET":
        comment = request.form.get('comment')
        date = request.form.get('date')
        status = request.form.get('inlineRadioOptions')

        if (status == 'R'):
            chairEmailQuery = "SELECT email_lu FROM staff WHERE role = 'Postgraduate Chair'"
            connection.execute(chairEmailQuery)
            chairEmail = connection.fetchone()[0]
            studentName = student[2] + " " + student[1]
            studentID = student[0]
            emailTitle = f"{studentName} has a Red status"
            emailBody = f"{studentName} (ID: {studentID}) has been marked Red"
            sendMail(emailTitle, chairEmail, emailBody)

        insertQuery = f"""
                        INSERT INTO section_e_convenor (report_id, staff_id, comments, date, student_status)
                        VALUE ("{report_id}", "{profile[0]}", "{comment}", "{date}", "{status}")
                        """

        updateQuery = f"""
                        UPDATE report_progress
                        SET convenor_completed = 1
                        WHERE report_id = {report_id}
                        """
        
        connection.execute(insertQuery)
        connection.execute(updateQuery)
        return redirect(url_for('convenor.view6MR'))
    
    return render_template("convenor_section_e.html", profile=profile, student=student) 

# This feature lists all 6MRs of students in the same department for convenor
@convenor_bp.route("/6mr", methods=["GET", "POST"])
def view6MR():  
    profile = getprofile()
    query = f"""
                SELECT s.student_id, 
                    concat(fname,' ',lname) student_name,
                    r.report_id,
                    concat(rept_term,' ',rept_year) rept_term,
                    due_date
                FROM student s
                INNER JOIN (SELECT * FROM report WHERE due_date = (SELECT max(due_date) FROM report)) r ON s.student_id = r.student_id 
                INNER JOIN report_progress rp ON r.report_id = rp.report_id 
                INNER JOIN (SELECT student_id, count(*) no_supvs FROM supervision GROUP BY student_id ) sp ON sp.student_id = s.student_id
                WHERE 
                dept_code = "{profile[9]}"
                AND s.student_id NOT IN (SELECT student_id FROM supervision WHERE staff_id IN (SELECT staff_id FROM staff WHERE role = 'Convenor')) 
                AND supervisors_completed = no_supvs 
                AND convenor_completed = 0; 
            """
    connection = getCursor()
    connection.execute(query)
    reportList = connection.fetchall()
    return render_template("convenor_view6MR.html", reportList=reportList)

# This feature is viewing student's 6MR details
@convenor_bp.route("/view6mrdeatil/<int:report_id>/<int:student_id>", methods=["GET", "POST"])
def view6MrDetail(report_id, student_id): 
    report_id=report_id
    connection = getCursor()
    # section a to f
    # get supervisor
    query_supervisor = f"""
                SELECT CONCAT(S.fname, ' ', S.lname) AS Name, V.supv_type
                FROM supervision V
                LEFT JOIN staff S ON V.staff_id = S.staff_id
                WHERE V.student_id = {student_id}
                """
    
    connection.execute(query_supervisor)
    supervisors = connection.fetchall()

    # get student profile
    connection.execute("SELECT * \
                        FROM student s \
                        WHERE s.student_id = %s",(student_id,))
    profile = connection.fetchall()

    # get scholalrship 
    connection.execute("SELECT * \
                            FROM scholarship \
                            WHERE student_id = %s",(student_id,))
    scholarship= connection.fetchall()
    # get employment
    connection.execute("SELECT * \
                            FROM employment \
                            WHERE student_id = %s",(student_id,))
    employment= connection.fetchall()
    # view b history
    connection.execute("SELECT * FROM section_b WHERE report_id = %s",(report_id,))
    section_b = connection.fetchall()

    # view c
    connection.execute("SELECT * FROM section_c WHERE report_id = %s",(report_id,))
    section_c = connection.fetchall()
    connection.execute("SELECT * FROM section_d WHERE report_id = %s",(report_id,))
    section_d = connection.fetchall()

    # parse JSON string into Python objects
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
    return render_template("convenor_view6mrDetail.html", profile=profile, supervisors=supervisors, scholarship=scholarship, employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e,section_e_convenor=section_e_convenor)   #,report_progress=report_progress
    #return render_template("convenor_view6mrDetail.html", profile=profile, supervisors=supervisors, scholarship=scholarship, employment=employment)

# This feature lists all supervisees of the convenor in the role of a supervisor - Bree
@convenor_bp.route("/coSuperviseeList", methods=["GET", "POST"])
def coSuperviseeList():
    username = session.get('username')
    connection = getCursor()
    query = "SELECT st.student_id, CONCAT(st.fname, ' ', st.lname) Name, st.phone, st.email_lu, d.dept_name \
            FROM student st \
            LEFT JOIN supervision su ON st.student_id = su.student_id \
            LEFT JOIN department d ON st.dept_code = d.dept_code \
            LEFT JOIN staff s ON su.staff_id = s.staff_id \
            WHERE s.email_lu = %s"
    query += " GROUP BY st.student_id;"
    connection.execute(query, (username,))
    superviseeList = connection.fetchall()

    if request.method == "POST":
        # Get the search parameters from the form
        student_id = request.form.get('studentID')
        student_name = request.form.get('studentName')
        department_name = request.form.get('departmentName')

        # Define the base query to fetch supervisees
        base_query = "SELECT st.student_id, CONCAT(st.fname, ' ', st.lname) Name, st.phone, st.email_lu, d.dept_name, d.faculty_name \
                    FROM student st \
                    LEFT JOIN supervision su ON st.student_id = su.student_id \
                    LEFT JOIN department d ON st.dept_code = d.dept_code \
                    LEFT JOIN staff s ON su.staff_id = s.staff_id \
                    WHERE s.email_lu = %s"

        # Define the parameters to be used in the query
        params = [username]

        # Add conditions to the query based on the search parameters
        if student_id.isdigit():
            base_query += " AND st.student_id = %s"
            params.append(student_id)

        if student_name:
            base_query += " AND (st.fname LIKE %s OR st.lname LIKE %s)"
            params.append(f"%{student_name}%")
            params.append(f"%{student_name}%")

        # Execute the query with the parameters
        connection.execute(base_query, tuple(params))
        superviseeList = connection.fetchall()

        # Check if any results were found and return a message if not
        if not superviseeList:
            no_results_message = "No results found."
            return render_template("convenor_supervisee.html", superviseeList=superviseeList, no_results_message=no_results_message)

        return render_template("convenor_supervisee.html", superviseeList=superviseeList)

    return render_template("convenor_supervisee.html", superviseeList=superviseeList)

##### convenor view all supervisee report status as supervisor role, supervisor to assess and view report---Bree & Special
@convenor_bp.route("/convenor_fill6mr", methods=["GET", "POST"])
def coFill6mr():
    username = session.get('username')

    success_message = request.args.get('success_message')
    connection = getCursor()

    query = """SELECT st.student_id, CONCAT(st.fname, ' ', st.lname) AS Name, r.report_id, rp.supervisor_approved, rp.supervisors_completed, 
            su.staff_id, CONCAT(s.fname, ' ', s.lname) AS sName, su.supv_type 
            FROM student st 
            LEFT JOIN supervision su ON st.student_id = su.student_id 
            LEFT JOIN staff s ON su.staff_id = s.staff_id 
            LEFT JOIN (SELECT report_id, student_id, ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY report_id DESC) AS row_num FROM report) r 
                ON st.student_id = r.student_id AND r.row_num = 1 
            LEFT JOIN report_progress rp ON r.report_id = rp.report_id 
            WHERE s.email_lu = %s"""
    connection.execute(query, (username,)) 
    fill6mrlist = connection.fetchall()
    report_ids = []
    for row in fill6mrlist:
        report_ids.append(row[2]) 

    staff_counts = []
    for report_id in report_ids:
        connection.execute("""SELECT COUNT(DISTINCT su.staff_id) 
                FROM supervision su 
                JOIN report r ON su.student_id = r.student_id 
                WHERE r.report_id = %s""", (report_id,))
        staff_count = connection.fetchone()[0]
        staff_counts.append(staff_count)

    return render_template("convenor_fill6mr.html", fill6mrlist=fill6mrlist, staff_counts=staff_counts, success_message=success_message, username=username)

##### convenor fill the section E as supervisor role --- Bree & Special
@convenor_bp.route("/convenor_superviserSectionE", methods=["GET", "POST"])
def co_section_e():
    report_id = request.args.get('report_id')
    student_id = request.args.get("student_id")
    student_name = request.args.get("student_name")
    staff_id = request.args.get("staff_id")
    staff_name = request.args.get("staff_name")
    supv_type = request.args.get("supv_type")
    connection = getCursor()
    connection.execute("SELECT * FROM section_e_spvrs WHERE report_id = %s and staff_id = %s", (report_id,staff_id,))
    previous_data = connection.fetchall()
    if request.method == 'POST':
        # Get the form data
        overall_6m = request.form.get('overall_6m')
        overall_full = request.form.get('overall_full')
        work_quality = request.form.get('work_quality')
        technical_skill = request.form.get('technical_skill')
        likelihood_6m = request.form.get('likelihood_6m')
        recommendation = request.form.get('recommendation')
        comments = request.form.get('Comments')
        date = request.form.get('date')

        if report_id:
            # Check if the record already exists
            connection.execute("SELECT * FROM section_e_spvrs WHERE report_id = %s and staff_id = %s", (report_id,staff_id,))
            previous_data = connection.fetchone()

            if previous_data:
                # Update the existing record
                connection.execute("""
                    UPDATE section_e_spvrs
                    SET overall_6m = %s, overall_full = %s, work_quality = %s, technical_skill = %s,
                        likelihood_6m = %s, recommendation = %s, comments = %s, date = %s
                    WHERE report_id = %s
                """, (
                    overall_6m, overall_full, work_quality, technical_skill, likelihood_6m,
                    recommendation, comments, date, report_id
                ))
            else:
                # Insert a new record
                connection.execute("""
                    INSERT INTO section_e_spvrs (report_id, student_name, student_id, spvr_name, staff_id,
                        supv_type, overall_6m, overall_full, work_quality, technical_skill,
                        likelihood_6m, recommendation, comments, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    report_id, student_name, student_id, staff_name, staff_id, supv_type,
                    overall_6m, overall_full, work_quality, technical_skill, likelihood_6m,
                    recommendation, comments, date
                ))
                connection.execute("UPDATE report_progress SET supervisors_completed = supervisors_completed + 1 WHERE report_id = %s", (report_id,))
                username = session.get('username')
                emailTitle = "Supervisor evaluated section E"
                emailBody = "Supervisors have completed 6MR, please check in the system."
                getConvenorEmail ="SELECT email_lu FROM staff WHERE dept_code = (SELECT dept_code FROM staff WHERE email_lu = %s) AND role = 'convenor'"
                connection.execute(getConvenorEmail, (username,))
                convenorEmail = connection.fetchone()[0]
                sendMail(emailTitle, convenorEmail, emailBody)

            success_message = "Section E updated successfully"
            return redirect(url_for('convenor.coFill6mr') + '?success_message=' + success_message)
        else:
            # Handle the case where report_id is missing
            return "Error: Report ID is missing"
    
    else:
        # Get the previously selected options from the database if they exist
        if len(previous_data) == 0:
            return render_template("convenor_superviserSectionE.html", student_id=student_id, student_name=student_name,
                               staff_id=staff_id, staff_name=staff_name, report_id=report_id,
                               supv_type=supv_type)
        else:
            return render_template("convenor_superviserSectionE.html", student_id=student_id, student_name=student_name,
                               staff_id=staff_id, staff_name=staff_name, report_id=report_id,
                               supv_type=supv_type, previous_data=previous_data)

##### convenor view 6MR as supervisor role
@convenor_bp.route("/convenor_suView6mr", methods=["GET", "POST"])
def co_view_6mr():  
    cur = getCursor()
    if request.method == "POST":
        report_id = request.form.get('report_id')
        if "approval" in request.form:
            # Update the report_progress table to set supervisor_approved as 1
            cur.execute("UPDATE report_progress SET supervisor_approved = 1 WHERE report_id = %s", (report_id,))
            flash("You have approved this report. Please evaluate it in section E.", "info")
            return redirect(url_for('convenor.coFill6mr'))      
        else:
            
            flash("You have rejected this report. The supervisee will receive your comment in email", "info")
            # send email to supervisee with reject comments
            cur.execute("SELECT s.email_lu FROM student s JOIN report r ON r.student_id = s.student_id WHERE r.report_id = %s", (report_id,))
            email = cur.fetchone()[0]
            emailTitle = '6MR Report Rejected By Main Supervisor!'
            emailBody = request.form.get('reject_reason')
            sendMail(emailTitle, email, emailBody)
            return redirect(url_for('convenor.coFill6mr'))
    else:
        username = session.get('username')
        report_id = request.args.get('report_id')  
        cur.execute("SELECT student_id FROM report WHERE report_id = %s",(report_id,))
        student_id = cur.fetchone()
        
        cur.execute("SELECT n.supv_type FROM supervision n \
                    JOIN staff s ON s.staff_id = n.staff_id \
                    WHERE n.student_id = %s AND s.email_lu = %s",(student_id[0], username))
        currentSuperType = cur.fetchone()[0]
        
        cur.execute("SELECT * FROM student WHERE student_id = %s",(student_id[0],))
        profile = cur.fetchall()
        
        cur.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                    FROM staff s left join supervision n on s.staff_id = n.staff_id \
                    WHERE n.student_id = %s AND n.supv_type = 'Main Supervisor'",(student_id[0],))
        super1 = cur.fetchall()
        
        cur.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                    FROM staff s left join supervision n on s.staff_id = n.staff_id\
                    WHERE n.student_id = %s AND n.supv_type = 'Associate Supervisor'",(student_id[0],))
        super2 = cur.fetchone()
        
        cur.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                    FROM staff s left join supervision n on s.staff_id = n.staff_id\
                    WHERE n.student_id = %s AND n.supv_type = 'Other Supervisor'",(student_id[0],))
        super3 = cur.fetchall()
        
        cur.execute("SELECT * FROM scholarship WHERE student_id = %s",(profile[0][0],))
        scholarship = cur.fetchall()
        
        cur.execute("SELECT * FROM employment WHERE student_id = %s",(profile[0][0],))
        employment= cur.fetchall()
        
        cur.execute("SELECT * FROM section_b WHERE report_id = %s",(report_id[0],))
        section_b = cur.fetchall()
        
        cur.execute("SELECT * FROM section_c WHERE report_id = %s",(report_id[0],))
        section_c = cur.fetchall()
        
        cur.execute("SELECT * FROM section_d WHERE report_id = %s",(report_id[0],))
        section_d = cur.fetchall()
        # parse JSON string into Python objects
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
        cur.execute("SELECT * FROM section_e_spvrs WHERE report_id = %s",(report_id[0],))
        section_e = cur.fetchall()
        cur.execute("SELECT CONCAT(s.fname, ' ', s.lname) AS Name, e.date, e.comments, e.student_status FROM section_e_convenor e JOIN staff s ON s.staff_id = e.staff_id WHERE report_id = %s",(report_id,))
        section_e_convenor = cur.fetchall()
        cur.execute("SELECT supervisor_approved FROM report_progress WHERE report_id = %s", (report_id,))
        report_progress = cur.fetchone()[0]
        return render_template("convenor_suView6mr.html", profile=profile,currentSuperType=currentSuperType, super1=super1,super2=super2,super3=super3,scholarship=scholarship,employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e,section_e_convenor=section_e_convenor, report_id=report_id, report_progress=report_progress,)
    
#####↓↓↓↓↓ Yu-Tzu Chang ↓↓↓↓↓#####
@convenor_bp.route("/status", methods=["GET", "POST"])
def viewStatus():
    cur = getCursor()
    convenor_email = session.get('username')
    cur.execute("SELECT dept_code FROM staff WHERE email_lu = %s", (convenor_email,))
    dept = cur.fetchone()[0]
    dept_code = f"s.dept_code = '{dept}'"
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
        status = request.form.get('status')
        reportYear = request.form.get('reportYear')
        reportTerm = request.form.get('reportTerm')
        studentName = request.form.get('studentName')
        department = request.form.get('department')
        conditions = [dept_code]

        if student_id is not None and student_id.isdigit():
            conditions.append(f"s.student_id = {student_id}")
            
        if status is not None:
            if status == "incomplete":
                status = 0
            else:
                status = 1
            conditions.append(f"rp.full_report_completed = {status}")
            
        if reportYear is not None:
            conditions.append(f"r.rept_year = {reportYear}")
        
        if reportTerm is not None:
            conditions.append(f"r.rept_term = '{reportTerm}'")
        
        if studentName is not None and len(studentName.strip()) > 0:
            conditions.append(f"(s.fname LIKE '%{studentName}%' OR s.lname LIKE '%{studentName}%')")
        
        if department is not None:
            conditions.append(f"s.dept_code = '{department}'")

        if conditions:
            query += " WHERE (" + " AND ".join(conditions) + ") ORDER BY s.student_id"
        cur.execute(query)
        studentList = cur.fetchall()
        return render_template("convenor_viewstatus.html", studentList=studentList,student_id=student_id,status=status,reportYear=reportYear,reportTerm=reportTerm,studentName=studentName,department=department)
    else:
        query += " WHERE r.rept_year = (SELECT MAX(rept_year) FROM report) AND " + dept_code + " ORDER BY s.student_id"
        cur.execute(query)
        studentList = cur.fetchall()
        return render_template("convenor_viewstatus.html",studentList=studentList)