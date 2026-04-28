% rift.mzn
enum RIFT;  % set of vaccines for Rift Valley Fever available
RIFT: dummy; % dummy vaccine
%% the dummy vaccine is always the first 
constraint forall(v in RIFT)
                 (assert(dummy <= v, "vaccine \(v) appears before dummy\n"));

int: n; % number of test groups
set of int: GROUP = 1..n;

int: w; % number of weeks
set of int: WEEK = 1..w;

enum TREAT = { N, V, S, U, B  };
array[TREAT] of int: c;

int: vm;                                                    
array[TREAT] of int: mint;
array[TREAT] of int: maxt;

opt bool: stageD;
opt float: maxfn;
opt float: maxfp;
enum STRAIN = { ALPHA, BETA, GAMMA, OMEGA };

array[GROUP,WEEK] of var TREAT: s;
array[GROUP] of var set of RIFT: vs;

%Stage A: Treatment Plans%
include "globals.mzn";

% A1: Each vaccine given either 0 or 2 times
%Here we are counting how many weeks a group has been vaccinated (s[g,wk] = V)
%I am using bool2int to sum over the number of times a vaccine has been given
%This ensures whether the vaccine is used either 2 or 0 times by a group
constraint forall(g in GROUP) (
    sum(wk in WEEK)(bool2int(s[g,wk] = V)) = 2 * card(vs[g])
);

% A2: Each group must have a different set of vaccines
% using a simple unequality clause to ensure each group have a unique set of vaccine
%I wasn't able to use all_different in this constraint due to it being a set
constraint forall(g1, g2 in GROUP where g1 < g2)(
  vs[g1] != vs[g2]
);

% A3: One group gets no vaccines, one group gets only dummy
%using exists operation to ensure that there is a group with only none vaccine and one with only dummy vaccine
constraint exists(g in GROUP) (vs[g] = {});
constraint exists(g in GROUP) (vs[g] = {dummy});

% A4: Max vm vaccinated per week
%limiting the total number of vaccines using bool2int operator to sum over the number of times a vaccine has been provided
constraint forall(wk in WEEK) (
  sum(g in GROUP)(bool2int(s[g,wk] = V)) <= vm
);

% A5: Minimum and maximum number of each treatment per group
% limiting the number of treatments given to a group within the given minimum treatment and maximum treatment
%here I am using the bool2int operator to sum over the number of treatment and binding it between maxt and mint
constraint forall(g in GROUP, t in TREAT) (
    mint[t] <= sum(wk in WEEK)(bool2int(s[g,wk] = t)) /\
    sum(wk in WEEK)(bool2int(s[g,wk] = t)) <= maxt[t]
);

% A6: Before vaccination must be None
%for ensuring the treatment a week before vaccine should be none I am using the exist operator
constraint forall(g in GROUP, wk in 2..w)(s[g,wk] = V -> s[g,wk-1] = N);


% A7: No blood test unless saliva happened earlier
%similary using the exists operator to ensure that there exists a saliva treatment done before the blood test by iterating over the weeks before blood test
constraint forall(g in GROUP, wk in WEEK where s[g,wk] = B)(
                  exists(p in 1..wk-1)(s[g,p]=S)
                  );

% A8: First and Last treatment must not be None
%simple inequality operator to confirm that last and first treatment as not none
constraint forall(g in GROUP)(s[g,1] != N /\ s[g,w] != N);

%STAGE B:  Minimal Expenditure%

% Cost for each group
% summing up the group costs of all the treatments using the sum operator
array[GROUP] of var int: group_costs = 
  [sum(wk in WEEK)(c[s[g,wk]]) | g in GROUP];

% Total cost of the entire plan
% calcculating the total cost using the already calculated group costs
var int: total_cost = sum(g in GROUP)(group_costs[g]);

% Solve: minimize total cost
solve minimize total_cost;


% STAGE C: Range of Expenditure%

% C1: Each group's cost must be different
%using all different constraint gave problems so using the manual method to have unique costs for all groups
constraint forall(g1, g2 in GROUP where g1 < g2) (
    group_costs[g1] != group_costs[g2]
);


% C2: No plan more than twice expensive than any other
%putting constraint to keep the group costs within 2 times of any other group using and operator and comparison
constraint forall(g1, g2 in GROUP) (
    group_costs[g1] <= 2 * group_costs[g2] /\
    group_costs[g2] <= 2 * group_costs[g1]
);




