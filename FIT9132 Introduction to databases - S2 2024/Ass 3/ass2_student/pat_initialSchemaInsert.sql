/*
  Database Unit 2024 Semester 2
  --Paris Arrow Transport Schema File and Initial Data--
  --pat_initialSchemaInsert.sql

  Description:
  This file creates the Paris Arrow Transport tables
  and populates several of the tables (those shown in purple on the supplied model).
  You should read this schema file carefully
  and be sure you understand the various data requirements.

Author: FIT Database Teaching Team
License: Copyright Monash University, unless otherwise stated. All Rights Reserved.
COPYRIGHT WARNING
Warning
This material is protected by copyright. For use within Monash University only. NOT FOR RESALE.
Do not remove this notice.

*/

-- Drop all tables
DROP TABLE country_region CASCADE CONSTRAINTS;

DROP TABLE driver CASCADE CONSTRAINTS;

DROP TABLE driver_language CASCADE CONSTRAINTS;

DROP TABLE language CASCADE CONSTRAINTS;

DROP TABLE location CASCADE CONSTRAINTS;

DROP TABLE location_type CASCADE CONSTRAINTS;

DROP TABLE manufacturer CASCADE CONSTRAINTS;

DROP TABLE official CASCADE CONSTRAINTS;

DROP TABLE trip CASCADE CONSTRAINTS;

DROP TABLE vehicle CASCADE CONSTRAINTS;

DROP TABLE vehicle_model CASCADE CONSTRAINTS;

-- Create purple tables
CREATE TABLE country_region (
    cr_ioc_code    CHAR(3) NOT NULL,
    cr_name        VARCHAR2(40) NOT NULL,
    cr_no_athletes NUMBER(10) NOT NULL
);

COMMENT ON COLUMN country_region.cr_ioc_code IS
    'IOC country code - identifier';

COMMENT ON COLUMN country_region.cr_name IS
    'Country/Region name';

COMMENT ON COLUMN country_region.cr_no_athletes IS
    'Number of athletes sent by the country/region';

ALTER TABLE country_region ADD CONSTRAINT country_region_pk PRIMARY KEY ( cr_ioc_code
);

ALTER TABLE country_region ADD CONSTRAINT cr_name_uq UNIQUE ( cr_name );

CREATE TABLE driver (
    driver_id        NUMBER(4) NOT NULL,
    driver_given     VARCHAR2(30),
    driver_family    VARCHAR2(30),
    driver_licence   CHAR(12) NOT NULL,
    driver_dob       DATE NOT NULL,
    driver_clearance CHAR(1) DEFAULT 'R' NOT NULL,
    driver_suspended CHAR(1) NOT NULL
);

ALTER TABLE driver
    ADD CONSTRAINT driver_clearance_chk CHECK ( driver_clearance IN ( 'F', 'R' ) );

ALTER TABLE driver
    ADD CHECK ( driver_suspended IN ( 'N', 'Y' ) );

COMMENT ON COLUMN driver.driver_id IS
    'Driver identifier';

COMMENT ON COLUMN driver.driver_given IS
    'Driver given name';

COMMENT ON COLUMN driver.driver_family IS
    'Driver family name';

COMMENT ON COLUMN driver.driver_licence IS
    'Driver licence number';

COMMENT ON COLUMN driver.driver_dob IS
    'Driver date of birth';

COMMENT ON COLUMN driver.driver_clearance IS
    'Clearance granted to driver (F, R) - default R';

COMMENT ON COLUMN driver.driver_suspended IS
    'Driver suspended (Y or N)';

ALTER TABLE driver ADD CONSTRAINT driver_pk PRIMARY KEY ( driver_id );

ALTER TABLE driver ADD CONSTRAINT driver_licence_uq UNIQUE ( driver_licence );

CREATE TABLE driver_language (
    driver_id     NUMBER(4) NOT NULL,
    lang_iso_code CHAR(2) NOT NULL
);

COMMENT ON COLUMN driver_language.driver_id IS
    'Driver identifier';

COMMENT ON COLUMN driver_language.lang_iso_code IS
    'ISO639-1 two character language codes - identifier';

ALTER TABLE driver_language ADD CONSTRAINT driver_language_pk PRIMARY KEY ( driver_id
,
                                                                            lang_iso_code
                                                                            );

