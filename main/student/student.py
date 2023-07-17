from flask import (flash, redirect, render_template, request, session, url_for)
from main.student import student_bp
from main.common import getCursor
from main.config import sendMail
import json

@student_bp.route("/")
def index():
    username = session.get('username')
    return render_template("student.html", username = username)

@student_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@student_bp.route("/employ", methods=["GET", "POST"])
def employ():
    profile = getprofile()
    # get employment info
    employ = getemploy()
    return render_template("employ.html", profile = profile, employ = employ)

@student_bp.route("/employ.edit/<int:em_id>")
def employedit(em_id):
    connection = getCursor()
    profile = getprofile()
     #get scholarship      
    connection.execute("SELECT * \
                            FROM employment \
                            WHERE empt_id = %s",(em_id,))
    employ=connection.fetchone()
    return render_template("employedit.html", profile = profile, employ = employ)

@student_bp.route("/semploy", methods=["GET", "POST"])
def semploy():
    profile = getprofile()
    studentid = getstudent_id()
    connection = getCursor()
    if request.method == 'POST':
        em_id = request.form.get('em_id')
        employment = request.form.get('employment')
        sdate = request.form.get('sdate')
        edate = request.form.get('edate')
        if em_id == '':
            # insert
            connection.execute("INSERT INTO employment (student_id,company_name,employment_start_date,employment_end_date ) VALUES(%s,%s,%s,%s);",(studentid[0], employment, sdate, edate or None,))
        #get scholarship      
            connection.execute("SELECT * \
                            FROM employment \
                            WHERE student_id = %s",(studentid[0],))
        
            employ=connection.fetchall()
            success_message = "Your employment saved successfully"
            return render_template("employ.html", profile = profile, employ = employ, success_message = success_message)

            
        else:
            connection.execute("UPDATE employment set company_name = %s , employment_start_date = %s, employment_end_date = %s where empt_id = %s;",(employment, sdate, edate or None, em_id))
            connection.execute("SELECT * \
                            FROM employment \
                            WHERE empt_id = %s",(em_id,))
            employ=connection.fetchone()
            success_message = "Your employment updated successfully"
            return render_template("employedit.html", profile = profile, employ = employ, success_message = success_message)
            
    else:
        return render_template("employedit.html", profile = profile ) 

@student_bp.route("/scholar")
def scholar():
    profile = getprofile()
    #get scholarship      
    scholar = getscholar() 
    return render_template("scholar.html", profile = profile, scholar = scholar)   

@student_bp.route("/scholaredit/<int:sid>")
def scholaredit(sid):
    connection = getCursor()
    profile = getprofile()
     #get scholarship      
    connection.execute("SELECT * \
                            FROM scholarship \
                            WHERE sola_id = %s",(sid,))
    scholarship=connection.fetchone()
    return render_template("scholaredit.html", profile = profile, scholarship = scholarship)

@student_bp.route("/savescholar", methods=["GET", "POST"])
def savescholar():
    profile = getprofile()
    connection = getCursor()
    studentid = getstudent_id()
    if request.method == 'POST':
        sid = request.form.get('solaid')
        scholar_name = request.form.get('scholar1')
        value = request.form.get('value1')
        tenure= request.form.get('tenure1')
        start= request.form.get('s1')
        end= request.form.get('e1')
        if sid==''or None:
            connection.execute("INSERT INTO scholarship (student_id,scholarship_name,scholarship_value,scholarship_tenure,scholarship_start_date,scholarship_end_date ) VALUES(%s,%s,%s,%s,%s,%s);",(studentid[0],scholar_name,value,tenure,start,end))
        #get scholarship      
            connection.execute("SELECT * \
                            FROM scholarship \
                            WHERE student_id = %s",(studentid[0],))
            scholarship=connection.fetchall()
            success_message = "Your scholarship saved successfully"
            return render_template("scholar.html", profile = profile, scholar = scholarship, success_message = success_message) 
        else:
            connection.execute("UPDATE scholarship set scholarship_name = %s, scholarship_value = %s, scholarship_tenure = %s, scholarship_start_date = %s, scholarship_end_date = %s where sola_id = %s;",(scholar_name,value,tenure,start,end,sid,))
            connection.execute("SELECT * \
                            FROM scholarship \
                            WHERE sola_id = %s",(sid,))
            scholarship=connection.fetchone()
            success_message = "Your scholarship updated successfully"
            return render_template("scholaredit.html", profile = profile, scholarship = scholarship, success_message = success_message)
    else:
        return render_template("scholaredit.html", profile = profile ) 

@student_bp.route("/super", methods=["GET", "POST"])
def super():
    profile = getprofile()
    # get the main supervisor list
    super1,super2,super3= getsuper()
    return render_template("super.html", profile = profile, super1 = super1, super2 = super2, super3 = super3)

