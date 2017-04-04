#!/usr/local/bin/python3
import member as mbr
from PyQt5 import QtCore, QtGui, QtWidgets, uic

'''-----------------------------------------------------------
Setting main window layout and class
-----------------------------------------------------------'''
qtCreatorFile = "mainwindow.ui"
UI_MainWindow, QtBaseClass = uic.loadUiType( qtCreatorFile )

class MainApp( QtWidgets.QMainWindow, UI_MainWindow ):
    def __init__( self ):
        QtWidgets.QMainWindow.__init__( self )
        UI_MainWindow.__init__( self )
        self.setupUi( self )
        self.curr_mbr = mbr.member()

        self.gui_qpixmap = QtGui.QPixmap( "Resource/none_photo.jpg" )
        self.gui_mbr_info_update_photo()

        ''' ---------------------------------------------
        Additional widgets attributes
        ----------------------------------------------'''
        self.edit_mbr_birth_ROC.setValidator( QtGui.QIntValidator(0,1000, self) )

        ''' ---------------------------------------------
        Connect each widget to its method
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

    def gui_mbr_read_from_db( self ):
        try:
            query_id = int(self.edit_mbr_id.text())
            self.curr_mbr.load_from_db( query_id )
            self.gui_fill_line_edit_with_curr_mbr()
            self.gui_mbr_info_update_photo()
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    def gui_fill_line_edit_with_curr_mbr( self ):
        self.edit_mbr_address.setText(      "{}".format( self.curr_mbr.address )    )
        self.edit_mbr_area.setText(         "{}".format( self.curr_mbr.area )       )
        self.edit_mbr_birth_ROC.setText(    "{}".format( self.curr_mbr.birthdayROC ))
        self.edit_mbr_birthday.setText(     "{}".format( self.curr_mbr.birthday )   )
        self.edit_mbr_cellphone.setText(    "{}".format( self.curr_mbr.cell_phone ) )
        self.edit_mbr_idcard.setText(       "{}".format( self.curr_mbr.id_card )    )
        self.edit_mbr_name.setText(         "{}".format( self.curr_mbr.name )       )
        self.edit_mbr_phone1.setText(       "{}".format( self.curr_mbr.phone )      )
        self.edit_mbr_phone2.setText(       "{}".format( self.curr_mbr.phone2 )     )
        self.edit_mbr_position.setText(     "{}".format( self.curr_mbr.position )   )
        self.edit_mbr_photo_path.setText(   "{}".format( self.curr_mbr.photo )      )

    def gui_fill_curr_mbr_with_line_edit( self ):
        self.curr_mbr.mem_id        = int( self.edit_mbr_id.text()          )
        self.curr_mbr.position      = str( self.edit_mbr_position.text()    )
        self.curr_mbr.name          = str( self.edit_mbr_name.text()        )
        self.curr_mbr.id_card       = str( self.edit_mbr_idcard.text()      )
        self.curr_mbr.birthdayROC   = int( self.edit_mbr_birth_ROC.text()   )
        self.curr_mbr.birthday      = str( self.edit_mbr_birthday.text()    )
        self.curr_mbr.area          = str( self.edit_mbr_area.text()        )
        self.curr_mbr.cell_phone    = str( self.edit_mbr_cellphone.text()   )
        self.curr_mbr.phone         = str( self.edit_mbr_phone1.text()      )
        self.curr_mbr.phone2        = str( self.edit_mbr_phone2.text()      )
        self.curr_mbr.address       = str( self.edit_mbr_address.text()     )
        self.curr_mbr.photo         = str( self.edit_mbr_photo_path.text()  )

    def gui_mbr_info_update_photo( self ):
        impath = self.curr_mbr.photo

        self.gui_qpixmap = QtGui.QPixmap( impath )

        if self.gui_qpixmap.isNull():
            self.gui_qpixmap = QtGui.QPixmap( "Resource/none_photo.jpg" )
            print( "Path is invalid" )

        lblsize = self.lbl_mbr_photo.size()
        self.lbl_mbr_photo.setPixmap( self.gui_qpixmap.scaled( lblsize, QtCore.Qt.KeepAspectRatio ) )

    def gui_get_mbr_file_path( self ):
        fname = QtWidgets.QFileDialog.getOpenFileName( self, '選擇一張照片', "./Resource", "Image Files (*.png *.jpg *.bmp)" )
        if fname[0]:
            import os
            self.edit_mbr_photo_path.setText( os.path.relpath( fname[0] ) )

    def gui_save_curr_mbr_to_db( self ):
        self.gui_fill_curr_mbr_with_line_edit()
        self.curr_mbr.save_to_db()

    def gui_update_curr_mbr_to_db( self ):
        self.gui_fill_curr_mbr_with_line_edit()
        self.curr_mbr.update_to_db()

    def gui_delete_curr_mbr( self ):
        self.curr_mbr.delete_item( int( self.edit_mbr_id.text() ) )

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
-----------------------------------------------------------'''
