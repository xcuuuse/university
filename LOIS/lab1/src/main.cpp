/*
 * Лабораторная работа №3 по дисциплине "Логические основы интеллектуальных систем"
 * Выполнена студентами группы 421702 БГУИР Говор Георгий Геннадьевич, Евик Алексей Николаевич, Лойко Станислав Павлович
 */
/*
 * Точка входа: читает имя файла базы знаний со стандартного ввода, выполняет прямой нечёткий
 * вывод, между итерациями принимает команды пользователя (Enter — дальше, a — до конца,
 * q — прервать), печатает протокол и выведенные факты на экран и сохраняет протокол в файл.
 * Требования к программе - Третья лабораторная работа по логическим основам интеллектуальных систем -
 *     URL: https://scnedu.sourceforge.net/variety/_/index.html?variety=everface.json&gradient=interscreen.json
 *     (дата обращения: 01.03.2024)
 * Использованные материалы - Логические основы интеллектуальных систем. Практикум: учеб.-метод. пособие /
 *     В. В. Голенков [и др.]. — Минск: БГУИР, 2011. — 70 с. (с. 64: результаты сохраняются в файле)
 * Версия 2.0 (13.10.2026): упрощённая версия программы.
 */
#include "logic.h"

#include <fstream>
#include <iostream>
#include <sstream>

#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#endif

// Удаляет пробелы и кавычки по краям строки (кавычки появляются при перетаскивании файла в консоль).
std::string trim(const std::string& text) {
    const std::size_t first = text.find_first_not_of(" \t\r\n\"'");
    const std::size_t last = text.find_last_not_of(" \t\r\n\"'");
    return first == std::string::npos ? "" : text.substr(first, last - first + 1);
}

// Читает имя файла, выполняет вывод, печатает протокол на экран и сохраняет его в <имя>_result.txt.
int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);  // русский текст в консоли Windows
    SetConsoleCP(CP_UTF8);
#endif
    std::cout << "Введите имя файла базы знаний: ";
    std::string path;
    std::getline(std::cin, path);
    path = trim(path);
    std::ifstream file(path);
    if (!file) {
        std::cerr << "Не удалось открыть файл \"" << path << "\"\n";
        return 1;
    }
    KnowledgeBase kb;
    try {
        kb = parseKnowledgeBase(file);
    } catch (const std::exception& error) {
        std::cerr << "Ошибка в базе знаний: " << error.what() << "\n";
        return 1;
    }

    std::ostringstream log;  // протокол: показывается на экране и сохраняется в файл
    std::size_t shown = 0;   // сколько символов протокола уже напечатано

    // Печатает на экран ещё не показанную часть протокола.
    auto flush = [&] {
        const std::string text = log.str();
        std::cout << text.substr(shown);
        shown = text.size();
    };

    // Спрашивает пользователя после итерации: Enter — дальше, a — до конца без вопросов, q — прервать.
    auto ask = [&](int iteration) {
        flush();
        std::cout << "Итерация " << iteration << " завершена. Enter - дальше, a - до конца, q - прервать: ";
        std::string answer;
        if (!std::getline(std::cin, answer)) return Command::All;  // ввод закончился
        answer = trim(answer);
        return answer == "q" ? Command::Stop : answer == "a" ? Command::All : Command::Next;
    };

    log << "Факты:\n";
    for (const Fact& fact : kb.facts) log << "  " << toString(fact) << "\n";
    log << "Правила:\n";
    for (const Rule& rule : kb.rules) log << "  " << toString(kb, rule) << "\n";

    const Result result = infer(kb, log, ask);

    log << "\nВыведенные факты (" << result.derived.size() << "):\n";
    for (const Fact& fact : result.derived) log << "  " << toString(fact) << "   из " << fact.origin << "\n";
    flush();

    const std::size_t dot = path.find_last_of('.');
    const std::size_t slash = path.find_last_of("/\\");
    const bool hasExtension = dot != std::string::npos && (slash == std::string::npos || dot > slash);
    const std::string reportPath = (hasExtension ? path.substr(0, dot) : path) + "_result.txt";
    std::ofstream report(reportPath);
    report << "Файл базы знаний: " << path << "\n" << log.str();
    std::cout << (report ? "\nПротокол сохранён в " : "\nНе удалось сохранить протокол в ") << reportPath << "\n";
    return 0;
}