# get basic profile
def getprofile():
    username = session.get('username')
    connection = getCursor()
    # get basic profile which can not be edited
    connection.execute("SELECT * \
                        FROM student s \
                        WHERE s.email_lu = %s",(username,))
    profile = connection.fetchall()
    return profile

# get reportid
def getreport_id():
    connection = getCursor()
    connection.execute("SELECT report_id\
                            FROM report   \
                            WHERE rept_year=%s and rept_term=%s and student_id = %s",('2023', 'JUNE', studentid[0],)) 
    reportid = connection.fetchone()
    return reportid

# get student id
def getstudent_id():
    username = session.get('username')
    connection = getCursor()
    # get student id first
    connection.execute("SELECT s.student_id \
                        FROM student s \
                        WHERE s.email_lu = %s",(username,))
    studentid = connection.fetchone()
    return studentid

# get report id
def getreport_id():
    connection = getCursor()
    studentid = getstudent_id()
    # get reportid
    connection.execute("SELECT report_id\
                            FROM report   \
                            WHERE rept_year = %s and rept_term = %s and student_id = %s",('2023', 'JUNE', studentid[0],)) 
    reportid = connection.fetchone()
    return reportid

# get supervisor
def getsuper():
    connection = getCursor()
    student_id = getstudent_id()
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
    
    # connection.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
    #                     FROM staff s left join supervision n on s.staff_id = n.staff_id\
    #                     WHERE n.student_id = %s AND n.supv_type = 'Co-Supervisor'",(student_id[0],))
    # super3=connection.fetchone()
    
    connection.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
                        FROM staff s left join supervision n on s.staff_id = n.staff_id\
                        WHERE n.student_id = %s AND n.supv_type = 'Other Supervisor'",(student_id[0],))
    super3=connection.fetchall()
    
    # connection.execute("SELECT concat(s.fname, ' ', s.lname)as main_name \
    #                     FROM staff s left join supervision n on s.staff_id = n.staff_id\
    #                     WHERE n.student_id = %s AND n.supv_type = 'Advisor'",(student_id[0],))
    # super5=connection.fetchone()
    return super1,super2,super3

# get employment info
def getemploy():
    connection = getCursor()
    student_id = getstudent_id()
    connection.execute("SELECT * \
                            FROM employment \
                            WHERE student_id = %s",(student_id[0],))
    employ = connection.fetchall()

    return employ

# get scholarship
def getscholar():
    connection = getCursor()
    student_id = getstudent_id()
    # get scholar id first
    connection.execute("SELECT * \
                            FROM scholarship \
                            WHERE student_id = %s",(student_id[0],))
    scholar = connection.fetchall()
    return scholar

#view the student's profile --Na
@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get('username') # Get the username from the session
    connection = getCursor()
    profile = getprofile()
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        address = request.form.get('address')
        otheremail = request.form.get('otheremail')
        # update profile
        connection.execute("UPDATE student set phone = %s , current_address = %s, email_other = %s where email_lu = %s ;",(phone,address,otheremail ,username,))
        # updated profile
        connection.execute("SELECT s.student_id, s.lname, s.fname, s.enrollment_date, s.current_address, s.phone, s.email_lu, s.email_other,s.part_full_time, s.dept_code \
                        FROM student s \
                        WHERE s.email_lu = %s",(username,)) 
        profile = connection.fetchall()
        success_message = "Your profile updated successfully"
        return render_template("profile.html", profile = profile, success_message = success_message )
    else:
        return render_template("profile.html", profile = profile)

@student_bp.route("/sectiona")
def sectiona():
    connection = getCursor()
    student_id = getstudent_id()
    # get basic profile which can not be edited
    profile = getprofile()
    # get supervisor
    super1,super2,super3 = getsuper()
    
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
    # create the new report if not exists check first
    connection.execute("SELECT report_id \
                            FROM report \
                            WHERE student_id = %s and rept_year=%s and rept_term=%s",(profile[0][0],'2023','JUNE'))
    result= connection.fetchone()
    if result== None:
        connection.execute("INSERT INTO report (student_id,rept_year, rept_term, due_date ) VALUES(%s,%s,%s,%s);",(student_id[0],'2023','JUNE','2023-06-30'))
    else:
        #    check if abcd done???
        report_id=getreport_id()
        connection.execute("SELECT student_abcd_completed \
                            FROM report_progress \
                            WHERE report_id = %s",(report_id[0],))
        complete = connection.fetchone()
        if complete[0]== 1:
            section_msg= "You have already submittd the from."
            return render_template("student.html", section_msg=section_msg)
        else:
        
            return render_template("section_a.html", profile=profile, super1=super1,super2=super2,super3=super3,scholarship=scholarship, employment=employment)
    
