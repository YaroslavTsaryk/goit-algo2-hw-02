from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

    def __init__(self, p_job: Dict):
        self.id = p_job["id"]
        self.volume = p_job["volume"]
        self.priority = p_job["priority"]
        self.print_time = p_job["print_time"]


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

    def __init__(self, constraint: Dict):
        self.max_volume = constraint["max_volume"]
        self.max_items = constraint["max_items"]


@dataclass
class Epoch:
    volume: float
    max_items: int
    time: int
    items: List

    def __init__(self, pc: PrinterConstraints):
        self.volume = pc.max_volume
        self.max_items = pc.max_items
        self.time = 0
        self.items = list()


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Тут повинен бути ваш код

    # for job in print_jobs:
    #     print(job)

    pc = PrinterConstraints(constraints)

    job_list = [PrintJob(job) for job in print_jobs]

    exec_jobs = []

    epoch = Epoch(pc)
    print_order = []

    for priority in range(1, 4):
        for job in job_list:
            # print(f"TEST JOB: {job}")
            if job.priority == priority:
                # print(f"TEST JOB: {job}")
                if epoch.volume > job.volume and epoch.max_items > 0:
                    epoch.items.append(job)
                    # print_jobs.remove(job)
                    epoch.volume -= job.volume
                    epoch.max_items -= 1
                    epoch.time = max(epoch.time, job.print_time)
                    print_order.append(job.id)
                else:
                    exec_jobs.append(epoch)
                    epoch = Epoch(pc)
                    epoch.items.append(job)
                    # print_jobs.remove(job)
                    epoch.volume -= job.volume
                    epoch.max_items -= 1
                    epoch.time = max(epoch.time, job.print_time)
                    print_order.append(job.id)

    exec_jobs.append(epoch)

    print(exec_jobs)

    exec_time = 0
    for ep in exec_jobs:
        exec_time += ep.time

    return {"print_order": print_order, "total_time": exec_time}


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\n\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\n\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
