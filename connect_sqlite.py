import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

#### Create Tables
create_dept_table = """
CREATE TABLE Department (
    dept_id varchar(5) NOT NULL,
    department_name varchar(20) NOT NULL,
    chair_first_name varchar(15),
    chair_last_name varchar (15),
    numb_of_faculty int,
    PRIMARY KEY(dept_id)
    );
    """
cursor.execute(create_dept_table)

create_major_table = """
CREATE TABLE Major (
    major_code varchar(3) NOT NULL CHECK (Length(major_code)=3),
    major_name varchar(20) NOT NULL,
    dept_id varchar(5) NOT NULL,
    PRIMARY KEY(major_code),
    FOREIGN KEY(dept_id) REFERENCES Department
    );
    """
cursor.execute(create_major_table)

create_event_table = """
CREATE TABLE Event (
    event_id varchar(5) NOT NULL,
    event_name varchar(20) NOT NULL,
    /* Setting current date to Jun 30 , 2021 */
    startDate date NOT NULL CHECK (startDate > '06-06-2021' ),
    endDate date NOT NULL CHECK (endDate > startDate),
    PRIMARY KEY(event_id)
    );
	"""
cursor.execute(create_event_table)
	
create_student_table = """
CREATE TABLE Student (
    stu_id INT NOT NULL CHECK(stu_id < 1000000000 AND stu_id > 99999999),
    first_name varchar(15) NOT NULL,
    last_name varchar(15) NOT NULL,
    initials varchar(3) NOT NULL CHECK (Length(initials)>1) ,
    PRIMARY KEY(stu_id) 
    );
    """
cursor.execute(create_student_table)

create_hosting_event_table = """
CREATE TABLE Hosting_event (
    dept_id varchar(5) NOT NULL,
    event_id varchar(5) NOT NULL,
    PRIMARY KEY(dept_id,event_id),
    FOREIGN KEY(dept_id) REFERENCES Department,
    FOREIGN KEY(event_id) REFERENCES Event
    );	
    """
cursor.execute(create_hosting_event_table)

create_attending_event_table = """
CREATE TABLE Attending_event (
    stu_id INT NOT NULL 
CHECK(stu_id <1000000000 AND stu_id > 99999999),
    event_id varchar(5) NOT NULL,
    PRIMARY KEY(stu_id,event_id),
    FOREIGN KEY(stu_id) REFERENCES Student,
    FOREIGN KEY(event_id) REFERENCES Event
    );
   """
cursor.execute(create_attending_event_table)

create_declaring_major_table = """
CREATE TABLE Declaring_major (
    stu_id INT NOT NULL 
	CHECK(stu_id <1000000000 AND stu_id > 99999999),
    major_code varchar(3) NOT NULL,
    PRIMARY KEY(stu_id,major_code),
    FOREIGN KEY(stu_id) REFERENCES Student,
    FOREIGN KEY(major_code) REFERENCES Major
    );
    """
cursor.execute(create_declaring_major_table)