@student_bp.route('/save_sec_a', methods=['GET','POST'])   
def save_sec_a():
    section_msg= "Your draft saved successfully"
    return render_template("student.html", section_msg=section_msg)

#     connection = getCursor()
#     title = request.form.get('title')
#     scholar1 = request.form.get('scholar1')
#     value1 = request.form.get('value1')
#     tenure1 = request.form.get('tenure1')
#     enddate1 =request.form.get('enddate1')
#     scholar2 = request.form.get('scholar2')
#     value2 = request.form.get('value2')
#     tenure2 = request.form.get('tenure2')
#     enddate2 = request.form.get('enddate2')
#     teaching = request.form.get('teaching')
#     research = request.form.get('research')
#     employment = request.form.get('employment')
#     # check value1 , value2 empty
#     if value2 == '':
#         value2 = None
#     else:
#         value2=value2
#     if value1 == '':
#         value2 = None
#     else:
#         value1=value1
#     profile=getprofile()
#     name=profile[0][1] + profile[0][2]
#     # get supervisor
#     super1,super2,super3 = getsuper()
#     # check if it has history data
#     reportid=getreport_id()
#     connection.execute("SELECT thesis_title, scholarship_name_1,scholarship_value_1, scholarship_tenure_1,scholarship_end_date_1,  scholarship_name_2,scholarship_value_2, scholarship_tenure_2,scholarship_end_date_2, employment_teaching, employment_research, employment_other \
#                             FROM section_a s \
#                             WHERE report_id = %s",(reportid[0],))
#     section= connection.fetchall()
#     if len(section)==0:
#         connection.execute("INSERT INTO section_a (name, enrollmentdate, current_address,phone, email_lu,email_other,is_your_study,thesis_title,supervisor,asst_spvr, other_spvr_advr, scholarship_name_1, scholarship_value_1, scholarship_tenure_1, scholarship_end_date_1,scholarship_name_2, scholarship_value_2, scholarship_tenure_2, scholarship_end_date_2,employment_teaching, employment_research, employment_other ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(name,profile[0][3],profile[0][4],profile[0][5],profile[0][6],profile[0][7],profile[0][8],title,super1[0],super2[0],super3[0],scholar1,value1,tenure1,enddate1,scholar2,value2,tenure2,enddate2,teaching, research, employment, ))
#         section_msg="Your report saved successfully"
#         return render_template("student.html", section_a_msg=section_msg)
#     else:
#         connection.execute("UPDATE section_a set thesis_title=%s , scholarship_name_1=%s, scholarship_value_1=%s,  scholarship_tenure_1=%s,scholarship_end_date_1=%s,scholarship_name_2=%s,scholarship_value_2=%s,scholarship_tenure_2=%s,scholarship_end_date_2=%s,employment_teaching=%s,employment_research=%s,employment_other=%s where report_id=%s ;",(title,scholar1,value1,tenure1,enddate1,scholar2,value2,tenure2,enddate2,teaching, research, employment,reportid[0],))
#         section_msg= "Your report saved successfully"
#         return render_template("student.html", section_msg=section_msg)

# check b history
def check_b_history():
    connection = getCursor()
    reportid = getreport_id()
    connection.execute("SELECT inducion_completed_date,mutual_expec_completed_date,kaupapa_completed_date,intellectual_prop_completed_date,thesis_prop_completed_date,research_prop_completed_date,lu_pg_conference_completed_date,thesis_result_completed_date,human_ethics,health_and_safety,animal_ethics, insti_bio_safety,radiation_protection,reporting_box  \
                            FROM section_b s \
                            WHERE report_id = %s",(reportid[0],))
    sectionb = connection.fetchall()
    return sectionb

@student_bp.route("/sectionb",methods=["GET","POST"])
def sectionb():
    # save section A
    #  no need
    # get section B history
    sectionb = check_b_history()
    if len(sectionb) == 0:
        return render_template("section_b.html")
    else:
        return render_template("section_b.html",sectionb = sectionb)


