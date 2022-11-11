import file_handeling as file
import helper
import OMR_main as omr
import os
import cv2
from tkinter import *
from tkinter import messagebox as msg
from tkinter import filedialog
import batch_scan
import live_scan
from tkinter import font as tkFont

root = Tk()

root.title("OMR Scanner")

app_width = 400
app_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

###########    Frame1 ################################


# Frames 1
deatils_frame = LabelFrame(root, text="Subject Details", width=450, height=50, pady=3)

# Labels
subject_name_label = Label(deatils_frame, text="Subject Name:")
select_directory_label = Label(deatils_frame, text="Select Directory for saving files: ")

# Text Box

subject_name_txt_box = Entry(deatils_frame, width=50, borderwidth=5)
path_txt_box = Entry(deatils_frame, width=50, borderwidth=5)


def create_new():
    deatils_frame.grid(row=1, column=0, padx=30)
    subject_name_label.grid(row=0, column=0, sticky="w")
    subject_name_txt_box.grid(row=1, column=0, sticky="w")
    select_directory_label.grid(row=2, column=0, sticky="w")
    path_txt_box.grid(row=3, column=0, sticky="w", columnspan=5)
    btn_select_path.grid(row=3, column=1)
    btn_create_files.grid(row=4, column=0)
    btn_next1.place(relx=0.5, rely=0.75, anchor=CENTER)
    btn_start.place_forget()


def gui_directory():
    path_txt_box.delete(0, END)
    path = f'{filedialog.askdirectory()}'
    # print(path)
    path_txt_box.insert(0, path)


def create_Files():
    try:
        folder_name = str(subject_name_txt_box.get()) + "_Results"
        #print(folder_name)
        p = str(path_txt_box.get())
        file.create_folder_setCWD(p, folder_name)
        file.create_csv("Result")
        file.create_folder("Scanned_images")
        file.create_file("Answers", "txt")
        confirm = msg.showinfo("Success", "Files Created Successfully")
        if (confirm == "ok"):
            btn_next1.config(state=NORMAL)
            btn_create_files.config(state=DISABLED)
            btn_select_path.config(state=DISABLED)


    except:
        pass


def nxt_1st():
    btn_start.grid_forget()
    answer_frame.place(relx=0.5, rely=0.4, anchor=CENTER, )
    answer_frame.tkraise()
    deatils_frame.grid_forget()
    btn_next1.place_forget()
    btn_next2.place(relx=0.5, rely=0.75, anchor=CENTER)


def nxt_2nd():
    answer_frame.place_forget()
    select_method_frame.place(relx=0.5, rely=0.4, anchor=CENTER)
    btn_next2.place_forget()


# Button font

helv36 = tkFont.Font(family='Helvetica', size=30, weight=tkFont.BOLD)

# Buttons
btn_select_path = Button(deatils_frame, text="Browse", state=NORMAL, cursor="hand2", command=gui_directory)
btn_create_files = Button(deatils_frame, text="Create Files", command=create_Files, cursor="hand2", state=NORMAL)
btn_start = Button(root, text="Create New", padx=5, pady=2, font=helv36, bg="#264653", fg='white', cursor="hand2",
                   command=create_new)
btn_next1 = Button(root, text="Next", command=nxt_1st, padx=15, pady=5, state=DISABLED, cursor="hand2", )
btn_next2 = Button(root, text="Next", command=nxt_2nd, padx=15, pady=5, cursor="hand2", state=DISABLED)

btn_start.place(relx=0.5, rely=0.5, anchor=CENTER)

################## FRAME 2 #######################

# Frame 2
answer_frame = LabelFrame(root)

# Labels
number_of_qusn_label = Label(answer_frame, text="Number of Question :").grid(row=0, column=0)
number_of_options_label = Label(answer_frame, text="Number of options :").grid(row=1, column=0)

# Entry Boxes

number_of_qusn_box = Entry(answer_frame, width=5)
number_of_option_box = Entry(answer_frame, width=5)

#
number_of_qusn_box.grid(row=0, column=1, pady=5)
number_of_option_box.grid(row=1, column=1, pady=5)

# Process Function
number_of_qusns = 0
number_of_optios = 0
# ans_input_window = None
entry_list = []
answer = []


def proceed():
    number_of_qusns = int(number_of_qusn_box.get())
    number_of_optios = int(number_of_option_box.get())
    omr.set_q(number_of_qusns)
    omr.set_c(number_of_optios)
    global ans_input_window
    ans_input_window = Toplevel()
    insert_label = Label(ans_input_window, text="Insert Answer For Each Question")
    insert_label.grid(row=0, column=0)
    ans_input_window.title("Input Window")
    for x in range(number_of_qusns):
        n = Label(ans_input_window, text=f'{x + 1} :').grid(row=x + 1, column=0, padx=5)
        ans = Entry(ans_input_window, width=5)
        ans.grid(row=x + 1, column=1)
        entry_list.append(ans)
    btn_confirm = Button(ans_input_window, text="Confirm", cursor="hand2", command=confirm).grid(
        row=number_of_qusns + 2, column=1, padx=10, pady=5)


