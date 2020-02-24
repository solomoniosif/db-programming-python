import pymysql
from tabulate import tabulate
from secrets import host, password, user


#! 1. Connect genericaly to MySQL and create the todo_app database
db = pymysql.connect(host, user, password, "")
create_database = "CREATE DATABASE IF NOT EXISTS todo_app DEFAULT CHARACTER SET utf8;"
with db.cursor() as c:
    c._defer_warnings = True
    c.execute(create_database)
db.close()

#! 2. CONNECT to newly created database
db = pymysql.connect(host, user, password, "todo_app")


#! 3.  CREATE tasks table
create_table = """CREATE TABLE IF NOT EXISTS tasks(
        id INT PRIMARY KEY AUTO_INCREMENT,
        task TEXT NOT NULL,
        done TINYINT(1));"""
# * SQL Statement to add a `tags` column to `tasks` table
# alter_table = "ALTER TABLE tasks ADD tags TEXT"
with db.cursor() as c:
    c._defer_warnings = True
    c.execute(create_table)
db.close()


# * Functions to comunicate with the database based on user input
def show_task_list(c):
    select_stmt = "SELECT id, task FROM tasks WHERE done != 1 ORDER BY id;"
    c.execute(select_stmt)
    rows = c.fetchall()
    headers = [d[0] for d in c.description]
    print(' This are all the unfinished tasks!')
    print(tabulate(rows, headers, tablefmt="psql"))


def mark_as_done(c, db, task_id):
    sql_c = "UPDATE tasks SET done = 1 WHERE id = %s"
    c.execute(sql_c, task_id)
    db.commit()


def add_new_task(c, db, task_name):
    sql_c = "INSERT INTO tasks(task, done) VALUES(%s, 0)"
    c.execute(sql_c, task_name)
    db.commit()


def show_completed_tasks(c):
    sql_c = "SELECT id, task FROM tasks WHERE done = 1 ORDER BY id;"
    c.execute(sql_c)
    rows = c.fetchall()
    headers = [d[0] for d in c.description]
    print(tabulate(rows, headers, tablefmt="psql"))


def delete_task(c, db, task_id):
    sql_c = "DELETE FROM tasks WHERE id = %s"
    c.execute(sql_c, task_id)
    db.commit()


def add_tags_to_task(c, db, task_id, tags):
    sql_c = "UPDATE tasks SET tags = %s WHERE id = %s"
    c.execute(sql_c, (tags, task_id))
    db.commit()


def find_task_by_tag(c, db, tag):
    sql_c = "SELECT id, task FROM tasks WHERE tags LIKE %s;"
    f_tag = f'%{tag}%'
    c.execute(sql_c, f_tag)
    rows = c.fetchall()
    headers = [d[0] for d in c.description]
    print(f' This are all the tasks with tha tag : `{tag}`')
    print(tabulate(rows, headers, tablefmt="psql"))


if __name__ == "__main__":
    db = pymysql.connect(host, user, password, "todo_app")
    menu = """
    WELCOME TO YOUR TO-DO APP:
        1 - Show task list
        2 - Show completed tasks
        3 - Mark task as done
        4 - Add new task
        5 - Add tags to a task
        6 - Find tasks by tag
        7 - Delete task
        8 - Exit application
    """
    with db.cursor() as c:
        c._defer_warnings = True
        while True:
            print(menu)
            option = int(input('Your choice : '))
            if option not in range(1, 9):
                continue
            elif option == 1:  # * Show task list
                show_task_list(c)
            elif option == 2:  # * Show completed tasks
                show_completed_tasks(c)
            elif option == 3:  # * Mark task as done
                task_id = int(
                    input('Enter the id of the task you would like to mark as done : '))
                mark_as_done(c, db, task_id)
            elif option == 4:  # * Add new task
                task_name = input('Enter the new task name : ')
                add_new_task(c, db, task_name)
            elif option == 5:  # * Add tags to a task
                task_id = int(
                    input('Select the id of the task you would like to add a tag to : '))
                tags = input(
                    'Enter a tag or a list of comma separated tags : ')
                add_tags_to_task(c, db, task_id, tags)
            elif option == 6:  # * Find tasks by tag
                tag = input('Enter the tag : ')
                find_task_by_tag(c, db, tag)
            elif option == 7:  # * Delete task
                task_id = int(
                    input('Enter the id of the task you would like to delete : '))
                delete_task(c, db, task_id)
            elif option == 8:  # * Exit application
                break
    db.close()