CREATE TABLE language (
    lang_iso_code CHAR(2) NOT NULL,
    lang_name     VARCHAR2(50) NOT NULL
);

COMMENT ON COLUMN language.lang_iso_code IS
    'ISO639-1 two character language codes - identifier';

COMMENT ON COLUMN language.lang_name IS
    'Name of language';

ALTER TABLE language ADD CONSTRAINT language_pk PRIMARY KEY ( lang_iso_code );

ALTER TABLE language ADD CONSTRAINT lang_name_uq UNIQUE ( lang_name );

CREATE TABLE location (
    locn_id      NUMBER(3) NOT NULL,
    locn_name    VARCHAR2(50) NOT NULL,
    locn_address VARCHAR2(100) NOT NULL,
    locntype_id  NUMBER(2) NOT NULL
);

COMMENT ON COLUMN location.locn_id IS
    'Idenfifier for location';

COMMENT ON COLUMN location.locn_name IS
    'Name of location';

COMMENT ON COLUMN location.locn_address IS
    'Address of this location';

COMMENT ON COLUMN location.locntype_id IS
    'Location type identifier';

ALTER TABLE location ADD CONSTRAINT location_pk PRIMARY KEY ( locn_id );

ALTER TABLE location ADD CONSTRAINT locn_name_uq UNIQUE ( locn_name );

CREATE TABLE location_type (
    locntype_id          NUMBER(2) NOT NULL,
    locntype_description VARCHAR2(50) NOT NULL
);

COMMENT ON COLUMN location_type.locntype_id IS
    'Location type identifier';

COMMENT ON COLUMN location_type.locntype_description IS
    'Description of location type';

ALTER TABLE location_type ADD CONSTRAINT location_type_pk PRIMARY KEY ( locntype_id )
;

ALTER TABLE location_type ADD CONSTRAINT locntype_desc_uq UNIQUE ( locntype_description
);

CREATE TABLE manufacturer (
    man_id   NUMBER(3) NOT NULL,
    man_name VARCHAR2(30) NOT NULL
);

COMMENT ON COLUMN manufacturer.man_id IS
    'Identifier for manufacturer';

COMMENT ON COLUMN manufacturer.man_name IS
    'Name of manufacturer';

ALTER TABLE manufacturer ADD CONSTRAINT manufacturer_pk PRIMARY KEY ( man_id );

ALTER TABLE manufacturer ADD CONSTRAINT man_name_uq UNIQUE ( man_name );

CREATE TABLE vehicle_model (
    vm_model_id NUMBER(4) NOT NULL,
    vm_model    VARCHAR2(30) NOT NULL,
    man_id      NUMBER(3) NOT NULL
);

COMMENT ON COLUMN vehicle_model.vm_model_id IS
    'Surrogate key added due to the length natural key ';

COMMENT ON COLUMN vehicle_model.vm_model IS
    'Model identifier (name of model)';

COMMENT ON COLUMN vehicle_model.man_id IS
    'Identifier for manufacturer';

ALTER TABLE vehicle_model ADD CONSTRAINT vehicle_model_pk PRIMARY KEY ( vm_model_id )
;

ALTER TABLE driver_language
    ADD CONSTRAINT driver_driver_language_fk FOREIGN KEY ( driver_id )
        REFERENCES driver ( driver_id );

ALTER TABLE driver_language
    ADD CONSTRAINT language_driver_lang_fk FOREIGN KEY ( lang_iso_code )
        REFERENCES language ( lang_iso_code );

ALTER TABLE location
    ADD CONSTRAINT locationtype_location_fk FOREIGN KEY ( locntype_id )
        REFERENCES location_type ( locntype_id );

ALTER TABLE vehicle_model
    ADD CONSTRAINT manufacturer_veh_model_fk FOREIGN KEY ( man_id )
        REFERENCES manufacturer ( man_id );

