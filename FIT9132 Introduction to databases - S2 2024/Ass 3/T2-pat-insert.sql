/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T2-pat-insert.sql

--Student ID: 34525416
--Student Name: RISHABH RAY

/* Comments for your marker:




*/

--------------------------------------
--INSERT INTO official
--------------------------------------
INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    1,
    'Dwi',
    'Rahayu',
    'USA',
    NULL
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    2,
    'Lindsay',
    'Smith',
    'ESP',
    1
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    3,
    'Charlotte',
    'Pierce',
    'JPN',
    1
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    4,
    'Arif',
    'Hidayat',
    'FRA',
    1
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    5,
    'Minh',
    'Le',
    'EGY',
    2
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    6,
    'Shuyi',
    'Sun',
    'CHN',
    3
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    7,
    'Rodion',
    'Sharlov',
    'AUS',
    1
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    8,
    'Adel',
    'Ahmadi',
    'GER',
    1
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    9,
    'Ahmed',
    'Fahmin',
    'RSA',
    2
);

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    10,
    'Arnab',
    'Biswas',
    'BRA',
    1
);

COMMIT;

--------------------------------------
--INSERT INTO vehicle
--------------------------------------

INSERT INTO vehicle(
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '5J6RE4H48BL023237',
    'AB123CD',
    TO_DATE('2022', 'YYYY'),
    10000,
    4,
    1
);

INSERT INTO vehicle(
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '1HGCE1899RA009926',
    'CD456EF',
    TO_DATE('2021', 'YYYY'),
    15000,
    6,
    1
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '1JCCM85E5BT001312',
    'EF789GH',
    TO_DATE('2020', 'YYYY'),
    8000,
    4,
    2
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    'JH4DB1540PS000784',
    'GH123IJ',
    TO_DATE('2023', 'YYYY'),
    5000,
    5,
    2
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '1G4GJ11Y9HP422546',
    'IJ456KL',
    TO_DATE('2019', 'YYYY'),
    30000,
    6,
    3
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '1G1ZT51FX6F111393',
    'KL789MN',
    TO_DATE('2021', 'YYYY'),
    20000,
    5,
    3
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    'JH4KA3160LC017215',
    'MN123OP',
    TO_DATE('2020', 'YYYY'),
    25000,
    4,
    1
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    'JH4KA8162MC010197',
    'OP456QR',
    TO_DATE('2023', 'YYYY'),
    15000,
    6,
    2
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '5XYKU4A12BG001739',
    'QR789ST',
    TO_DATE('2019', 'YYYY'),
    40000,
    4,
    3
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    'JH4DA3450KS009535',
    'ST123UV',
    TO_DATE('2022', 'YYYY'),
    12000,
    5,
    1
);

COMMIT;

--------------------------------------
--INSERT INTO trip
--------------------------------------
-- Parallel trips (same intended pickup/drop-off times and locations)

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    1,
    4,
    TO_DATE('2024-08-02 09:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 09:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 09:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 09:30', 'YYYY-MM-DD HH24:MI'),
    '5J6RE4H48BL023237',
    2002,
    103,
    104,
    'en',
    2
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    2,
    2,
    TO_DATE('2024-08-02 09:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 09:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 09:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 09:30', 'YYYY-MM-DD HH24:MI'),
    '1HGCE1899RA009926',
    2001,
    103,
    104,
    'en',
    2
);

