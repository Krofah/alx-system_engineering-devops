#!/usr/bin/python3
"""Exports to-do list information for a given employee ID to CSV format."""
import csv
import requests
from sys import argv


def to_csv():
    """Export API data to CSV"""
    if len(argv) < 2:
        print("Error: Employee ID not provided.")
        print("Usage: python3 1-export_to_CSV.py <employee_id>")
        return

    try:
        employee_id = int(argv[1])
    except ValueError:
        print("Error: Invalid employee ID. Please provide a valid integer.")
        return

    users = requests.get("http://jsonplaceholder.typicode.com/users")
    if users.status_code != 200:
        print("Error: Failed to retrieve user data from the API.")
        return

    for user in users.json():
        if user.get('id') == employee_id:
            username = user.get('username')
            break
    else:
        print(f"Error: User with ID {employee_id} not found.")
        return

    task_status_title = []
    todos = requests.get("http://jsonplaceholder.typicode.com/todos")
    if todos.status_code != 200:
        print("Error: Failed to retrieve task data from the API.")
        return

    for task in todos.json():
        if task.get('userId') == employee_id:
            task_status_title.append((task.get('completed'), task.get('title')))

    filename = f"{employee_id}.csv"
    with open(filename, "w") as csvfile:
        fieldnames = ["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for task in task_status_title:
            writer.writerow({
                "USER_ID": employee_id,
                "USERNAME": username,
                "TASK_COMPLETED_STATUS": task[0],
                "TASK_TITLE": task[1]
            })


if __name__ == "__main__":
    to_csv()