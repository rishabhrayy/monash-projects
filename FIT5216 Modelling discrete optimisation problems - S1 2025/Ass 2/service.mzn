%%%% Service and Maintenance scheduling
int: endtime;                   % latest time to be scheduled
set of int: TIME = 0..endtime;
enum SERVICE;                   % services to be scheduled
array[SERVICE] of TIME: start;  % start time of service
array[SERVICE] of TIME: end;    % end time of service
enum STYPE;
array[SERVICE] of STYPE: stype; % type of each service

enum TRUCK;                      % truck 
TRUCK: dtruck;                   % dummy truck
enum TTYPE = { SML, MED, LRG, DUMMY };  % truck type
array[TRUCK] of TTYPE: ttype;    % type of each truck
array[TRUCK] of int: prework;    % units of work since last major maintenance
constraint assert(forall(t in TRUCK)(ttype[t] = DUMMY <-> t = dtruck),"dummy type only for dtruck\n");
array[TTYPE] of int: maxsty;     % max service types for each truck type

enum MAINTYPE = { NO, SH, LG, MJ }; % NO means no maintenance
array[MAINTYPE] of int: maintdur; % duration of maintenance
array[MAINTYPE] of int: maxsep;   % max elapsed time since last maint of this type or higher
constraint assert(maintdur[NO] = 0 /\ maxsep[NO] = 0, "rules for empty maintenance\n");

int: minwork;                   % minimal percentage of time each truck that works is working
int: minservice;                % minimal percentage of services performed

int: majorwork;                 % amount of work allowed before major maintenance required


array[SERVICE] of var TRUCK: truck; % which truck takes each service: dtruck if none

int: maxmaint;
set of int: MAINT = 1..maxmaint;
array[TRUCK,MAINT] of var MAINTYPE: mt; % maintenance for each truck NO means not used.
array[TRUCK,MAINT] of var TIME: ms;     % maintenance start time for each truck

include "globals.mzn";


% --- Stage A: Assigning Services ---

% Added this constraint so that if two services are assigned to the same truck (not dtruck), they must not overlap
constraint forall(s1, s2 in SERVICE where s1 < s2)(
  truck[s1] != dtruck /\ truck[s2] != dtruck /\ truck[s1] = truck[s2] ->
    (end[s1] <= start[s2] \/ end[s2] <= start[s1])
);

% --- Stage B: Truck Usage, Service Guarantee ---

% Calculates the total work done by each truck
array[TRUCK] of var int: work_done;  

% here I compute total working time per truck by summing durations of services it performs
constraint forall(t in TRUCK)(
  work_done[t] = sum(s in SERVICE)(if truck[s] = t then end[s] - start[s] else 0 endif)
);

% this constraint ensure that any truck that is doing work must meet the minimum work percentage of the total available time (endtime) working.
constraint forall(t in TRUCK where t != dtruck)(
  work_done[t] > 0 -> 100 * work_done[t] >= minwork * endtime
);
% this constraint ensure at least the required percentage of services are performed (ignoring the dtruck)
var int: serve_count = sum(s in SERVICE)(bool2int(truck[s] != dtruck));
constraint 100 * serve_count >= minservice * card(SERVICE);

% --- Stage C: Work Types ---

% This constraint checks for each truck and each service type whether the truck performs at least one service of that type using a service does variable here to check for the service type
array[TRUCK, STYPE] of var bool: serve_does;
constraint forall(t in TRUCK, st in STYPE)(
  serve_does[t, st] = exists(s in SERVICE)(truck[s] = t /\ stype[s] = st)
);

% As stated by the question each truck (except dtruck) may only handle a limited number of distinct service types
constraint forall(t in TRUCK where t != dtruck)(
  sum(st in STYPE)(bool2int(serve_does[t, st])) <= maxsty[ttype[t]]
);

% --- Stage D : Maintenance ---

% This constraint ensures that unused trucks (no services) should have only NO maintenance scheduled
constraint forall(t in TRUCK) (
    (sum(s in SERVICE)(bool2int(truck[s] = t)) = 0 
    -> forall(m in MAINT)(mt[t, m] = NO)
));

% To put all NO maintenance entries must be at the end of the sequence we have checked for the first NO and then put all NO after that
constraint forall(t in TRUCK, i in 1..maxmaint-1)(
    mt[t, i] = NO -> mt[t, i+1] = NO
);

% Assigning a maintenance ordering to ensure non-NO maintenances are scheduled sequentially without any overlap
constraint forall(t in TRUCK, i in 1..maxmaint-1)(
    (mt[t, i] != NO /\ mt[t, i+1] != NO) 
    -> ms[t, i] + maintdur[mt[t, i]] <= ms[t, i+1]
);


% ---  Stage E : Objective ---

% Here I am counting that for each time unit how many maintenances are happening for a time unit t0
array[TIME] of var int: maint_active;
constraint  
  forall(t0 in TIME) (
    maint_active[t0] = sum([ bool2int(
      t != dtruck /\
      exists(m in MAINT)(
        mt[t, m] != NO /\
        ms[t, m] <= t0 /\
        t0 < ms[t, m] + maintdur[mt[t, m]]
      )
    ) | t in TRUCK ])
  );
  
% I have summed the square of the number of simultaneous maintenences over all time units to penalize overlaps more heavily and spread out the maintanences.
var int: total_maintenance = sum(t0 in TIME)(maint_active[t0] * maint_active[t0]);

% Here I total the duration of all performed services (assigned to non-dummy trucks).
var int: total_service = sum(s in SERVICE)(if truck[s] != dtruck then end[s] - start[s] else 0 endif);

% For calculating the objective I am using a combination to minimize maintenance overlap by heavily penalizing it (multiplying it by 1000) and maximize service delivery
var int: objective = total_maintenance * 1000 - total_service;

solve minimize objective;

% ---  Stage F : Major Maintenance ---

% For stage F I am putting a constrait that for each truck work between major maintenances does not exceed the given majorwork limit
constraint forall(t in TRUCK where t != dtruck)(
  let {
    array[MAINT] of var int: work_since_MJ = [
      (if m = 1 then
         prework[t] + sum(s in SERVICE)(if truck[s] = t /\ end[s] <= ms[t, m] then end[s] - start[s] else 0 endif)
       else
         sum(s in SERVICE)(if truck[s] = t /\ end[s] > ms[t, m-1] + maintdur[mt[t, m-1]] /\ end[s] <= ms[t, m] then end[s] - start[s] else 0 endif)
       endif)
      | m in MAINT
    ]
  } in
    forall(m in MAINT where mt[t, m] = MJ)(
      work_since_MJ[m] <= majorwork
    )
);