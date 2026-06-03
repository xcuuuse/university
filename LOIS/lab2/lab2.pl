:- encoding(utf8).
:- set_prolog_flag(encoding, utf8).

%  Лабораторная работа № 2 по дисциплине "Логические основы интеллектуальных систем"
%  Выполнена студентом БГУИР Евик Алексей Николаевич
%  Условие: Два берега реки. На одном из берегов есть три семейные пары, требуется с помощью лодки, вмещающий
% не более двух человек, переправить всех на другой берег. Нельзя оставлять чужую жену и чужого мужа
% вместе без супругов.

people(N, People) :-
    findall(P, (between(1,N,I), member(P,[h(I),w(I)])), Raw),
    sort(Raw, People).

start_state(N, st(People, [], left))  :- people(N, People).
goal_state(N,  st([], People, right)) :- people(N, People).

safe_bank(Bank) :-
    ( \+ member(h(_), Bank) -> true
    ;  forall(member(w(I), Bank), member(h(I), Bank))).

safe(st(L, R, _)) :- safe_bank(L), safe_bank(R).

move(st(L, R, left),  st(L1, R1, right)) :-
    choose_passengers(L, Pass, L1), append(Pass, R, R0), sort(R0, R1).
move(st(L, R, right), st(L1, R1, left)) :-
    choose_passengers(R, Pass, R1), append(Pass, L, L0), sort(L0, L1).

choose_passengers(Bank, [A], Rest)   :- select(A, Bank, Rest).
choose_passengers(Bank, [A,B], Rest) :-
    select(A, Bank, B1), select(B, B1, Rest), A @< B.

solve(Start, Goal, Path) :-
    bfs([[Start]], Goal, [Start], RevPath),
    reverse(RevPath, Path).

bfs([[Goal|T]|_], Goal, _, [Goal|T]) :- !.
bfs([Path|Rest], Goal, Visited, Sol) :-
    Path = [State|_],
    findall(Next, (move(State,Next), safe(Next), \+member(Next,Visited)), Nexts),
    extend_paths(Nexts, Path, New),
    append(Visited, Nexts, Vis1),
    append(Rest, New, Queue),
    bfs(Queue, Goal, Vis1, Sol).

extend_paths([], _, []).
extend_paths([N|Ns], P, [[N|P]|More]) :- extend_paths(Ns, P, More).

print_solution(Path) :-
    length(Path, Len), Steps is Len - 1,
    format("~nНайдено решение за ~w переправ:~n~n", [Steps]),
    print_states(Path, 0).

print_states([S], N) :- !,
    format("[~w] ", [N]), print_banks(S),
    write('цель достигнута'), nl.
print_states([S1,S2|T], N) :-
    format("[~w] ", [N]), print_banks(S1),
    describe_move(S1, S2),
    N1 is N+1, print_states([S2|T], N1).

print_banks(st(L, R, B)) :-
    persons_str(L, LS), persons_str(R, RS),
    ( B == left
    -> format("ЛЕВ [~w] {лодка}  ||  ПРАВ [~w]~n", [LS, RS])
    ;  format("ЛЕВ [~w]  ||  {лодка} ПРАВ [~w]~n", [LS, RS])).

describe_move(st(L1,_,B1), st(L2,_,_)) :-
    ( B1 == left
    -> subtract(L1, L2, Pass), Dir = 'ЛЕВ --> ПРАВ'
    ;  subtract(L2, L1, Pass), Dir = 'ПРАВ --> ЛЕВ'),
    persons_str(Pass, PS),
    format("        переправа: ~w  (~w)~n", [PS, Dir]).

persons_str([], '-').
persons_str(Ps, Str) :-
    Ps \= [],
    maplist(person_str, Ps, Ss),
    atomic_list_concat(Ss, ', ', Str).

person_str(h(I), S) :- atomic_list_concat(['муж',  I], S).
person_str(w(I), S) :- atomic_list_concat(['жена', I], S).

solve_couples(N) :-
    start_state(N, Start), goal_state(N, Goal),
    ( solve(Start, Goal, Path)
    -> print_solution(Path)
    ;  write("Решения не существует."), nl).

main :- solve_couples(3).
