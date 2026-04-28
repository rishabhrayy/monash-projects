// *****PLEASE ENTER YOUR DETAILS BELOW*****
// T6-pat-mongo.mongodb.js

// Student ID: 34525416
// Student Name: RISHABH RAY

//Comments for your marker:

// ===================================================================================
// Do not add new comments to this playground
// OR modify or remove any of the comments below (items marked with //)
// ===================================================================================

// Use (connect to) your database - you MUST update xyz001
// with your authcate username

use("rray0009");

// (b)
// PLEASE PLACE REQUIRED MONGODB COMMAND TO CREATE THE COLLECTION HERE
// YOU MAY PICK ANY COLLECTION NAME
// ENSURE that your query is formatted and has a semicolon
// (;) at the end of this answer

// Drop collection

db.driver.drop();


// Create collection and insert documents

db.driver.insertMany([{"_id":2001,"name":"Pierre Martin","licence_num":"120501123456","no_of_trips":4,"suspended":"N","trips_info":[{"trip_id":2,"veh_vin":"1HGCE1899RA009926","pick-up":{"location_id":103,"location_name":"Champ de Mars Arena","intended_datetime":"02/08/2024 09:00","actual_datetime":"02/08/2024 09:05"},"drop off":{"location_id":104,"location_name":"Eiffel Tower Stadium","intended_datetime":"02/08/2024 09:30","actual_datetime":"02/08/2024 09:30"}},{"trip_id":19,"veh_vin":"1G4GJ11Y9HP422546","pick-up":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"03/08/2024 09:15","actual_datetime":"03/08/2024 09:20"},"drop off":{"location_id":115,"location_name":"Eiffel Tower","intended_datetime":"03/08/2024 10:00","actual_datetime":"03/08/2024 10:00"}},{"trip_id":6,"veh_vin":"1G1ZT51FX6F111393","pick-up":{"location_id":109,"location_name":"Paris La Defense Arena","intended_datetime":"05/08/2024 08:30","actual_datetime":"05/08/2024 08:35"},"drop off":{"location_id":110,"location_name":"Pierre Mauroy Stadium","intended_datetime":"05/08/2024 09:15","actual_datetime":"05/08/2024 09:15"}},{"trip_id":3,"veh_vin":"1JCCM85E5BT001312","pick-up":{"location_id":101,"location_name":"Bordeaux Stadium","intended_datetime":"01/08/2024 08:00","actual_datetime":"01/08/2024 08:05"},"drop off":{"location_id":102,"location_name":"Bercy Arena","intended_datetime":"01/08/2024 08:30","actual_datetime":"01/08/2024 08:30"}}]}, 
    {"_id":2002,"name":"Marie Dupont","licence_num":"34082A789012","no_of_trips":3,"suspended":"N","trips_info":[{"trip_id":1,"veh_vin":"5J6RE4H48BL023237","pick-up":{"location_id":103,"location_name":"Champ de Mars Arena","intended_datetime":"02/08/2024 09:00","actual_datetime":"02/08/2024 09:05"},"drop off":{"location_id":104,"location_name":"Eiffel Tower Stadium","intended_datetime":"02/08/2024 09:30","actual_datetime":"02/08/2024 09:30"}},{"trip_id":12,"veh_vin":"5XYKU4A12BG001739","pick-up":{"location_id":119,"location_name":"Arc de Triomphe","intended_datetime":"01/08/2024 10:00","actual_datetime":"01/08/2024 10:05"},"drop off":{"location_id":120,"location_name":"The Basilica of the Sacred Heart of Paris","intended_datetime":"01/08/2024 10:35","actual_datetime":"01/08/2024 10:35"}},{"trip_id":9,"veh_vin":"5XYKU4A12BG001739","pick-up":{"location_id":115,"location_name":"Eiffel Tower","intended_datetime":"07/08/2024 09:15","actual_datetime":"07/08/2024 09:20"},"drop off":{"location_id":116,"location_name":"Louvre Museum","intended_datetime":"07/08/2024 10:00","actual_datetime":"07/08/2024 10:00"}}]},                                                                                                                                                                                                                                                                                                                                        
    {"_id":2003,"name":"Louis Dubois","licence_num":"45112B654321","no_of_trips":3,"suspended":"N","trips_info":[{"trip_id":4,"veh_vin":"JH4DB1540PS000784","pick-up":{"location_id":105,"location_name":"South Paris Arena","intended_datetime":"03/08/2024 10:00","actual_datetime":"03/08/2024 10:05"},"drop off":{"location_id":106,"location_name":"La Beaujoire Stadium","intended_datetime":"03/08/2024 10:45","actual_datetime":"03/08/2024 10:45"}},{"trip_id":10,"veh_vin":"JH4DA3450KS009535","pick-up":{"location_id":117,"location_name":"Tuileries Garden","intended_datetime":"08/08/2024 14:00","actual_datetime":"08/08/2024 14:05"},"drop off":{"location_id":118,"location_name":"Sainte-Chapelle","intended_datetime":"08/08/2024 14:40","actual_datetime":"08/08/2024 14:40"}},{"trip_id":7,"veh_vin":"JH4KA3160LC017215","pick-up":{"location_id":111,"location_name":"Porte de La Chapelle Arena","intended_datetime":"06/08/2024 09:30","actual_datetime":"06/08/2024 09:35"},"drop off":{"location_id":112,"location_name":"Roland Garros Stadium","intended_datetime":"06/08/2024 10:15","actual_datetime":"06/08/2024 10:15"}}]},                                                                                                                                                                                                                                                                                                                                             
    {"_id":2004,"name":"Antoine Lefevre","licence_num":"670495098765","no_of_trips":1,"suspended":"N","trips_info":[{"trip_id":5,"veh_vin":"1G4GJ11Y9HP422546","pick-up":{"location_id":107,"location_name":"North Paris Arena","intended_datetime":"04/08/2024 11:00","actual_datetime":"04/08/2024 11:05"},"drop off":{"location_id":108,"location_name":"Parc des Princes","intended_datetime":"04/08/2024 11:30","actual_datetime":"04/08/2024 11:30"}}]},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    {"_id":2005,"name":"Sophie Bernard","licence_num":"89122a345678","no_of_trips":3,"suspended":"N","trips_info":[{"trip_id":8,"veh_vin":"JH4KA8162MC010197","pick-up":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"07/08/2024 07:45","actual_datetime":"07/08/2024 07:50"},"drop off":{"location_id":114,"location_name":"Champions Park","intended_datetime":"07/08/2024 08:25","actual_datetime":"07/08/2024 08:25"}},{"trip_id":20,"veh_vin":"5J6RE4H48BL023237","pick-up":{"location_id":115,"location_name":"Eiffel Tower","intended_datetime":"02/08/2024 10:00","actual_datetime":"02/08/2024 10:05"},"drop off":{"location_id":116,"location_name":"Louvre Museum","intended_datetime":"02/08/2024 10:40","actual_datetime":"02/08/2024 10:40"}},{"trip_id":17,"veh_vin":"JH4DB1540PS000784","pick-up":{"location_id":111,"location_name":"Porte de La Chapelle Arena","intended_datetime":"28/07/2024 15:00","actual_datetime":"28/07/2024 15:05"},"drop off":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"28/07/2024 15:35","actual_datetime":"28/07/2024 15:35"}}]},                                                                                                                                                                                                                                                                                                                                
    {"_id":2010,"name":"Naoki Fujimoto","licence_num":"110685765432","no_of_trips":1,"suspended":"N","trips_info":[{"trip_id":18,"veh_vin":"JH4DB1540PS000784","pick-up":{"location_id":111,"location_name":"Porte de La Chapelle Arena","intended_datetime":"04/08/2024 08:30","actual_datetime":"04/08/2024 08:35"},"drop off":{"location_id":112,"location_name":"Roland Garros Stadium","intended_datetime":"04/08/2024 09:15","actual_datetime":"04/08/2024 09:15"}}]},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    {"_id":2011,"name":"Mathieu Girard","licence_num":"22102A456789","no_of_trips":2,"suspended":"N","trips_info":[{"trip_id":11,"veh_vin":"5J6RE4H48BL023237","pick-up":{"location_id":119,"location_name":"Arc de Triomphe","intended_datetime":"21/07/2024 09:00","actual_datetime":"21/07/2024 09:05"},"drop off":{"location_id":117,"location_name":"Tuileries Garden","intended_datetime":"21/07/2024 09:30","actual_datetime":"21/07/2024 09:30"}},{"trip_id":16,"veh_vin":"5J6RE4H48BL023237","pick-up":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"07/08/2024 17:00","actual_datetime":"07/08/2024 17:05"},"drop off":{"location_id":106,"location_name":"La Beaujoire Stadium","intended_datetime":"07/08/2024 17:50","actual_datetime":"07/08/2024 17:50"}}]},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    {"_id":2012,"name":"Mansour","licence_num":"33022B678901","no_of_trips":1,"suspended":"N","trips_info":[{"trip_id":13,"veh_vin":"1HGCE1899RA009926","pick-up":{"location_id":110,"location_name":"Pierre Mauroy Stadium","intended_datetime":"21/07/2024 09:00","actual_datetime":"21/07/2024 09:05"},"drop off":{"location_id":111,"location_name":"Porte de La Chapelle Arena","intended_datetime":"21/07/2024 09:30","actual_datetime":"21/07/2024 09:30"}}]},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    {"_id":2013,"name":"Lei Xiong","licence_num":"441270890123","no_of_trips":1,"suspended":"N","trips_info":[{"trip_id":14,"veh_vin":"1JCCM85E5BT001312","pick-up":{"location_id":117,"location_name":"Tuileries Garden","intended_datetime":"04/08/2024 10:00","actual_datetime":"04/08/2024 10:05"},"drop off":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"04/08/2024 11:00","actual_datetime":"04/08/2024 11:20"}}]},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    {"_id":2014,"name":"Claire Robert","licence_num":"55052a543210","no_of_trips":1,"suspended":"N","trips_info":[{"trip_id":100,"veh_vin":"1C4SDHCT9FC614231","pick-up":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"30/07/2024 12:30","actual_datetime":"30/07/2024 12:30"},"drop off":{"location_id":111,"location_name":"Porte de La Chapelle Arena","intended_datetime":"30/07/2024 14:00","actual_datetime":"30/07/2024 14:15"}}]},                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    {"_id":2015,"name":"Nathalie Renaud","licence_num":"660725432109","no_of_trips":1,"suspended":"N","trips_info":[{"trip_id":15,"veh_vin":"JH4DA3450KS009535","pick-up":{"location_id":109,"location_name":"Paris La Defense Arena","intended_datetime":"06/08/2024 20:30","actual_datetime":"06/08/2024 20:35"},"drop off":{"location_id":113,"location_name":"Olympic and Paralympic village","intended_datetime":"06/08/2024 23:10","actual_datetime":"06/08/2024 23:10"}}]}]);