def save_section_b(connection):
    induction = request.form.get('induction')
    mutual = request.form.get('mutual')
    maori = request.form.get('maori')
    intellectual = request.form.get('intellectual')
    thesis = request.form.get('thesis')
    research = request.form.get('research')
    conference = request.form.get('conference')
    seminar = request.form.get('seminar')
    human = request.form.get('human')
    health = request.form.get('health')
    animal = request.form.get('animal')
    institutional = request.form.get('institutional')
    radiation = request.form.get('radiation')
    report_box = request.form.get('report_box')

    reportid = getreport_id()
    sectionb = check_b_history()

    if len(sectionb) == 0:
        connection.execute(
            "INSERT INTO section_b (report_id, inducion_completed_date, mutual_expec_completed_date, kaupapa_completed_date, intellectual_prop_completed_date, thesis_prop_completed_date, research_prop_completed_date, lu_pg_conference_completed_date, thesis_result_completed_date, human_ethics, health_and_safety, animal_ethics, insti_bio_safety, radiation_protection, reporting_box) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                reportid[0],
                induction or None,
                mutual or None,
                maori or None,
                intellectual or None,
                thesis or None,
                research or None,
                conference or None,
                seminar or None,
                human,
                health,
                animal,
                institutional,
                radiation,
                report_box,
            ),
        )
        return "Your draft saved successfully"
    else:
        connection.execute(
            "UPDATE section_b SET inducion_completed_date=%s, mutual_expec_completed_date=%s, kaupapa_completed_date=%s, intellectual_prop_completed_date=%s, thesis_prop_completed_date=%s, research_prop_completed_date=%s, lu_pg_conference_completed_date=%s, thesis_result_completed_date=%s, human_ethics=%s, health_and_safety=%s, animal_ethics=%s, insti_bio_safety=%s, radiation_protection=%s, reporting_box=%s WHERE report_id=%s",
            (
                induction or None,
                mutual or None,
                maori or None,
                intellectual or None,
                thesis or None,
                research or None,
                conference or None,
                seminar or None,
                human,
                health,
                animal,
                institutional,
                radiation,
                report_box,
                reportid[0],
            ),
        )
        return "Your draft saved successfully"

@student_bp.route('/save_sec_b', methods=['GET', 'POST'])
def save_sec_b():
    connection = getCursor()
    section_msg = save_section_b(connection)
    return render_template("student.html", section_msg=section_msg)

# check c history
def check_c_history():
    connection = getCursor()
    reportid = getreport_id()
    connection.execute("SELECT access_principal,access_principal_comment,access_asst_other,access_asst_other_comment,expertise_principal,expertise_principal_comment,expertise_asst_other,expertise_asst_other_comment,quality_principal,quality_principal_comment,quality_asst_other,quality_asst_other_comment,timeless_principal,timeless_principal_comment,timeless_asst_other,timelessy_asst_other_comment,courses_available,courses_available_comment,workspace,workspace_comment,computer_facilities,computer_faci_comment,its_supt,its_supt_comment,research_software,research_software_comment,library_facilities,library_faci_comment,teach_Learn_supt,teach_Learn_supt_comment,statistical_supt,statistical_supt_comment,research_equip,research_equip_comment,technical_supt,technical_supt_comment,financial_resource,financial_resource_comment,other,other_comment,meeting_frequency,feedback_period,feedback_type \
                            FROM section_c s \
                            WHERE report_id = %s",(reportid[0],))
    sectionc= connection.fetchall()
    # Assuming you have retrieved the 'feedback' values from the database into a variable called 'feedback_data'
    # feedback_type = sectionc[0]['feedback_type']
    # # Split the 'feedback_data' into a list of individual values
    # feedback_type_values = feedback_type.split()
    
    # value1, value2, value3, value4 = feedback_values
    return sectionc

@student_bp.route("/sectionc", methods=["GET", "POST"])
def sectionc():
    connection = getCursor()
    # na

    # 
    # 
     # Check if the request came from the section_d route
    from_section_d = request.referrer.endswith("/section_d")

    if not from_section_d:
        section_msg = save_section_b(connection)
    
    # get section c history
    sectionc = check_c_history()
    if len(sectionc) == 0:
        return render_template("section_c.html")
    else:
        return render_template("section_c.html", sectionc = sectionc)

