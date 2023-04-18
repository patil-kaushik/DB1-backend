CREATE TABLE USERS (
  id INT(11) NOT NULL AUTO_INCREMENT,
  user_type INT(11) NOT NULL DEFAULT 0,
  account_status INT(11) NOT NULL DEFAULT 0,
  email VARCHAR(50),
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  password VARCHAR(50),
  phone VARCHAR(15),
  dob DATE,
  street VARCHAR(50),
  city VARCHAR(50),
  zipcode VARCHAR(10),
  state VARCHAR(50),
  country VARCHAR(50),
  created_on TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
  updated_on TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT PK_ID PRIMARY KEY(id),
  CONSTRAINT UQ_EMAIL UNIQUE(email)
);

CREATE TABLE SERVICE_CATEGORY (
    id INT(10) NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    code VARCHAR(10),
    CONSTRAINT PK_SERVICE_CATEGORY PRIMARY KEY(id),
    CONSTRAINT UQ_NAME UNIQUE(name),
    CONSTRAINT UQ_CODE UNIQUE(code)
);

--CREATE TABLE `PRODUCTS` (
--  `id` int(11) NOT NULL AUTO_INCREMENT,
--  `name` varchar(50) NOT NULL,
--  `images` json NOT NULL,
--  `description` varchar(200) NOT NULL,
--  `condition` varchar(45) NOT NULL DEFAULT 'New' COMMENT '“New”, “Used”',
--  `available_quantity` int(11) NOT NULL,
--  `availability` varchar(45) NOT NULL COMMENT '“InStock”, “OutOfStock”',
--  `category` varchar(45) NOT NULL COMMENT '“Food and Groceries”\n“C”\n“Furniture”\n“Automotive”\n“Electronics”\n“Miscellaneous”',
--  `seller_id` int(11) NOT NULL,
--  `offer` json NOT NULL COMMENT 'Offer JSON:\\n{\\n		"type": "Offer",\\n		"priceCurrency": "USD",\\n		"originalPrice": "119.99",\\n		"offerPrice": "99.99",\\n		"priceValidUntil": "2020-11-05"\\n}\\n\\nType can be: “Offer”, “None”, priceValidUntil format is : YYYY-MM-DD and it can be empty if offerPrice does not expire.',
--  PRIMARY KEY (`id`)
--  );

CREATE TABLE SERVICE_REQUEST (
    id INT(10) NOT NULL AUTO_INCREMENT,
    service_category_code VARCHAR(10),
    customer_id INT(10),
    vendor_id INT(10),
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    requested_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_status INT(1) DEFAULT 0,
    request_status INT(1) DEFAULT 0,
    CONSTRAINT PK_ID PRIMARY KEY(id),
    CONSTRAINT FK_SERVICE_CATEGORY FOREIGN KEY (service_category_code) REFERENCES SERVICE_CATEGORY(code),
    CONSTRAINT FK_CUSTOMER FOREIGN KEY (customer_id) REFERENCES USERS(id),
    CONSTRAINT FK_VENDOR FOREIGN KEY (vendor_id) REFERENCES USERS(id)
);

CREATE TABLE CART (
  id INT(10) NOT NULL AUTO_INCREMENT,
  customer_id INT(10),
  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  products JSON,
  status INT(1) DEFAULT 0,
  CONSTRAINT PK_ID PRIMARY KEY(id),
  CONSTRAINT FK_CUSTOMER FOREIGN KEY (customer_id) REFERENCES USERS(id)
);

-- CREATE TABLE CUSTOMER (
--     id INT(10) NOT NULL AUTO_INCREMENT,
--     first_name VARCHAR(20),
--     last_name VARCHAR(20),
--     email VARCHAR(500),
--     password VARCHAR(10),
--     contact_number CHAR(10),
--     street VARCHAR(50),
--     city VARCHAR(50),
--     zipcode CHAR(5),
--     state VARCHAR(50),
--     country VARCHAR(50),
--     created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     points INT(10),
--     CONSTRAINT PK_ID PRIMARY KEY(id),
--     CONSTRAINT UQ_EMAIL UNIQUE(email)
-- );

-- CREATE TABLE VENDOR (
--     id INT(10) NOT NULL AUTO_INCREMENT,
--     name VARCHAR(20),
--     email VARCHAR(500),
--     password VARCHAR(10),
--     street VARCHAR(50),
--     city VARCHAR(50),
--     zipcode CHAR(5),
--     state VARCHAR(50),
--     country VARCHAR(50),
--     contact_number CHAR(10),
--     created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT PK_ID PRIMARY KEY(id),
--     CONSTRAINT UQ_EMAIL UNIQUE(email)
-- );

-- CREATE TABLE SERVICE_CATEGORY (
--     id INT(10) NOT NULL AUTO_INCREMENT,
--     name VARCHAR(50),
--     code VARCHAR(10),
--     max_bid FLOAT(5, 2),
--     CONSTRAINT PK_SERVICE_CATEGORY PRIMARY KEY(id),
--     CONSTRAINT UQ_NAME UNIQUE(name),
--     CONSTRAINT UQ_CODE UNIQUE(code)
-- );

-- CREATE TABLE SERVICE_REQUEST (
--     id INT(10) NOT NULL AUTO_INCREMENT,
--     service_category_id INT(10),
--     customer_id INT(10),
--     vendor_id INT(10),
--     created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     requested_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     completed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     payment_status INT(1) DEFAULT 0,
--     request_status INT(1) DEFAULT 0,
--     current_bid FLOAT(5, 2),
--     max_bid FLOAT(5, 2),
--     CONSTRAINT PK_ID PRIMARY KEY(id),
--     CONSTRAINT FK_SERVICE_CATEGORY FOREIGN KEY (service_category_id) REFERENCES SERVICE_CATEGORY(id),
--     CONSTRAINT FK_CUSTOMER FOREIGN KEY (customer_id) REFERENCES CUSTOMER(id),
--     CONSTRAINT FK_VENDOR FOREIGN KEY (vendor_id) REFERENCES VENDOR(id)
-- );

-- CREATE TABLE VENDOR_BIDDING (
--     vendor_id INT(10),
--     service_request_id INT(10),
--     bid FLOAT(5, 2),
--     created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     CONSTRAINT FK_VENDOR_BIDDING FOREIGN KEY (vendor_id) REFERENCES VENDOR(id),
--     CONSTRAINT FK_SERVICE_REQUEST FOREIGN KEY (service_request_id) REFERENCES SERVICE_REQUEST(id)
-- );

-- CREATE TABLE VENDOR_RATING (
--     vendor_id INT(10),
--     rating FLOAT(2, 1),
--     review VARCHAR(500),
--     customer_id INT(10)
-- );

-- CREATE TABLE PRODUCT_REQUESTS (
--     id INT(10) NOT NULL AUTO_INCREMENT,
--     prod_id INT(11),
--     requested_by INT(11),
--     filled INT(11) NOT NULL DEFAULT 0,
--     quantity INT(11),
-- 	  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- 	  updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
-- 	  CONSTRAINT PK_ID PRIMARY KEY(id)
-- )