// List all documents you added


// (c)
// PLEASE PLACE REQUIRED MONGODB COMMAND/S FOR THIS PART HERE
// ENSURE that your query is formatted and has a semicolon
// (;) at the end of this answer

db.driver.find(
    {"trips_info.drop off.location_name":{"$in":["Champions Park", "Porte de La Chapelle Arena"]}},
    {"name":1, "licence_num":1}
);



// (d)
// PLEASE PLACE REQUIRED MONGODB COMMAND/S FOR THIS PART HERE
// ENSURE that your query is formatted and has a semicolon
// (;) at the end of this answer

// Show document before the new trip is added and the driver is suspended

db.driver.find(
    {"_id":2004}
);


// Add new trip and set the driver to suspended

db.driver.updateOne(
    {"_id": 2004},
    {"$push":
        {
            "trips_info":
            {
                "trip_id": 22,
                "veh_vin": "1G4GJ11Y9HP422546",
                "pick-up":
                {
                    "location_id": 117,
                    "location_name": "Tuileries Garden",
                    "intended_datetime": "05/08/2024 17:00",
                    "actual_datetime": "05/08/2024 16:30"
                },
                "drop off":
                {
                    "location_id": 118,
                    "location_name": "Sainte-Chapelle",
                    "intended_datetime": "05/08/2024 19:00",
                    "actual_datetime": "05/08/2024 18:50"
                }
            }
        },
        "$set":
        {
            "suspended":"Y"
        }
    }
);


// Illustrate/confirm changes made

db.driver.find(
    {"trips_info.trip_id":22}
);