--Loading initial data
--COUNTRY_REGION
INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LIE',
    'Liechtenstein',
    1
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LTU',
    'Lithuania',
    51
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LUX',
    'Luxembourg',
    14
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MAD',
    'Madagascar',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MAW',
    'Malawi',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MAS',
    'Malaysia',
    26
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MDV',
    'Maldives',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MLI',
    'Mali',
    23
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MLT',
    'Malta',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MHL',
    'Marshall Islands',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MTN',
    'Mauritania',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MRI',
    'Mauritius',
    13
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MEX',
    'Mexico',
    107
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MDA',
    'Republic of Moldova',
    26
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MON',
    'Monaco',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MGL',
    'Mongolia',
    32
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MNE',
    'Montenegro',
    19
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MAR',
    'Morocco',
    60
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MOZ',
    'Mozambique',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MYA',
    'Myanmar',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NAM',
    'Namibia',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NRU',
    'Nauru',
    1
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NEP',
    'Nepal',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NED',
    'Netherlands',
    258
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NZL',
    'New Zealand',
    195
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NCA',
    'Nicaragua',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NIG',
    'Niger',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NGR',
    'Nigeria',
    88
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PRK',
    'Democratic People''s Republic of Korea',
    16
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'MKD',
    'Republic of North Macedonia',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'NOR',
    'Norway',
    107
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'OMA',
    'Oman',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PAK',
    'Pakistan',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PLW',
    'Palau',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PLE',
    'Palestine',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PAN',
    'Panama',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PNG',
    'Papua New Guinea',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PAR',
    'Paraguay',
    28
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PER',
    'Peru',
    26
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PHI',
    'Philippines',
    22
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'POL',
    'Poland',
    210
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'POR',
    'Portugal',
    73
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'PUR',
    'Puerto Rico',
    51
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'QAT',
    'Qatar',
    14
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'EOR',
    'IOC Refugee Olympic Team',
    37
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CGO',
    'Congo',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ROU',
    'Romania',
    106
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'RWA',
    'Rwanda',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SKN',
    'Saint Kitts and Nevis',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LCA',
    'Saint Lucia',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'VIN',
    'St Vincent and The Grenadines',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SAM',
    'Samoa',
    24
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SMR',
    'San Marino',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'STP',
    'Sao Tome and Principe',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KSA',
    'Saudi Arabia',
    9
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SEN',
    'Senegal',
    11
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SRB',
    'Serbia',
    113
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SEY',
    'Seychelles',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SLE',
    'Sierra Leone',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SGP',
    'Singapore',
    23
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SVK',
    'Slovakia',
    28
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SLO',
    'Slovenia',
    90
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SOL',
    'Solomon Islands',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SOM',
    'Somalia',
    1
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'RSA',
    'South Africa',
    149
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KOR',
    'Republic of Korea',
    141
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SSD',
    'South Sudan',
    14
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ESP',
    'Spain',
    383
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SRI',
    'Sri Lanka',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SUD',
    'Sudan',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SUR',
    'Suriname',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SWE',
    'Sweden',
    117
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SUI',
    'Switzerland',
    127
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SYR',
    'Syrian Arab Republic',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TJK',
    'Tajikistan',
    14
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TAN',
    'United Republic of Tanzania',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'THA',
    'Thailand',
    51
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GAM',
    'Gambia',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TOG',
    'Togo',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TGA',
    'Tonga',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TTO',
    'Trinidad and Tobago',
    18
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TUN',
    'Tunisia',
    27
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TUR',
    'Turkey',
    102
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TKM',
    'Turkmenistan',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TUV',
    'Tuvalu',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'UGA',
    'Uganda',
    24
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'UKR',
    'Ukraine',
    140
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'UAE',
    'United Arab Emirates',
    13
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'USA',
    'United States of America',
    592
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'URU',
    'Uruguay',
    25
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'UZB',
    'Uzbekistan',
    86
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'VAN',
    'Vanuatu',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'VEN',
    'Venezuela',
    33
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'VIE',
    'Vietnam',
    16
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ISV',
    'Virgin Islands, US',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'YEM',
    'Yemen',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ZAM',
    'Zambia',
    27
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ZIM',
    'Zimbabwe',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'AFG',
    'Afghanistan',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ALB',
    'Albania',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ALG',
    'Algeria',
    45
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ASA',
    'American Samoa',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'AND',
    'Andorra',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ANG',
    'Angola',
    24
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ANT',
    'Antigua and Barbuda',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ARG',
    'Argentina',
    136
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ARM',
    'Armenia',
    15
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ARU',
    'Aruba',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'AUS',
    'Australia',
    460
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'AUT',
    'Austria',
    78
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'AZE',
    'Azerbaijan',
    48
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BAH',
    'Bahamas',
    18
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BRN',
    'Bahrain',
    13
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BAN',
    'Bangladesh',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BAR',
    'Barbados',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BEL',
    'Belgium',
    165
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BIZ',
    'Belize',
    1
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BEN',
    'Benin',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BER',
    'Bermuda',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BHU',
    'Bhutan',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BOL',
    'Bolivia',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BIH',
    'Bosnia and Herzegovina',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BOT',
    'Botswana',
    11
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BRA',
    'Brazil',
    277
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'IVB',
    'Virgin Islands, British',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BRU',
    'Brunei Darussalam',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BUL',
    'Bulgaria',
    47
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BUR',
    'Burkina Faso',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'BDI',
    'Burundi',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CAM',
    'Cambodia',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CMR',
    'Cameroon',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CAN',
    'Canada',
    315
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CPV',
    'Cape Verde',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CAY',
    'Cayman Islands',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CAF',
    'Central African Republic',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CHA',
    'Chad',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CHI',
    'Chile',
    48
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CHN',
    'People''s Republic of China',
    388
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TPE',
    'Chinese Taipei',
    60
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'COL',
    'Colombia',
    87
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'COM',
    'Comoros',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'COK',
    'Cook Islands',
    2
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CRC',
    'Costa Rica',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CRO',
    'Croatia',
    73
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CUB',
    'Cuba',
    61
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CYP',
    'Cyprus',
    16
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CZE',
    'Czech Republic',
    111
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'COD',
    'Democratic Republic of the Congo',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'DEN',
    'Denmark',
    124
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'DJI',
    'Djibouti',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'DMA',
    'Dominica',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'DOM',
    'Dominican Republic',
    58
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'TLS',
    'Democratic Republic of Timor-Leste',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ECU',
    'Ecuador',
    40
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'EGY',
    'Egypt',
    148
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ESA',
    'El Salvador',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GEQ',
    'Equatorial Guinea',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ERI',
    'Eritrea',
    12
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'EST',
    'Estonia',
    24
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'SWZ',
    'Eswatini',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ETH',
    'Ethiopia',
    34
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'FSM',
    'Federated States of Micronesia',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'FIJ',
    'Fiji',
    33
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'FIN',
    'Finland',
    56
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'FRA',
    'France',
    573
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GAB',
    'Gabon',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GEO',
    'Georgia',
    28
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GER',
    'Germany',
    428
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GHA',
    'Ghana',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GBR',
    'Great Britain',
    327
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GRE',
    'Greece',
    100
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GRN',
    'Grenada',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GUM',
    'Guam',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GUA',
    'Guatemala',
    16
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GBS',
    'Guinea-Bissau',
    6
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GUI',
    'Guinea',
    24
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'GUY',
    'Guyana',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'HAI',
    'Haiti',
    7
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'HON',
    'Honduras',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'HKG',
    'Hong Kong, China',
    36
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'HUN',
    'Hungary',
    170
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ISL',
    'Iceland',
    5
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'IND',
    'India',
    117
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'IOA',
    'Independent Olympic Athletes',
    32
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'INA',
    'Indonesia',
    29
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'IRI',
    'Islamic Republic of Iran',
    40
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'IRQ',
    'Iraq',
    22
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'IRL',
    'Ireland',
    134
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ISR',
    'Israel',
    88
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'ITA',
    'Italy',
    371
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'CIV',
    'Cote d''Ivoire',
    11
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'JAM',
    'Jamaica',
    58
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'JPN',
    'Japan',
    403
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'JOR',
    'Jordan',
    12
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KAZ',
    'Kazakhstan',
    79
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KEN',
    'Kenya',
    72
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KIR',
    'Kiribati',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KOS',
    'Kosovo',
    9
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KUW',
    'Kuwait',
    9
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'KGZ',
    'Kyrgyzstan',
    16
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LAO',
    'Lao People''s Democratic Republic',
    4
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LAT',
    'Latvia',
    29
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LBN',
    'Lebanon',
    10
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LES',
    'Lesotho',
    3
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LBR',
    'Liberia',
    8
);

