from tkinter import *
from tkinter import messagebox
import csv
from csv import *
import os
import pandas as pd
root = Tk()
root.title('Insert Data')
depts = ['Select','Coding', 'Math', 'HR', 'Support', 'ELA', 'PS']
alphabet = 'abcdefghijklmnopqrstuvwxyz'

####[ Functions ]####
def clearfields():
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    email_entry.delete(0, END)
    age_spinbox.delete(0, END)
    age_spinbox.insert(0, 18)
    identification_entry.delete(0, END)
    dept_var.set(depts[0])
    agree_var.set(0)

def search():
    id = identification_entry.get()
    df = pd.read_csv('all_data.csv')
    if sum(df.ID == id):
        decision = messagebox.askquestion('Warning', 'This record already exists. Do you want to update this record ?')
        if decision == 'yes':
            new_df = df[df.ID == id]
            dept_var.set(list(new_df['Department'])[0])

            first_name_entry.delete(0, END)
            first_name_entry.insert(0, list(new_df['First Name'])[0])

            last_name_entry.delete(0, END)
            last_name_entry.insert(0, list(new_df['Last Name'])[0])

            email_entry.delete(0, END)
            email_entry.insert(0, list(new_df['Email'])[0])

            age_spinbox.delete(0, END)
            age_spinbox.insert(0, list(new_df['Age'])[0])

            new_df = df[df.ID != id]
            new_df.to_csv('all_data.csv', index=False)
            done.config(text='Update')
            messagebox.showwarning('Warning', "Don't forget to click update before closing the application")
        else:
            identification_entry.delete(0, END)
    else:
        messagebox.showinfo('Oops', 'No record found') 

def save_data():
    id = identification_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    age = age_spinbox.get()
    agree = agree_var.get()
    department = dept_var.get()
    

    first_name_check = True
    last_name_check = True
    at_check = False
    department_check = True
    for q in first_name:
        if q.lower() not in alphabet:
            first_name_check = False
            messagebox.showerror('Error', 'Check the First Name')
            break
    for q in last_name:
        if q.lower() not in alphabet:
            last_name_check = False
            messagebox.showerror('Error', 'Check the Last Name')
            break
    for q in email:
        if q == '@':
            at_check = True
            break
    com_check = True if email[-4:] == '.com' else False
    if not (at_check and com_check):
        messagebox.showerror('Error', 'Check the Email')
    if not agree:
        messagebox.showerror('Error', 'You must agree to all conditions')
    if department == 'Select':
        messagebox.showerror('Error', 'Choose a department')
        department_check = False

    all_checks = first_name_check and last_name_check and at_check and com_check and agree and department_check
    if all_checks:
        cols = ['ID', 'Department', 'First Name', 'Last Name', 'Email', 'Age']
        df = pd.read_csv('all_data.csv')
        all_data = [id, department, first_name, last_name, email, age]
        df.loc[len(df)] = all_data
        df.to_csv('all_data.csv', index=False)
        messagebox.showinfo('Data Entry', 'All data has been added')

####[ Main Code ]####
## Identification Frame
identification_frame = LabelFrame(root, text='Identification')
identification_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=20)

identification_label = Label(identification_frame, text='Employee ID')
identification_label.grid(row=0, column=0, padx=5)

identification_entry = Entry(identification_frame)
identification_entry.grid(row=0, column=1, padx=10)

search_button = Button(identification_frame, text='Check', command=search )
search_button.grid(row=0, column=2)

clear = Button(identification_frame, text='Clear Fields', command=clearfields)
clear.grid(row=0, column=3, padx=10)

## user Info Frame
user_info_frame = LabelFrame(root, text='User Information')
user_info_frame.grid(row=1, column=0, padx=20, pady=20)

dept_label = Label(user_info_frame, text='Department')
dept_label.grid(row=0, column=0)
dept_var = StringVar()
dept_var.set(depts[0])
dept_optionmenu = OptionMenu(user_info_frame, dept_var, *depts)
dept_optionmenu.grid(row=1, column=0)

first_name_label = Label(user_info_frame, text='First Name')
first_name_label.grid(row=0, column=1)
first_name_entry = Entry(user_info_frame)
first_name_entry.grid(row=1, column=1)

last_name_label = Label(user_info_frame, text='Last Name')
last_name_label.grid(row=0, column=2)
last_name_entry = Entry(user_info_frame)
last_name_entry.grid(row=1, column=2)

email_label = Label(user_info_frame, text='Email')
email_label.grid(row=0, column=3)
email_entry = Entry(user_info_frame)
email_entry.grid(row=1, column=3)

## Agreement Frame
agreement_labelframe = LabelFrame(root, text='Agreement')
agreement_labelframe.grid(row=2, column=0, sticky='ew',padx=20, pady=20)

age_label = Label(agreement_labelframe, text='Age')
age_label.grid(row=0, column=0, columnspan=2)
age_spinbox = Spinbox(agreement_labelframe, from_=18, to=120)
age_spinbox.grid(row=1, column=0, columnspan=2)

agree_var = IntVar()
check = Checkbutton(agreement_labelframe, text='I agree that I am an awesome person', variable=agree_var)
check.grid(row=0, column=2, rowspan=2)

## Done button
done = Button(root, text='Done', command=save_data)
done.grid(row=3, column=0, sticky='ew', padx=20, pady=20)

root.mainloop()