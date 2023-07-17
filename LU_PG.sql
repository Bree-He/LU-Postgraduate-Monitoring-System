/*
DROP SCHEMA IF EXISTS LU_PG_MONITOR;
*/

/*
DROP TABLE IF EXISTS SECTION_B;
DROP TABLE IF EXISTS SECTION_C;
DROP TABLE IF EXISTS SECTION_D;
DROP TABLE IF EXISTS SECTION_E_SPVRS;
DROP TABLE IF EXISTS SECTION_E_CONVENOR;
DROP TABLE IF EXISTS SECTION_F;
DROP TABLE IF EXISTS REPORT_PROGRESS;
DROP TABLE IF EXISTS REPORT;
DROP TABLE IF EXISTS SCHOLARSHIP;
DROP TABLE IF EXISTS EMPLOYMENT;
DROP TABLE IF EXISTS SUPERVISION;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS STUDENT;
DROP TABLE IF EXISTS STAFF;
DROP TABLE IF EXISTS DEPARTMENT;
*/



CREATE SCHEMA IF NOT EXISTS LU_PG_MONITOR;
USE LU_PG_MONITOR;

CREATE TABLE IF NOT EXISTS DEPARTMENT (
    dept_code VARCHAR(5) PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL,
    faculty_code VARCHAR(5) NOT NULL,
    faculty_name VARCHAR(50) NOT NULL
);

INSERT INTO DEPARTMENT (dept_code, dept_name, faculty_code, faculty_name)
VALUES 
('DEM', 'Department of Environmental Management', 'ESD', 'Faculty of Environment, Society and Design'),
('DTSS', 'Department of Tourism, Sport and Society', 'ESD', 'Faculty of Environment, Society and Design'),
('SOLA', 'School of Landscape Architecture', 'ESD', 'Faculty of Environment, Society and Design')
;


CREATE TABLE IF NOT EXISTS STAFF (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    lname VARCHAR(50) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL,
    employment_start_date DATE,
    employment_end_date DATE,
    room VARCHAR(200) NOT NULL,
    email_lu VARCHAR(50) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    dept_code VARCHAR(5),
    FOREIGN KEY (dept_code) REFERENCES DEPARTMENT(dept_code)
);

INSERT INTO STAFF (lname, fname, role, employment_start_date, room, email_lu, phone, dept_code)
VALUES 
('Anthony', 'Patricia', 'Postgraduate Chair', '2011-01-01', 'Landscape 031', 'yao.su@lincolnuni.ac.nz', '98846260226', NULL),
('Holyoake', 'Andrew', 'Postgraduate Director', '2003-01-01', 'Landscape 123', 'andrew.holyoake@lincoln.ac.nz', '56322064554', NULL),
('Broughton', 'Douglas', 'Postgraduate Administrator', '2015-01-01', 'Landscape 123', 'yu-tzu.chang@lincolnuni.ac.nz', '67472923655', NULL),
('Joe', 'John', 'Convenor', '2020-01-01','Room 101', 'frank.niu@lincolnuni.ac.nz', '1234567890', 'DEM'),
('Smith', 'Jane', 'Convenor', '2018-07-01', 'Room 202', 'janesmith@lincoln.ac.nz', '0987654321', 'DTSS'),
('Johnson', 'David', 'Convenor', '2021-09-01', 'Room 303', 'davidjohnson@lincoln.ac.nz', '9876543210', 'SOLA'),
('Jones', 'Mary', 'Supervisor', '2019-02-01', 'Room 404', 'bree.he@lincolnuni.ac.nz', '3456789012', 'DEM'),
('Lee', 'Mike', 'Supervisor', '2017-05-01', 'Room 505', 'mikelee@lincoln.ac.nz', '2345678901', 'DEM'),
('Nguyen', 'Hieu', 'Supervisor', '2022-01-01', 'Room 606', 'hieunguyen@lincoln.ac.nz', '4567890123', 'DEM'),
('Brown', 'Chris', 'Supervisor', '2021-03-01', 'Room 707', 'chrisbrown@lincoln.ac.nz', '3456789012', 'DEM'),
('Kim', 'Jin', 'Supervisor', '2018-06-01', 'Room 808', 'jinkim@lincoln.ac.nz', '2345678901', 'DEM'),
('Garcia', 'Maria', 'Supervisor', '2020-11-01', 'Room 909', 'mariagarcia@lincoln.ac.nz', '4567890123', 'DTSS'),
('Johnson', 'Sarah', 'Supervisor', '2017-09-01', 'Room 1010', 'sarahjohnson@lincoln.ac.nz', '7890123456', 'DTSS'),
('Wu', 'Yan', 'Supervisor', '2019-05-01', 'Room 1111', 'yanwu@lincoln.ac.nz', '8901234567', 'SOLA'),
('Gupta', 'Raj', 'Supervisor', '2016-08-01', 'Room 1212', 'rajgupta@lincoln.ac.nz', '9012345678', 'SOLA')
;


CREATE TABLE IF NOT EXISTS STUDENT (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    lname VARCHAR(50) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    enrollment_date DATE NOT NULL,
    current_address VARCHAR(200) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email_lu VARCHAR(50) NOT NULL UNIQUE,
    email_other VARCHAR(50) NOT NULL,
    part_full_time ENUM('Part time', 'Full time') NOT NULL,
    dept_code VARCHAR(5) NOT NULL,
    thesis_title VARCHAR(200) NOT NULL,
    FOREIGN KEY (dept_code) REFERENCES DEPARTMENT(dept_code)
);

INSERT INTO STUDENT (lname, fname, enrollment_date, current_address, phone, email_lu, email_other, part_full_time, dept_code, thesis_title)
VALUES
('Doe', 'John', '2021-01-15', '123 Main St, Anytown, NZ', '0214758593', 'na.bian@lincolnuni.ac.nz', 'johndoe@gmail.com', 'Full time', 'DEM', 'Theis Title 1'),
('Smith', 'Jane', '2021-01-15', '456 Maple St, Anytown, NZ', '022475475', 'janesmith@lincoln.ac.nz', 'janesmith@yahoo.com', 'Part time', 'DEM', 'Theis Title 2'),
('Nguyen', 'Hoa', '2021-02-01', '789 Oak St, Anytown, NZ', '0213698745', 'hoanguyen@lincoln.ac.nz', 'hoanguyen@yahoo.com', 'Full time', 'DEM', 'Theis Title 3'),
('Lee', 'Soo-Jin', '2021-02-01', '234 Elm St, Anytown, NZ', '0271234567', 'soojinlee@lincoln.ac.nz', 'soojinlee@hotmail.com', 'Part time', 'DEM', 'Theis Title 4'),
('Wilson', 'Mark', '2021-02-01', '345 Pine St, Anytown, NZ', '0219876543', 'markwilson@lincoln.ac.nz', 'mwilson@gmail.com', 'Full time', 'DTSS', 'Theis Title 5'),
('Chen', 'Yun', '2021-03-01', '567 Birch St, Anytown, NZ', '0279876543', 'yunchen@lincoln.ac.nz', 'yunchen@hotmail.com', 'Part time', 'DTSS', 'Theis Title 6'),
('Smith', 'Tom', '2021-03-01', '789 Cedar St, Anytown, NZ', '0217894561', 'tomsmith@lincoln.ac.nz', 'tomsmith@gmail.com', 'Full time', 'DTSS', 'Theis Title 7'),
('Takahashi', 'Ryota', '2021-04-01', '890 Ash St, Anytown, NZ', '0271112222', 'ryotatakahashi@lincoln.ac.nz', 'ryotatakahashi@yahoo.co.jp', 'Part time', 'DTSS', 'Theis Title 8'),
('Kim', 'Min-Jae', '2021-04-01', '123 Walnut St, Anytown, NZ', '0229876543', 'minjaekim@lincoln.ac.nz', 'minjaekim@gmail.com', 'Full time', 'SOLA', 'Theis Title 9'),
('Smith', 'Lisa', '2021-05-01', '456 Oak St, Anytown, NZ', '0273698521', 'lisasmith@lincoln.ac.nz', 'lisa_smith@yahoo.com', 'Part time', 'SOLA', 'Theis Title 10'),
('Gupta', 'Rajesh', '2021-05-01', '567 Elm St, Anytown, NZ', '0211112222', 'rajeshgupta@lincoln.ac.nz', 'rajeshgupta@gmail.com', 'Full time', 'SOLA', 'Theis Title 11'),
('Jones', 'Michael', '2021-06-01', '789 Pine St, Anytown, NZ', '0225556666', 'michaeljones@lincoln.ac.nz', 'mike_jones@yahoo.com', 'Part time', 'SOLA', 'Theis Title 12');


