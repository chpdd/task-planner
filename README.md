# Task Planner Library

Core logic and algorithms for intelligent task scheduling and daily planning.  
This library helps organize and prioritize tasks based on multiple parameters such as importance, interest level, workload, and deadlines.

## 📦 Installation

To use this library in your own projects:

### 1. Using Poetry (Recommended)

Add it as a Git dependency in your `pyproject.toml`:
```bash
poetry add git+https://github.com/chpdd/task-planner.git
```

Or for local development (if the repo is in a neighboring folder):
```bash
poetry add ../task-planner
```

### 2. Using Pip

```bash
pip install git+https://github.com/chpdd/task-planner.git
```

## 🛠 Project Structure

The project uses the standard `src` layout:
```
task-planner/
├── pyproject.toml
├── README.md
└── src/
    └── task_planner/
        ├── __init__.py    # Exports Planner, Task, Day, etc.
        ├── planner.py     # Main allocation logic
        ├── calendar.py    # Calendar management
        ├── task.py        # Task models
        └── ...
```

## 🚀 Quick Start

```python
from task_planner import Planner, Task, Day
import datetime as dt

# 1. Create tasks
tasks = [
    Task(name="Project Alpha", importance=8, interest=9, work_hours=4, deadline=dt.date.today() + dt.timedelta(days=2)),
    Task(name="Admin Work", importance=4, interest=2, work_hours=2)
]

# 2. Setup planner
planner = Planner(tasks=tasks, start_date=dt.date.today())

# 3. Calculate schedule
planner.importance_allocation()

# 4. View results
print(planner.calendar_str_tables_rus())
```

## ⚖️ Allocation Methods

- `importance_allocation()`: Balances importance and deadlines.
- `interest_allocation()`: Prioritizes what you enjoy doing most.
- `procrastination_allocation()`: Pushes tasks as close to deadlines as possible.
- `points_allocation()`: Score-based prioritization.

---
*Created by [chpdd](https://github.com/chpdd)*
