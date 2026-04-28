/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T4-pat-mods.sql

--Student ID: 34525416
--Student Name: RISHABH RAY


/* Comments for your marker:




*/

/*(a)*/
DROP TABLE roles CASCADE CONSTRAINTS;

CREATE TABLE roles (
    role_id NUMBER NOT NULL,
    role_name VARCHAR2(50) NOT NULL
);

COMMENT ON COLUMN roles.role_id IS 'Identifier for the role';
COMMENT ON COLUMN roles.role_name IS 'Name of the role (e.g., General, Administrator)';

ALTER TABLE roles
    ADD CONSTRAINT roles_pk PRIMARY KEY (
        role_id
    );

INSERT INTO roles VALUES (
    1,
    'General'
);

INSERT INTO roles VALUES (
    2,
    'Administrator'
);

INSERT INTO roles VALUES (
    3,
    'Head Coach'
);

INSERT INTO roles VALUES (
    4,
    'Coach'
);

INSERT INTO roles VALUES (
    5,
    'Physician'
);

COMMIT;

ALTER TABLE official
    ADD role_id NUMBER DEFAULT 1;

COMMENT ON COLUMN official.role_id IS 'Role assigned to the official (default is General)';

UPDATE official
SET
    role_id = 2
WHERE
    off_cdm IS NULL;

-- UPDATE official
-- SET
--     role_id = 1
-- WHERE
--     off_cdm IS NULL;

ALTER TABLE official
    ADD CONSTRAINT fk_role_id FOREIGN KEY (
        role_id
    )
        REFERENCES roles(
            role_id
        );

SELECT
    *
FROM
    roles;

DESC official;

SELECT
    *
FROM
    official;

COMMIT;

/*(b)*/

DROP TABLE complaint_categories CASCADE CONSTRAINTS;

CREATE TABLE complaint_categories (
    category_id NUMBER NOT NULL,
    category_name VARCHAR2(50) NOT NULL,
    demerit_points NUMBER NOT NULL CHECK (demerit_points > 0)
);

COMMENT ON COLUMN complaint_categories.category_id IS 'Identifier for the complaint category';
COMMENT ON COLUMN complaint_categories.category_name IS 'Category of complaint (e.g., Late Arrival)';
COMMENT ON COLUMN complaint_categories.demerit_points IS 'Demerit points assigned to the complaint category';

ALTER TABLE complaint_categories
    ADD CONSTRAINT complaint_categories_pk PRIMARY KEY (
        category_id
    );

DROP TABLE complaints CASCADE CONSTRAINTS;

CREATE TABLE complaints (
    complaint_id NUMBER NOT NULL,
    trip_id NUMBER NOT NULL,
    official_id int NOT NULL,
    complaint_date DATE NOT NULL,
    category_id NUMBER NOT NULL,
    detailed_comment VARCHAR2(255),
    is_valid CHAR(1) DEFAULT 'N'
);

COMMENT ON COLUMN complaints.complaint_id IS 'Unique identifier for each complaint';
COMMENT ON COLUMN complaints.trip_id IS 'Identifier for the trip associated with the complaint';
COMMENT ON COLUMN complaints.official_id IS 'Identifier for the official associated with the complaint';
COMMENT ON COLUMN complaints.complaint_date IS 'Date and time of the complaint';
COMMENT ON COLUMN complaints.category_id IS 'Identifier for the complaint category';
COMMENT ON COLUMN complaints.detailed_comment IS 'Detailed comment for the complaint';
COMMENT ON COLUMN complaints.is_valid IS 'Flag indicating if the complaint is valid';

ALTER TABLE complaints
    ADD CONSTRAINT complaints_pk PRIMARY KEY (
        complaint_id
    );

ALTER TABLE complaints
    ADD CONSTRAINT fk_trip_id FOREIGN KEY (
        trip_id
    )
        REFERENCES trip(
            trip_id
        );

ALTER TABLE complaints
    ADD CONSTRAINT fk_official_id FOREIGN KEY (
        official_id
    )
        REFERENCES official(
            off_id
        );

ALTER TABLE complaints
    ADD CONSTRAINT fk_category_id FOREIGN KEY (
        category_id
    )
        REFERENCES complaint_categories(
            category_id
        );

INSERT INTO complaint_categories (
    category_id,
    category_name,
    demerit_points
) VALUES (
    1,
    'Late Arrival',
    1
);

INSERT INTO complaint_categories (
    category_id,
    category_name,
    demerit_points
) VALUES (
    2,
    'Rude Behaviour',
    2
);

INSERT INTO complaint_categories (
    category_id,
    category_name,
    demerit_points
) VALUES (
    3,
    'Poor Driving',
    2
);

INSERT INTO complaint_categories (
    category_id,
    category_name,
    demerit_points
) VALUES (
    4,
    'Failing to Assist',
    1
);

SELECT
    *
FROM
    complaint_categories;

DESC COMPLAINT_CATEGORIES;

DESC COMPLAINTS;

COMMIT;