CREATE TABLE IF NOT EXISTS USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email_lu VARCHAR(50) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin_flag BOOLEAN NOT NULL
);

DROP TRIGGER IF EXISTS trg_user_email_lu;

DELIMITER //
CREATE TRIGGER trg_user_email_lu
BEFORE INSERT ON USER
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM STAFF WHERE email_lu = NEW.email_lu
        UNION ALL
        SELECT 1 FROM STUDENT WHERE email_lu = NEW.email_lu
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email_lu value';
    END IF;
END//
DELIMITER ;

INSERT INTO USER (email_lu, role, password, admin_flag)
VALUES 
('yao.su@lincolnuni.ac.nz', 'Postgraduate Chair', '$2b$12$PCZm4l5T9LB8JVT6MRwn2.xeOVHksK/PEbljg1q9KymofkJCTaN86', 1),
('andrew.holyoake@lincoln.ac.nz', 'Postgraduate Director', '$2b$12$vs/OZ/wRWPrgy.f4UZryWukyXbNXMRn0FROMUHL2smw9V9nkeFHMK', 1),
('yu-tzu.chang@lincolnuni.ac.nz', 'Postgraduate Administrator', '$2b$12$o0ADyYFuuZGaB7x9jn6IfedfJO7IbvG.SiQuIBAjjoZ/LIN1rfocu', 1),
('davidjohnson@lincoln.ac.nz', 'Convenor', '$2b$12$G23d4FjZnczJ1pjRe3uiOeK7uv3xAMV050W9qZrlApqLX.99GyRi.', 1),
('frank.niu@lincolnuni.ac.nz', 'Convenor', '$2b$12$TX/ae0Zp1DvEjEZT4w6HHu6Xyn1HDge0o6DW71GAFGuSeBQ/S8J8O', 1),
('bree.he@lincolnuni.ac.nz', 'Supervisor', '$2b$12$PjwRidUlOZx1xhRoR5pxo.5/bnzLu0X3WrqZVUm6Ds8H7.hln87tq', 1),
('na.bian@lincolnuni.ac.nz', 'Student', '$2b$12$CsZ75vIrrjTiDxMvuwmvUOZwHEz8xcAlZqrd/FiQu8YMh7xZdEInG', 1),
('mikelee@lincoln.ac.nz','Supervisor','$2b$12$0PBObjx4l5nBXe4wmtWbuuawXxr8e7raLCPFslhAaDQx4A6ENLCDa',1),
('janesmith@lincoln.ac.nz','Student','$2b$12$UWWBbeujGxYtiz1JIe6Q5OB0DXl6ERkQVvYD7CvkRVjs8uefUcL4a',0),
('hoanguyen@lincoln.ac.nz','Student','$2b$12$oY4fo7b.XJeGllwZkmQslePrbAzneQQdyZrn.o/9dV5nr48GlZKeC',0)
;


CREATE TABLE IF NOT EXISTS SUPERVISION (
    supervision_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    staff_id INT NOT NULL,
    supv_type ENUM('Main Supervisor', 'Associate Supervisor', 'Other Supervisor') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id)
);

INSERT INTO SUPERVISION (student_id, staff_id, supv_type) VALUES
(1, 4, 'Main Supervisor'),
(1, 7, 'Associate Supervisor'),
(1, 8, 'Other Supervisor'),
(1, 9, 'Other Supervisor'),
(2, 7, 'Main Supervisor'),
(2, 8, 'Associate Supervisor'),
(2, 9, 'Other Supervisor'),
(2, 10, 'Other Supervisor'),
(2, 11, 'Other Supervisor'),
(3, 8, 'Main Supervisor'),
(3, 11, 'Associate Supervisor'),
(4, 4, 'Main Supervisor'),
(4, 10, 'Associate Supervisor'),
(4, 7, 'Other Supervisor'),
(5, 11, 'Main Supervisor'),
(6, 12, 'Main Supervisor'),
(6, 13, 'Associate Supervisor'),
(7, 13, 'Main Supervisor'),
(7, 12, 'Associate Supervisor'),
(8, 12, 'Main Supervisor'),
(8, 5, 'Associate Supervisor'),
(9, 14, 'Main Supervisor'),
(9, 15, 'Associate Supervisor'),
(10, 6, 'Main Supervisor'),
(10, 15, 'Associate Supervisor'),
(11, 14, 'Main Supervisor'),
(11, 15, 'Associate Supervisor'),
(12, 14, 'Main Supervisor'),
(12, 15, 'Associate Supervisor')
;


