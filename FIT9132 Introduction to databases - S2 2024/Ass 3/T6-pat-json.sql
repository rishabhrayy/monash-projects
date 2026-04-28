/*****PLEASE ENTER YOUR DETAILS BELOW*****/
--T6-pat-json.sql

--Student ID: 34525416
--Student Name: RISHABH RAY


/* Comments for your marker:




*/

-- PLEASE PLACE REQUIRED SQL SELECT STATEMENT TO GENERATE 
-- THE COLLECTION OF JSON DOCUMENTS HERE
-- ENSURE that your query is formatted and has a semicolon
-- (;) at the end of this answer

SELECT
        JSON_OBJECT(
            '_id' VALUE DRI.DRIVER_ID,
                    'name' VALUE TRIM(DRI.DRIVER_GIVEN
                                 || ' '
                                 || DRI.DRIVER_FAMILY),
                    'licence_num' VALUE DRI.DRIVER_LICENCE,
                    'no_of_trips' VALUE COUNT(TRIP_ID),
                    'suspended' VALUE DRI.DRIVER_SUSPENDED,
                    'trips_info' VALUE JSON_ARRAYAGG(
                JSON_OBJECT(
                    'trip_id' VALUE TRIP_ID,
                            'veh_vin' VALUE VEH_VIN,
                            'pick-up' VALUE
                        JSON_OBJECT(
                            'location_id' VALUE PICKUP_LOCN_ID,
                                    'location_name' VALUE LOC1.LOCN_NAME,
                                    'intended_datetime' VALUE TO_CHAR(TRIP_INT_PICKUPDT, 'DD/MM/YYYY HH24:MI'),
                                    'actual_datetime' VALUE TO_CHAR(TRIP_ACT_PICKUPDT, 'DD/MM/YYYY HH24:MI')
                        ),
                            'drop off' VALUE
                        JSON_OBJECT(
                            'location_id' VALUE DROPOFF_LOCN_ID,
                                    'location_name' VALUE LOC2.LOCN_NAME,
                                    'intended_datetime' VALUE TO_CHAR(TRIP_INT_DROPOFFDT, 'DD/MM/YYYY HH24:MI'),
                                    'actual_datetime' VALUE TO_CHAR(TRIP_ACT_DROPOFFDT, 'DD/MM/YYYY HH24:MI')
                        )
                )
            )
        FORMAT JSON)
        || ','
FROM
         TRIP
    JOIN LOCATION LOC1 ON LOC1.LOCN_ID = PICKUP_LOCN_ID 
    JOIN LOCATION LOC2 ON LOC2.LOCN_ID = DROPOFF_LOCN_ID
    JOIN DRIVER DRI ON TRIP.DRIVER_ID = DRI.DRIVER_ID
GROUP BY
    DRI.DRIVER_ID,
    DRI.DRIVER_GIVEN,
    DRI.DRIVER_FAMILY,
    DRI.DRIVER_LICENCE,
    DRI.DRIVER_SUSPENDED
ORDER BY
    DRI.DRIVER_ID;