def confirm():
    for entry in entry_list:
        x = (str(entry.get())).upper()
        answer.append(x)
    file.write_answer(answer)
    omr.set_ans()
    ans_input_window.destroy()
    btn_process.config(state=DISABLED)
    btn_next2.config(state=NORMAL)
    print(answer)


# Button proceed

btn_process = Button(answer_frame, text="Process", cursor="hand2", command=proceed)
btn_process.grid(row=2, column=1, pady=5, padx=5)

########### FRAME 3 #####################

select_method_frame = LabelFrame(root)


# functions for batch scan

def batch_scan_btn():
    select_method_frame.place_forget()
    batch_scan_frame.place(relx=0.5, rely=0.4, anchor=CENTER)


# functions for live scan

def live_scan_btn():
    #batch_scan_frame.place_forget()
    select_method_frame.place_forget()
    live_scan_frame.place(relx=0.5, rely=0.4, anchor=CENTER)
def live_scan_strt():
    ip_get = str(live_ip_box.get())
    ip_add = f"{ip_get}/video"
    ip_add.strip()
    #print(ip_add)
    live_scan.live(ip_add)
    live_scan_frame.place_forget()
    last_frame.place(relx=0.5, rely=0.4, anchor=CENTER)

# Buttons

btn_batch_scan = Button(select_method_frame, text="Batch Scan", padx=10, pady=5, cursor="hand2", font=helv36,
                        command=batch_scan_btn)
btn_live_scan = Button(select_method_frame, text="Live Scan", padx=10, pady=5, cursor="hand2", font=helv36,
                       command=live_scan_btn)

btn_batch_scan.grid(row=0, column=0, pady=10, padx=5)
btn_live_scan.grid(row=1, column=0, pady=10, padx=5)

############# BATCH SCAN ##############

# Batch Scan Frame

batch_scan_frame = LabelFrame(root)


# FUNCTIONS BATCH SCAN
def browse_batch():
    batch_path = str(filedialog.askdirectory())
    batch_path_box.insert(0, batch_path)
    btn_batch_start.config(state=NORMAL)


def batch_scan_start():
    batch_scan.batch_scan(str(batch_path_box.get()))
    confirm = msg.showinfo("Success", "Task Completed Successfully")
    if (confirm == "ok"):
        batch_scan_frame.place_forget()
        last_frame.place(relx=0.5, rely=0.4, anchor=CENTER)


# Labels

info_label = Label(batch_scan_frame, text="Select the folder containing OMR sheet images:")
info_label.grid(row=0, column=0, pady=10, sticky="w")

# Entry Box

batch_path_box = Entry(batch_scan_frame, width=50, borderwidth=5)
batch_path_box.grid(row=1, column=0, pady=10, sticky="w", padx=2)

# Button

btn_batch_path = Button(batch_scan_frame, text="Browse", padx=10, pady=5, cursor="hand2", command=browse_batch)
btn_batch_start = Button(batch_scan_frame, text="Start", state=DISABLED, cursor="hand2", command=batch_scan_start)
btn_batch_path.grid(row=1, column=1, padx=4)
btn_batch_start.grid(row=3, pady=5)

# Live scan frame

live_scan_frame = LabelFrame(root)

# Labels

live_info_label = Label(live_scan_frame, text="Step-1: Run IP Camera app on mobile & Start the server")
live_info_label.grid(row=0, column=0, pady=10, sticky="w")
ip_label = Label(live_scan_frame, text="Step-2: Insert IP Camera Link")
ip_label.grid(row=1, column=0, pady=10, sticky="w")

# Entry Box

live_ip_box = Entry(live_scan_frame, width=50, borderwidth=5)
live_ip_box.grid(row=2, column=0, pady=10, sticky="w", padx=2)
live_ip_box.insert(0,"http://")

# Buttons

btn_live_start = Button(live_scan_frame, text="Start",  cursor="hand2", command=live_scan_strt)
btn_live_start.grid(row=3, pady=5)


# Last Frame

last_frame = LabelFrame(root)


# LAST FUNCTION

def exitOMR():
    root.destroy()


# def start_again():
#     btn_start.place(relx=0.5, rely=0.5, anchor=CENTER)
#     last_frame.place_forget()



btn_exit = Button(last_frame, text="Exit", padx=10, pady=5, cursor="hand2", font=helv36, command=exitOMR)
#btn_start_again = Button(last_frame, text="Start Again", padx=10, pady=5, cursor="hand2", font=helv36, command=start_again)

btn_exit.grid(row=0, column=0, pady=10, padx=5)
#btn_start_again.grid(row=1, column=0, pady=10, padx=5)

root.mainloop()