CREATE TABLE IF NOT EXISTS SCHOLARSHIP (
    sola_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    scholarship_name VARCHAR(50) NOT NULL,
    scholarship_value DECIMAL(10, 2) NOT NULL,
    scholarship_tenure VARCHAR(100) NOT NULL,
    scholarship_start_date DATE NOT NULL,
    scholarship_end_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

INSERT INTO SCHOLARSHIP (student_id, scholarship_name, scholarship_value, scholarship_tenure, scholarship_start_date, scholarship_end_date) 
VALUES
(1, 'Merit Scholarship', 5000.00, 'One academic year', '2021-05-01', '2022-04-30'),
(1, 'Need-Based Scholarship', 2500.00, 'One semester', '2022-05-01', '2023-08-15'),
(1, 'Community Service Scholarship', 5000.00, 'One semester', '2023-01-01', '2023-05-15'),
(1, 'Music Scholarship', 3500.00, 'One academic year', '2023-06-01', '2024-05-31'),
(2, 'Athletic Scholarship', 7500.00, 'Full four-year program', '2020-06-01', '2024-05-31'),
(3, 'STEM Scholarship', 10000.00, 'Two academic years', '2021-08-01', '2023-05-31'),
(3, 'Music Scholarship', 3500.00, 'One academic year', '2023-06-01', '2024-05-31'),
(3, 'Community Service Scholarship', 5000.00, 'One semester', '2023-01-01', '2023-05-15'),
(3, 'Research Scholarship', 6000.00, 'Summer program', '2022-11-21', '2023-01-31'),
(4, 'STEM Scholarship', 10000.00, 'Two academic years', '2022-08-01', '2024-05-31'),
(5, 'Community Service Scholarship', 2000.00, 'One academic year', '2023-08-01', '2024-05-31'),
(6, 'Fine Arts Scholarship', 5000.00, 'One academic year', '2023-08-01', '2024-05-31'),
(7, 'International Student Scholarship', 7500.00, 'One academic year', '2022-08-01', '2023-05-31'),
(8, 'Underrepresented Minority Scholarship', 3000.00, 'One academic year', '2023-08-01', '2024-05-31'),
(9, 'Military Service Scholarship', 10000.00, 'Full four-year program', '2020-08-01', '2024-05-31'),
(10, 'Research Fellowship', 5000.00, 'One academic year', '2022-08-01', '2023-05-31'),
(11, 'Entrepreneurship Scholarship', 5000.00, 'One academic year', '2023-08-01', '2024-05-31'),
(12, 'Research Scholarship', 6000.00, 'Summer program', '2022-11-21', '2023-01-31')
;


CREATE TABLE IF NOT EXISTS EMPLOYMENT (
    empt_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    company_name VARCHAR(50) NOT NULL,
    employment_start_date DATE NOT NULL,
    employment_end_date DATE,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

INSERT INTO EMPLOYMENT (student_id, company_name, employment_start_date, employment_end_date) 
VALUES
(1, 'ABC Company', '2021-06-01', '2022-05-31'),
(1, '456 Solutions', '2022-01-01', '2022-06-30'),
(1, 'XYZ Corporation', '2023-01-15', NULL),
(2, '123 Industries', '2021-09-01', '2022-05-31'),
(2, 'DEF Corporation', '2021-08-15', '2022-08-14'),
(2, 'Acme Inc.', '2023-02-01', NULL),
(3, 'DEF Corporation', '2021-08-15', '2022-08-14'),
(3, 'GHI Enterprises', '2022-06-01', '2022-12-31'),
(4, 'JKL Corporation', '2023-05-01', NULL),
(5, '789 Industries', '2022-03-01', '2022-08-31'),
(6, 'MNO Corporation', '2021-11-01', '2022-05-31')
;


CREATE TABLE IF NOT EXISTS REPORT (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    rept_year YEAR NOT NULL,  
    rept_term ENUM('JUNE', 'DEC') NOT NULL,
    due_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
);

INSERT INTO REPORT (student_id, rept_year, rept_term, due_date)
VALUES
(1, 2022, 'DEC', '2022-12-31'),
(2, 2022, 'DEC', '2022-12-31'),
(3, 2022, 'DEC', '2022-12-31'),
(4, 2022, 'DEC', '2022-12-31'),
(5, 2022, 'DEC', '2022-12-31'),
(6, 2022, 'DEC', '2022-12-31'),
(9, 2022, 'DEC', '2022-12-31'),
(1, 2023, 'JUNE', '2023-06-30'),
(2, 2023, 'JUNE', '2023-06-30'),
(3, 2023, 'JUNE', '2023-06-30'),
(4, 2023, 'JUNE', '2023-06-30'),
(5, 2023, 'JUNE', '2023-06-30'),
(6, 2023, 'JUNE', '2023-06-30'),
(9, 2023, 'JUNE', '2023-06-30')
;


CREATE TABLE IF NOT EXISTS REPORT_PROGRESS (
    report_id INT PRIMARY KEY,
    student_abcd_completed BOOLEAN,
    student_f_completed BOOLEAN,
    supervisor_approved BOOLEAN,
    supervisors_completed INT,
    convenor_completed BOOLEAN,
    full_report_completed BOOLEAN,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id)
);

INSERT INTO REPORT_PROGRESS (report_id, student_abcd_completed, student_f_completed, supervisor_approved, supervisors_completed, convenor_completed, full_report_completed)
VALUES
-- previous reports
(1, 1, 0, 1, 4, 1, 1),
(2, 1, 0, 1, 5, 1, 1),
(3, 1, 0, 1, 2, 1, 1),
(4, 1, 0, 1, 3, 1, 1),
(5, 1, 0, 1, 1, 1, 1),
(6, 1, 0, 1, 2, 1, 1),
(7, 1, 0, 1, 2, 1, 1),
-- current reports
(8, 1, 1, 1, 4, 0, 0), -- waiting for convenor to complete section E; convenor is sup so pass to chair)
(9, 1, 0, 1, 3, 0, 0), -- waiting for sup to complete E (total 5 spvs)
(10, 1, 0, 0, 0, 0, 0), -- waiting for sup to approve a-c
(11, 0, 0, 0, 0, 0, 0), -- waiting for std to complete a-c
(12, 1, 1, 1, 1, 1, 0), -- waiting for admin to mark report complete
(13, 1, 1, 1, 2, 1, 1),-- report complete
(14, 1, 0, 1, 2, 1, 0) -- waiting for or admin to mark report complete
;


CREATE TABLE IF NOT EXISTS SECTION_B (
    report_id INT PRIMARY KEY,
    inducion_completed_date DATE,
    mutual_expec_completed_date DATE,
    kaupapa_completed_date DATE,
    intellectual_prop_completed_date DATE,
    thesis_prop_completed_date DATE,
    research_prop_completed_date DATE,
    lu_pg_conference_completed_date DATE,
    thesis_result_completed_date DATE,
    human_ethics ENUM('Needed', 'Approved', 'Not Needed') NOT NULL,
    health_and_safety ENUM('Needed', 'Approved', 'Not Needed') NOT NULL,
    animal_ethics ENUM('Needed', 'Approved', 'Not Needed') NOT NULL,
    insti_bio_safety ENUM('Needed', 'Approved', 'Not Needed') NOT NULL,
    radiation_protection ENUM('Needed', 'Approved', 'Not Needed') NOT NULL,
    reporting_box ENUM('1', '2', '3','4', '5', '6') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id)
);

