import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    priority INTEGER NOT NULL
)
""")
conn.commit()


def show_tasks():
    """
    Displays all tasks saved in the database.
    """
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("*** No tasks found in the database ***")
    else:
        for task in tasks:
            print(task)


def add_task():
    """
    Adds a task to the database with interactive input and basic validation.
    """
    task_name = input("Enter task name: ").strip()
    if not task_name:
        print("Task name cannot be empty!")
        return

    # Check if the task already exists
    cursor.execute("SELECT * FROM tasks WHERE name = ?", (task_name,))
    if cursor.fetchone():
        print("Task with this name already exists!")
        return

    try:
        priority = int(input("Enter priority (>=1): ").strip())
        if priority < 1:
            print("Priority must be greater than or equal to 1!")
            return
    except ValueError:
        print("Invalid priority! Please enter an integer value.")
        return

    cursor.execute("INSERT INTO tasks (name, priority) VALUES (?, ?)", (task_name, priority))
    conn.commit()
    print("Task added successfully!")


def change_priority():
    """
    Updates the priority of an existing task.
    """
    try:
        task_id = int(input("Enter the task ID to update priority: ").strip())
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            print("Task with this ID does not exist!")
            return

        new_priority = int(input("Enter new priority (>=1): ").strip())
        if new_priority < 1:
            print("Priority must be greater than or equal to 1!")
            return

        cursor.execute("UPDATE tasks SET priority = ? WHERE id = ?", (new_priority, task_id))
        conn.commit()
        print("Task priority updated successfully!")
    except ValueError:
        print("Invalid input! Please enter valid numbers.")


def delete_task():
    """
    Deletes a task from the database based on its ID.
    """
    try:
        task_id = int(input("Enter the task ID to delete: ").strip())
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        if not cursor.fetchone():
            print("Task with this ID does not exist!")
            return

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        print("Task deleted successfully!")
    except ValueError:
        print("Invalid input! Please enter a valid task ID.")


def main_menu():
    """
    Displays the main menu and allows the user to choose options interactively.
    """
    while True:
        print("\nMenu:")
        print("1. Show Tasks")
        print("2. Add Task")
        print("3. Change Priority")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            change_priority()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice! Please try again.")



if __name__ == "__main__":
    main_menu()
