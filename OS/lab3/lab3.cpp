#include <iostream>
#include <fstream>
#include <queue>
#include <cmath>
#include <pthread.h>
#include <memory>
#include <chrono>
#include <thread>
#include <ctime>

using namespace std;

class Point{

public:
    double x;
    double y;
    chrono::system_clock::time_point created;

    Point(double _x, double _y)
    : x(_x), y(_y), created(chrono::system_clock::now()) {}

};


queue<shared_ptr<Point>> buffer;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
bool finished = false;

ofstream dataFile("data.txt");
ofstream logFile("log.txt");

void* generator(void*)
{
    using namespace std::chrono_literals;
    for (double x = 0.0; x <= 10; x++)
    {
        auto p = make_shared<Point>(x, x * x);
        
        pthread_mutex_lock(&mutex);
        buffer.push(p);
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);

        this_thread::sleep_for(400ms);

    }

    pthread_mutex_lock(&mutex);
    finished = true;

    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&mutex);

    pthread_exit(nullptr);
}

void* writer(void*) {
    while (true) {
        pthread_mutex_lock(&mutex);
        while (buffer.empty() && !finished)
            pthread_cond_wait(&cond, &mutex);

        if (buffer.empty() && finished) {
            pthread_mutex_unlock(&mutex);
            break;
        }

        auto p = buffer.front();
        buffer.pop();
        pthread_mutex_unlock(&mutex);

        auto write_time = chrono::system_clock::now();

        dataFile << "x=" << p->x << " y=" << p->y << "\n";

        time_t t1 = chrono::system_clock::to_time_t(p->created);
        time_t t2 = chrono::system_clock::to_time_t(write_time);

        pthread_mutex_lock(&mutex);
        logFile << "[LOG] Point (" << p->x << ", " << p->y << ") "
                << "created at " << ctime(&t1)
                << "      written at " << ctime(&t2) << "\n";
        pthread_mutex_unlock(&mutex);
    }

    pthread_exit(nullptr);
}

void* logger(void*) {
    using namespace chrono_literals;
    while (!finished) {
        pthread_mutex_lock(&mutex);
        size_t size = buffer.size();
        pthread_mutex_unlock(&mutex);
        cout << "[Logger] Queue size: " << size << "\n";
        this_thread::sleep_for(0.4s);
    }
    pthread_exit(nullptr);
}

int main() {
    pthread_t t1, t2, t3;

    cout << "Starting threads..." << "\n";

    pthread_create(&t1, nullptr, generator, nullptr);
    pthread_create(&t2, nullptr, writer, nullptr);
    pthread_create(&t3, nullptr, logger, nullptr);

    pthread_join(t1, nullptr);
    pthread_join(t2, nullptr);
    pthread_join(t3, nullptr);

    dataFile.close();
    logFile.close();

    cout << "All threads finished.\n";
    cout << "Check data.txt and log.txt for results.\n";
}
