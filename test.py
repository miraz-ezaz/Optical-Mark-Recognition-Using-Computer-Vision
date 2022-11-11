# import file_handeling as f
# import os
# import helper as h
# #print(f.return_answer("ans.txt"))
#
# # result = []
# # for x in range(2):
# #     r = input("Roll: ")
# #     m = input("\nMark: ")
# #     s = f'{r},{m}\n'
# #     result.append(s)
# # print(result)
# # file = open("result.csv","w")
# # for r in result:
# #     file.write(r)
# #
# # file.close()
# #print(h.r_path(os.getcwd()))
# #print(f.ask_directory())
# #options= ['A','B','C','D','E']
# #f.write_answer(5,options,"ans.txt")
# #print(f.return_answer("ans.txt"))
from tkinter import *

import live_scan


root = Tk()
root.title("OMR Scanner")

b = Button(root,text = "click",command=lambda : live_scan.live()).pack()

root.mainloop()