# save section c 
def save_section_c(connection):
    access_principal = request.form.get('access_principal')
    co_access_principal = request.form.get('co_access_principal')
    access_others = request.form.get('access_others')
    co_access_others = request.form.get('co_access_others')
    ex_principal = request.form.get('ex_principal')
    co_ex_principal = request.form.get('co_ex_principal')
    ex_others = request.form.get('ex_others')
    co_ex_others = request.form.get('co_ex_others')
    q_principal = request.form.get('q_principal')
    co_q_principal = request.form.get('co_q_principal')
    q_others = request.form.get('q_others')
    co_q_others = request.form.get('co_q_others')
    t_principal = request.form.get('t_principal')
    co_t_principal = request.form.get('co_t_principal')
    t_others = request.form.get('t_others')
    co_t_others = request.form.get('co_t_others')
    course = request.form.get('course')
    co_course = request.form.get('co_course')
    work = request.form.get('work')
    co_work= request.form.get('co_work')
    computer = request.form.get('computer')
    co_computer = request.form.get('co_computer')
    its = request.form.get('its')
    co_its = request.form.get('co_its')
    software = request.form.get('software')
    co_software = request.form.get('co_software')
    library = request.form.get('library')
    co_library = request.form.get('co_library')
    teaching = request.form.get('teaching')
    co_teaching = request.form.get('co_teaching')
    statistical = request.form.get('statistical')
    co_statistical = request.form.get('co_statistical')
    equip = request.form.get('equip')
    co_equip = request.form.get('co_equip')
    tech = request.form.get('tech')
    co_tech = request.form.get('co_tech')
    financial = request.form.get('financial')
    co_financial = request.form.get('co_financial')
    other = request.form.get('other')
    co_other = request.form.get('co_other')
    other = request.form.get('other')
    frequent = request.form.get('frequent')
    period = request.form.get('period')
    # multiple feedback!!!!!

    feedback = request.form.getlist('feedback')
    # Join the selected values into a single string
    feedback = ', '.join(feedback)
    # get report id 
    reportid = getreport_id()
    sectionc = check_c_history()
    # 44 columns
    if len(sectionc) == 0:
        connection.execute(
            "INSERT INTO section_c (report_id,access_principal,access_principal_comment,access_asst_other,access_asst_other_comment,expertise_principal,expertise_principal_comment,expertise_asst_other,expertise_asst_other_comment,quality_principal,quality_principal_comment,quality_asst_other,quality_asst_other_comment,timeless_principal,timeless_principal_comment,timeless_asst_other,timelessy_asst_other_comment,courses_available,courses_available_comment,workspace,workspace_comment,computer_facilities,computer_faci_comment,its_supt,its_supt_comment,research_software,research_software_comment,library_facilities,library_faci_comment,teach_Learn_supt,teach_Learn_supt_comment,statistical_supt,statistical_supt_comment,research_equip,research_equip_comment,technical_supt,technical_supt_comment,financial_resource,financial_resource_comment,other,other_comment,meeting_frequency,feedback_period,feedback_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)",
            (
                reportid[0],
                access_principal ,
                co_access_principal ,
                access_others ,
                co_access_others ,
                ex_principal ,
                co_ex_principal ,
                ex_others ,
                co_ex_others ,
                q_principal,
                co_q_principal,
                q_others,
                co_q_others,
                t_principal,
                co_t_principal,
                t_others,
                co_t_others,
                course,
                co_course,
                work,
                co_work,
                computer,
                co_computer,
                its,
                co_its,
                software,
                co_software,
                library,
                co_library,
                teaching,
                co_teaching,
                statistical ,
                co_statistical,
                equip,
                co_equip,
                tech,
                co_tech,
                financial,
                co_financial,
                other,
                co_other,
                frequent,
                period,
                feedback,
            ),
        )
        return "Your draft saved successfully"
    else:
        connection.execute(
            "UPDATE section_c SET access_principal=%s,access_principal_comment=%s,access_asst_other=%s,access_asst_other_comment=%s,expertise_principal=%s,expertise_principal_comment=%s,expertise_asst_other=%s,expertise_asst_other_comment=%s,quality_principal=%s,quality_principal_comment=%s,quality_asst_other=%s,quality_asst_other_comment=%s,timeless_principal=%s,timeless_principal_comment=%s,timeless_asst_other=%s,timelessy_asst_other_comment=%s,courses_available=%s,courses_available_comment=%s,workspace=%s,workspace_comment=%s,computer_facilities=%s,computer_faci_comment=%s,its_supt=%s,its_supt_comment=%s,research_software=%s,research_software_comment=%s,library_facilities=%s,library_faci_comment=%s,teach_Learn_supt=%s,teach_Learn_supt_comment=%s,statistical_supt=%s,statistical_supt_comment=%s,research_equip=%s,research_equip_comment=%s,technical_supt=%s,technical_supt_comment=%s,financial_resource=%s,financial_resource_comment=%s,other=%s,other_comment=%s,meeting_frequency=%s,feedback_period=%s,feedback_type=%s WHERE report_id=%s",
            (
                access_principal ,
                co_access_principal ,
                access_others ,
                co_access_others ,
                ex_principal ,
                co_ex_principal ,
                ex_others ,
                co_ex_others ,
                q_principal,
                co_q_principal,
                q_others,
                co_q_others,
                t_principal,
                co_t_principal,
                t_others,
                co_t_others,
                course,
                co_course,
                work,
                co_work,
                computer,
                co_computer,
                its,
                co_its,
                software,
                co_software,
                library,
                co_library,
                teaching,
                co_teaching,
                statistical ,
                co_statistical,
                equip,
                co_equip,
                tech,
                co_tech,
                financial,
                co_financial,
                other,
                co_other,
                frequent,
                period,
                feedback,
                reportid[0],
            ),
        )
        return "Your draft saved successfully"

@student_bp.route('/save_sec_c', methods=['GET','POST']) 
def save_sec_c():
    connection = getCursor()
    section_msg = save_section_c(connection)
    return render_template("student.html", section_msg=section_msg)