INSERT INTO country_region (
    cr_ioc_code,
    cr_name,
    cr_no_athletes
) VALUES (
    'LBA',
    'Libya',
    6
);

--MANUFACTURER
INSERT INTO manufacturer (
    man_id,
    man_name
) VALUES (
    101,
    'Mercedes-Benz'
);

INSERT INTO manufacturer (
    man_id,
    man_name
) VALUES (
    104,
    'Peugeot'
);

INSERT INTO manufacturer (
    man_id,
    man_name
) VALUES (
    105,
    'Renault'
);

INSERT INTO manufacturer (
    man_id,
    man_name
) VALUES (
    103,
    'Toyota'
);

INSERT INTO manufacturer (
    man_id,
    man_name
) VALUES (
    102,
    'Volvo '
);

--VEHICLE_MODEL
INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    1,
    'Sprinter Passenger Van',
    101
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    2,
    'Citaro',
    101
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    3,
    '9700',
    102
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    4,
    '9700 DD',
    102
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    5,
    '7900 Electric',
    102
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    6,
    'Hiace',
    103
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    7,
    'Alphard',
    103
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    8,
    'Traveller',
    104
);

INSERT INTO vehicle_model (
    vm_model_id,
    vm_model,
    man_id
) VALUES (
    9,
    'Master III',
    105
);

