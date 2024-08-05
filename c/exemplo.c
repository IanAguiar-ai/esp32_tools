#include "fila_inteligente.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

void print1() {
    printf("1");
    fflush(stdout);
}

void print2() {
    printf("2");
    fflush(stdout);
}

void print3() {
    printf("3");
    fflush(stdout);
}

void print4() {
    printf("4");
    fflush(stdout);
}

void print_dash() {
    printf("-");
    fflush(stdout);
}

int main() {
    Task tasks[5];
    int task_count = 0;

    add_task(tasks, &task_count, print1, 1.0);
    add_task(tasks, &task_count, print2, 2.0);
    add_task(tasks, &task_count, print3, 3.0);
    add_task(tasks, &task_count, print4, 4.0);
    add_task(tasks, &task_count, print_dash, 0.2);

    run_tasks(tasks, task_count);

    return 0;
}

