#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import os
import json
import member as mbr
import competition as cmpt
from PyQt5 import QtCore, QtGui, QtWidgets, uic

'''-----------------------------------------------------------
Setting main window layout and class
-----------------------------------------------------------'''
qtCreatorFile = "mainwindow.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType( qtCreatorFile )

'''-----------------------------------------------------------
Tab member menu enum
-----------------------------------------------------------'''
TAB_MEMBER_INFO         = 0
TAB_MEMBER_TABLE        = 1
TAB_MEMBER_STATISTIC    = 2
TAB_MEMBER_GROUP        = 3
TAB_MEMBER_VOLUNTEER    = 4

'''-----------------------------------------------------------
Tab competition menu enum
-----------------------------------------------------------'''
TAB_CMPT_MENU_SETUP     = 0
TAB_CMPT_MENU_MBR_TBL   = 1
TAB_CMPT_MENU_STATISTIC = 2

class MainApp( QtWidgets.QMainWindow, UI_MainWindow ):
    def __init__( self ):
        QtWidgets.QMainWindow.__init__( self )
        UI_MainWindow.__init__( self )
        self.setupUi( self )
        self.curr_mbr = mbr.member()
        self.curr_cmpt = cmpt.competition()

        self.gui_qpixmap = QtGui.QPixmap( mbr.DEFAULT_PHOTO )
        self.gui_mbr_info_update_photo()

        ''' ---------------------------------------------
        Additional widgets attributes
        ----------------------------------------------'''
        self.edit_mbr_birth_ROC.setValidator( QtGui.QIntValidator( 0, 1000, self ) )

        ''' ---------------------------------------------
        Tab of Member Init
        ----------------------------------------------'''
        # Line Edit Widget
        self.edit_mbr_id.editingFinished.connect( self.gui_mbr_read_from_db )   # Or use returnPressed signal

        # Menubar action
        self.actionExport_to_excel.triggered.connect( self.curr_mbr.cnvt_db_to_excel )
        self.actionImport_from_excel.triggered.connect( self.curr_mbr.cnvt_excel_to_db )

        # Button widget action
        self.btn_mbr_info_img_file_diag.clicked.connect( self.gui_get_mbr_file_path )
        self.btn_mbr_info_create.clicked.connect( self.gui_save_curr_mbr_to_db )
        self.btn_mbr_info_update.clicked.connect( self.gui_update_curr_mbr_to_db )
        self.btn_mbr_info_delete.clicked.connect( self.gui_delete_curr_mbr )

        ''' ---------------------------------------------
        Tab of Competition Init
        ----------------------------------------------'''
        self.tab_member_menu.currentChanged.connect( self.gui_tab_member_menu_change_hndl )
        self.btn_cmpt_create.clicked.connect( self.gui_create_competition )

        self.gui_cmbo_selc_competition_init()

    def gui_tab_member_menu_change_hndl( self, curr_idx ):
        if( TAB_MEMBER_TABLE == curr_idx ):
            ''' ---------------------------------------------
            Table is filled only when TAB_MEMBER_TABLE is selected
            ----------------------------------------------'''
            self.gui_fill_data_table()

    ''' ---------------------------------------------
    Member Table procedure
    ----------------------------------------------'''
    def gui_fill_data_table( self ):
        self.gui_remove_data_table()
        self.gui_update_data_table()

    def gui_update_data_table( self ):
        mbrdata = self.curr_mbr.retrieve_all_data()

        HeaderLabel = [
            "編號", "職稱", "姓名", "身分證",  "出生年月日", "地區",
            "手機", "電話1", "電話2", "地址" ]
        self.mbrTable.setColumnCount( len( HeaderLabel ) )
        self.mbrTable.setHorizontalHeaderLabels(HeaderLabel)
        self.mbrTable.verticalHeader().setVisible(False)

        for row in mbrdata:
            indx = mbrdata.index( row )
            birthstr = "{}.{}.{}".format( row[mbr.DBItem.DB_birthday_Y.value],
                                          row[mbr.DBItem.DB_birthday_M.value],
                                          row[mbr.DBItem.DB_birthday_D.value] )
            self.mbrTable.insertRow( indx )
            self.mbrTable.setItem( indx, 0, QtWidgets.QTableWidgetItem( str( row[mbr.DBItem.DB_id.value] ) ) )  # index
            self.mbrTable.setItem( indx, 1, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_position.value] ) )   # position
            self.mbrTable.setItem( indx, 2, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_name.value] ) )       # name
            self.mbrTable.setItem( indx, 3, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_idcard.value] ) )     # idcard number
            self.mbrTable.setItem( indx, 4, QtWidgets.QTableWidgetItem( str( birthstr ) ) )                     # Birthday
            self.mbrTable.setItem( indx, 5, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_area.value] ) )       # area
            self.mbrTable.setItem( indx, 6, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_cell_phone.value] ) ) # cell phone
            self.mbrTable.setItem( indx, 7, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_phone.value] ) )      # phone
            self.mbrTable.setItem( indx, 8, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_phone2.value] ) )     # phone2
            self.mbrTable.setItem( indx, 9, QtWidgets.QTableWidgetItem( row[mbr.DBItem.DB_address.value] ) )    # Address

        for col in range( 0, len( HeaderLabel ) ):
            self.mbrTable.horizontalHeader().setSectionResizeMode( col, QtWidgets.QHeaderView.ResizeToContents )

    def gui_remove_data_table( self ):
        rows = self.mbrTable.rowCount()
        for row in range( 0, rows ):
            self.mbrTable.removeRow( 0 )

    ''' ---------------------------------------------
    Edit member widgets procedures
    ----------------------------------------------'''
    def gui_mbr_read_from_db( self ):
        try:
            query_id = int(self.edit_mbr_id.text())
            self.curr_mbr.load_from_db( query_id )
            self.gui_fill_line_edit_with_curr_mbr()
            self.gui_mbr_info_update_photo()
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    def gui_fill_line_edit_with_curr_mbr( self ):
        self.edit_mbr_address.setText(      "{}".format( self.curr_mbr.address )            )
        self.edit_mbr_area.setText(         "{}".format( self.curr_mbr.area )               )
        self.edit_mbr_birth_ROC.setText(    "{}".format( self.curr_mbr.birthday_Y )         )
        self.edit_mbr_birthday.setText(     "{}.{}.{}".format( self.curr_mbr.birthday_Y,
                                                               self.curr_mbr.birthday_M,
                                                               self.curr_mbr.birthday_D )   )
        self.edit_mbr_cellphone.setText(    "{}".format( self.curr_mbr.cell_phone )         )
        self.edit_mbr_idcard.setText(       "{}".format( self.curr_mbr.id_card )            )
        self.edit_mbr_name.setText(         "{}".format( self.curr_mbr.name )               )
        self.edit_mbr_phone1.setText(       "{}".format( self.curr_mbr.phone )              )
        self.edit_mbr_phone2.setText(       "{}".format( self.curr_mbr.phone2 )             )
        self.edit_mbr_position.setText(     "{}".format( self.curr_mbr.position )           )
        self.edit_mbr_photo_path.setText(   "{}".format( self.curr_mbr.photo )              )

    def gui_fill_curr_mbr_with_line_edit( self ):
        ret = False
        birth_list = self.curr_mbr.birthday_str_to_list( self.edit_mbr_birthday.text() )

        if birth_list == None:
            print( "Birth List value is Empty")
        elif len( birth_list ) != 3:
            print( "Len of Birth List is not eqult to 3 ({})".format( len( birth_list ) ) )
        else:
            try:
                self.curr_mbr.mem_id    = int( self.edit_mbr_id.text()      )
            except ValueError as err:
                print( "[Exception]: {}".format( err ) )

            self.curr_mbr.position      = str( self.edit_mbr_position.text()    )
            self.curr_mbr.name          = str( self.edit_mbr_name.text()        )
            self.curr_mbr.id_card       = str( self.edit_mbr_idcard.text()      )
            self.curr_mbr.birthday_Y    = int( birth_list[0]                    )
            self.curr_mbr.birthday_M    = int( birth_list[1]                    )
            self.curr_mbr.birthday_D    = int( birth_list[2]                    )
            self.curr_mbr.area          = str( self.edit_mbr_area.text()        )
            self.curr_mbr.cell_phone    = str( self.edit_mbr_cellphone.text()   )
            self.curr_mbr.phone         = str( self.edit_mbr_phone1.text()      )
            self.curr_mbr.phone2        = str( self.edit_mbr_phone2.text()      )
            self.curr_mbr.address       = str( self.edit_mbr_address.text()     )
            self.curr_mbr.photo         = str( self.edit_mbr_photo_path.text()  )
            ret = True

        return ret

    def gui_mbr_info_update_photo( self ):
        impath = self.curr_mbr.photo

        self.gui_qpixmap = QtGui.QPixmap( impath )

        if self.gui_qpixmap.isNull():
            self.gui_qpixmap = QtGui.QPixmap( mbr.DEFAULT_PHOTO )
            print( "Photo Path is invalid, showing with default photo" )

        lblsize = self.lbl_mbr_photo.size()
        self.lbl_mbr_photo.setPixmap( self.gui_qpixmap.scaled( lblsize, QtCore.Qt.KeepAspectRatio ) )

    def gui_get_mbr_file_path( self ):
        fname = QtWidgets.QFileDialog.getOpenFileName( self, '選擇一張照片', "./Resource", "Image Files (*.png *.jpg *.bmp)" )
        if fname[0]:
            import os
            self.edit_mbr_photo_path.setText( os.path.relpath( fname[0] ) )

    def gui_save_curr_mbr_to_db( self ):
        if True == self.gui_fill_curr_mbr_with_line_edit():
            self.curr_mbr.save_to_db()
            self.edit_mbr_id.setText( str( self.curr_mbr.mem_id ) )

    def gui_update_curr_mbr_to_db( self ):
        if True == self.gui_fill_curr_mbr_with_line_edit():
            self.curr_mbr.update_to_db()

    def gui_delete_curr_mbr( self ):
        self.curr_mbr.delete_item( int( self.edit_mbr_id.text() ) )

    ''' ---------------------------------------------
    Competition Tab Widgets action callback
    ----------------------------------------------'''
    def gui_cmbo_selc_competition_init( self ):
        ''' ---------------------------------------------
        No slot is connected to signal and hence disconnect()
        will failed. Just pass it and show err message
        ----------------------------------------------'''
        try:
            self.cmbo_selc_competition.currentIndexChanged.disconnect()
        except TypeError as err:
            print( "[cmbo_selc_competition] {}".format( err ) );

        self.cmbo_selc_competition.clear()
        self.cmbo_selc_competition.addItem( "請選擇賽事" )
        for name in os.listdir( cmpt.CMPT_RSC_BASE_PATH ):
            if os.path.isdir( "{}{}".format( cmpt.CMPT_RSC_BASE_PATH, name ) ):
                self.cmbo_selc_competition.addItem( name )

        self.cmbo_selc_competition.currentIndexChanged.connect(
            self.gui_cmbo_selc_competition_chng
            )

    def gui_cmbo_selc_competition_chng( self, i ):
        ''' ---------------------------------------------
        Note that we should restrict file encoding as utf8
        ----------------------------------------------'''
        print("[cmbo_selc_cmpt]: select {} ( {} )".format( i, self.cmbo_selc_competition.currentText() ))
        if i != 0:
            cmpt_filename = "{}{}/cmpt.json".format(
                cmpt.CMPT_RSC_BASE_PATH,
                self.cmbo_selc_competition.currentText() )
            with open(cmpt_filename, "r", encoding='utf-8' ) as cmpt_info:
                cmpt_data = json.load( cmpt_info )
                print(cmpt_data)
                self.edit_cmpt_name.setText( "{}".format( cmpt_data['name']))
                self.edit_cmpt_location.setText( "{}".format( cmpt_data['location']))
                self.edit_cmpt_date.setText( "{}".format( cmpt_data['date']))

                self.curr_cmpt.target_cmpt_set( cmpt_data['name'] )

    def gui_create_competition( self ):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("賽事建立")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        cmpt_name = str( self.edit_cmpt_name.text() )
        cmpt_locl = str( self.edit_cmpt_location.text() )
        cmpt_date = str( self.edit_cmpt_date.text() )

        ''' ---------------------------------------------
        Folder name = [date]_[name]
        ----------------------------------------------'''
        cmpt_fldr = cmpt_date + "_" + cmpt_name

        ''' ---------------------------------------------
        Sanity check if the competition folder has been created
        ----------------------------------------------'''
        for name in os.listdir( cmpt.CMPT_RSC_BASE_PATH ):
            print("{} {}".format(name, cmpt_fldr))
            if name == cmpt_fldr:
                msg.setText("{} 已經建立過囉!".format(cmpt_fldr))
                retval = msg.exec_()

        try:
            os.makedirs( cmpt.CMPT_RSC_BASE_PATH + cmpt_fldr )
            data = { "name": cmpt_name, "location": cmpt_locl, "date": cmpt_date }

            with open( cmpt.CMPT_RSC_BASE_PATH + cmpt_fldr + "/cmpt.json", 'w',
                    encoding='utf-8' ) as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4, separators=(',', ': ') )

            self.curr_cmpt.target_cmpt_set( cmpt_fldr )
            self.curr_cmpt.create_tbl()

            msg.setText("{} 完成建立!".format(cmpt_fldr))
            retval = msg.exec_()

            self.gui_cmbo_selc_competition_init()
        except:
            print("Failed to create competition")

'''-----------------------------------------------------------
Main entry point
-----------------------------------------------------------'''
def main():
    import sys
    app = QtWidgets.QApplication( sys.argv )
    window = MainApp()
    window.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()

'''-----------------------------------------------------------
Reference
1. An framework to integrate UI file into a class:
   http://pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/
2. http://stackoverflow.com/questions/30017853/sqlite3-table-into-qtablewidget-sqlite3-pyqt5
3. ComboBox: https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
4. Json load with UTF-8:
    http://stackoverflow.com/questions/12468179/unicodedecodeerror-utf8-codec-cant-decode-byte-0x9c
5. http://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
6. http://www.cnblogs.com/stubborn412/p/3818423.html
-----------------------------------------------------------'''