#####↓↓↓↓↓ Yu-Tzu Chang ↓↓↓↓↓#####
def check_d_history():
    cur = getCursor()
    reportid = getreport_id()
    cur.execute("SELECT * FROM section_d WHERE report_id = %s",(reportid[0],))
    section_d = cur.fetchall()
    return section_d

@student_bp.route("/section_d", methods=["GET", "POST"])
def section_d():
    # save section c first!!!
    cur = getCursor()
    section_msg = save_section_c(cur)
    # get d history!!
    section_d = check_d_history()
    if len(section_d) == 0:
        username = session.get('username')
        cur.execute("SELECT CONCAT(s.fname, ' ', s.lname) AS name FROM student s WHERE email_lu = %s", (username,))
        student_name = cur.fetchall()[0][0]
        return render_template("section_d.html", student_name = student_name)
    else:
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
        return render_template("section_d.html", section_d = section_d, t1_list = t1_list, t2_list = t2_list, t3_list = t3_list, t4_list = t4_list, t5_list = t5_list)

def save_section_d(cur):
    # retrieve section D part 1
    part_1_inputs1 = request.form.getlist('research_objectives')
    part_1_inputs2 = request.form.getlist('comments[]')
    part_1_dropdowns = request.form.getlist('status[]')
    part_1_comments = request.form.get('comment_part_1')
    part_1_json_data = []
    for i in range(len(part_1_inputs1)):
        data = {
            'research_objectives': part_1_inputs1[i],
            'comments': part_1_inputs2[i],
            'status': part_1_dropdowns[i]
        }
        part_1_json_data.append(data)
    t1 = json.dumps(part_1_json_data) # t1 is now JSON string
    
    # retrieve section D part 2
    part_2_inputs = request.form.getlist('section_d_part_2')
    part_2_json_data = []
    for i in range(len(part_2_inputs)):
        data = {'effects': part_2_inputs[i]}
        part_2_json_data.append(data)
    t2 = json.dumps(part_2_json_data) # t2 is now JSON string
    
    # retrieve section D part 3
    part_3_inputs = request.form.getlist('section_d_part_3')
    part_3_json_data = []
    for i in range(len(part_3_inputs)):
        data = {'achievements': part_3_inputs[i]}
        part_3_json_data.append(data)
    t3 = json.dumps(part_3_json_data) # t3 is now JSON string
    
    # retrieve section D part 4
    part_4_inputs1 = request.form.getlist('part_4_research_objectives')
    part_4_inputs2 = request.form.getlist('problems')
    part_4_dates = request.form.getlist('target_date')
    part_4_json_data = []
    for i in range(len(part_4_inputs1)):
        data = {
            'research_objectives': part_4_inputs1[i],
            'problems': part_4_inputs2[i],
            'target_date': part_4_dates[i]
        }
        part_4_json_data.append(data)
    t4 = json.dumps(part_4_json_data) # t4 is now JSON string
    
    # retrieve section D part 5
    part_5_inputs1 = request.form.getlist('item')
    part_5_inputs2 = request.form.getlist('amount')
    part_5_inputs3 = request.form.getlist('notes')
    part_5_comments = request.form.get('comment_part_5')
    part_5_json_data = []
    for i in range(len(part_5_inputs1)):
        data = {
            'item': part_5_inputs1[i],
            'amount': part_5_inputs2[i],
            'notes': part_5_inputs3[i]
        }
        part_5_json_data.append(data)
    t5 = json.dumps(part_5_json_data) # t5 is now JSON string
    
    student_name = request.form.get('student_name')
    report_date = request.form.get('report_date')
    
    cur = getCursor()
    section_d = check_d_history()
    report_id = getreport_id()[0]
    if len(section_d) == 0:
        query = "INSERT INTO section_d (report_id, t1, t1_comment, t2, t3, t4, t5, t5_comment, student_name, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        cur.execute(query, (report_id, t1, part_1_comments, t2, t3, t4, t5, part_5_comments, student_name, report_date))
        return "Your draft saved successfully"
    else:
        section_d_query = "UPDATE section_d SET t1 = %s, t1_comment = %s, t2 = %s, t3 = %s, t4 = %s, t5 = %s, t5_comment = %s, date = %s WHERE report_id = %s"
        cur.execute(section_d_query, (t1, part_1_comments, t2, t3, t4, t5, part_5_comments, report_date, report_id))
        return "Your draft saved successfully"

@student_bp.route('/save_sec_d', methods=['GET','POST']) 
def save_sec_d():
    cur = getCursor()
    section_msg = save_section_d(cur)
    return render_template("student.html", section_msg=section_msg)

