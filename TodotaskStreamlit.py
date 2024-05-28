import streamlit as st
from datetime import datetime
from collections import defaultdict

class Node:
    def __init__(self, data, date=None, time=None):
        self.data = data
        self.date = date
        self.time = time
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task, date, time):
        new_node = Node(task, date, time)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def remove_task(self, task):
        current = self.head
        previous = None
        while current is not None:
            if current.data == task:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def display_tasks(self):
        task_groups = defaultdict(list)
        current = self.head
        while current is not None:
            task_groups[current.date].append(current)
            current = current.next
        return task_groups

if 'tasks_list' not in st.session_state:
    st.session_state['tasks_list'] = LinkedList()

def main():
    st.title("To-Do List App with Linked List")

    user_name = st.sidebar.text_input("Enter your name", value="Your name")

    tasks_list = st.session_state['tasks_list']

    task_input = st.sidebar.text_input("Add Task:")
    task_date = st.sidebar.date_input("Task Date:", datetime.today())

    if 'task_time' not in st.session_state:
        st.session_state['task_time'] = datetime.now().time()

    task_time = st.sidebar.time_input("Task Time:", st.session_state['task_time'])

    st.session_state['task_time'] = task_time

    if st.sidebar.button("Add"):
        if task_input:
            tasks_list.add_task(task_input, task_date, task_time)

    task_to_remove = st.sidebar.text_input("Remove Task:")
    if st.sidebar.button("Remove"):
        if task_to_remove:
            if tasks_list.remove_task(task_to_remove):
                st.sidebar.success("Task removed successfully!")
            else:
                st.sidebar.error("Task not found.")

    st.write(f"## {user_name}'s To-Do List:")
    task_groups = tasks_list.display_tasks()

    if not task_groups:
        st.write("No tasks yet. Add your task by using sidebar!")

    for date, tasks in sorted(task_groups.items()):
        st.write(f"### {date.strftime('%Y-%m-%d')}")
        for i, task in enumerate(tasks, start=1):
            if task.date and task.time:
                st.write(f"{i}. {task.data} at {task.time.strftime('%I:%M %p')}")
            else:
                st.write(f"{i}. {task.data}")

if __name__ == "__main__":
    main()
