#include <bits/stdc++.h>

using namespace std;

struct student
{
    char surname[100];
    int groupNum;
    int grades[3];
    double gpa;
};


student addStudent(){
    int grade, sumOfGrades = 0, groupNum;
    char surname[100];
    student temp;
    cout<<"Enter surname:";
    cin >> surname;
    int letter = 0;
    while(surname[letter] != '\0'){
        temp.surname[letter] = surname[letter];
        letter++;
    }
    temp.surname[letter] = '\0';
    cout<<"Enter number of the group:";
    cin >> groupNum;
    temp.groupNum = groupNum;
    cout<<"Enter grades Math/Physics/Informatics"<<endl;
    for(int j = 0; j < 3; j++){
        cout <<"Enter grade "<< j + 1 << ":";
        cin >> grade;
        temp.grades[j] = grade;
        sumOfGrades += grade;
    }
    temp.gpa = sumOfGrades / 3.0;
    return temp;
}


int main(){
    int n, grade, sumOfGrades = 0, groupNum;
    char surname[100];
    cout<<"Enter number of students:";
    cin>>n;
    student *students = new student[n];
    for(int i = 0; i < n; i++){
        students[i] = addStudent();
    }

    while (true){
        cout << "Choose an option: 1 - add new student, 2 - delete student, 3 - change student's information, 4 - individual task, ";
        cout << "5 - sort students, 6 - read from file, 7 - end the program:";
        int option;
        cin >> option;
        switch(option){

            case 1: {
                student *buffer = new student[n + 1];
                for(int i = 0; i < n; i++){
                    buffer[i] = students[i];
                }
                buffer[n] = addStudent();
                n++;
                delete [] students;

                students = buffer;
                cout << "Student successfully added";
                break;
            }

            case 2: {
                int studentNum;
                cout << "Enter number of the student who will be deleted:";
                cin >> studentNum;
                for(int i = studentNum - 1; i < n - 1; i++){
                    students[i] = students[i+1];
                }
                n--;
                cout << "Successfully deleted";
                break;
            }

            case 3: {
                int studentNum;
                cout << "Enter number of the student who's information will be changed:";
                cin >> studentNum;
                int operationNum;
                cout<< "Enter 1 - to change surname, 2 - to change group number, 3 - to change grades:";
                cin >> operationNum;
                switch(operationNum){
                    case 1: {
                        char surname[100];
                        cout<<"Enter surname: ";
                        cin >> surname;
                        int letter = 0;
                        while(surname[letter] != '\0'){
                            students[studentNum - 1].surname[letter] = surname[letter];
                            letter++;
                        }
                        students[studentNum - 1].surname[letter] = '\0';
                        break;
                    }
                    case 2: {
                        int groupNum;
                        cout<<"Enter number of the group:";
                        cin >> groupNum;
                        students[studentNum - 1].groupNum = groupNum;
                        break;
                    }
                    case 3: {
                        int gradeNum, grade;
                        cout<<"Enter numbers to change grades. 1 - Math, 2 - Physics, 3 - Informatics"<<endl;
                        cout<<"Enter number:";
                        cin >> gradeNum;
                        if(gradeNum < 1 || gradeNum > 3){
                            cout << "Error";
                            break;
                        }
                        cout<<"Enter new grade: ";
                        cin >> grade;

                        student temp = students[studentNum - 1];
                        int sumOfGrades = temp.grades[0] + temp.grades[1] + temp.grades[2];
                        sumOfGrades += grade - temp.grades[gradeNum - 1];
                        students[studentNum - 1].grades[gradeNum - 1] = grade;
                        students[studentNum - 1].gpa = sumOfGrades / 3.0;

                    }
                }
                break;

            }

            case 4: {
                double totalGpa = 0;
                int targetGroup;

                // Вычисляем общий средний балл
                for(int i = 0; i < n; i++) {
                    totalGpa += students[i].gpa;
                }
                double avgGpa = totalGpa / n;

                cout << "Enter group number:";
                cin >> targetGroup;

                cout << "Average GPA across all students:" << avgGpa << endl;
                cout << "Students from group " << targetGroup << " with GPA above average:" << endl;

                ofstream outFile;
                outFile.open("storage.txt");
                if(outFile.is_open()){
                    for(int i = 0; i < n; i++){
                        if(students[i].groupNum == targetGroup && students[i].gpa > avgGpa) {
                            student temp = students[i];
                            cout << temp.surname << " (GPA: " << temp.gpa << ")" << endl;

                            outFile << temp.surname << endl;
                            outFile << temp.groupNum << endl;
                            outFile << temp.grades[0] << endl;
                            outFile << temp.grades[1] << endl;
                            outFile << temp.grades[2] << endl;
                            outFile << temp.gpa;
                            outFile << endl << endl;
                        }
                    }
                    outFile.close();
                    cout << "Successfully saved to file";
                }
                else{
                    cout<<"Problems with writing into the file";
                }
                break;
            }

            case 5: {
                cout << "Enter a number to choose way of sorting. ";
                cout << "1 - by surname, 2 - by group number, 3 - by GPA:";
                int sortType;
                cin >> sortType;
                cout << "Enter 1 for ascending sorting, 2 - for descending:";
                int sortOrder;
                cin >> sortOrder;

                if (sortOrder == 1) {
                    switch (sortType) {
                        case 1: { // Sort by surname
                            for (int i = 0; i < n - 1; i++) {
                                for (int j = i + 1; j < n; j++) {
                                    int k = 0;
                                    while (students[i].surname[k] != '\0' && students[j].surname[k] != '\0') {
                                        if (students[i].surname[k] > students[j].surname[k]) {
                                            swap(students[i], students[j]);
                                            break;
                                        }
                                        else if (students[i].surname[k] < students[j].surname[k]) {
                                            break;
                                        }
                                        else k++;
                                    }
                                }
                            }
                            break;
                        }

                        case 2: { // Sort by group number
                            for (int i = 0; i < n - 1; i++) {
                                for (int j = i + 1; j < n; j++) {
                                    if (students[i].groupNum > students[j].groupNum) {
                                        swap(students[i], students[j]);
                                    }
                                }
                            }
                            break;
                        }

                        case 3: { // Sort by GPA
                            for (int i = 0; i < n - 1; i++) {
                                for (int j = i + 1; j < n; j++) {
                                    if (students[i].gpa > students[j].gpa) {
                                        swap(students[i], students[j]);
                                    }
                                }
                            }
                            break;
                        }
                    }
                } else if (sortOrder == 2) {
                    switch (sortType) {
                        case 1: { // Sort by surname (descending)
                            for (int i = 0; i < n - 1; i++) {
                                for (int j = i + 1; j < n; j++) {
                                    int k = 0;
                                    while (students[i].surname[k] != '\0' && students[j].surname[k] != '\0') {
                                        if (students[i].surname[k] < students[j].surname[k]) {
                                            swap(students[i], students[j]);
                                            break;
                                        }
                                        else if (students[i].surname[k] > students[j].surname[k]) {
                                            break;
                                        }
                                        else k++;
                                    }
                                }
                            }
                            break;
                        }

                        case 2: { // Sort by group number (descending)
                            for (int i = 0; i < n - 1; i++) {
                                for (int j = i + 1; j < n; j++) {
                                    if (students[i].groupNum < students[j].groupNum) {
                                        swap(students[i], students[j]);
                                    }
                                }
                            }
                            break;
                        }

                        case 3: { // Sort by GPA (descending)
                            for (int i = 0; i < n - 1; i++) {
                                for (int j = i + 1; j < n; j++) {
                                    if (students[i].gpa < students[j].gpa) {
                                        swap(students[i], students[j]);
                                    }
                                }
                            }
                            break;
                        }
                    }
                }

                // Print sorted students
                cout << "Sorted students:" << endl;
                for (int i = 0; i < n; i++) {
                    cout << "Surname: " << students[i].surname
                         << ", Group Number: " << students[i].groupNum
                         << ", Grades: [" << students[i].grades[0] << ", "
                         << students[i].grades[1] << ", " << students[i].grades[2]
                         << "], GPA: " << students[i].gpa << endl;
                }

                cout << "Successfully sorted" << endl;
                break;
            }


            case 6: {
                ifstream fromFile;
                fromFile.open("storage.txt");
                if(fromFile.is_open()){
                    char line[100];
                    int k = 0;
                    int studentsAmount = 0;
                    while(fromFile.getline(line, 100)){
                        if(k == 6){
                            studentsAmount++;
                            k = 0;
                        }
                        k++;
                    }
                    int studentNum = 0;
                    n = studentsAmount;
                    student *buffer = new student[n];

                    fromFile.clear();
                    fromFile.seekg(0, ios::beg);
                    while(studentNum < n){
                        fromFile.getline(buffer[studentNum].surname, 100);
                        fromFile.getline(line, 100);
                        buffer[studentNum].groupNum = atoi(line);
                        fromFile.getline(line, 100);
                        buffer[studentNum].grades[0] = atoi(line);
                        fromFile.getline(line, 100);
                        buffer[studentNum].grades[1] = atoi(line);
                        fromFile.getline(line, 100);
                        buffer[studentNum].grades[2] = atoi(line);
                        fromFile.getline(line, 100);
                        buffer[studentNum].gpa = atof(line);
                        fromFile.getline(line, 100);
                        studentNum++;
                    }
                    fromFile.close();
                    delete [] students;
                    students = buffer;
                    cout << "Information about students has been updated";

                }
                else cout << "Problems with reading from file";
                break;
            }

            case 7: {
                delete [] students;
                return 0;
            }

            default: {
                cout << "Enter only numbers from 1 to 7";
            }
        }
        cout << endl;
    }
    return 0;
}