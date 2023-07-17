from main.common import getCursor
from flask import (redirect, render_template,request, session, url_for, flash)
from main.supervisor import supervisor_bp
from main.config import sendMail
import json

@supervisor_bp.route("/")
def index():
    username = session.get('username')
    return render_template("supervisor.html", username=username)

@supervisor_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

######view and update the supervisor's information --Bree
@supervisor_bp.route("/suprofile", methods=["GET", "POST"])
def suprofile():
    username = session.get('username') # Get the username from the session
    connection = getCursor()
    query = "SELECT staff.staff_id, staff.fname, staff.lname, staff.employment_start_date, \
                        staff.role, staff.room, staff.email_lu, staff.phone, department.dept_name, department.faculty_name \
                        FROM staff \
                        LEFT JOIN user ON staff.email_lu = user.email_lu \
                        LEFT JOIN department ON staff.dept_code = department.dept_code \
                        WHERE user.email_lu = %s"
    connection.execute(query,(username,)) 
    supervisor_profile = connection.fetchall()
    if request.method == 'POST':
        contact_number = request.form.get("phone")
        room = request.form.get("room")
        # Update the supervisor's information using the username
        connection.execute("UPDATE staff SET phone = %s, room = %s WHERE email_lu = %s", (contact_number, room, username))
        # Set the success message
        success_message = "Your profile updated successfully"
        connection.execute(query,(username,)) 
        supervisor_profile = connection.fetchall()
        return render_template("suprofile.html", suprofile = supervisor_profile, success_message =success_message)
    else:
        return render_template("suprofile.html", suprofile = supervisor_profile)
    
######view the supervisee's information --Frank & Bree
@supervisor_bp.route("/supervisee_list", methods=["GET", "POST"])
def supervisee_list():
    username = session.get('username') # Get the username from the session
    connection = getCursor()
    query = "SELECT st.student_id, CONCAT(st.fname, ' ', st.lname) Name, st.phone, st.email_lu, d.dept_name, st.current_address\
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

        if department_name:
            base_query += " AND st.dept_code LIKE %s"
            params.append(f"%{department_name}%")

        # Execute the query with the parameters
        connection.execute(base_query, tuple(params))
        superviseeList = connection.fetchall()

        # Check if any results were found and return a message if not
        if not superviseeList:
            no_results_message = "No results found."
            return render_template("supervisee.html", superviseeList=superviseeList, no_results_message=no_results_message)

        return render_template("supervisee.html", superviseeList=superviseeList)

    return render_template("supervisee.html", superviseeList=superviseeList)