@student_bp.route('/report_submit', methods=['GET','POST']) 
def report_submit():
    cur = getCursor()
    save_section_d(cur)
    report_id = getreport_id()[0]
    report_progress_query = "UPDATE report_progress SET student_abcd_completed = '1' WHERE report_id = %s"
    cur.execute(report_progress_query, (report_id,))
    section_msg = "Your report submitted successfully"
    # send email notification to main supervisor
    emailTitle = "Supervisee Complete 6MR"
    emailBody = "One of your supervisee has complete 6MR, please check in the system!"
    mainSuper = getsuper()[0][0]
    getMainSuperEmail = "SELECT email_lu FROM staff WHERE CONCAT(fname,' ', lname) = %s"
    cur.execute(getMainSuperEmail, (mainSuper,))
    mainSuperEmail = cur.fetchone()[0]
    sendMail(emailTitle, mainSuperEmail, emailBody)
    return render_template("student.html", section_msg=section_msg)

# view previous
@student_bp.route("/view")
def view():
    # only can check the completed ones!
    studentid = getstudent_id()
    profile = getprofile()
    connection = getCursor()
    # !!!!check the completed ones and then select all the completed ones
    connection.execute("SELECT r.report_id, r.student_id, r.rept_year, r.rept_term, r.due_date \
                            FROM report r left join report_progress p on r.report_id= p.report_id\
                            WHERE r.student_id= %s and full_report_completed='1'",(studentid[0],))
    report=connection.fetchall()
    return render_template("view.html", profile=profile,report=report)


@student_bp.route("/view6mreport/<int:report_id>", methods=["GET", "POST"])
def view6mreport(report_id):
    report_id=report_id
    print("<<<<<<<<", report_id)
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
    connection.execute("SELECT * FROM section_f WHERE report_id = %s",(report_id,))
    section_f = connection.fetchall()
    print("+++++", section_f)
    return render_template("view6mreport.html", profile=profile,super1=super1,super2=super2,super3=super3,scholarship=scholarship, employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e,section_e_convenor=section_e_convenor,section_f=section_f)



### Section F -- Frank

def sectionf_supervisors():
    username = session.get('username')
    connection = getCursor()
    # get student which can not be edited
    connection.execute("SELECT CONCAT(s.fname, ' ', s.lname) Name\
                        FROM student s \
                        WHERE s.email_lu = %s",(username,))
    student_name= connection.fetchall()
    student_name = student_name[0][0]
    query = "SELECT CONCAT(staff.fname, ' ', staff.lname) staff_name \
               FROM supervision \
               left join student on supervision.student_id = student.student_id \
               right join staff on supervision.staff_id = staff.staff_id \
               where CONCAT(student.fname, ' ', student.lname) = %s \
               Order by staff.staff_id ASC"
    connection.execute(query, (student_name,))
    supervisors = connection.fetchall()
    return supervisors 

def sectionabcd_result():
    connection = getCursor()
    # Check if section A to D is completed
    report_id = getreport_id()[0]
    connection.execute("SELECT student_abcd_completed FROM report_progress WHERE report_id = %s", (report_id,))
    sectionabcd_result = connection.fetchone()
    return sectionabcd_result

# check F history
def check_f_history():
    connection = getCursor()
    report_id = getreport_id()
    connection.execute("SELECT *  \
                            FROM section_f s \
                            WHERE report_id = %s",(report_id[0],))
    sectionf = connection.fetchall()
    return sectionf


@student_bp.route("/sectionf",methods=["GET","POST"])
def sectionf():
    username = session.get('username')
    connection = getCursor()
    sectionabcd_result_value = sectionabcd_result()
    if sectionabcd_result_value and sectionabcd_result_value[0] != 1:
        msg="Please fill up section A to D first before filling section F thanks"
        return render_template("student.html", msg=msg)
    else:
        sectionf = check_f_history()
        if len(sectionf) == 0:
           # get student which can not be edited
             connection.execute("SELECT CONCAT(s.fname, ' ', s.lname) Name\
                        FROM student s \
                        WHERE s.email_lu = %s",(username,))
             student_name = connection.fetchall()
             supervisors = sectionf_supervisors()
             return render_template("section_f.html", student_name=student_name, supervisors=supervisors)
        else:
           # get student which can not be edited
            connection.execute("SELECT CONCAT(s.fname, ' ', s.lname) Name\
                        FROM student s \
                        WHERE s.email_lu = %s",(username,))
            student_name = connection.fetchall()
            supervisors = sectionf_supervisors() 
            return render_template("section_f.html", student_name=student_name, supervisors=supervisors, sectionf=sectionf)



