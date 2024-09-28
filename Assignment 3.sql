-- DROP DATABASE our_space;
-- restarted my DB left this in to show how you can delete a DB

-- Desiging a database to help track their subscription type & useage of facilties

CREATE DATABASE our_space;

USE our_space;

-- create all tables required for our_space

CREATE TABLE members
(member_id INT PRIMARY KEY, 
first_name VARCHAR(50) NOT NULL, -- ensures a value is added
last_name VARCHAR(50) NOT NULL,
email VARCHAR(50),
phone_number VARCHAR(50), -- so '0' is picked up
membership_type VARCHAR (50), -- need to make FK
join_date DATE,
active_status BIT -- boolean yes true/(1) or no false/(0)
 );

-- need to make email unique do avoid dups

AlTER TABLE members
MODIFY email VARCHAR(100) UNIQUE;

CREATE TABLE memberships
(membership_id INT PRIMARY KEY,
membership_type VARCHAR(50) UNIQUE, 
monthly_cost FLOAT,
access_level VARCHAR(50),
max_classes_per_month INT
 );

-- adding so only postive values are entered for cost

-- ALTER TABLE memberships
-- ADD CONSTRAINT chk_monthly_cost_postive
-- CHECK (monthly_cost > 0);

-- Mistake made so removed Constraint to make it include 0
-- ALTER TABLE memberships
-- DROP CONSTRAINT chk_monthly_cost_postive;

SELECT CONSTRAINT_NAME 
FROM information_schema.TABLE_CONSTRAINTS 
WHERE TABLE_NAME = 'memberships' AND CONSTRAINT_TYPE = 'CHECK';

-- Edited so I have have 0

ALTER TABLE memberships
ADD CONSTRAINT chk_monthly_cost_postive_or_equal
CHECK (monthly_cost >= 0);

ALTER TABLE members
ADD CONSTRAINT fk_membership_type FOREIGN KEY (membership_type)
REFERENCES memberships(membership_type);

CREATE TABLE member_classes (
    class_id INT PRIMARY KEY AUTO_INCREMENT,
    class_name VARCHAR(50),
    trainer_name VARCHAR(100), 
    class_time DATETIME,
    max_participants INT,
    class_location VARCHAR(50)
);

CREATE TABLE class_attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    class_id VARCHAR(50), -- fk ref member_classes
    member_id VARCHAR(100), -- fk ref members
    attendance_date DATETIME
);

-- incorrectly made class_id a varchar the types need to match to be a fK

AlTER TABLE class_attendance
MODIFY class_id INT;

ALTER TABLE class_attendance
ADD CONSTRAINT fk_class_id FOREIGN KEY (class_id)
REFERENCES member_classes(class_id);

CREATE TABLE clubs (
    club_id INT PRIMARY KEY,
    club_facilities VARCHAR(100),
    facility_description VARCHAR(100),
    club_location VARCHAR(100)
);

-- Now to insert all data into all tables

INSERT INTO memberships (membership_id, membership_type, monthly_cost, access_level, max_classes_per_month)
VALUES 
('1','STAFF', 0, 'Full Access', 10),
('2','BUDDY', 35.00, 'Off-Peak Access', 5),
('3','COMP', 200.00, 'Full Access', 20),
('4','GROUP PLUS', 400.00, 'Group Access', 15),
('5','GROUP', 300.00, 'Group Off-Peak Access', 15),
('6','HEADLINE', 150.00, 'Club Only Access', 10);


INSERT INTO members (member_id, first_name, last_name, email, phone_number, membership_type, join_date, active_status)
VALUES 
('1001001', 'Louisa', 'Mussington', 'lou.mussington@yahoo.co.uk', '07123456789', 'STAFF', '2024-01-15', TRUE),
('1001002', 'Melissa', 'Boreham', 'mel.boreham@gmail.com', '075305535554', 'BUDDY', '2024-05-15', TRUE),
('1001003', 'Linda', 'Lindebauma', 'llindenb@yahoo.co.uk', '07544585012', 'COMP', '2023-12-11', TRUE),
('1001004', 'Lucie', 'Kovacova', 'lkovecova@outlook.com', '07453247011', 'GROUP PLUS', '2022-11-11', TRUE),
('1001005', 'Louis', 'Mustard', 'louis.mustard@yahoo.co.uk', '07123456790', 'GROUP', '2024-10-15', TRUE),
('1001006', 'Stephen', 'Blain', 'Step.blain@gmail.com', '075305535565', 'GROUP', '2021-07-15', TRUE),
('1001007', 'Barry', 'Allen', 'BA@yahoo.co.uk', '07544585013', 'HEADLINE', '2020-12-11', TRUE),
('1001008', 'Luca', 'Kelvin', 'lkelvin@outlook.com', '07453247001', 'HEADLINE', '2021-11-11', TRUE),
('1001009', 'Liam', 'Gallagher', 'liamGG@outlook.com', '07453247551', 'GROUP PLUS', '2020-09-11', TRUE);

