/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T3-pat-dml.sql

--Student ID: 34525416
--Student Name: RISHABH RAY

/* Comments for your marker:




*/

/*(a)*/

DROP SEQUENCE seq_official;

DROP SEQUENCE seq_trip;

CREATE SEQUENCE seq_official
    START WITH 100
    INCREMENT BY 10;

CREATE SEQUENCE seq_trip
    START WITH 100
    INCREMENT BY 10;

/*(b)*/

INSERT INTO official (
    off_id,
    off_given,
    off_family,
    cr_ioc_code,
    off_cdm
) VALUES (
    seq_official.NEXTVAL,
    'Franklin',
    'Gateau',
    'SWZ',
    NULL
);

INSERT INTO vehicle (
    veh_vin,
    veh_rego,
    veh_year,
    veh_curr_odo,
    veh_nopassengers,
    vm_model_id
) VALUES (
    '1C4SDHCT9FC614231',
    'ALP1234',
    TO_DATE('2022', 'YYYY'),
    5000,
    6,
    (SELECT vm_model_id FROM vehicle_model WHERE vm_model = 'Alphard')
);

/*(c)*/
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
    seq_trip.NEXTVAL,
    6,
    TO_DATE('2024-07-30 12:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-30 12:30', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-30 14:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-30 14:00', 'YYYY-MM-DD HH24:MI'),
    '1C4SDHCT9FC614231',
    (SELECT driver_id FROM driver WHERE driver_licence= '55052a543210'),
    (SELECT locn_id FROM location WHERE locn_name = 'Olympic and Paralympic village'),
    (SELECT locn_id FROM location WHERE locn_name = 'Porte de La Chapelle Arena'),
    'en',
    (SELECT off_id FROM official WHERE off_given = 'Franklin' AND off_family = 'Gateau')
);

INSERT INTO trip (
    trip_id,
    trip_nopassengers,
    trip_int_pickupdt,
    trip_int_dropoffdt,
    veh_vin,
    driver_id,
    pickup_locn_id,
    dropoff_locn_id,
    lang_iso_code,
    off_id
) VALUES (
    seq_trip.NEXTVAL,
    6,
    TO_DATE('2024-07-30 20:00', 'YYYY-MM-DD HH24:MI'),
    TO_DATE('2024-07-30 21:15', 'YYYY-MM-DD HH24:MI'),
    '1C4SDHCT9FC614231',
    (SELECT driver_id FROM driver WHERE driver_licence= '55052a543210'),
    (SELECT locn_id FROM location WHERE locn_name = 'Porte de La Chapelle Arena'),
    (SELECT locn_id FROM location WHERE locn_name = 'Olympic and Paralympic village'),
    'en',
    (SELECT off_id FROM official WHERE off_given = 'Franklin' AND off_family = 'Gateau')
);

/*(d)*/

UPDATE trip
SET
    trip_act_pickupdt = TO_DATE(
        '2024-07-30 12:30',
        'YYYY-MM-DD HH24:MI'
    ),
    trip_act_dropoffdt = TO_DATE(
        '2024-07-30 14:15',
        'YYYY-MM-DD HH24:MI'
    )
WHERE
    veh_vin = '1C4SDHCT9FC614231'
    AND trip_int_pickupdt = TO_DATE('2024-07-30 12:30', 'YYYY-MM-DD HH24:MI');

DELETE FROM trip
WHERE
    driver_id = (
        SELECT
            driver_id
        FROM
            driver
        WHERE
            driver_given = 'Claire'
    )
    AND trip_int_pickupdt >= TO_DATE('2024-07-30 17:00', 'YYYY-MM-DD HH24:MI');

COMMIT;