####Insert rows into tables
insert_all_rows = """
INSERT INTO Department VALUES ('bio12','Molecular Biology','John','Doe','15');
INSERT INTO Department VALUES ('mth11','Applied Mathematics','Issac','Newton','10');
INSERT INTO Department VALUES ('arch1','Architechture','Frank','Wright','25');
INSERT INTO Department VALUES ('eng01','English Literature','Walt','Whitman','35');
INSERT INTO Department VALUES ('csc01','Computer Science','Odelia','Schwartz','27');

INSERT INTO Major VALUES ('bio','Biology','bio12');
INSERT INTO Major VALUES ('mth','Mathematics','mth11');
INSERT INTO Major VALUES ('csc','Computer Science','csc01');
INSERT INTO Major VALUES ('eng','Creative Writting','eng01');
INSERT INTO Major VALUES ('arc','Architecture','arch1');

INSERT INTO Event VALUES ('com22','Comencement 2022','08-08-2022', '09-08-2022');
INSERT INTO Event VALUES ('fai22','Expo Fair 2022','09-09-2022', '16-09-2022');
INSERT INTO Event VALUES ('ftr22','Food Trucks December','09-12-2021', '16-12-2021');
INSERT INTO Event VALUES ('art01','Art Basel UM','20-10-2021', '24-10-2021');
INSERT INTO Event VALUES ('bk003','Discount Books Sales','20-01-2022', '20-02-2022');

INSERT INTO Student VALUES ('123456789','Tom','Vega','TV');
INSERT INTO Student VALUES ('103456789','Jane','Smith','JS');
INSERT INTO Student VALUES ('100456789','John','Doe','JD');
INSERT INTO Student VALUES ('100056789','Rob','Garcia','RG');
INSERT INTO Student VALUES ('100006789','Lynn','Johnston','LJ');

INSERT INTO Hosting_event VALUES ('bio12','fai22');
INSERT INTO Hosting_event VALUES ('bio12','ftr22');
INSERT INTO Hosting_event VALUES ('arch1','art01');
INSERT INTO Hosting_event VALUES ('mth11','bk003');
INSERT INTO Hosting_event VALUES ('eng01','bk003');

INSERT INTO Attending_event VALUES ('123456789','fai22');
INSERT INTO Attending_event VALUES ('123456789','ftr22');
INSERT INTO Attending_event VALUES ('103456789','art01');
INSERT INTO Attending_event VALUES ('123456789','bk003');
INSERT INTO Attending_event VALUES ('100006789','bk003');

INSERT INTO Declaring_major VALUES ('123456789','csc');
INSERT INTO Declaring_major VALUES ('103456789','bio');
INSERT INTO Declaring_major VALUES ('100456789','mth');
INSERT INTO Declaring_major VALUES ('100056789','eng');
INSERT INTO Declaring_major VALUES ('100006789','csc');
	"""
cursor.executescript(insert_all_rows)

#### Select data
#List the details of students that are attending a named event
query1 = """
/*List the details of students that are attending a named event*/
SELECT s.*
    FROM Student s, Event e, Attending_event a
    WHERE s.stu_id=a.stu_id
    AND a.event_id=e.event_id
    AND e.event_name='Discount Books Sales';
"""
cursor.execute(query1)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print("-----------------------------------------------------------\r")
print(df)
print(df.columns)

#Count the number of Majors offered by department. List by major count and department name
query2 = """
SELECT count(major_code) AS Major_count, department_name
    FROM Major m, Department d
    WHERE d.dept_id=m.dept_id
    GROUP BY major_code, department_name
    ORDER BY count(major_code);
"""
cursor.execute(query2)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print("-----------------------------------------------------------\r")
print(df)
print(df.columns)

#List events being hosted by named department
query3 = """
SELECT event_name, department_name AS hosted_by
    FROM Department d, Event e, Hosting_event h
    WHERE e.event_id=h.event_id
    AND d.dept_id=h.dept_id
    AND d.department_name='English Literature';
"""
cursor.execute(query3)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print("-----------------------------------------------------------\r")
print(df)
print(df.columns)

#Find the events being attended by a named student and also list the same student’s major (or majors). 
query4 = """
SELECT first_name, last_name, event_name, major_name
    FROM Student s, Event e, Attending_event a, Declaring_major d, Major m
    WHERE s.stu_id=a.stu_id
    AND e.event_id=a.event_id
    AND s.stu_id=d.stu_id
    AND d.major_code=m.major_code
    AND s.first_name='Tom'
    AND s.last_name='Vega';
"""

#List the chair name for every department. 
cursor.execute(query4)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print("-----------------------------------------------------------\r")
print(df)
print(df.columns)

query5 = """
SELECT chair_first_name, chair_last_name, department_name
FROM Department
    
"""
cursor.execute(query5)
column_names = [row[0] for row in cursor.description]
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
print("-----------------------------------------------------------\r")
print(df)
print(df.columns)
print("-----------------------------------------------------------\r")

# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
