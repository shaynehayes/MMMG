% Design Assistant Problem Encoding
% = Generate =
% First read in pre-authored data
in(T,P,R) :- pre(T,P,R).
% Then generate moves to fit around that data
{ in(T,P,R) : room(R) } = 1 :- discovertime(D), person(P), T=1..D.

% = Define =
% Rooms are adjacent to themselves
adj(R,R) :- room(R).
% Rooms have vision on themselves
vision(R,R) :- room(R).
% Separate machine-authored data from hand-authored data
gen(T,P,R) :- in(T,P,R), not pre(T,P,R).
% Separate the innocents from the murderer and victim
innocent(P) :- person(P), not murderer(P), not victim(P).
% If P1 and P2 are both in room R, then they are together
together(T,P1,P2) :- P1 != P2, in(T,P1,R), in(T,P2,R).
% If P1 is in R1 at the same time that P2 is in R2, and R1 has vision on R2, then P1 has seen P2 (the victim doesn't count)
seen(T,P1,P2) :- P1 != P2, vision(R1,R2), in(T,P1,R1), in(T,P2,R2), not victim(P1).
seen(T,P) :- seen(T,_,P).
% A person has stayed in a room R for duration B-A if they are in R for all timesteps in [A,B] and they are not in R before or after. 
stayed(B-A,P,R) :- { in(T,P,R): T=A..B } = B-A, not in(A-1,P,R), not in(B+1,P,R), person(P), room(R), discovertime(D), A=1..D-1,B=A+1..D.
% Edge case where a person stays in a room for literally every timestep
stayed(D,P,R) :- { in(T,P,R): T=1..D } = D, person(P), room(R), discovertime(D).

% = Test =
% Characters may only move to adjacent rooms
:- not adj(R1,R2), in(T,P,R1), in(T+1,P,R2), person(P), discovertime(D), T=1..D-1.
% Characters cannot move down paths blocked for them
:- block(P,R1,R2), in(T,P,R1), in(T+1,P,R2), discovertime(D), T=1..D-1.
% Characters may not immediately move back to the room they just came from (in the generated data only)
% Commented out now that room time limits are implemented
% :- R1 == R3, R1 != R2, gen(T,P,R1), gen(T+1,P,R2), gen(T+2,P,R3), person(P), discovertime(D), T=1..D-2.
% Characters may not stay in a room for longer than its max time limit (except for the victim)
:- M < D, stayed(D,P,R), maxtime(R,M), not victim(P).
% Characters may not stay in a room for shorter than its min time limit
:- M > D, stayed(D,P,R), mintime(R,M).
% All innocent characters must be seen at each timestep
:- not seen(T,P), innocent(P), discovertime(D), T=1..D.
% The murderer must be with the victim at the time of the crime
:- not together(M,K,V), murdertime(M), murderer(K), victim(V).
% The murderer must not be with the victim at the time of discovery
:- together(D,K,V), discovertime(D), murderer(K), victim(V).
% The victim may not move after the murder
:- R1 != R2, in(T,V,R1), in(T+1,V,R2), victim(V), murdertime(M), discovertime(D), T=M..D-1.
% The victim must not be seen during or after the murder by any innocent before the time of discovery
:- seen(T,I,V), innocent(I), victim(V), murdertime(M), discovertime(D), T=M-3..D-1.
% The victim must be discovered at the time of discovery
:- not seen(D,P,V), victim(V), discovertime(D), innocent(P).

% = Display =
#show gen/3.