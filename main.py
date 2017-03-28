#!/usr/local/bin/python3
import member as mbr
import tkinter as tk

"""
Main window settings
"""
MainWindow_W = 720
MainWindow_H = 480

MenuFrame_W = MainWindow_H
MenuFrame_H = 100

MainFrame_W = MainWindow_H
MainFrame_H = MainWindow_H - MenuFrame_H

"""
Main window class
"""
class Application:

    def __init__(self, master):

        self.curr_mbr = mbr.member()

        self.master = master
        self.menuFrame = tk.Frame( self.master, width = MenuFrame_W, height = MenuFrame_H )
        self.menuFrame.grid( row = 0, column = 0 )
        self.MenuHandler( self.menuFrame )

        self.mainFrame = tk.Frame( self.master, width = MainFrame_W, height = MainFrame_H )
        self.mainFrame.grid( row = 1, column = 0 )

        self.gui_pg_insert_member( self.mainFrame )

    def MenuHandler( self, frame ):
        """         Constant        """
        BTN_MBR_INFO_PG_STR     = "會員資料"
        BTN_STATISTIC_PG_STR    = "統計資料"
        BTN_GROUP_PG_STR        = "分組名單"
        BTN_VOLUNTEER_PG_STR    = "馬拉松志工調度"

        """         Menu Setting    """
        self.btn_mbr_info_pg    = tk.Button( frame, text = BTN_MBR_INFO_PG_STR  )
        self.btn_statistic_pg   = tk.Button( frame, text = BTN_STATISTIC_PG_STR )
        self.btn_group_pg       = tk.Button( frame, text = BTN_GROUP_PG_STR     )
        self.btn_volunteer_pg   = tk.Button( frame, text = BTN_VOLUNTEER_PG_STR )

        self.btn_mbr_info_pg.grid(  row = 0, column = 0)
        self.btn_statistic_pg.grid( row = 0, column = 1)
        self.btn_group_pg.grid(     row = 0, column = 2)
        self.btn_volunteer_pg.grid( row = 0, column = 3)

    def gui_pg_member_table( self, frame ):
        print( "Currently not supported..." )

    def gui_pg_insert_member(self, frame ):
        """
        TODO: Use an general array and dict to organize widgets and their attributes
              and create them in an iteration manner.
        """
        self.PositionEntry_Var      = tk.StringVar()
        self.NameEntry_Var          = tk.StringVar()
        self.IDCardEntry_Var        = tk.StringVar()
        self.BorthYearROCEntry_Var  = tk.StringVar()
        self.BorthYMDEntry_Var      = tk.StringVar()
        self.AreaEntry_Var          = tk.StringVar()
        self.CellPhoneEntry_Var     = tk.StringVar()
        self.PhonePrimaryEntry_Var  = tk.StringVar()
        self.PhoneSecondEntry_Var   = tk.StringVar()
        self.AddressEntry_Var       = tk.StringVar()

        self.QueryID_Var            = tk.IntVar()

        self.PositionLabel      = tk.Label( frame, text = "Position: " )
        self.NameLabel          = tk.Label( frame, text = "Name: " )
        self.IDCardLabel        = tk.Label( frame, text = "ID Card: " )
        self.BorthYearROCLabel  = tk.Label( frame, text = "Birth( Republic Era): " )
        self.BorthYMDLabel      = tk.Label( frame, text = "Birth: " )
        self.AreaLabel          = tk.Label( frame, text = "Area: " )
        self.CellPhoneLabel     = tk.Label( frame, text = "Cell Phone: " )
        self.PhonePrimaryLabel  = tk.Label( frame, text = "Primary Phone: " )
        self.PhoneSecondLabel   = tk.Label( frame, text = "Secondary Phone: " )
        self.AddressLabel       = tk.Label( frame, text = "Address: " )

        self.queryidLabel       = tk.Label( frame, text = "Search ID: " )

        self.PositionEntry      = tk.Entry( frame, textvariable = self.PositionEntry_Var        )
        self.NameEntry          = tk.Entry( frame, textvariable = self.NameEntry_Var            )
        self.IDCardEntry        = tk.Entry( frame, textvariable = self.IDCardEntry_Var          )
        self.BorthYearROCEntry  = tk.Entry( frame, textvariable = self.BorthYearROCEntry_Var    )
        self.BorthYMDEntry      = tk.Entry( frame, textvariable = self.BorthYMDEntry_Var        )
        self.AreaEntry          = tk.Entry( frame, textvariable = self.AreaEntry_Var            )
        self.CellPhoneEntry     = tk.Entry( frame, textvariable = self.CellPhoneEntry_Var       )
        self.PhonePrimaryEntry  = tk.Entry( frame, textvariable = self.PhonePrimaryEntry_Var    )
        self.PhoneSecondEntry   = tk.Entry( frame, textvariable = self.PhoneSecondEntry_Var     )
        self.AddressEntry       = tk.Entry( frame, textvariable = self.AddressEntry_Var         )

        self.queryidEntry       = tk.Entry( frame, textvariable = self.QueryID_Var )
        self.queryidEntry.bind('<Return>', ( lambda event: self.queryMember() ) )

        self.queryidBtn         = tk.Button( frame, text = "Search", command = self.queryMember )
        self.saveCurrentBtn     = tk.Button( frame, text = "Save", command = self.SaveMemberInDB )

        """ Test function button """
        self.cnvt_excel_to_db = tk.Button( frame, text = "Excel to DB", command = self.curr_mbr.cnvt_excel_to_db )
        self.cnvt_db_to_excel = tk.Button( frame, text = "DB to Excel", command = self.curr_mbr.cnvt_db_to_excel )

        """ Organize the widgets """
        self.queryidLabel.grid(     row = 0, column = 0 )
        self.queryidEntry.grid(     row = 0, column = 1 )

        self.PositionLabel.grid(        row = 1,  column = 0 )
        self.NameLabel.grid(            row = 2,  column = 0 )
        self.IDCardLabel.grid(          row = 3,  column = 0 )
        self.BorthYearROCLabel.grid(    row = 4,  column = 0 )
        self.BorthYMDLabel.grid(        row = 5,  column = 0 )
        self.AreaLabel.grid(            row = 6,  column = 0 )
        self.CellPhoneLabel.grid(       row = 7,  column = 0 )
        self.PhonePrimaryLabel.grid(    row = 8,  column = 0 )
        self.PhoneSecondLabel.grid(     row = 9,  column = 0 )
        self.AddressLabel.grid(         row = 10, column = 0 )

        self.PositionEntry.grid(        row = 1,  column = 1 )
        self.NameEntry.grid(            row = 2,  column = 1 )
        self.IDCardEntry.grid(          row = 3,  column = 1 )
        self.BorthYearROCEntry.grid(    row = 4,  column = 1 )
        self.BorthYMDEntry.grid(        row = 5,  column = 1 )
        self.AreaEntry.grid(            row = 6,  column = 1 )
        self.CellPhoneEntry.grid(       row = 7,  column = 1 )
        self.PhonePrimaryEntry.grid(    row = 8,  column = 1 )
        self.PhoneSecondEntry.grid(     row = 9,  column = 1 )
        self.AddressEntry.grid(         row = 10, column = 1 )

        self.queryidBtn.grid(       row = 0, column = 2 )
        self.saveCurrentBtn.grid(   row = 0, column = 3 )
        self.cnvt_excel_to_db.grid( row = 0, column = 4 )
        self.cnvt_db_to_excel.grid( row = 0, column = 5 )

        self.GUI_blank_entry()

    """
    Need to wrap sqlite to fill up the data item
    """
    def GUI_fill_entry(self):
        self.NameEntry_Var.set( self.curr_mbr.name )
        self.CellPhoneEntry_Var.set( self.curr_mbr.cell_phone )

        self.PositionEntry_Var.set(     self.curr_mbr.cell_phone    )
        self.NameEntry_Var.set(         self.curr_mbr.name          )
        self.IDCardEntry_Var.set(       self.curr_mbr.cell_phone    )
        self.BorthYearROCEntry_Var.set( self.curr_mbr.cell_phone    )
        self.BorthYMDEntry_Var.set(     self.curr_mbr.cell_phone    )
        self.AreaEntry_Var.set(         self.curr_mbr.cell_phone    )
        self.CellPhoneEntry_Var.set(    self.curr_mbr.cell_phone    )
        self.PhonePrimaryEntry_Var.set( self.curr_mbr.cell_phone    )
        self.PhoneSecondEntry_Var.set(  self.curr_mbr.cell_phone    )
        self.AddressEntry_Var.set(      self.curr_mbr.cell_phone    )

    def GUI_blank_entry(self):
        self.NameEntry_Var.set( "" )
        self.CellPhoneEntry_Var.set( "" )

    def queryMember(self):
        self.curr_mbr.load_from_db( self.QueryID_Var.get() )

        self.PositionEntry_Var.set(     self.curr_mbr.position      )
        self.NameEntry_Var.set(         self.curr_mbr.name          )
        self.IDCardEntry_Var.set(       self.curr_mbr.id_card       )
        self.BorthYearROCEntry_Var.set( self.curr_mbr.birthdayROC   )
        self.BorthYMDEntry_Var.set(     self.curr_mbr.birthday      )
        self.AreaEntry_Var.set(         self.curr_mbr.area          )
        self.CellPhoneEntry_Var.set(    self.curr_mbr.cell_phone    )
        self.PhonePrimaryEntry_Var.set( self.curr_mbr.phone         )
        self.PhoneSecondEntry_Var.set(  self.curr_mbr.phone2        )
        self.AddressEntry_Var.set(      self.curr_mbr.address       )

    def SaveMemberInDB(self):
        self.curr_mbr.position      = str( self.PositionEntry_Var.get()     )
        self.curr_mbr.name          = str( self.NameEntry_Var.get()         )
        self.curr_mbr.id_card       = str( self.IDCardEntry_Var.get()       )
        self.curr_mbr.birthdayROC   = str( self.BorthYearROCEntry_Var.get() )
        self.curr_mbr.birthday      = str( self.BorthYMDEntry_Var.get()     )
        self.curr_mbr.area          = str( self.AreaEntry_Var.get()         )
        self.curr_mbr.cell_phone    = str( self.CellPhoneEntry_Var.get()    )
        self.curr_mbr.phone         = str( self.PhonePrimaryEntry_Var.get() )
        self.curr_mbr.phone2        = str( self.PhoneSecondEntry_Var.get()  )
        self.curr_mbr.address       = str( self.AddressEntry_Var.get()      )

        self.curr_mbr.save_to_db()

def main():
    root = tk.Tk()

    root.geometry('{}x{}'.format( MainWindow_W, MainWindow_H ))
    root.title( "蘆洲慢跑會員系統" )

    app = Application( root )

    root.mainloop()

if __name__ == '__main__':
    main()


"""
Reference

1. Entry constructor and grid should be stated separatly
   http://stackoverflow.com/questions/1101750/tkinter-attributeerror-nonetype-object-has-no-attribute-get
2. Using lambda to call function instead handling by callback function
   http://stackoverflow.com/questions/21943718/how-to-bind-the-enter-key-to-a-button-in-tkinter
"""
