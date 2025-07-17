create database HR_SAMPLE;
use HR_SAMPLE;

CREATE TABLE regions (
	region_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	region_name VARCHAR (25) DEFAULT NULL
);

CREATE TABLE countries (
	country_id CHAR (2) PRIMARY KEY,
	country_name VARCHAR (40) DEFAULT NULL,
	region_id INT (11) NOT NULL,
	FOREIGN KEY (region_id) REFERENCES regions (region_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE locations (
	location_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	street_address VARCHAR (40) DEFAULT NULL,
	postal_code VARCHAR (12) DEFAULT NULL,
	city VARCHAR (30) NOT NULL,
	state_province VARCHAR (25) DEFAULT NULL,
	country_id CHAR (2) NOT NULL,
    
	FOREIGN KEY (country_id) REFERENCES countries (country_id) ON DELETE CASCADE ON UPDATE CASCADE
);



CREATE TABLE jobs (
	job_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	job_title VARCHAR (35) NOT NULL,
	min_salary DECIMAL (8, 2) DEFAULT NULL,
	max_salary DECIMAL (8, 2) DEFAULT NULL
);

CREATE TABLE departments (
	department_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	department_name VARCHAR (30) NOT NULL,
	location_id INT (11) DEFAULT NULL,
    
	FOREIGN KEY (location_id) REFERENCES locations (location_id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE clients (
	client_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	client_name VARCHAR (250) DEFAULT NULL,
	industry VARCHAR (255) NOT NULL,
   	adress VARCHAR (255) , 
	email VARCHAR (150) NOT NULL,
	phone_number VARCHAR (20) DEFAULT NULL,
    -- utiliser lheure actualle
	created_at timestamp DEFAULT current_timestamp
	
);
 
 
 
 
 
CREATE TABLE hr_services (
	service_id INT (11) AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
	service_type ENUM('recruitment','training','consulting','payrol','other'),
	start_date DATE,
    end_date DATE,
    service_status ENUM('ongoing', 'completed', 'cancelled'),
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
	
);



-- table reclamation brute
DROP TABLE claims_raw;
CREATE TABLE claimss_raw (
	claim_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	client_id INT,
    claim_date DATE NOT NULL,
	claim_amount DECIMAL (10.2) NOT NULL,
    claim_type ENUM('health', 'vehicle','property', 'travel','other') NOT NULL,
   	submission_date timestamp DEFAULT current_timestamp , 
    claim_statuts ENUM('submitted', 'under review','approved', 'rejected') DEFAULT 'submitted',
	description TEXT ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
	
);



 
 CREATE TABLE salaries (
	salary_id INT (11) AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
	salary_amount DECIMAL (10.2) NOT NULL,
   	salary_date DATE NOT NULL , 
    bonus DECIMAL (10.2) DEFAULT 0.00,
    tax_deductions DECIMAL (15.2) DEFAULT 0.00,
    net_salary DECIMAL(15.2) GENERATED ALWAYS AS (salary_amount+bonus-tax_deductions)STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
	
);


 CREATE TABLE promotions (
	promotion_id INT (11) AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    old_job_title VARCHAR(250),
    new_job_title VARCHAR(255) NOT NULL,
	old_salary DECIMAL (10.2) ,
	new_salary DECIMAL (10.2) NOT NULL,
   	promotion_date DATE NOT NULL , 
    reason TEXT,
    approved_by INT,
	
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
	FOREIGN KEY (approved_by) REFERENCES employees(employee_id)

);

CREATE TABLE retirements (
	retirement_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	employee_id INT,   
	retirement_date DATE NOT NULL , 
    age_at_retirement INT NOT NULL,
    eligibility_date DATE NOT NULL,
    
	pension_amount DECIMAL (10.2) NOT NULL,
    statuts ENUM('pending', 'retired', 'deferred') DEFAULT 'pending',
	description TEXT ,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
	
);

CREATE TABLE turnover (
	turnover_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	employee_id INT,   
	departure_date DATE NOT NULL ,  
    departure_reason ENUM('resignation', 'termination', 'retirement','entract end','other') NOT NULL,
    -- raison de demission
    resignation_reason TEXT ,
    statuts ENUM('processed', 'pending') DEFAULT 'pending',
	feedback TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
	
);
 
CREATE TABLE absences (
	absence_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	employee_id INT,  
	absence_type ENUM('paid leave', 'sick leave', 'unpaid leave','maternity leave','worck accident','other') NOT NULL,
	start_date DATE NOT NULL ,  
    end_date DATE NOT NULL ,  
    -- duree dabsence  en jours
    duration INT GENERATED ALWAYS AS (DATEDIFF(end_date,start_date)+1) STORED, 
	statuts ENUM('pending', 'approved','rejected') DEFAULT 'pending',
    approved_by INT,
    
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
	FOREIGN KEY (approved_by) REFERENCES employees(employee_id)

);

CREATE TABLE employees (
	employee_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR (20) DEFAULT NULL,
	last_name VARCHAR (25) NOT NULL,
	email VARCHAR (100) NOT NULL,
	phone_number VARCHAR (20) DEFAULT NULL,
	hire_date DATE NOT NULL,
	job_id INT (11) NOT NULL,
	salary DECIMAL (8, 2) NOT NULL,
	manager_id INT (11) DEFAULT NULL,
	department_id INT (11) DEFAULT NULL,
	FOREIGN KEY (job_id) REFERENCES jobs (job_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (manager_id) REFERENCES employees (employee_id)
);
 
 CREATE TABLE managers (
	manager_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR (20) DEFAULT NULL,
	last_name VARCHAR (50) NOT NULL,
	hire_date DATE NOT NULL,
	salary DECIMAL (8, 2) NOT NULL,
	job_id INT (11) NOT NULL,
	supervisor_id INT (11),
	department_id INT (11) DEFAULT NULL,
 	FOREIGN KEY (job_id) REFERENCES jobs (job_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (supervisor_id) REFERENCES managers (manager_id) ,
	FOREIGN KEY (department_id) REFERENCES departments (department_id) ON DELETE CASCADE ON UPDATE CASCADE

);
 
 

CREATE TABLE dependents (
	dependent_id INT (11) AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR (50) NOT NULL,
	last_name VARCHAR (50) NOT NULL,
	relationship VARCHAR (25) NOT NULL,
	employee_id INT (11) NOT NULL,
	FOREIGN KEY (employee_id) REFERENCES employees (employee_id) ON DELETE CASCADE ON UPDATE CASCADE
);
