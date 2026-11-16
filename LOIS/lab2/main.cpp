/*
* Лабораторная работа №4 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Точка входа. Запрашивает имя файла через стандартный ввод, разбирает его (parser), выполняет обратный
 * нечёткий логический вывод на основе композиции max(xi·yi) (solver), выводит протокол в консоль
 * и сохраняет его в файл с тем же именем и расширением .result.
 * Версия 1.0 от 16.11.2026.
 * Использованные материалы - Практикум по логическим основам интеллектуальных систем
 *     (требования к лабораторной работе №4).
 */

#include "parser.h"
#include "solver.h"
#include <fstream>
#include <iostream>
#ifdef _WIN32
#include <windows.h>
#endif
using namespace std;

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
    cout << "Введите имя файла: ";
    string file;
    getline(cin, file);
    Task t;
    try {
        t = parse(file);
    }
    catch (ParserError& e) {
        cout << "Ошибка" << (e.line ? " в строке " + to_string(e.line) : "") << ": " << e.message << endl;
        return 1;
    }
    string text = solve(t);
    size_t dot = file.find_last_of('.'), slash = file.find_last_of("/\\");
    string rf = (dot != string::npos && (slash == string::npos || dot > slash)?
        file.substr(0, dot) : file) + ".result";
    ofstream(rf) << text;
    cout << "\n" << text << "\nПротокол сохранён в файл " << rf << endl;
    return 0;


}