--LOCATION_TYPE
INSERT INTO location_type (
    locntype_id,
    locntype_description
) VALUES (
    2,
    'Arena'
);

INSERT INTO location_type (
    locntype_id,
    locntype_description
) VALUES (
    1,
    'Stadium'
);

INSERT INTO location_type (
    locntype_id,
    locntype_description
) VALUES (
    4,
    'Tourist attraction'
);

INSERT INTO location_type (
    locntype_id,
    locntype_description
) VALUES (
    3,
    'Village'
);

--LOCATION
INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    101,
    'Bordeaux Stadium',
    'Cr Jules Ladoumegue, 33300 Bordeaux, France',
    1
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    102,
    'Bercy Arena',
    '8 Bd de Bercy, 75012 Paris, France',
    2
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    103,
    'Champ de Mars Arena',
    '2 Pl. Joffre, 75007 Paris, France',
    2
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    104,
    'Eiffel Tower Stadium',
    'Pl. Jacques Rueff, 75007 Paris, France',
    1
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    105,
    'South Paris Arena',
    '1 Pl. de la Prte de Versailles, 75015 Paris, France',
    2
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    106,
    'La Beaujoire Stadium',
    '333 Rte de Saint-Joseph, 44300 Nantes, France',
    1
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    107,
    'North Paris Arena',
    'Hall 8, 82 Av. des Nations, 93420 Villepinte, France',
    2
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    108,
    'Parc des Princes',
    '24 Rue du Commandant Guilbaud, 75016 Paris, France',
    1
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    109,
    'Paris La Defense Arena',
    '99 Jard. de l''Arche, 92000 Nanterre, France',
    2
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    110,
    'Pierre Mauroy Stadium',
    '261 Bd de Tournai, 59650 Villeneuve-d''Ascq, France',
    1
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    111,
    'Porte de La Chapelle Arena',
    '56 Bd Ney, 75018 Paris, France',
    2
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    112,
    'Roland Garros Stadium',
    '2 Av. Gordon Bennett, 75016 Paris, France',
    1
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    113,
    'Olympic and Paralympic village',
    'D1, 93200 Saint-Denis, France',
    3
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    114,
    'Champions Park',
    '75116 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    115,
    'Eiffel Tower',
    'Av. Gustave Eiffel, 75007 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    116,
    'Louvre Museum',
    '75001 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    117,
    'Tuileries Garden',
    '75001 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    118,
    'Sainte-Chapelle',
    '10 Bd du Palais, 75001 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    119,
    'Arc de Triomphe',
    'Pl. Charles de Gaulle, 75008 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    120,
    'The Basilica of the Sacred Heart of Paris',
    '35 Rue du Chevalier de la Barre, 75018 Paris, France',
    4
);

INSERT INTO location (
    locn_id,
    locn_name,
    locn_address,
    locntype_id
) VALUES (
    121,
    'Saint-Quentin-en-Yvelines Velodrome',
    '1 Rue Laurent Fignon, Pl. de la Paix Celeste, 78180 Montigny-le-Bretonneux, France'
    ,
    1
);

