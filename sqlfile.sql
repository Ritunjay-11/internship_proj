CREATE TABLE Student(
SRN varchar(12) primary key,
Name varchar(255),
Phone_no varchar(10),
Email varchar(255)
);

CREATE TABLE Admin (
    Admin_ID INT PRIMARY KEY
);

DELIMITER //

CREATE FUNCTION GetTotalDurationForStudent(student_srn VARCHAR(12))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_duration INT;

    SELECT SUM(Duration) INTO total_duration
    FROM Internship
    WHERE SRN = student_srn;

    RETURN total_duration;
END;

//

DELIMITER ;

CREATE TABLE Company (
    company_name VARCHAR(255) PRIMARY KEY,
    website_link VARCHAR(255)
);


CREATE TABLE Manager (
    manager_ID INT PRIMARY KEY,
    manager_phone_no VARCHAR(10),
    manager_name VARCHAR(255),
    manager_email VARCHAR(255),
    company_name VARCHAR(255), 
    FOREIGN KEY (company_name) REFERENCES Company(company_name)
);


CREATE TABLE Internship (
    Internship_ID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255),
    start_date DATE,
    end_date DATE,
    Duration INT,
    Type VARCHAR(255),
    company_name VARCHAR(255), -- Foreign Key reference to Company
    manager_ID INT, -- Foreign Key reference to Manager
    SRN VARCHAR(12),
    FOREIGN KEY (company_name) REFERENCES Company(company_name),
    FOREIGN KEY (manager_ID) REFERENCES Manager(manager_ID),
    FOREIGN KEY (SRN) REFERENCES Student(SRN)
);





create table manager_srn_map 
(
manager_id INT,
SRN varchar(12),
FOREIGN KEY (manager_ID) REFERENCES Manager(manager_ID),
FOREIGN KEY (SRN) REFERENCES Student(SRN)
);

CREATE TABLE Manager_Review (
    Review_ID INT PRIMARY KEY auto_increment,
    Rating INT,
    Feedback VARCHAR(255),
    manager_ID INT, 
    SRN VARCHAR(12), 
    FOREIGN KEY (manager_ID) REFERENCES Manager(manager_ID),
    FOREIGN KEY (SRN) REFERENCES Student(SRN)
);

CREATE TABLE Application (
    Application_ID INT PRIMARY KEY auto_increment,
    application_status VARCHAR(255) DEFAULT 'pending',
    SRN VARCHAR(255),
    Admin_ID INT,
    manager_review_status VARCHAR(255) DEFAULT 'pending',
    FOREIGN KEY (SRN) REFERENCES Student(SRN),
    FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
);
use mini_project;
-- Delete all entries from child tables first



DELIMITER //
CREATE TRIGGER after_manager_review_insert
AFTER INSERT ON Manager_Review
FOR EACH ROW
BEGIN
    -- Update manager_review_status to 'completed' in Application table
    UPDATE Application
    SET manager_review_status = 'completed'
    WHERE SRN = NEW.SRN;
END;
//
DELIMITER ;


SELECT 
            A.Application_ID,
            S.SRN AS Student_SRN,
            S.Name AS Student_Name
        FROM 
            Application A
        JOIN
            Student S ON A.SRN = S.SRN
        WHERE
            A.application_status != 'pending'