#!/usr/local/bin/python3
import member as mbr
import tkinter as tk
import pygubu

"""
Main window settings
"""
MainWindow_W = 640
MainWindow_H = 480

MainFrame_W = 500
MainFrame_H = 400

"""
Main window class
"""
class Application:

    def __init__(self, master):

        self.curr_mbr = mbr.member()

        self.master = master
        self.mainFrame = tk.Frame( self.master, width = MainFrame_W, height = MainFrame_H )
        self.mainFrame.pack( fill=tk.BOTH)

        self.NameLebel = tk.Label( self.mainFrame, text = "Name: " ).grid( row = 1 , column = 0)
        self.IDLebel = tk.Label( self.mainFrame, text = "ID: " ).grid( row = 2 , column = 0)
        self.PhoneLebel = tk.Label( self.mainFrame, text = "Phone: " ).grid( row = 3 , column = 0)

        self.NameEntry_Var  = tk.StringVar()
        self.IDEntry_Var    = tk.IntVar()
        self.PhoneEntry_Var = tk.StringVar()
        self.QueryID_Var    = tk.IntVar()

        self.NameEntry = tk.Entry( self.mainFrame, textvariable = self.NameEntry_Var ).grid( row = 1, column = 1)
        self.IDEntry = tk.Entry( self.mainFrame, textvariable = self.IDEntry_Var ).grid( row = 2, column = 1)
        self.PhoneEntry = tk.Entry( self.mainFrame, textvariable = self.PhoneEntry_Var ).grid( row = 3, column = 1)

        self.queryidLabel = tk.Label( self.mainFrame, text = "Search ID: " ).grid( row = 0, column = 0 )
        self.queryidEntry = tk.Entry( self.mainFrame, textvariable = self.QueryID_Var ).grid( row = 0, column = 1 )
        self.queryidBtn = tk.Button( self.mainFrame, text = "Search", command = self.queryMember ).grid( row = 0, column = 2 )

        self.saveCurrentBtn = tk.Button( self.mainFrame, text = "Save", command = self.SaveMemberInDB ).grid( row = 0, column = 3 )

        self.GUI_fill_entry()

    """
    Need to wrap sqlite to fill up the data item
    """
    def GUI_fill_entry(self):
        self.NameEntry_Var.set( self.curr_mbr.name )
        self.IDEntry_Var.set( self.curr_mbr.mem_id )
        self.PhoneEntry_Var.set( self.curr_mbr.cell_phone)

    def queryMember(self):
        self.curr_mbr.load_from_db( int( self.QueryID_Var.get() ) )
        self.NameEntry_Var.set( self.curr_mbr.name )
        self.IDEntry_Var.set( self.curr_mbr.mem_id )
        self.PhoneEntry_Var.set( self.curr_mbr.cell_phone )

    def SaveMemberInDB(self):
        self.curr_mbr.name = str(self.NameEntry_Var.get())
        self.curr_mbr.mem_id = int(self.IDEntry_Var.get())
        self.curr_mbr.cell_phone = str(self.PhoneEntry_Var.get())

        self.curr_mbr.save_to_db()


def main():
    root = tk.Tk()

    root.geometry('{}x{}'.format( MainWindow_W, MainWindow_H ))
    root.title( "蘆洲慢跑會員系統" )

    app = Application( root )

    root.mainloop()

if __name__ == '__main__':
    main()