-- --------------------------------------
-- Task 2: Populate TRIP Table with 20 Entries
-- --------------------------------------

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    3,
    3,
    TO_DATE('2024-08-01 08:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 08:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 08:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 08:30', 'YYYY-MM-DD HH24:MI'),
    '1JCCM85E5BT001312',
    2001,
    101,
    102,
    'en',
    1
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    4,
    1,
    TO_DATE('2024-08-03 10:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-03 10:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-03 10:45', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-03 10:45', 'YYYY-MM-DD HH24:MI'),
    'JH4DB1540PS000784',
    2003,
    105,
    106,
    'fr',
    3
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    5,
    2,
    TO_DATE('2024-08-04 11:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 11:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 11:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 11:30', 'YYYY-MM-DD HH24:MI'),
    '1G4GJ11Y9HP422546',
    2004,
    107,
    108,
    'pt',
    4
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    6,
    5,
    TO_DATE('2024-08-05 08:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-05 08:35', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-05 09:15', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-05 09:15', 'YYYY-MM-DD HH24:MI'),
    '1G1ZT51FX6F111393',
    2001,
    109,
    110,
    'de',
    5
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    7,
    3,
    TO_DATE('2024-08-06 09:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-06 09:35', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-06 10:15', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-06 10:15', 'YYYY-MM-DD HH24:MI'),
    'JH4KA3160LC017215',
    2003,
    111,
    112,
    'fr',
    6
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    8,
    6,
    TO_DATE('2024-08-07 07:45', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 07:50', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 08:25', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 08:25', 'YYYY-MM-DD HH24:MI'),
    'JH4KA8162MC010197',
    2005,
    113,
    114,
    'es',
    7
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    9,
    4,
    TO_DATE('2024-08-07 09:15', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 09:20', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 10:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 10:00', 'YYYY-MM-DD HH24:MI'),
    '5XYKU4A12BG001739',
    2002,
    115,
    116,
    'fr',
    8
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    10,
    5,
    TO_DATE('2024-08-08 14:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-08 14:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-08 14:40', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-08 14:40', 'YYYY-MM-DD HH24:MI'),
    'JH4DA3450KS009535',
    2003,
    117,
    118,
    'en',
    9
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    11,
    4,
    TO_DATE('2024-07-21 09:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-21 09:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-21 09:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-21 09:30', 'YYYY-MM-DD HH24:MI'),
    '5J6RE4H48BL023237',
    2011,
    119,
    117,
    'en',
    1
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    12,
    3,
    TO_DATE('2024-08-01 10:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 10:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 10:35', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 10:35', 'YYYY-MM-DD HH24:MI'),
    '5XYKU4A12BG001739',
    2002,
    119,
    120,
    'fr',
    10
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    13,
    6,
    TO_DATE('2024-07-21 09:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-21 09:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-21 09:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-21 09:30', 'YYYY-MM-DD HH24:MI'),
    '1HGCE1899RA009926',
    2012,
    110,
    111,
    'fr',
    2
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    14,
    4,
    TO_DATE('2024-08-04 10:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 10:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 11:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 11:20', 'YYYY-MM-DD HH24:MI'),
    '1JCCM85E5BT001312',
    2013,
    117,
    113,
    'zh',
    3
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    15,
    4,
    TO_DATE('2024-08-06 20:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-06 20:35', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-06 23:10', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-06 23:10', 'YYYY-MM-DD HH24:MI'),
    'JH4DA3450KS009535',
    2015,
    109,
    113,
    'pt',
    8
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    16,
    6,
    TO_DATE('2024-08-07 17:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 17:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 17:50', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-07 17:50', 'YYYY-MM-DD HH24:MI'),
    '5J6RE4H48BL023237',
    2011,
    113,
    106,
    'en',
    1
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    17,
    2,
    TO_DATE('2024-07-28 15:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-28 15:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-28 15:35', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-28 15:35', 'YYYY-MM-DD HH24:MI'),
    'JH4DB1540PS000784',
    2005,
    111,
    113,
    'es',
    10
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    18,
    4,
    TO_DATE('2024-08-04 08:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 08:35', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 09:15', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-04 09:15', 'YYYY-MM-DD HH24:MI'),
    'JH4DB1540PS000784',
    2010,
    111,
    112,
    'ja',
    4
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    19,
    5,
    TO_DATE('2024-08-03 09:15', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-03 09:20', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-03 10:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-03 10:00', 'YYYY-MM-DD HH24:MI'),
    '1G4GJ11Y9HP422546',
    2001,
    113,
    115,
    'de',
    6
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    20,
    2,
    TO_DATE('2024-08-02 10:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 10:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 10:40', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-02 10:40', 'YYYY-MM-DD HH24:MI'),
    '5J6RE4H48BL023237',
    2005,
    115,
    116,
    'es',
    3
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_act_pickupdt,
    trip_int_dropoffdt,
    trip_act_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    21,
    3,
    TO_DATE('2024-08-01 18:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 18:05', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 19:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-08-01 19:35', 'YYYY-MM-DD HH24:MI'),
    '1HGCE1899RA009926',
    2014,
    102,
    104,
    'en',
    10
);

COMMIT;