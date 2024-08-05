#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include "fila_inteligente.h"

double current_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec / 1e9;
}

void add_task(Task *tasks, int *task_count, void (*func)(void), double interval) {
    tasks[*task_count].func = func;
    tasks[*task_count].interval = interval;
    tasks[*task_count].next_run = current_time() + interval;
    (*task_count)++;
}

void run_tasks(Task *tasks, int task_count) {
    while (1) {
        double now = current_time();
        for (int i = 0; i < task_count; i++) {
            if (tasks[i].next_run <= now) {
                tasks[i].func();
                tasks[i].next_run = now + tasks[i].interval;
            }
        }
        usleep(1000); //Espera 1 milissegundo
    }
}

