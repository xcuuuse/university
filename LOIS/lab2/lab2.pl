:- encoding(utf8).
:- set_prolog_flag(encoding, utf8).

%  Лабораторная работа № 2 по дисциплине "Логические основы интеллектуальных систем"
%  Выполнена студентом БГУИР Евик Алексей Николаевич
%  Условие: Два берега реки. На одном из берегов есть три семейные пары, требуется с помощью лодки, вмещающий
% не более двух человек, переправить всех на другой берег. Нельзя оставлять чужую жену и чужого мужа
% вместе без супругов.
% Использованные материалы:
%	Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
%    В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с.
%	 Основные элементы языка PROLOG - URL: https://alatyr.chuvsu.ru/download/RLP.pdf (дата доступа 11.05.2026)


% people(+N, -People) - множество всех персон для N пар.
people(N, People) :-
    numlist(1, N, Is),
    findall(P, ( member(I, Is), member(P, [h(I), w(I)]) ), Raw),
    sort(Raw, People).

% Начальное состояние по умолчанию: все на левом берегу, лодка слева.
start_state(N, st(People, [], left)) :- people(N, People).

% Целевое состояние по умолчанию: все на правом берегу, лодка справа.
goal_state(N, st([], People, right)) :- people(N, People).

%  Берег безопасен, если на нем нет ни одного мужа,
%  ЛИБО каждая присутствующая на берегу жена находится рядом со своим мужем.

safe_bank(Bank) :-
    ( \+ member(h(_), Bank)                               -> true
    ;  forall( member(w(I), Bank), member(h(I), Bank) )).

safe(st(L, R, _)) :-
    safe_bank(L),
    safe_bank(R).

%  За один ход в лодку садятся 1 или 2 человека с того берега, 
%  где находится лодка; лодка переплывает на другой берег.
move(st(L, R, left), st(L1, R1, right)) :-
    choose_passengers(L, Pass, L1),
    append(Pass, R, R0), sort(R0, R1).
move(st(L, R, right), st(L1, R1, left)) :-
    choose_passengers(R, Pass, R1),
    append(Pass, L, L0), sort(L0, L1).

% Выбор 1 или 2 пассажиров из списка людей на берегу.
choose_passengers(Bank, [A], Rest) :-
    select(A, Bank, Rest).
choose_passengers(Bank, [A, B], Rest) :-
    select(A, Bank, Bank1),
    select(B, Bank1, Rest),
    A @< B.                 

solve(Start, Goal, Path) :-
    bfs([[Start]], Goal, [Start], RevPath),
    reverse(RevPath, Path).

bfs([[Goal | Tail] | _], Goal, _, [Goal | Tail]) :- !.   
bfs([Path | Rest], Goal, Visited, Solution) :-
    Path = [State | _],
    findall(Next,
            ( move(State, Next), safe(Next), \+ member(Next, Visited) ),
            Nexts),
    extend_paths(Nexts, Path, NewPaths),
    append(Visited, Nexts, Visited1),
    append(Rest, NewPaths, Queue),
    bfs(Queue, Goal, Visited1, Solution).

extend_paths([], _, []).
extend_paths([N | Ns], Path, [[N | Path] | More]) :-
    extend_paths(Ns, Path, More).

% вывод шагов решения
print_solution(Path) :-
    length(Path, Len),
    Steps is Len - 1,
    format("~nНайдено решение за ~w переправ:~n~n", [Steps]),
    print_states(Path, 0).

print_states([S], N) :- !,
    format("[~w] ", [N]), print_banks(S),
    write('цель достигнута'), nl.
print_states([S1, S2 | T], N) :-
    format("[~w] ", [N]), print_banks(S1),
    describe_move(S1, S2),
    N1 is N + 1,
    print_states([S2 | T], N1).

% Печать содержимого берегов и положения лодки.
print_banks(st(L, R, B)) :-
    persons_str(L, LS),
    persons_str(R, RS),
    ( B == left
    -> format("ЛЕВ [~w] {лодка}  ||  ПРАВ [~w]~n", [LS, RS])
    ;  format("ЛЕВ [~w]  ||  {лодка} ПРАВ [~w]~n", [LS, RS])
    ).

% Описание одного хода: кто плывет и в какую сторону.
describe_move(st(L1, _, B1), st(L2, _, _)) :-
    ( B1 == left
    -> subtract(L1, L2, Pass), Dir = 'ЛЕВ --> ПРАВ'
    ;  subtract(L2, L1, Pass), Dir = 'ПРАВ --> ЛЕВ'
    ),
    persons_str(Pass, PS),
    format("        переправа: ~w  (~w)~n", [PS, Dir]).

persons_str([], '-').
persons_str([P | Ps], Str) :-
    Ps \== [], !,
    person_str(P, S),
    persons_str(Ps, Rest),
    atomic_list_concat([S, ', ', Rest], Str).
persons_str([P], S) :- person_str(P, S).

person_str(h(I), S) :- atomic_list_concat(['муж',  I], S).
person_str(w(I), S) :- atomic_list_concat(['жена', I], S).


solve_couples(N) :-
    start_state(N, Start),
    goal_state(N, Goal),
    ( solve(Start, Goal, Path)
    -> print_solution(Path)
    ;  format("Решения не существует.~n", [])
    ).

% Приведение состояния к каноническому виду (отсортированные берега).
normalize(st(L0, R0, B), st(L, R, B)) :- sort(L0, L), sort(R0, R).

% Демонстрация при ?- main.
main :- solve_couples(3).

:- initialization(main).