####### view the student's scholarship and employment information---Bree
@supervisor_bp.route("/studentinfo/<int:student_id>", methods=["GET", "POST"])
def viewStudengDetail(student_id):
    query_profile = f"""
                SELECT S.student_id, S.fname, S.lname, S.enrollment_date, S.current_address, S.phone, S.email_lu, S.email_other, S.part_full_time, D.dept_name , S.thesis_title
                FROM STUDENT S
                LEFT JOIN DEPARTMENT D ON S.dept_code = D.dept_code
                WHERE S.student_id = {student_id}
                """
    query_scholarship = f"""
                SELECT student_id, scholarship_name, scholarship_value, scholarship_tenure, scholarship_start_date, scholarship_end_date
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
                FROM SUPERVISION V
                LEFT JOIN STAFF S ON V.staff_id = S.staff_id
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
    return render_template("studentInfo.html", studentProfile=studentProfile, studentScholarship=studentScholarship, studentEmployment=studentEmployment, studentSupervisor=studentSupervisor)

########supervisor view all supervisee report status to assess and view report---Bree & Special
@supervisor_bp.route("/fill6mr", methods=["GET", "POST"])
def fill6mr():
    username = session.get('username')
    success_message = request.args.get('success_message')
    connection = getCursor()

    query = """
        SELECT st.student_id, CONCAT(st.fname, ' ', st.lname) AS Name, r.report_id, rp.supervisor_approved, rp.supervisors_completed, 
        su.staff_id, CONCAT(s.fname, ' ', s.lname) AS sName, su.supv_type 
        FROM student st 
        LEFT JOIN supervision su ON st.student_id = su.student_id 
        LEFT JOIN staff s ON su.staff_id = s.staff_id 
        LEFT JOIN (
            SELECT report_id, student_id, ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY report_id DESC) AS row_num
            FROM report
        ) r ON st.student_id = r.student_id AND r.row_num = 1 
        LEFT JOIN report_progress rp ON r.report_id = rp.report_id 
        WHERE s.email_lu = %s
    """
    connection.execute(query, (username,))
    fill6mrlist = connection.fetchall()
    report_ids = [row[2] for row in fill6mrlist]

    staff_counts = []
    for report_id in report_ids:
        connection.execute("""
            SELECT COUNT(DISTINCT su.staff_id) 
            FROM supervision su 
            JOIN report r ON su.student_id = r.student_id 
            WHERE r.report_id = %s
        """, (report_id,))
        staff_count = connection.fetchone()[0]
        staff_counts.append(staff_count)

    if request.method == "POST":
        student_name = request.form.get('studentName')
        report_id = request.form.get('report_id')

        # Define the base query to fetch supervisees'report
        base_query = """
            SELECT st.student_id, CONCAT(st.fname, ' ', st.lname) AS Name, r.report_id, rp.supervisor_approved, rp.supervisors_completed, 
            su.staff_id, CONCAT(s.fname, ' ', s.lname) AS sName, su.supv_type 
            FROM student st 
            LEFT JOIN supervision su ON st.student_id = su.student_id 
            LEFT JOIN staff s ON su.staff_id = s.staff_id 
            LEFT JOIN (
                SELECT report_id, student_id, ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY report_id DESC) AS row_num
                FROM report
            ) r ON st.student_id = r.student_id AND r.row_num = 1 
            LEFT JOIN report_progress rp ON r.report_id = rp.report_id 
            WHERE s.email_lu = %s
        """

        # Define the parameters to be used in the query
        params = [username]

        # Add conditions to the query based on the search parameters
        if student_name:
            base_query += " AND (st.fname LIKE %s OR st.lname LIKE %s)"
            params.append(f"%{student_name}%")
            params.append(f"%{student_name}%")

        if report_id:
            base_query += " AND r.report_id LIKE %s"
            params.append(f"%{report_id}%")

        # Execute the query with the parameters
        connection.execute(base_query, tuple(params))
        fill6mrlist = connection.fetchall()

        # Check if any results were found and return a message if not
        if not fill6mrlist:
            no_results_message = "No results found."
            return render_template("fill6mr.html", fill6mrlist=fill6mrlist, staff_counts=staff_counts, success_message=success_message, no_results_message=no_results_message, username=username)

        return render_template("fill6mr.html", fill6mrlist=fill6mrlist, staff_counts=staff_counts, success_message=success_message, username=username)

    return render_template("fill6mr.html", fill6mrlist=fill6mrlist, staff_counts=staff_counts, success_message=success_message, username=username)






###### supervisor fill the section e --- Bree & Special
@supervisor_bp.route("/su_section_e", methods=["GET", "POST"])
def su_section_e():
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
            return redirect(url_for('supervisor.fill6mr') + '?success_message=' + success_message)
        else:
            # Handle the case where report_id is missing
            return "Error: Report ID is missing"
    
    else:
        # Get the previously selected options from the database if they exist
        if len(previous_data) == 0:
            return render_template("su_section_e.html", student_id=student_id, student_name=student_name,
                               staff_id=staff_id, staff_name=staff_name, report_id=report_id,
                               supv_type=supv_type)
        else:
            return render_template("su_section_e.html", student_id=student_id, student_name=student_name,
                               staff_id=staff_id, staff_name=staff_name, report_id=report_id,
                               supv_type=supv_type, previous_data=previous_data)



#####↓↓↓↓↓ Yu-Tzu Chang ↓↓↓↓↓#####
@supervisor_bp.route("/view6mr", methods=["GET", "POST"])
def su_view_6mr():  
    cur = getCursor()
    if request.method == "POST":
        report_id = request.form.get('report_id')
        if "approval" in request.form:
            # Update the report_progress table to set supervisor_approved as 1
            cur.execute("UPDATE report_progress SET supervisor_approved = 1 WHERE report_id = %s", (report_id,))
            flash("You have approved this report. Please evaluate it in section E.", "info")
            return redirect(url_for('supervisor.fill6mr'))      
        else:
            
            flash("You have rejected this report. The supervisee will receive your comment in email", "info")
            # send email to supervisee with reject comments
            cur.execute("SELECT s.email_lu FROM student s JOIN report r ON r.student_id = s.student_id WHERE r.report_id = %s", (report_id,))
            email = cur.fetchone()[0]
            emailTitle = '6MR Report Rejected By Main Supervisor!'
            emailBody = request.form.get('reject_reason')
            sendMail(emailTitle, email, emailBody)
            return redirect(url_for('supervisor.fill6mr'))
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
        super1 = cur.fetchone()
        
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
        return render_template("suview6mr.html", profile=profile,currentSuperType=currentSuperType, super1=super1,super2=super2,super3=super3,scholarship=scholarship,employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e, report_id=report_id, report_progress=report_progress,section_e_convenor=section_e_convenor)
