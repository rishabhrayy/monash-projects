/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T5-pat-select.sql

--Student ID: 34525416
--Student Name: RISHABH RAY


/* Comments for your marker:




*/


/* (a) */

SELECT
    l.locn_id,
    l.locn_name,
    l.locn_address,
    lt.locntype_description,
    count(*)                AS pickup_dropoff_count
FROM
    location      l
    JOIN location_type lt
    ON l.locntype_id = lt.locntype_id
    JOIN trip t
    ON l.locn_id = t.pickup_locn_id
    OR l.locn_id = t.dropoff_locn_id
WHERE
    t.trip_act_dropoffdt IS NOT NULL
GROUP BY
    l.locn_id,
    l.locn_name,
    l.locn_address,
    lt.locntype_description
ORDER BY
    pickup_dropoff_count DESC,
    l.locn_id;

/* (b) */

SELECT
    d.driver_id,
    trim(d.driver_given
         || ' '
         || d.driver_family) AS full_name,
    CASE
        WHEN count(t.trip_id) = 0 THEN
            'No Trips'
        ELSE
            to_char(sum((t.trip_act_dropoffdt - t.trip_int_pickupdt) * 24) * 45.42, '$9990.00')
    END                      AS total_payment
FROM
    driver d
    LEFT JOIN trip t
    ON d.driver_id = t.driver_id
    AND t.trip_act_pickupdt >= TO_DATE('2024-08-01',
    'YYYY-MM-DD')
    AND t.trip_act_dropoffdt <= TO_DATE('2024-08-07',
    'YYYY-MM-DD')
GROUP BY
    d.driver_id,
    trim(d.driver_given
         || ' '
         || d.driver_family)
ORDER BY
    d.driver_id;