-- class_id is an auto_increment so don't add to the insert

INSERT INTO member_classes (class_name, trainer_name, class_time, max_participants, class_location)
VALUES 
('Yoga Fundamentals', 'Alice James', '2024-09-25 10:00:00', 15, 'Soho Studio 1'),
('HIIT Workout', 'Mark Smith', '2024-09-26 12:00:00', 20, 'Mayfair Studio 1'),
('Pilates Fundamentals', 'Emma Brown', '2024-09-27 09:00:00', 10, 'Marylebone Studio 2'),
('Cycle', 'Liam Taylor', '2024-09-28 18:00:00', 25, 'Canary Wharf Cycle Studio 1'),
('Kickboxing', 'Jake Thompson', '2024-09-30 17:00:00', 20, 'City Studio 2'),
('Sound bath', 'Sophia Clark', '2024-10-01 07:30:00', 10, 'Moorgate Mind & Body Studio 1'),
('TRX', 'James Lewis', '2024-10-02 11:00:00', 15, 'City Studio 1'),
('Lift', 'Olivia Martinez', '2024-10-03 13:00:00', 20, 'Canary Wharf Studio 1'),
('Formula 3', 'Ethan Hall', '2024-10-04 19:00:00', 30, 'Marylevone Studio 1'),
('Hyrox Run', 'Mia Young', '2024-10-05 16:00:00', 15, 'Mayfair Studio 1');

-- checking to see if auto-increment works

SELECT * FROM member_classes

 -- clubs, club_id INT PRIMARY KEY, club_facilities VARCHAR(100), facility_description VARCHAR(100),club_location VARCHAR(100)
 
INSERT INTO clubs (club_id, club_facilities,facility_description, club_location)
VALUES
('1', 'Gym, Combat, Mind & Body, Studio, Sauna, Steam, Swimming pool', ' In the heart of Soho, Central Club', 'Soho'),
('2', 'Gym, Combat, Mind & Body, Studio, Sauna, Steam ', ' In the Central East of London, Central East Club', 'Moorgate'),
('3', 'Gym, Reformer, Mind & Body, Studio, Sauna, Steam', ' In the Centre of London, Central', 'Mayfair'),
('4', 'Gym, Reformer, Mind & Body, Studio, Sauna, Steam, Swimming pool', ' In the Centre West of London, Central', 'Marylebone'),
('5', 'Gym, Reformer,Combat, Mind & Body, Studio, Sauna, Steam, Swimming pool', ' The Biggest Club in Europe', 'Canary Wharf'),
('6', 'Gym, Combat, Studio, Sauna, Steam, Swimming pool', ' A Hidden Central gem', 'City'),
('7', 'Gym, Combat, Studio, Sauna, Steam, Swimming pool', ' In the heart of the City', 'Marylevone'),
('8', 'Gym, Combat, Studio, Sauna, Steam, Swimming pool, Ice bath', ' Where Londoners came to socialise', 'Islington');

SELECT * FROM clubs

-- Correct typo Marylevone to Marylebone

-- Getting error 1175 Disable safe update mode

SET SQL_SAFE_UPDATES = 0;

UPDATE clubs
SET club_location = 'Marylebone'
WHERE club_location = 'Marylevone';

-- Adding back safety feature 

SET SQL_SAFE_UPDATES = 1;

-- Check it worked

SELECT club_location = 'Marylebone' FROM clubs;

-- now to add data into the class_attendance table using the fK's
-- attendance_id AUTO_INCREMENT, class_id -- fk ref member_classes, member_id -- fk ref members, attendance_date
-- DATETIME YYYY-MM-DD HH:MM
  
  -- review class_id from member_class table
  
  SELECT class_id, class_name FROM member_classes;
  
  SELECT* FROM member_classes
  
