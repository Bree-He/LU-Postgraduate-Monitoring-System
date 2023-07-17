from datetime import datetime
import json
from flask import (redirect, render_template, request, session, url_for)
from main.common import getCursor
from main.chair import chair_bp
from main.config import sendMail

@chair_bp.route("/")
def index():
    username = session.get('username')
    # return ("Chair")
    return render_template("chair.html", username=username)

@chair_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

### 10# Chair view student --Frank

@chair_bp.route("/studentlist", methods=["GET", "POST"])
def studentlist():
    query = """
                SELECT S.student_id, CONCAT(S.fname, ' ', S.lname) Name, S.phone, S.email_lu, S.part_full_time, D.dept_name 
                FROM student S
                LEFT JOIN department D ON S.dept_code = D.dept_code
                """
    
    if request.method != "GET":
        student_id = request.form.get('studentID')
        student_name = request.form.get('Name')
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
    connection.fetchall()
    return render_template("studentlist.html", studentList=studentList)

### 10# Chair view student --Frank

@chair_bp.route('/studentprofile')
def student_profile():
    connection = getCursor()
    student_name = request.args.get('Name').replace("+", " ")  # replace '+' with ' '
    # Store student_name in a variable and use it in the query
    query_1 = "SELECT *, CONCAT(S.fname, ' ', S.lname) Name FROM student S \
            LEFT JOIN report ON S.student_id = report.student_id \
            LEFT JOIN report_progress ON report.report_id = report_progress.report_id \
            LEFT JOIN section_e_convenor ON report.report_id = section_e_convenor.report_id \
            LEFT JOIN section_f on  report.report_id = section_f.report_id \
            WHERE CONCAT(S.fname, ' ', S.lname) = %s \
            ORDER BY report.report_id ASC"
    connection.execute(query_1, (student_name,))
    report_data = connection.fetchall()
    student_profile = report_data[0]
    report_data = report_data
    query_2 = "SELECT supervision.supv_type, supervision.staff_id, CONCAT(student.fname, ' ', student.lname) Name, CONCAT(staff.fname, ' ', staff.lname) staff_name \
               FROM supervision \
               left join student on supervision.student_id = student.student_id \
               right join staff on supervision.staff_id = staff.staff_id \
               where CONCAT(student.fname, ' ', student.lname) = %s \
               Order by staff.staff_id ASC"
    connection.execute(query_2, (student_name,))
    Supervisor_list = connection.fetchall()
    query_3 = "SELECT scholarship.scholarship_name, scholarship.scholarship_value, scholarship.scholarship_tenure, scholarship.scholarship_start_date, scholarship.scholarship_end_date, CONCAT(student.fname, ' ', student.lname) Name \
               FROM scholarship \
               left join student on scholarship.student_id = student.student_id \
               where CONCAT(student.fname, ' ', student.lname) = %s \
               Order by scholarship.scholarship_start_date DESC"
    connection.execute(query_3, (student_name,))
    Scholarship_list = connection.fetchall()
    query_4 = "SELECT E.company_name, E.employment_start_date, E.employment_end_date, CONCAT(student.fname, ' ', student.lname) Name \
               FROM employment E \
               left join student on E.student_id = student.student_id \
               where CONCAT(student.fname, ' ', student.lname) = %s \
               Order by E.employment_start_date DESC"
    connection.execute(query_4, (student_name,))
    Employment_list = connection.fetchall()
    return render_template('studentprofile.html', student_profile=student_profile, report_data=report_data, Supervisor_list=Supervisor_list, Scholarship_list=Scholarship_list, Employment_list=Employment_list)

### #11 Chair view supervisors

