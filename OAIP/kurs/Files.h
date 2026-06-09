#ifndef KURS_WORK_FILES_H
#define KURS_WORK_FILES_H
#include "iostream"
#include "Airplanes.h"
#include "fstream"
#include "cstring"

void create_file(const char* filename);
void view_info(const char* filename);
void add_to_file(const char* filename);
void edit_info(const char* filename);
void delete_from_file(const char* filename);
void create_report_file(const char* binary_filename, const char* report_filename);
int read_from_file_to_array(const char* filename, Airplane flights[], int max_size);
#endif
