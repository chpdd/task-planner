# Task Planner

App for intelligent task scheduling and daily planning.  
This project implements a task planner library that helps organize and prioritize tasks based on multiple parameters such as importance, interest, workload, and deadlines. Users can define their daily available time and let the bot suggest an optimal schedule.

## 🧠 Features

The Task Planner is designed to help you:

- 📅 Add tasks with metadata including interest level, importance, estimated work time, and deadline.
- 🤖 Automatically calculate an optimal daily task schedule based on available working hours.
- ⚙️ Customize daily available time per day.
- 📈 Prioritize tasks using a scoring model combining multiple task attributes.

## 🚀 Motivation

I developed this app when I had *a massive list of tasks and needed help deciding what to do each day*. The bot uses a simple algorithm to balance urgency, importance, and personal interest, resulting in schedules that fit within daily constraints.

---

## 🧩 How It Works

Each task contains these parameters:

| Parameter    | Description                                              |
|--------------|----------------------------------------------------------|
| Interest     | How much you *want* to do the task                       |
| Work Time    | Estimated time needed to complete the task               |
| Importance   | How critical the task is                                  |
| Deadline     | By when the task needs to be completed                   |
| Available Time | Hours you plan to work each day                        |

The app then uses these values to determine which tasks should be scheduled earlier and which can wait, optimizing for a balanced daily workflow.

---

## 📦 Project Structure

```

/
├── fluentd/
├── postgres/
│   └── scripts/
├── web/
├── docker-compose.yml
├── README.md
└── TODO

````

- **fluentd/** — Logging and data collection configuration (if used).
- **postgres/scripts/** — Database initialization and schema scripts.
- **web/** — Web components or admin interfaces (if applicable).
- **docker-compose.yml** — Development and deployment configuration.

---

## 📥 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/chpdd/task-planner.git
   cd task-planner
   ```

2. **Configure environment**

   * Set up a `.env` file with your Telegram bot token and database credentials.
   * Example variables:

     ```env
     TELEGRAM_TOKEN=your_bot_token
     DATABASE_URL=postgres://user:password@host:port/dbname
     ```

3. **Run with Docker**

   ```bash
   docker-compose up --build
   ```

> You can also run individual components locally (bot, database, web) if you prefer.

---

## 📝 Usage

Start the bot and use Telegram commands to interact:

* `/add` — Add a new task
* `/list` — Show all tasks
* `/schedule` — Generate a daily plan
* `/delete` — Remove a task

*(Add actual supported commands once defined in code.)*

---

## 🎯 Example Scenario

1. Add a task:

   ```text
   /add Finish report | interest:7, importance:9, work_time:3, deadline:2025-12-20
   ```
2. Add more tasks.
3. Run the scheduler:

   ```text
   /schedule
   ```
4. The app returns an ordered list of tasks for today.

---

## 📌 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/xyz`)
3. Commit your changes
4. Push to your fork and open a Pull Request

---

