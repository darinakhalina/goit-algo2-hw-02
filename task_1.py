from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)
    sorted_jobs = sorted(jobs, key=lambda job: job.priority)

    job_sequence = []
    overall_duration = 0
    group_volume, group_item_count, group_duration = 0, 0, 0
    group_jobs = []
    job_index = 0

    while job_index < len(sorted_jobs):
        job = sorted_jobs[job_index]
        if (
            group_volume + job.volume <= printer.max_volume
            and group_item_count + 1 <= printer.max_items
        ):
            group_jobs.append(job)
            group_volume += job.volume
            group_item_count += 1
            group_duration = max(group_duration, job.print_time)
            job_index += 1
        else:
            if group_jobs:
                job_sequence.extend(j.id for j in group_jobs)
                overall_duration += group_duration
            group_volume, group_item_count, group_duration = 0, 0, 0
            group_jobs = []
            if job.volume <= printer.max_volume and 1 <= printer.max_items:
                group_jobs.append(job)
                group_volume = job.volume
                group_item_count = 1
                group_duration = job.print_time
                job_index += 1
            else:
                job_sequence.append(job.id)
                overall_duration += job.print_time
                job_index += 1

    if group_jobs:
        job_sequence.extend(j.id for j in group_jobs)
        overall_duration += group_duration

    return {
        "print_order": job_sequence,
        "total_time": overall_duration,
    }


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
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2,
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("Тест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("Тест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
