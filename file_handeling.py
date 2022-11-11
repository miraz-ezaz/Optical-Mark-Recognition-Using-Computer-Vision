import os
import tkinter as tk
from tkinter import filedialog
import time
import helper

def create_file(name,type):
    file_name = f'{name}.{type}'
    file = open(file_name,"w")
    file.close()
    return file_name
def create_csv(name):
    file_name = f'{name}.csv'
    file = open(file_name, "w")
    file.write("Roll,Mark\n")
    file.close()
    return file_name

def create_folder(name):
    os.makedirs(name)
    return name

def ask_directory():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    #path = helper.r_path(path)
    return path

def create_folder_setCWD(path,name):
    os.chdir(path)
    f_name = create_folder(name)
    n_path = f'{path}/{f_name}'
    os.chdir(n_path)
    return n_path
def write_answer(ans):

    file = open("Answers.txt","w")
    options = ['A', 'B', 'C', 'D', 'E']
    for x in ans:
        i = options.index(str(x))
        file.write(str(i)+"\n")
    file.close()
def return_answer(file_name):
    answer=[]
    file = open(file_name,"r")
    for line in file:
        answer.append(int(line))
    file.close()
    return answer

def insert_ans(file_name,result):
    file = open(file_name,"a")

    for r in result:
        file.write(r)
    file.close()