INSERT INTO class_attendance (class_id, member_id, attendance_date)
VALUES
(1, 1001001, '2024-09-25 10:00:00'),
(1, 1001002, '2024-09-25 10:00:00'),
(1, 1001005, '2024-09-25 10:00:00'),
(1, 1001007, '2024-09-25 10:00:00'),
(2, 1001002, '2024-09-26 12:00:00'),
(2, 1001007, '2024-09-26 12:00:00'),
(2, 1001004, '2024-09-26 12:00:00'),
(2, 1001009, '2024-09-26 12:00:00'),
(2, 1001003, '2024-09-26 12:00:00'),
(2, 1001008, '2024-09-26 12:00:00'),
(3, 1001003, '2024-09-27 09:00:00'),
(3, 1001005, '2024-09-27 09:00:00'),
(3, 1001009, '2024-09-27 09:00:00'),
(4, 1001006, '2024-09-28 18:00:00'),
(4, 1001009, '2024-09-28 18:00:00'),
(5, 1001003, '2024-09-30 17:00:00'),
(5, 1001008, '2024-09-30 17:00:00'),
(5, 1001009, '2024-09-30 17:00:00'),
(5, 1001006, '2024-09-30 17:00:00'),
(10, 1001004, '2024-10-05 16:00:00'),
(10, 1001002, '2024-10-05 16:00:00'),
(10, 1001001, '2024-10-05 16:00:00'),
(6, 1001007, '2024-10-01 07:30:00'),
(6, 1001003, '2024-10-01 07:30:00'),
(8, 1001009, '2024-10-03 13:00:00');

SELECT* FROM class_attendance

-- Query a list of all active members who are on the "GROUP" membership plan.
-- using alia's as using join
  
SELECT* FROM memberships

SELECT m.first_name AS fname, m.last_name AS lname, m.email AS email_address
FROM members AS m
INNER JOIN memberships AS ms ON m.membership_type = ms.membership_type
WHERE ms.membership_type = 'GROUP' AND m.active_status = TRUE;

-- Get the class list for all hyrox classes
-- checking how many values it will return
  
  SELECT class_name = 'Hyrox Run' FROM member_classes
  
SELECT class_name, class_location
FROM member_classes
WHERE class_id = 10
ORDER BY class_time;

-- List all facilities available at a specific club location (e.g., Soho).
  
  SELECT* FROM clubs -- check clubs table
  
  SELECT club_facilities
  FROM clubs
  WHERE club_location = 'Soho';
  
-- (Aggregate) Find out how many classes a member has enrolled in for a given month

SELECT COUNT(attendance_id) AS total_classes
FROM class_attendance
WHERE member_id = 1001006 AND MONTH(attendance_date) = 9 AND YEAR(attendance_date) = 2024;

-- checking to see if I have data in month I wish to review rev

SELECT * FROM members WHERE MONTH(join_date) = 11 AND YEAR(join_date) = 2021;

-- Now I can create a aggregate to calculate the total revenue generated from memberships in a specific period

SELECT SUM(ms.monthly_cost) AS total_revenue
FROM members AS m
INNER JOIN memberships AS ms ON m.membership_type = ms.membership_type
WHERE MONTH(m.join_date) = 11 AND YEAR(m.join_date) = 2021;
  
-- Find the average number of participants in each fitness class for the past month.
-- checking contents in class_attendance table

SELECT * FROM class_attendance
  
SELECT AVG(member_count) AS avg_attendance_count
FROM (
    SELECT COUNT(attendance_id) AS member_count
    FROM class_attendance
    WHERE MONTH(attendance_date) = 9 AND YEAR(attendance_date) = 2024
    GROUP BY class_id
) AS class_attending_members;
  
-- Delete members attendance to a class as they cancelled in the correct window
  
DELETE FROM class_attendance
WHERE member_id = 1001003 AND class_id = 2;
  
-- Creating a procedure to confirm how many classes a person has left based on their membership (members - max_classes_per_month & class_attendance)

SELECT * FROM memberships
SELECT * FROM class_attendance

DELIMITER // -- so ';' will not break the flow of the procedure

CREATE PROCEDURE check_classes_remaining (IN member_id INT, IN month INT, IN year INT)
BEGIN
    DECLARE max_class_bookings INT;
    DECLARE attended_classes INT;

-- Get the maximum classes allowed for the member's membership type with alias's
    
    SELECT ms.max_classes_per_month INTO max_class_bookings
    FROM memberships ms
    INNER JOIN members m ON m.membership_type = ms.membership_type
    WHERE m.member_id = member_id;

-- What is the the number of classes the member is already attended in for the given month and year

    SELECT COUNT(*) INTO attended_classes
    FROM class_attendance ca
    WHERE ca.member_id = member_id AND MONTH(ca.attendance_date) = month AND YEAR(ca.attendance_date) = year;

-- Now to show the remaining classes

    SELECT max_class_bookings - attended_classes AS classes_remaining;
END //

DELIMITER ;

-- check it works by calling it with a live member_ID

CALL check_classes_remaining(1001001, 10, 2024);

  
-- Write out the create scenario - In summary I wanted to track attendance and club bookings for a gym management system
-- The above database will allow the club management to efficiently handle the following:
-- Track members and their subscriptions, ensuring accurate billing and access control to classes and facilities.
-- Manage fitness class attendance, preventing overbooking and allowing easy reporting of class popularity.
-- Provide members with insights into their class attendance and how many classes they have left to book for the month.
-- Report on club facilities available at different locations, making it easier for members to select services.