@chair_bp.route("/supervisorlist", methods=["GET", "POST"])
def SupervisorList():
    query = """
                SELECT S.staff_id, CONCAT(S.fname, ' ', S.lname) Name, S.phone, S.email_lu, S.room, D.dept_name 
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
    return render_template("supervisorlist.html", supervisorList=supervisorList)

def getprofile():
    username = session.get('username')
    # get basic profile which can not be edited
    query = f"SELECT * FROM staff WHERE email_lu = '{username}'"
    connection = getCursor()
    connection.execute(query)
    profile = connection.fetchone()
    return profile

@chair_bp.route("/section_e/<int:report_id>", methods=["GET", "POST"])
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
        return redirect(url_for('chair.view6MR'))
    
    return render_template("chair_section_e.html", profile=profile, student=student) 

@chair_bp.route("/6mr", methods=["GET", "POST"])
def view6MR():
    query = f"""
                SELECT s.student_id, 
                    concat(lname,' ',fname) student_name,
                    r.report_id,
                    concat(rept_term,' ',rept_year) rept_term,
                    due_date
                FROM student s
                INNER JOIN (SELECT * FROM report WHERE due_date = (SELECT max(due_date) FROM report)) r ON s.student_id = r.student_id -- select current report
                INNER JOIN report_progress rp ON r.report_id = rp.report_id 
                INNER JOIN (SELECT student_id, count(*) no_supvs FROM supervision GROUP BY student_id ) sp ON sp.student_id = s.student_id -- count no of supervisors
                WHERE 
                    s.student_id IN (SELECT student_id FROM supervision WHERE staff_id IN (SELECT staff_id FROM staff WHERE role = 'Convenor')) -- filter to convenor is supervisor
                    AND supervisors_completed = no_supvs -- filter to supervisor completed reports
                    AND convenor_completed = 0; 
            """
    connection = getCursor()
    connection.execute(query)
    reportList = connection.fetchall()
    return render_template("6MRlist.html", reportList=reportList)

@chair_bp.route("/view6mrdeatil/<int:report_id>/<int:student_id>", methods=["GET", "POST"])
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
    connection.execute("SELECT * FROM section_f WHERE report_id = %s",(report_id,))
    section_f = connection.fetchall()
    return render_template("chair_view6mrDetail.html", profile=profile, supervisors=supervisors, scholarship=scholarship, employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e,section_e_convenor=section_e_convenor,section_f=section_f)
    #return render_template("convenor_view6mrDetail.html", profile=profile, supervisors=supervisors, scholarship=scholarship, employment=employment)

#####↓↓↓↓↓ Yu-Tzu Chang ↓↓↓↓↓#####
@chair_bp.route("/status", methods=["GET", "POST"])
def viewStatus():
    cur = getCursor()
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
        conditions = []

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
        return render_template("chair_viewstatus.html", studentList=studentList,student_id=student_id,status=status,reportYear=reportYear,reportTerm=reportTerm,studentName=studentName,department=department)
    else:
        query += " WHERE r.rept_year = '2023' ORDER BY s.student_id"
        cur.execute(query)
        studentList = cur.fetchall()
        return render_template("chair_viewstatus.html",studentList=studentList)
    

@chair_bp.route("/viewSectionF", methods=["GET", "POST"])
def viewSectionF():
    query = """
                SELECT F.report_id, F.student_name, F.spvrs_names, F.comments, F.talk_to, F.date, F.chair_response, F.resp_date, R.student_id
                FROM section_f F
                LEFT JOIN report R ON F.report_id = R.report_id
                WHERE resp_date IS NULL
                """
    
    if request.method != "GET":
        pass

    connection = getCursor()
    connection.execute(query)
    sectionFList = connection.fetchall()
    connection.fetchall()
    return render_template("sectionFList.html", sectionFList=sectionFList)

@chair_bp.route("/respondSectionF/<int:report_id>", methods=["GET", "POST"])
def respondSectionF(report_id):
    if request.method == "POST":
        response = request.form.get('response')
        query = f"""
                    UPDATE section_f
                    SET chair_response = "{response}",
                        resp_date = NOW()
                    WHERE report_id = {report_id};
                """

        connection = getCursor()

        connection.execute(query)


        studentEmailQuery = f"""
                SELECT email_lu
                FROM student
                WHERE student_id = (
                SELECT R.student_id
                FROM section_f F
                LEFT JOIN report R ON F.report_id = R.report_id
                WHERE R.report_id = {report_id})
                """
        
        print(studentEmailQuery)
        connection.execute(studentEmailQuery)
        

        emailTitle = "Chair responded your section F"
        recipientsEmail = connection.fetchone()[0]
        print(recipientsEmail)
        bodyContent = "Chair has repoonded your section F"
        sendMail(emailTitle, recipientsEmail, bodyContent)

        return redirect(url_for('chair.viewSectionF'))
    
    return render_template("sectionFResponse.html", report_id=report_id)

@chair_bp.route("/status_report", methods=["GET", "POST"])
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
    return render_template("chair_status_report.html", dem = dem, dem_supvr_max_length = dem_supvr_max_length, dtss = dtss, dtss_supvr_max_length = dtss_supvr_max_length, sola = sola, sola_supvr_max_length = sola_supvr_max_length)



### Admin check faculty performance analysis report -- Frank ###
@chair_bp.route("/facultyperformancereport", methods=["GET", "POST"])
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
    return render_template("chair_facultyperformancereport.html", alldata=alldata,totaldata=totaldata)