def save_section_f(connection, student_name):
    spvrs_name = request.form.getlist('spvrs_name[]')
    comments = request.form.get('comments')
    talk_to = request.form.get('talk_to')
    report_id = getreport_id()
    sectionf = check_f_history()

    if len(sectionf) == 0:
        connection.execute(
            "INSERT INTO section_f (report_id, student_name, spvrs_names, comments, talk_to, date) VALUES (%s, %s, %s, %s, %s, CURDATE())",
            (
              report_id[0], 
              student_name,
              ','.join(spvrs_name),
              comments, 
              talk_to
            ),
        )
        return "Data saved successfully."
    else:
        connection.execute(
            "UPDATE section_f SET student_name = %s, spvrs_names = %s, comments = %s, talk_to = %s, date = CURDATE() WHERE report_id = %s",
            (
               student_name, 
               ','.join(spvrs_name), 
               comments, 
               talk_to, 
               report_id[0]
            ),
        )
        return "Data saved successfully."



@student_bp.route('/save_sec_f', methods=['GET', 'POST'])
def save_sec_f():
    connection = getCursor()
    username = session.get('username')
    connection.execute("SELECT CONCAT(s.fname, ' ', s.lname) Name \
                        FROM student s \
                        WHERE s.email_lu = %s", (username,))
    student_name = connection.fetchone()[0]
    section_msg = save_section_f(connection, student_name)
    return render_template("student.html", section_msg=section_msg)


@student_bp.route('/sec_f_submit', methods=['GET', 'POST']) 
def sec_f_submit():
    connection = getCursor()
    save_sec_f()
    report_id = getreport_id()[0]
    sec_f_progress_query = "UPDATE report_progress SET student_f_completed = '1' WHERE report_id = %s"
    connection.execute(sec_f_progress_query, (report_id,))
    section_msg = "Section F submitted successfully"
    # send email notification to main supervisor
    emailTitle = "Supervisee Complete Section F in 6MR"
    emailBody = "One of your supervisees has completed Section F in 6MR, please check in the system!"
    getchairEmail = "SELECT email_lu FROM staff WHERE role = 'Postgraduate Chair'"
    connection.execute(getchairEmail)
    ChairEmail = connection.fetchone()[0]
    sendMail(emailTitle, ChairEmail, emailBody)
    return render_template("student.html", section_msg=section_msg)



# @student_bp.route("/view6mr/<int:report_id>", methods=["GET", "POST"])
# def view6mr(report_id):
#     report_id=report_id
#     connection = getCursor()
#     # section a to f
#     # get basic profile which can not be edited
#     profile = getprofile()

#     # get supervisor
#     super1,super2,super3 = getsuper()

#     # get scholalrship 
#     connection.execute("SELECT * \
#                             FROM scholarship \
#                             WHERE student_id = %s",(profile[0][0],))
#     scholarship= connection.fetchall()
#     # get employment
#     connection.execute("SELECT * \
#                             FROM employment \
#                             WHERE student_id = %s",(profile[0][0],))
#     employment= connection.fetchall()
#     # view b history
#     connection.execute("SELECT * FROM section_b WHERE report_id = %s",(report_id,))
#     section_b = connection.fetchall()

#     # view c
#     connection.execute("SELECT * FROM section_c WHERE report_id = %s",(report_id,))
#     section_c = connection.fetchall()
#     connection.execute("SELECT * FROM section_d WHERE report_id = %s",(report_id,))
#     section_d = connection.fetchall()
#     # # parse JSON string into Python objects
#     t1 = json.loads(section_d[0][1])
#     t2 = json.loads(section_d[0][3])
#     t3 = json.loads(section_d[0][4])
#     t4 = json.loads(section_d[0][5])
#     t5 = json.loads(section_d[0][6])
#     # convert Python objects into a list
#     t1_list = list(t1)
#     t2_list = list(t2)
#     t3_list = list(t3)
#     t4_list = list(t4)
#     t5_list = list(t5)
#     total_expenditure = 0
#     for t5 in t5:
#         total_expenditure += float(t5['amount'])
#     total_expenditure = '{:.0f}'.format(total_expenditure) #formatted the amount without decimal
#     connection.execute("SELECT * FROM section_e_spvrs WHERE report_id = %s",(report_id,))
#     section_e = connection.fetchall()
#     connection.execute("SELECT CONCAT(s.fname, ' ', s.lname) AS Name, e.date, e.comments, e.student_status FROM section_e_convenor e JOIN staff s ON s.staff_id = e.staff_id WHERE report_id = %s",(report_id,))
#     section_e_convenor = connection.fetchall()
#     connection.execute("SELECT * FROM section_f WHERE report_id = %s",(report_id,))
#     section_f = connection.fetchall()
#     return render_template("view6mr.html", profile=profile,super1=super1,super2=super2,super3=super3,scholarship=scholarship,employment=employment,section_b=section_b,section_c=section_c,section_d=section_d,t1_list=t1_list,t2_list=t2_list,t3_list=t3_list,t4_list=t4_list,t5_list=t5_list,total_expenditure=total_expenditure,section_e=section_e,section_e_convenor=section_e_convenor,section_f=section_f)