#ifndef FILA_INTELIGENTE_H
#define FILA_INTELIGENTE_H
	typedef struct {
		void (*func)(void);
		double interval;
		double next_run;
	} Task;

	//Função para obter o tempo atual em segundos
	double current_time();

	//Função que adiciona uma nova tarefa à lista
	void add_task(Task *tasks, int *task_count, void (*func)(void), double interval);

	//Função principal que executa as tarefas
	void run_tasks(Task *tasks, int task_count);
#endif