INSERT INTO SECTION_B (report_id, inducion_completed_date, mutual_expec_completed_date, kaupapa_completed_date, intellectual_prop_completed_date, thesis_prop_completed_date, research_prop_completed_date, lu_pg_conference_completed_date, thesis_result_completed_date, human_ethics, health_and_safety, animal_ethics, insti_bio_safety, radiation_protection, reporting_box)
VALUES
    (1, '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', 'Needed', 'Needed', 'Needed', 'Needed', 'Needed', '1'),
    (2, '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', 'Approved', 'Approved', 'Approved', 'Approved', 'Approved', '1'),
    (3, '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', '1'),
	(4, '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', 'Needed', 'Needed', 'Needed', 'Needed', 'Needed', '1'),
    (5, '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', '2022-12-28', 'Approved', 'Approved', 'Approved', 'Approved', 'Approved', '1'),
    (6, '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', '2022-12-27', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', '1'),
    (7, '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', '2022-12-29', 'Needed', 'Needed', 'Needed', 'Needed', 'Needed', '1'),
    (8, '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', 'Needed', 'Needed', 'Needed', 'Needed', 'Needed', '2'),
    (9, '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', 'Approved', 'Approved', 'Approved', 'Approved', 'Approved', '2'),
    (10, '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', '2'),
	(12, '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', '2023-05-29', 'Needed', 'Needed', 'Needed', 'Needed', 'Needed', '2'),
    (13, '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', '2023-05-28', 'Approved', 'Approved', 'Approved', 'Approved', 'Approved', '2'),
    (14, '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', '2023-05-27', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', 'Not Needed', '2')
    ;


CREATE TABLE IF NOT EXISTS SECTION_C (
    report_id INT PRIMARY KEY,
    access_principal ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    access_principal_comment TEXT,
    access_asst_other ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    access_asst_other_comment TEXT,
    expertise_principal ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    expertise_principal_comment TEXT,
    expertise_asst_other ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    expertise_asst_other_comment TEXT,
    quality_principal ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    quality_principal_comment TEXT,
    quality_asst_other ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    quality_asst_other_comment TEXT,
    timeless_principal ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    timeless_principal_comment TEXT,
    timeless_asst_other ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    timelessy_asst_other_comment TEXT,
    courses_available ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    courses_available_comment TEXT,
    workspace ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    workspace_comment TEXT,
    computer_facilities ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    computer_faci_comment TEXT,
    its_supt ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    its_supt_comment TEXT,
    research_software ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    research_software_comment TEXT,
    library_facilities ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    library_faci_comment TEXT,
    teach_Learn_supt ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    teach_Learn_supt_comment TEXT,
    statistical_supt ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    statistical_supt_comment TEXT,
    research_equip ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    research_equip_comment TEXT,
    technical_supt ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    technical_supt_comment TEXT,
    financial_resource ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    financial_resource_comment TEXT,
    other ENUM('Very Good', 'Good', 'Satisfactory','Unsatisfactory', 'Not Relevant') NOT NULL,
    other_comment TEXT,
    meeting_frequency ENUM('Weekly', 'Fortnightly', 'Monthly','Every 3 months', 'Half yearly', 'Not at all') NOT NULL,
    feedback_period ENUM('1 week', '2 weeks', '1 month', '3months') NOT NULL,
    feedback_type TEXT NOT NULL,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id)
);

INSERT INTO SECTION_C (report_id, access_principal, access_principal_comment, access_asst_other, access_asst_other_comment, expertise_principal, expertise_principal_comment, expertise_asst_other, expertise_asst_other_comment, quality_principal, quality_principal_comment, quality_asst_other, quality_asst_other_comment, timeless_principal, timeless_principal_comment, timeless_asst_other, timelessy_asst_other_comment, courses_available, courses_available_comment, workspace, workspace_comment, computer_facilities, computer_faci_comment, its_supt, its_supt_comment, research_software, research_software_comment, library_facilities, library_faci_comment, teach_Learn_supt, teach_Learn_supt_comment, statistical_supt, statistical_supt_comment, research_equip, research_equip_comment, technical_supt, technical_supt_comment, financial_resource, financial_resource_comment, other, other_comment, meeting_frequency, feedback_period, feedback_type)
VALUES
    (1, 'Very Good', 'Access principal comment for report ID 1', 'Very Good', 'Access assistant/other comment for report ID 1', 'Good', 'Expertise principal comment for report ID 1', 'Good', 'Expertise assistant/other comment for report ID 1', 'Satisfactory', 'Quality principal comment for report ID 1', 'Satisfactory', 'Quality assistant/other comment for report ID 1', 'Very Good', 'Timeless principal comment for report ID 1', 'Good', 'Timeless assistant/other comment for report ID 1', 'Good', 'Courses available comment for report ID 1', 'Very Good', 'Workspace comment for report ID 1', 'Good', 'Computer facilities comment for report ID 1', 'Satisfactory', 'IT support comment for report ID 1', 'Good', 'Research software comment for report ID 1', 'Satisfactory', 'Library facilities comment for report ID 1', 'Satisfactory', 'Teaching and learning support comment for report ID 1', 'Very Good', 'Statistical support comment for report ID 1', 'Good', 'Research equipment comment for report ID 1', 'Good', 'Technical support comment for report ID 1', 'Very Good', 'Financial resource comment for report ID 1', 'Not Relevant', 'Other comment for report ID 1', 'Weekly', '1 week', 'Softcopy'),
    (2, 'Good', 'Access principal comment for report ID 2', 'Very Good', 'Access assistant/other comment for report ID 2', 'Very Good', 'Expertise principal comment for report ID 2', 'Good', 'Expertise assistant/other comment for report ID 2', 'Good', 'Quality principal comment for report ID 2', 'Satisfactory', 'Quality assistant/other comment for report ID 2', 'Good', 'Timeless principal comment for report ID 2', 'Very Good', 'Timeless assistant/other comment for report ID 2', 'Satisfactory', 'Courses available comment for report ID 2', 'Satisfactory', 'Workspace comment for report ID 2', 'Very Good', 'Computer facilities comment for report ID 2', 'Good', 'IT support comment for report ID 2', 'Satisfactory', 'Research software comment for report ID 2', 'Good', 'Library facilities comment for report ID 2', 'Satisfactory', 'Teaching and learning support comment for report ID 2', 'Good', 'Statistical support comment for report ID 2', 'Good', 'Research equipment comment for report ID 2', 'Satisfactory', 'Technical support comment for report ID 2', 'Good', 'Financial resource comment for report ID 2', 'Not Relevant', 'Other comment for report ID 2', 'Fortnightly', '2 weeks', 'Softcopy'),
    (3, 'Satisfactory', 'Access principal comment for report ID 3', 'Good', 'Access assistant/other comment for report ID 3', 'Good', 'Expertise principal comment for report ID 3', 'Very Good', 'Expertise assistant/other comment for report ID 3', 'Very Good', 'Quality principal comment for report ID 3', 'Good', 'Quality assistant/other comment for report ID 3', 'Satisfactory', 'Timeless principal comment for report ID 3', 'Satisfactory', 'Timeless assistant/other comment for report ID 3', 'Very Good', 'Courses available comment for report ID 3', 'Very Good', 'Workspace comment for report ID 3', 'Good', 'Computer facilities comment for report ID 3', 'Good', 'IT support comment for report ID 3', 'Good', 'Research software comment for report ID 3', 'Good', 'Library facilities comment for report ID 3', 'Good', 'Teaching and learning support comment for report ID 3', 'Good', 'Statistical support comment for report ID 3', 'Very Good', 'Research equipment comment for report ID 3', 'Very Good', 'Technical support comment for report ID 3', 'Good', 'Financial resource comment for report ID 3', 'Not Relevant', 'Other comment for report ID 3', 'Monthly', '1 month', 'Softcopy'),
    (4, 'Unsatisfactory', 'Access principal comment for report ID 4', 'Unsatisfactory', 'Access assistant/other comment for report ID 4', 'Satisfactory', 'Expertise principal comment for report ID 4', 'Satisfactory', 'Expertise assistant/other comment for report ID 4', 'Very Good', 'Quality principal comment for report ID 4', 'Good', 'Quality assistant/other comment for report ID 4', 'Good', 'Timeless principal comment for report ID 4', 'Good', 'Timeless assistant/other comment for report ID 4', 'Good', 'Courses available comment for report ID 4', 'Good', 'Workspace comment for report ID 4', 'Satisfactory', 'Computer facilities comment for report ID 4', 'Satisfactory', 'IT support comment for report ID 4', 'Good', 'Research software comment for report ID 4', 'Satisfactory', 'Library facilities comment for report ID 4', 'Very Good', 'Teaching and learning support comment for report ID 4', 'Good', 'Statistical support comment for report ID 4', 'Good', 'Research equipment comment for report ID 4', 'Good', 'Technical support comment for report ID 4', 'Good', 'Financial resource comment for report ID 4', 'Not Relevant', 'Other comment for report ID 4', 'Every 3 months', '3months', 'Softcopy'),
    (5, 'Not Relevant', 'Access principal comment for report ID 5', 'Very Good', 'Access assistant/other comment for report ID 5', 'Not Relevant', 'Expertise principal comment for report ID 5', 'Very Good', 'Expertise assistant/other comment for report ID 5', 'Satisfactory', 'Quality principal comment for report ID 5', 'Good', 'Quality assistant/other comment for report ID 5', 'Unsatisfactory', 'Timeless principal comment for report ID 5', 'Unsatisfactory', 'Timeless assistant/other comment for report ID 5', 'Good', 'Courses available comment for report ID 5', 'Good', 'Workspace comment for report ID 5', 'Satisfactory', 'Computer facilities comment for report ID 5', 'Unsatisfactory', 'IT support comment for report ID 5', 'Unsatisfactory', 'Research software comment for report ID 5', 'Very Good', 'Library facilities comment for report ID 5', 'Very Good', 'Teaching and learning support comment for report ID 5', 'Satisfactory', 'Statistical support comment for report ID 5', 'Good', 'Research equipment comment for report ID 5', 'Good', 'Technical support comment for report ID 5', 'Good', 'Financial resource comment for report ID 5', 'Very Good', 'Other comment for report ID 5', 'Half yearly', '1 month', 'Softcopy'),
    (6, 'Satisfactory', 'Access principal comment for report ID 6', 'Good', 'Access assistant/other comment for report ID 6', 'Good', 'Expertise principal comment for report ID 6', 'Very Good', 'Expertise assistant/other comment for report ID 6', 'Satisfactory', 'Quality principal comment for report ID 6', 'Good', 'Quality assistant/other comment for report ID 6', 'Good', 'Timeless principal comment for report ID 6', 'Good', 'Timeless assistant/other comment for report ID 6', 'Good', 'Courses available comment for report ID 6', 'Good', 'Workspace comment for report ID 6', 'Good', 'Computer facilities comment for report ID 6', 'Good', 'IT support comment for report ID 6', 'Very Good', 'Research software comment for report ID 6', 'Satisfactory', 'Library facilities comment for report ID 6', 'Very Good', 'Teaching and learning support comment for report ID 6', 'Good', 'Statistical support comment for report ID 6', 'Good', 'Research equipment comment for report ID 6', 'Good', 'Technical support comment for report ID 6', 'Satisfactory', 'Financial resource comment for report ID 6', 'Not Relevant', 'Other comment for report ID 6', 'Not at all', '2 weeks', 'Softcopy'),
    (7, 'Unsatisfactory', 'Access principal comment for report ID 7', 'Unsatisfactory', 'Access assistant/other comment for report ID 7', 'Satisfactory', 'Expertise principal comment for report ID 7', 'Satisfactory', 'Expertise assistant/other comment for report ID 7', 'Very Good', 'Quality principal comment for report ID 7', 'Good', 'Quality assistant/other comment for report ID 7', 'Good', 'Timeless principal comment for report ID 7', 'Good', 'Timeless assistant/other comment for report ID 7', 'Good', 'Courses available comment for report ID 7', 'Good', 'Workspace comment for report ID 7', 'Satisfactory', 'Computer facilities comment for report ID 7', 'Satisfactory', 'IT support comment for report ID 7', 'Good', 'Research software comment for report ID 7', 'Satisfactory', 'Library facilities comment for report ID 7', 'Very Good', 'Teaching and learning support comment for report ID 7', 'Good', 'Statistical support comment for report ID 7', 'Good', 'Research equipment comment for report ID 7', 'Good', 'Technical support comment for report ID 7', 'Good', 'Financial resource comment for report ID 7', 'Not Relevant', 'Other comment for report ID 7', 'Every 3 months', '3months', 'Softcopy'),
	  (8, 'Very Good', 'Access principal comment for report ID 8', 'Very Good', 'Access assistant/other comment for report ID 8', 'Good', 'Expertise principal comment for report ID 8', 'Good', 'Expertise assistant/other comment for report ID 8', 'Satisfactory', 'Quality principal comment for report ID 8', 'Satisfactory', 'Quality assistant/other comment for report ID 8', 'Very Good', 'Timeless principal comment for report ID 8', 'Good', 'Timeless assistant/other comment for report ID 8', 'Good', 'Courses available comment for report ID 8', 'Very Good', 'Workspace comment for report ID 8', 'Good', 'Computer facilities comment for report ID 8', 'Satisfactory', 'IT support comment for report ID 8', 'Good', 'Research software comment for report ID 8', 'Satisfactory', 'Library facilities comment for report ID 8', 'Satisfactory', 'Teaching and learning support comment for report ID 8', 'Very Good', 'Statistical support comment for report ID 8', 'Good', 'Research equipment comment for report ID 8', 'Good', 'Technical support comment for report ID 8', 'Very Good', 'Financial resource comment for report ID 8', 'Not Relevant', 'Other comment for report ID 8', 'Weekly', '1 week', 'Softcopy'),
    (9, 'Good', 'Access principal comment for report ID 9', 'Very Good', 'Access assistant/other comment for report ID 9', 'Very Good', 'Expertise principal comment for report ID 9', 'Good', 'Expertise assistant/other comment for report ID 9', 'Good', 'Quality principal comment for report ID 9', 'Satisfactory', 'Quality assistant/other comment for report ID 9', 'Good', 'Timeless principal comment for report ID 9', 'Very Good', 'Timeless assistant/other comment for report ID 9', 'Satisfactory', 'Courses available comment for report ID 9', 'Satisfactory', 'Workspace comment for report ID 9', 'Very Good', 'Computer facilities comment for report ID 9', 'Good', 'IT support comment for report ID 9', 'Satisfactory', 'Research software comment for report ID 9', 'Good', 'Library facilities comment for report ID 9', 'Satisfactory', 'Teaching and learning support comment for report ID 9', 'Good', 'Statistical support comment for report ID 9', 'Good', 'Research equipment comment for report ID 9', 'Satisfactory', 'Technical support comment for report ID 9', 'Good', 'Financial resource comment for report ID 9', 'Not Relevant', 'Other comment for report ID 9', 'Fortnightly', '2 weeks', 'Softcopy'),
    (10, 'Satisfactory', 'Access principal comment for report ID 10', 'Good', 'Access assistant/other comment for report ID 10', 'Good', 'Expertise principal comment for report ID 10', 'Very Good', 'Expertise assistant/other comment for report ID 10', 'Very Good', 'Quality principal comment for report ID 10', 'Good', 'Quality assistant/other comment for report ID 10', 'Satisfactory', 'Timeless principal comment for report ID 10', 'Satisfactory', 'Timeless assistant/other comment for report ID 10', 'Very Good', 'Courses available comment for report ID 10', 'Very Good', 'Workspace comment for report ID 10', 'Good', 'Computer facilities comment for report ID 10', 'Good', 'IT support comment for report ID 10', 'Good', 'Research software comment for report ID 10', 'Good', 'Library facilities comment for report ID 10', 'Good', 'Teaching and learning support comment for report ID 10', 'Good', 'Statistical support comment for report ID 10', 'Very Good', 'Research equipment comment for report ID 10', 'Very Good', 'Technical support comment for report ID 10', 'Good', 'Financial resource comment for report ID 10', 'Not Relevant', 'Other comment for report ID 10', 'Monthly', '1 month', 'Softcopy'),
    (12, 'Unsatisfactory', 'Access principal comment for report ID 12', 'Unsatisfactory', 'Access assistant/other comment for report ID 12', 'Satisfactory', 'Expertise principal comment for report ID 12', 'Satisfactory', 'Expertise assistant/other comment for report ID 12', 'Very Good', 'Quality principal comment for report ID 12', 'Good', 'Quality assistant/other comment for report ID 12', 'Good', 'Timeless principal comment for report ID 12', 'Good', 'Timeless assistant/other comment for report ID 12', 'Good', 'Courses available comment for report ID 12', 'Good', 'Workspace comment for report ID 12', 'Satisfactory', 'Computer facilities comment for report ID 12', 'Satisfactory', 'IT support comment for report ID 12', 'Good', 'Research software comment for report ID 12', 'Satisfactory', 'Library facilities comment for report ID 12', 'Very Good', 'Teaching and learning support comment for report ID 12', 'Good', 'Statistical support comment for report ID 4', 'Good', 'Research equipment comment for report ID 12', 'Good', 'Technical support comment for report ID 12', 'Good', 'Financial resource comment for report ID 12', 'Not Relevant', 'Other comment for report ID 12', 'Every 3 months', '3months', 'Softcopy'),
    (13, 'Not Relevant', 'Access principal comment for report ID 13', 'Very Good', 'Access assistant/other comment for report ID 13', 'Not Relevant', 'Expertise principal comment for report ID 13', 'Very Good', 'Expertise assistant/other comment for report ID 13', 'Satisfactory', 'Quality principal comment for report ID 13', 'Good', 'Quality assistant/other comment for report ID 13', 'Unsatisfactory', 'Timeless principal comment for report ID 13', 'Unsatisfactory', 'Timeless assistant/other comment for report ID 13', 'Good', 'Courses available comment for report ID 13', 'Good', 'Workspace comment for report ID 13', 'Satisfactory', 'Computer facilities comment for report ID 13', 'Unsatisfactory', 'IT support comment for report ID 13', 'Unsatisfactory', 'Research software comment for report ID 13', 'Very Good', 'Library facilities comment for report ID 13', 'Very Good', 'Teaching and learning support comment for report ID 13', 'Satisfactory', 'Statistical support comment for report ID 13', 'Good', 'Research equipment comment for report ID 13', 'Good', 'Technical support comment for report ID 13', 'Good', 'Financial resource comment for report ID 13', 'Very Good', 'Other comment for report ID 13', 'Half yearly', '1 month', 'Softcopy'),
    (14, 'Satisfactory', 'Access principal comment for report ID 14', 'Good', 'Access assistant/other comment for report ID 14', 'Good', 'Expertise principal comment for report ID 14', 'Very Good', 'Expertise assistant/other comment for report ID 14', 'Satisfactory', 'Quality principal comment for report ID 14', 'Good', 'Quality assistant/other comment for report ID 14', 'Good', 'Timeless principal comment for report ID 14', 'Good', 'Timeless assistant/other comment for report ID 14', 'Good', 'Courses available comment for report ID 14', 'Good', 'Workspace comment for report ID 14', 'Good', 'Computer facilities comment for report ID 14', 'Good', 'IT support comment for report ID 14', 'Very Good', 'Research software comment for report ID 14', 'Satisfactory', 'Library facilities comment for report ID 14', 'Very Good', 'Teaching and learning support comment for report ID 14', 'Good', 'Statistical support comment for report ID 14', 'Good', 'Research equipment comment for report ID 14', 'Good', 'Technical support comment for report ID 14', 'Satisfactory', 'Financial resource comment for report ID 14', 'Not Relevant', 'Other comment for report ID 14', 'Not at all', '2 weeks', 'Softcopy')
    ;
    

CREATE TABLE IF NOT EXISTS SECTION_D (
    report_id INT PRIMARY KEY,
    t1 JSON NOT NULL,
    t1_comment TEXT,
    t2 JSON NOT NULL,
    t3 JSON NOT NULL,
    t4 JSON NOT NULL,
    t5 JSON NOT NULL,
    t5_comment TEXT NOT NULL,
    student_name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id)
);

