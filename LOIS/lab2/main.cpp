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
#include "inference.h"
#include <fstream>
#include <iostream>
#ifdef _WIN32
#include <windows.h>
#include <exception>
#endif
using namespace std;

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
    try {
        string file = "../base.txt";
        getline(cin, file);

        Task t;
        ParserError err;
        if (!parse(file, t, err)) {
            cout << "Ошибка" << (err.line ? " в строке " + to_string(err.line) : "") << ": " << err.message << endl;
            return 1;
        }

        string text = solve(t);
        cout << "\n" << text;

        size_t dot = file.find_last_of('.'), slash = file.find_last_of("/\\");
        string rf = (dot != string::npos && (slash == string::npos || dot > slash) ?
            file.substr(0, dot) : file) + ".result";
        ofstream res(rf);
        if (res << text) {
            cout << "\nПротокол сохранён в файл " << rf << endl;
        } else {
            cout << "\nНе удалось сохранить протокол в файл " << rf << endl;
        }
        return 0;
    } catch (const exception& e) {
        // Непредвиденные ошибки стандартной библиотеки (нехватка памяти и т.п.)
        cout << "Непредвиденная ошибка: " << e.what() << endl;
        return 2;
    }
}