--LANGUAGE
INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ab',
    'Abkhazian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'aa',
    'Afar'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'af',
    'Afrikaans'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ak',
    'Akan'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sq',
    'Albanian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'am',
    'Amharic'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ar',
    'Arabic'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'an',
    'Aragonese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'hy',
    'Armenian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'as',
    'Assamese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'av',
    'Avaric'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ae',
    'Avestan'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ay',
    'Aymara'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'az',
    'Azerbaijani'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bm',
    'Bambara'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ba',
    'Bashkir'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'eu',
    'Basque'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'be',
    'Belarusian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bn',
    'Bengali (Bangla)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bh',
    'Bihari'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bi',
    'Bislama'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bs',
    'Bosnian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'br',
    'Breton'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bg',
    'Bulgarian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'my',
    'Burmese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ca',
    'Catalan'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ch',
    'Chamorro'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ce',
    'Chechen'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ny',
    'Chichewa, Chewa, Nyanja'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'zh',
    'Chinese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'cv',
    'Chuvash'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kw',
    'Cornish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'co',
    'Corsican'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'cr',
    'Cree'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'hr',
    'Croatian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'cs',
    'Czech'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'da',
    'Danish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'dv',
    'Divehi, Dhivehi, Maldivian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'nl',
    'Dutch'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'dz',
    'Dzongkha'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'en',
    'English'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'eo',
    'Esperanto'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'et',
    'Estonian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ee',
    'Ewe'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'fo',
    'Faroese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'fj',
    'Fijian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'fi',
    'Finnish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'fr',
    'French'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ff',
    'Fula, Fulah, Pulaar, Pular'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'gv',
    'Gaelic (Manx)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'gd',
    'Gaelic (Scottish)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'gl',
    'Galician'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ka',
    'Georgian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'de',
    'German'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'el',
    'Greek'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'gn',
    'Guarani'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'gu',
    'Gujarati'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ht',
    'Haitian Creole'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ha',
    'Hausa'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'he',
    'Hebrew'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'hz',
    'Herero'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'hi',
    'Hindi'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ho',
    'Hiri Motu'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'hu',
    'Hungarian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'is',
    'Icelandic'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'io',
    'Ido'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ig',
    'Igbo'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'id',
    'Indonesian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ia',
    'Interlingua'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ie',
    'Interlingue'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'iu',
    'Inuktitut'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ik',
    'Inupiak'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ga',
    'Irish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'it',
    'Italian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ja',
    'Japanese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'jv',
    'Javanese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kl',
    'Kalaallisut, Greenlandic'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kn',
    'Kannada'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kr',
    'Kanuri'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ks',
    'Kashmiri'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kk',
    'Kazakh'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'km',
    'Khmer'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ki',
    'Kikuyu'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'rw',
    'Kinyarwanda (Rwanda)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'rn',
    'Kirundi'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kv',
    'Komi'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kg',
    'Kongo'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ko',
    'Korean'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ku',
    'Kurdish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'kj',
    'Kwanyama'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ky',
    'Kyrgyz'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'lo',
    'Lao'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'la',
    'Latin'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'lv',
    'Latvian (Lettish)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'li',
    'Limburgish ( Limburger)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ln',
    'Lingala'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'lt',
    'Lithuanian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'lu',
    'Luga-Katanga'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'lg',
    'Luganda, Ganda'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'lb',
    'Luxembourgish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mk',
    'Macedonian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mg',
    'Malagasy'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ms',
    'Malay'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ml',
    'Malayalam'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mt',
    'Maltese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mi',
    'Maori'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mr',
    'Marathi'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mh',
    'Marshallese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mo',
    'Moldavian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'mn',
    'Mongolian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'na',
    'Nauru'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'nv',
    'Navajo'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ng',
    'Ndonga'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ne',
    'Nepali'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'nd',
    'Northern Ndebele'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'no',
    'Norwegian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'nb',
    'Norwegian bokmål'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'nn',
    'Norwegian nynorsk'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'oc',
    'Occitan'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'oj',
    'Ojibwe'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'cu',
    'Old Church Slavonic, Old Bulgarian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'or',
    'Oriya'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'om',
    'Oromo (Afaan Oromo)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'os',
    'Ossetian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ps',
    'Pashto, Pushto'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'fa',
    'Persian (Farsi)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'pl',
    'Polish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'pt',
    'Portuguese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'pa',
    'Punjabi (Eastern)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'pi',
    'Pali'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'qu',
    'Quechua'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ro',
    'Romanian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'rm',
    'Romansh'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ru',
    'Russian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'se',
    'Sami'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sm',
    'Samoan'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sg',
    'Sango'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sa',
    'Sanskrit'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sr',
    'Serbian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sh',
    'Serbo-Croatian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'st',
    'Sesotho'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tn',
    'Setswana'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sn',
    'Shona'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ii',
    'Sichuan Yi, Nuosu'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sd',
    'Sindhi'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'si',
    'Sinhalese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sk',
    'Slovak'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sl',
    'Slovenian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'so',
    'Somali'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'nr',
    'Southern Ndebele'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'es',
    'Spanish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'su',
    'Sundanese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sw',
    'Swahili (Kiswahili)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ss',
    'Swati (Siswati)'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'sv',
    'Swedish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tl',
    'Tagalog'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ty',
    'Tahitian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tg',
    'Tajik'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ta',
    'Tamil'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tt',
    'Tatar'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'te',
    'Telugu'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'th',
    'Thai'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'bo',
    'Tibetan'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ti',
    'Tigrinya'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'to',
    'Tonga'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ts',
    'Tsonga'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tr',
    'Turkish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tk',
    'Turkmen'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'tw',
    'Twi'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'uk',
    'Ukrainian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ur',
    'Urdu'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'ug',
    'Uyghur'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'uz',
    'Uzbek'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    've',
    'Venda'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'vi',
    'Vietnamese'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'vo',
    'Volapük'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'wa',
    'Wallon'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'cy',
    'Welsh'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'fy',
    'Western Frisian'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'wo',
    'Wolof'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'xh',
    'Xhosa'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'yi',
    'Yiddish'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'yo',
    'Yoruba'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'za',
    'Zhuang, Chuang'
);