INSERT INTO SECTION_D (report_id, t1, t1_comment, t2, t3, t4, t5, t5_comment, student_name, date)
VALUES
    (1,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 1', '[{"effects": "Comment for t2 in report ID 1"}, {"effects": "Comment for t2-1 in report ID 1"}]', '[{"achievements": "Comment for t3 in report ID 1"}, {"achievements": "Comment for t3-1 in report ID 1"}, {"achievements": "Comment for t3-2 in report ID 1"}]', '[{"problems": "Anticipated problems for t4 in report ID 1", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 1', 'John Doe', '2022-12-29'),
    (2,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 2', '[{"effects": "Comment for t2 in report ID 2"}, {"effects": "Comment for t2-1 in report ID 2"}]', '[{"achievements": "Comment for t3 in report ID 2"}, {"achievements": "Comment for t3-1 in report ID 2"}, {"achievements": "Comment for t3-2 in report ID 2"}]', '[{"problems": "Anticipated problems for t4 in report ID 2", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 2', 'Jane Smith', '2022-12-28'),
    (3,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 3', '[{"effects": "Comment for t2 in report ID 3"}, {"effects": "Comment for t2-1 in report ID 3"}]', '[{"achievements": "Comment for t3 in report ID 3"}, {"achievements": "Comment for t3-1 in report ID 3"}, {"achievements": "Comment for t3-2 in report ID 3"}]', '[{"problems": "Anticipated problems for t4 in report ID 3", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 3', 'Hoa Nguyen', '2022-12-27'),
    (4,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 4', '[{"effects": "Comment for t2 in report ID 4"}, {"effects": "Comment for t2-1 in report ID 4"}]', '[{"achievements": "Comment for t3 in report ID 4"}, {"achievements": "Comment for t3-1 in report ID 4"}, {"achievements": "Comment for t3-2 in report ID 4"}]', '[{"problems": "Anticipated problems for t4 in report ID 4", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 4', 'Soo-Jin Lee', '2023-05-29'),
    (5,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 5', '[{"effects": "Comment for t2 in report ID 5"}, {"effects": "Comment for t2-1 in report ID 5"}]', '[{"achievements": "Comment for t3 in report ID 5"}, {"achievements": "Comment for t3-1 in report ID 5"}, {"achievements": "Comment for t3-2 in report ID 5"}]', '[{"problems": "Anticipated problems for t4 in report ID 5", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 5', 'Mark Wilson', '2023-05-28'),
    (6,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 6', '[{"effects": "Comment for t2 in report ID 6"}, {"effects": "Comment for t2-1 in report ID 6"}]', '[{"achievements": "Comment for t3 in report ID 6"}, {"achievements": "Comment for t3-1 in report ID 6"}, {"achievements": "Comment for t3-2 in report ID 6"}]', '[{"problems": "Anticipated problems for t4 in report ID 6", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 6', 'Yun Chen', '2023-05-27'),
    (7,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 7', '[{"effects": "Comment for t2 in report ID 7"}, {"effects": "Comment for t2-1 in report ID 7"}]', '[{"achievements": "Comment for t3 in report ID 7"}, {"achievements": "Comment for t3-1 in report ID 7"}, {"achievements": "Comment for t3-2 in report ID 7"}]', '[{"problems": "Anticipated problems for t4 in report ID 7", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 7', 'Min-Jae Kim', '2023-05-27'),
    (8,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 8', '[{"effects": "Comment for t2 in report ID 8"}, {"effects": "Comment for t2-1 in report ID 8"}]', '[{"achievements": "Comment for t3 in report ID 8"}, {"achievements": "Comment for t3-1 in report ID 8"}, {"achievements": "Comment for t3-2 in report ID 8"}]', '[{"problems": "Anticipated problems for t4 in report ID 8", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 8', 'John Doe', '2022-12-28'),
    (9,	'[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 9', '[{"effects": "Comment for t2 in report ID 9"}, {"effects": "Comment for t2-1 in report ID 9"}]', '[{"achievements": "Comment for t3 in report ID 9"}, {"achievements": "Comment for t3-1 in report ID 9"}, {"achievements": "Comment for t3-2 in report ID 9"}]', '[{"problems": "Anticipated problems for t4 in report ID 9", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 9', 'Jane Smith', '2022-12-27'),
    (10, '[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 10', '[{"effects": "Comment for t2 in report ID 10"}, {"effects": "Comment for t2-1 in report ID 10"}]', '[{"achievements": "Comment for t3 in report ID 10"}, {"achievements": "Comment for t3-1 in report ID 10"}, {"achievements": "Comment for t3-2 in report ID 10"}]', '[{"problems": "Anticipated problems for t4 in report ID 10", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 10', 'Hoa Nguyen', '2023-05-29'),
    (12, '[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 12', '[{"effects": "Comment for t2 in report ID 12"}, {"effects": "Comment for t2-1 in report ID 12"}]', '[{"achievements": "Comment for t3 in report ID 12"}, {"achievements": "Comment for t3-1 in report ID 12"}, {"achievements": "Comment for t3-2 in report ID 12"}]', '[{"problems": "Anticipated problems for t4 in report ID 12", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 12', 'Mark Wilson', '2023-05-28'),
    (13, '[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 13', '[{"effects": "Comment for t2 in report ID 13"}, {"effects": "Comment for t2-1 in report ID 13"}]', '[{"achievements": "Comment for t3 in report ID 13"}, {"achievements": "Comment for t3-1 in report ID 13"}, {"achievements": "Comment for t3-2 in report ID 13"}]', '[{"problems": "Anticipated problems for t4 in report ID 13", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 13', 'Yun Chen', '2023-05-27'),
    (14, '[{"status": "complete", "comments": "", "research_objectives": "Database"}, {"status": "incomplete", "comments": "sick due to covid-19", "research_objectives": "Python"}]', 'Comment for t1 in report ID 14', '[{"effects": "Comment for t2 in report ID 14"}, {"effects": "Comment for t2-1 in report ID 14"}]', '[{"achievements": "Comment for t3 in report ID 14"}, {"achievements": "Comment for t3-1 in report ID 14"}, {"achievements": "Comment for t3-2 in report ID 14"}]', '[{"problems": "Anticipated problems for t4 in report ID 14", "target_date": "2023-06-15", "research_objectives": "Advanced database"}]', '[{"item": "External hard driver", "notes": "must be SSD", "amount": "200"}, {"item": "Wireless mouse", "notes": "Logitech MX Anywhere 3", "amount": "99"}]', 'Comment for t5 in report ID 14', 'Min-Jae Kim', '2023-05-27')
   ;

CREATE TABLE IF NOT EXISTS SECTION_E_SPVRS (
    report_id INT NOT NULL,
    student_name VARCHAR(50) NOT NULL, 
    student_id INT NOT NULL, 
    spvr_name VARCHAR(50) NOT NULL,
    staff_id INT NOT NULL,
    supv_type ENUM('Main Supervisor', 'Associate Supervisor', 'Other Supervisor') NOT NULL,
    overall_6m ENUM('Excellent', 'Good', 'Satisfactory','Below Average', 'Unsatisfactory') NOT NULL,
    overall_full ENUM('Excellent', 'Good', 'Satisfactory','Below Average', 'Unsatisfactory') NOT NULL,
    work_quality ENUM('Excellent', 'Good', 'Satisfactory','Below Average', 'Unsatisfactory') NOT NULL,
    technical_skill ENUM('Excellent', 'Good', 'Satisfactory','Below Average', 'Unsatisfactory') NOT NULL,
    likelihood_6m ENUM('Excellent', 'Good', 'Satisfactory','Below Average', 'Unsatisfactory') NOT NULL,
    recommendation ENUM('Yes', 'No', 'N/A'),
    comments TEXT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (report_id,staff_id),
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
    FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id)
);

INSERT INTO SECTION_E_SPVRS (report_id, student_name, student_id, spvr_name, staff_id, supv_type, overall_6m, overall_full, work_quality, technical_skill, likelihood_6m, recommendation, comments, date)
VALUES
    (1, 'John Doe', 1, 'John Joe', 4, 'Main Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-15'),
    (1, 'John Doe', 1, 'Mary Jones', 7, 'Associate Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-16'),
    (1, 'John Doe', 1, 'Mike Lee', 8, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-17'),
    (1, 'John Doe', 1, 'Hieu Nguyen', 9, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-17'),
    (2, 'Jane Smith', 2, 'Mary Jones', 7, 'Main Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-15'),
    (2, 'Jane Smith', 2, 'Mike Lee', 8, 'Associate Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-16'),
    (2, 'Jane Smith', 2, 'Hieu Nguyen', 9, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-17'),
    (2, 'Jane Smith', 2, 'Chris Brown', 10, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-18'),
    (2, 'Jane Smith', 2, 'Jin Kim', 11, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2022-11-18'),
    (3, 'Hoa Nguyen', 3, 'Mike Lee', 8, 'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (3, 'Hoa Nguyen', 3, 'Jin Kim', 11, 'Associate Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (4, 'Soo-Jin Lee', 4, 'John Joe', 4,  'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (4, 'Soo-Jin Lee', 4, 'Chris Brown', 10, 'Associate Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (4, 'Soo-Jin Lee', 4, 'Mary Jones', 7 , 'Other Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (5, 'Mark Wilson', 5, 'Jin Kim', 11, 'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (6, 'Yun Chen', 6, 'Maria Garcia', 12, 'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (6, 'Yun Chen', 6, 'Sarah Johnson', 13, 'Associate Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),    
    (7, 'Min-Jae Kim', 9, 'Yan Wu', 14, 'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (7, 'Min-Jae Kim', 9, 'Raj Gupta', 15, 'Associate Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2022-11-15'),
    (8, 'John Doe', 1, 'John Joe', 4, 'Main Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-15'),
    (8, 'John Doe', 1, 'Mary Jones', 7, 'Associate Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-16'),
    (8, 'John Doe', 1, 'Mike Lee', 8, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-17'),
    (8, 'John Doe', 1, 'Hieu Nguyen', 9, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-17'),
    (9, 'Jane Smith', 2, 'Mary Jones', 7, 'Main Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-15'),
    (9, 'Jane Smith', 2, 'Mike Lee', 8, 'Associate Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-16'),
    (9, 'Jane Smith', 2, 'Hieu Nguyen', 9, 'Other Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.',  '2023-05-17'),
    (12, 'Mark Wilson', 5, 'Jin Kim', 11, 'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.',  '2023-05-18'),
    (13, 'Yun Chen', 6, 'Maria Garcia', 12, 'Main Supervisor', 'Good', 'Good', 'Satisfactory', 'Excellent', 'Good', 'Yes', 'Overall, the student has shown significant progress in the past 6 months.', '2023-05-18'),
    (13, 'Yun Chen', 6, 'Sarah Johnson', 13, 'Associate Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2023-05-15'),
    (14, 'Min-Jae Kim', 9, 'Yan Wu', 14, 'Main Supervisor', 'Satisfactory', 'Good', 'Good', 'Good', 'Satisfactory', 'Yes', 'The student''s work quality has been consistently satisfactory.', '2023-05-15'),
    (14, 'Min-Jae Kim', 9, 'Raj Gupta', 15, 'Associate Supervisor', 'Good', 'Good', 'Good', 'Satisfactory', 'Good', 'Yes', 'Overall, the student''s performance has been good.', '2023-05-20')
    ;


 CREATE TABLE IF NOT EXISTS SECTION_E_CONVENOR (
    report_id INT PRIMARY KEY,
    staff_id INT NOT NULL,
    comments TEXT NOT NULL,
    date DATE NOT NULL,
    student_status ENUM('G', 'O', 'R') NOT NULL,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id),
    FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id)
);	

INSERT INTO SECTION_E_CONVENOR (report_id, staff_id, comments, date, student_status)
VALUES
(1, 4, 'Improvements required.', '2022-11-09', 'O'),
(2, 4, 'Excellent.', '2022-11-09', 'G'),
(3, 4, 'Signficant improvements required.', '2022-11-09', 'R'),
(4, 4, 'Improvements required.', '2022-11-09', 'O'),
(5, 4, 'Excellent.', '2022-11-09', 'G'),
(6, 5, 'Signficant improvements required.', '2022-11-09', 'R'),
(7, 6, 'Improvements required.', '2022-11-09', 'O'),
(12, 4, 'Good.', '2023-05-10', 'G'),
(13, 5, 'Signficant improvements required.', '2023-05-10', 'R'),
(14, 6, 'Improvements required.', '2023-05-10', 'O')
;


CREATE TABLE IF NOT EXISTS SECTION_F (
    report_id INT PRIMARY KEY,
    student_name VARCHAR(50),
    spvrs_names VARCHAR(200),
    comments TEXT,
    talk_to ENUM('PG Chair', 'Convenor'),
    date DATE NOT NULL,
    chair_response TEXT,
    resp_date DATE,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id)
);

INSERT INTO SECTION_F (report_id, student_name, spvrs_names, comments, talk_to, date, chair_response, resp_date)
VALUES
(1, 'John Doe', 'Mary Jones,Mike Lee', 'need to change supervisor', 'PG Chair', '2022-12-11', 'advised convenor to address the issue', '2023-01-04'),
(12, 'Mark Wilson', 'Jin Kim', 'I have an issue with Chris and Hieu and need to discuss with the convenor personally', 'Convenor', '2022-12-15', NULL, NULL),
(13, 'Yun Chen', 'Maria Garcia, Sarah Johnson', 'supervisor is not helpful', 'Convenor', '2023-06-01', NULL, NULL);


CREATE TABLE email_msg (
    email_id VARCHAR(255),
    content TEXT
);
INSERT INTO email_msg (email_id, content)
VALUES ('e1', 'You 6MR is due soon, please fill it up!');

CREATE TABLE IF NOT EXISTS admin_note (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    note TEXT NOT NULL,
    note_date DATE,
    FOREIGN KEY (report_id) REFERENCES REPORT(report_id)
);

DROP VIEW IF EXISTS REPORT_CURRENT_STATUS;

CREATE VIEW REPORT_CURRENT_STATUS AS
SELECT r.student_id, 
	concat(lname,' ',fname) student_name,
	r.report_id, 
	concat(rept_term,' ',rept_year) rept_term,
	due_date,
    CASE WHEN student_abcd_completed <> 1 THEN 'Waiting for Student to Complete Section A-D'
		WHEN supervisors_completed <> no_supvs THEN 'Waiting for Supervisors to Complete Section E'
        WHEN convenor_completed <> 1 THEN 'Waiting for Convenor to Complete Section E'
        WHEN full_report_completed <> 1 THEN 'Waiting for Admin to Confirm Report is Completed'
        ELSE 'Report Completed'
	END AS Report_current_progress,
    CASE WHEN full_report_completed <> 1 and due_date < CURDATE() THEN 'Yes' END AS Overdue
FROM REPORT r
LEFT JOIN STUDENT s ON r.student_id = s.student_id
LEFT JOIN REPORT_PROGRESS rp ON r.report_id = rp.report_id
LEFT JOIN (SELECT student_id, count(*) no_supvs FROM SUPERVISION GROUP BY student_id ) sp ON sp.student_id = s.student_id;

DROP VIEW IF EXISTS REPORT_DTSS_STATUS;

CREATE VIEW REPORT_DTSS_STATUS AS
SELECT
  CONCAT(s.fname, ' ', s.lname) AS s_name,
  s.student_id,
  GROUP_CONCAT(DISTINCT CONCAT(f.fname, ' ', f.lname)) AS supervisors,
  GROUP_CONCAT(DISTINCT CONCAT(r.rept_year, ' ', r.rept_term, ' Status: ', se.student_status) ORDER BY r.rept_year SEPARATOR ', ') AS year_term_status,
  a.note
FROM
  student s
  LEFT JOIN supervision sv ON s.student_id = sv.student_id
  LEFT JOIN staff f ON sv.staff_id = f.staff_id
  LEFT JOIN report r ON r.student_id = s.student_id
  LEFT JOIN section_e_convenor se ON r.report_id = se.report_id  
  LEFT JOIN admin_note a ON r.report_id = a.report_id
WHERE
  s.dept_code = 'DTSS'
GROUP BY 1,2
ORDER BY 2, MIN(r.rept_year);

DROP VIEW IF EXISTS REPORT_SOLA_STATUS;

CREATE VIEW REPORT_SOLA_STATUS AS
SELECT
  CONCAT(s.fname, ' ', s.lname) AS s_name,
  s.student_id,
  GROUP_CONCAT(DISTINCT CONCAT(f.fname, ' ', f.lname)) AS supervisors,
  GROUP_CONCAT(DISTINCT CONCAT(r.rept_year, ' ', r.rept_term, ' Status: ', se.student_status) ORDER BY r.rept_year SEPARATOR ', ') AS year_term_status,
  a.note
FROM
  student s
  LEFT JOIN supervision sv ON s.student_id = sv.student_id
  LEFT JOIN staff f ON sv.staff_id = f.staff_id
  LEFT JOIN report r ON r.student_id = s.student_id
  LEFT JOIN section_e_convenor se ON r.report_id = se.report_id
  LEFT JOIN admin_note a ON r.report_id = a.report_id
WHERE
  s.dept_code = 'SOLA'
GROUP BY 1,2
ORDER BY 2, MIN(r.rept_year);
  
DROP VIEW IF EXISTS REPORT_DEM_STATUS;

CREATE VIEW REPORT_DEM_STATUS AS
SELECT
  CONCAT(s.fname, ' ', s.lname) AS s_name,
  s.student_id,
  GROUP_CONCAT(DISTINCT CONCAT(f.fname, ' ', f.lname)) AS supervisors,
  GROUP_CONCAT(DISTINCT CONCAT(r.rept_year, ' ', r.rept_term, ' Status: ', se.student_status) ORDER BY r.rept_year SEPARATOR ', ') AS year_term_status,
  a.note
FROM
  student s
  LEFT JOIN supervision sv ON s.student_id = sv.student_id
  LEFT JOIN staff f ON sv.staff_id = f.staff_id
  LEFT JOIN report r ON r.student_id = s.student_id
  LEFT JOIN section_e_convenor se ON r.report_id = se.report_id
  LEFT JOIN admin_note a ON r.report_id = a.report_id
WHERE
  s.dept_code = 'DEM'
GROUP BY 1,2
ORDER BY 2, MIN(r.rept_year);