INSERT INTO language (
    lang_iso_code,
    lang_name
) VALUES (
    'zu',
    'Zulu'
);

--DRIVER
INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2001,
    'Pierre',
    'Martin',
    '120501123456',
    TO_DATE('01-AUG-1994', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2002,
    'Marie',
    'Dupont',
    '34082A789012',
    TO_DATE('26-AUG-1996', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2003,
    'Louis',
    'Dubois',
    '45112B654321',
    TO_DATE('24-JUN-1968', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2004,
    'Antoine',
    'Lefevre',
    '670495098765',
    TO_DATE('06-OCT-1987', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2005,
    'Sophie',
    'Bernard',
    '89122a345678',
    TO_DATE('11-FEB-1994', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2006,
    'Arman',
    '23072b567890',
    TO_DATE('14-MAY-1972', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2007,
    'Jean',
    'Moreau',
    '560903234567',
    TO_DATE('20-NOV-1968', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2008,
    'Isabelle',
    'Fournier',
    '780350987654',
    TO_DATE('10-FEB-1967', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2009,
    'Emilie',
    'Michel',
    '900115876543',
    TO_DATE('03-MAR-1968', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2010,
    'Naoki',
    'Fujimoto',
    '110685765432',
    TO_DATE('06-MAR-1980', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2011,
    'Mathieu',
    'Girard',
    '22102A456789',
    TO_DATE('16-FEB-1992', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2012,
    'Mansour',
    '33022B678901',
    TO_DATE('01-JUL-1974', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2013,
    'Lei',
    'Xiong',
    '441270890123',
    TO_DATE('17-AUG-1973', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2014,
    'Claire',
    'Robert',
    '55052a543210',
    TO_DATE('13-MAR-1997', 'DD-MON-YYYY'),
    'R',
    'N'
);

INSERT INTO driver (
    driver_id,
    driver_given,
    driver_family,
    driver_licence,
    driver_dob,
    driver_clearance,
    driver_suspended
) VALUES (
    2015,
    'Nathalie',
    'Renaud',
    '660725432109',
    TO_DATE('28-NOV-1970', 'DD-MON-YYYY'),
    'R',
    'N'
);

--DRIVER_LANGUAGE
INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2001,
    'de'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2001,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2001,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2002,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2002,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2003,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2003,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2004,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2004,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2004,
    'pt'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2005,
    'es'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2005,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2006,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2006,
    'kk'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2007,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2007,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2008,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2009,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2009,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2010,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2010,
    'ja'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2011,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2011,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2012,
    'ar'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2012,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2013,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2013,
    'zh'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2014,
    'en'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2014,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2015,
    'fr'
);

INSERT INTO driver_language (
    driver_id,
    lang_iso_code
) VALUES (
    2015,
    'pt'
);

COMMIT;