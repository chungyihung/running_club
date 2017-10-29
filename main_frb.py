#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import frb_member as frb
import competition as cmpt
import frb_competition as frb_cmpt
import etu as myetu
import ui_util as ui_utl
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

MEMBER_TBLVU_HEADER = [
    "編號", "職稱", "姓名", "身分證",  "出生年月日", "地區",
    "手機", "電話1", "電話2", "地址", "T-Shirt尺寸", "風衣尺寸" ]

'''-----------------------------------------------------------
Tab competition menu enum
-----------------------------------------------------------'''
TAB_CMPT_MENU_SETUP     = 0
TAB_CMPT_MENU_WRKR_TBL  = 1
TAB_CMPT_MENU_STATISTIC = 2

CMPT_WRKR_TBLVU_HEADER = [
    "編號", "姓名", "電話",  "身分證", "葷素",
    "主任務", "次任務1", "次任務2", "T-Shirt尺寸", "風衣尺寸", "會員ID"  ]

'''-----------------------------------------------------------
Competition Worker Table Constant
-----------------------------------------------------------'''
N_COL_WRKRTBL_JOB_GRP = 6

class MainApp( QtWidgets.QMainWindow, UI_MainWindow ):
    def __init__( self ):
        QtWidgets.QMainWindow.__init__( self )
        UI_MainWindow.__init__( self )
        self.setupUi( self )

        self.frb = frb.frb_member()
        self.frbc = frb_cmpt.frb_competition()

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
        self.actionExport_to_excel.triggered.connect( self.frb.cnvt_db_to_excel )
        self.actionImport_from_excel.triggered.connect( self.frb.cnvt_excel_to_db )

        # Button widget action
        self.btn_mbr_info_img_file_diag.clicked.connect( self.gui_get_mbr_file_path )
        self.btn_mbr_info_create.clicked.connect( self.gui_save_curr_mbr_to_db )
        self.btn_mbr_info_update.clicked.connect( self.gui_update_curr_mbr_to_db )
        self.btn_mbr_info_delete.clicked.connect( self.gui_delete_curr_mbr )

        self.tab_member_menu.currentChanged.connect( self.gui_tab_member_menu_change_hndl )

        self.btn_mbr_tbl_save_to_excel.clicked.connect( self.btn_mbr_tbl_save_to_excel_clicked )

        #Combo widget init
        self.gui_cmbo_cloth_sz_init( self.cmbo_mbr_tshirt_sz, frb_cmpt.THIRT_SZ )
        self.gui_cmbo_cloth_sz_init( self.cmbo_mbr_coat_sz, frb_cmpt.COAT_SZ )

        ''' ---------------------------------------------
        Tab of Competition Init
        ----------------------------------------------'''
        self.tab_competition_menu.currentChanged.connect( self.gui_tab_cmpt_menu_change_hndl )
        self.btn_cmpt_create.clicked.connect( self.gui_create_competition )
        self.btn_cmpt_update.clicked.connect( self.gui_update_competition )

        self.gui_cmbo_selc_competition_init()
        self.gui_cmbo_wrktbl_mode_init( frb_cmpt.WRKTBL_MODE_NAME )

        self.btn_cmpt_tbl_save_to_excel.clicked.connect( self.btn_cmpt_tbl_save_to_excel_clicked )

    def gui_tab_cmpt_menu_change_hndl( self, curr_idx ):
        if( TAB_CMPT_MENU_WRKR_TBL == curr_idx ):
            ''' ---------------------------------------------
            Table is filled only when TAB_CMPT_MENU_WRKR_TBL is selected
            ----------------------------------------------'''
            self.gui_fill_worker_data_table()

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
        mbrdata = self.frb.get_all_member()

        self.mbrTable.setColumnCount( len( MEMBER_TBLVU_HEADER ) )
        self.mbrTable.setHorizontalHeaderLabels(MEMBER_TBLVU_HEADER)
        self.mbrTable.verticalHeader().setVisible(False)

        indx = 0

        ''' ---------------------------------------------
        mbrdata is a list. each row represent member as
        in dict type.
        ----------------------------------------------'''
        for mem in mbrdata:
            if mem != None:
                birthstr = "{}.{}.{}".format( mem[frb.BirthY], mem[frb.BirthM], mem[frb.BirthD] )

                mbr_thsirt_sz = frb_cmpt.THIRT_SZ[ mem["tshirt_sz"] ]
                mbr_coat_sz   = frb_cmpt.COAT_SZ[ mem["coat_sz"] ]

                self.mbrTable.insertRow( indx )
                self.mbrTable.setItem( indx, 0, QtWidgets.QTableWidgetItem( "{:04d}".format( mem[frb.MemberID] ) ) )  # index
                self.mbrTable.setItem( indx, 1, QtWidgets.QTableWidgetItem( mem[frb.Position] ) )               # position
                self.mbrTable.setItem( indx, 2, QtWidgets.QTableWidgetItem( mem[frb.Name] ) )                   # name
                self.mbrTable.setItem( indx, 3, QtWidgets.QTableWidgetItem( mem[frb.IDCard] ) )                 # idcard number
                self.mbrTable.setItem( indx, 4, QtWidgets.QTableWidgetItem( str( birthstr ) ) )               # Birthday
                self.mbrTable.setItem( indx, 5, QtWidgets.QTableWidgetItem( mem[frb.Area] ) )                   # area
                self.mbrTable.setItem( indx, 6, QtWidgets.QTableWidgetItem( mem[frb.CellPhone] ) )              # cell phone
                self.mbrTable.setItem( indx, 7, QtWidgets.QTableWidgetItem( mem[frb.Phone] ) )                  # phone
                self.mbrTable.setItem( indx, 8, QtWidgets.QTableWidgetItem( mem[frb.Phone2] ) )                 # phone2
                self.mbrTable.setItem( indx, 9, QtWidgets.QTableWidgetItem( mem[frb.Address] ) )                   # Address
                self.mbrTable.setItem( indx, 10, QtWidgets.QTableWidgetItem( mbr_thsirt_sz ) )                # TShirt sz
                self.mbrTable.setItem( indx, 11, QtWidgets.QTableWidgetItem( mbr_coat_sz ) )                  # coat sz
                indx = indx + 1

        for col in range( 0, len( MEMBER_TBLVU_HEADER ) ):
            self.mbrTable.horizontalHeader().setSectionResizeMode( col, QtWidgets.QHeaderView.ResizeToContents )

    def gui_remove_data_table( self ):
        rows = self.mbrTable.rowCount()
        for row in range( 0, rows ):
            self.mbrTable.removeRow( 0 )

    def btn_mbr_tbl_save_to_excel_clicked( self ):
        sheet_title = "會員名單"
        filepath =  sheet_title + ".xlsx"
        myetu.ETU_cmpt_tbl_save_to_excel( self.mbrTable, sheet_title, filepath )

    ''' ---------------------------------------------
    Edit member widgets procedures
    ----------------------------------------------'''
    def gui_mbr_read_from_db( self ):
        try:
            query_id = int(self.edit_mbr_id.text())
            memdata = self.frb.get_member( query_id )
            if memdata != None:
                self.gui_fill_widget_with_curr_mbr(memdata)
                self.gui_mbr_info_update_photo(memdata[frb.Photo])
            else:
                print("{} member not found".format(query_id))
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    def gui_fill_widget_with_curr_mbr( self, mem ):
        self.edit_mbr_address.setText(      "{}".format( mem[frb.Address])          )
        self.edit_mbr_area.setText(         "{}".format( mem[frb.Area])             )
        self.edit_mbr_birth_ROC.setText(    "{}".format( mem[frb.BirthY])           )
        self.edit_mbr_birthday.setText(     "{}.{}.{}".format( mem[frb.BirthY],
                                                               mem[frb.BirthM],
                                                               mem[frb.BirthD] )    )
        self.edit_mbr_cellphone.setText(    "{}".format( mem[frb.CellPhone])        )
        self.edit_mbr_idcard.setText(       "{}".format( mem[frb.IDCard])           )
        self.edit_mbr_name.setText(         "{}".format( mem[frb.Name])             )
        self.edit_mbr_phone1.setText(       "{}".format( mem[frb.Phone])            )
        self.edit_mbr_phone2.setText(       "{}".format( mem[frb.Phone2])           )
        self.edit_mbr_position.setText(     "{}".format( mem[frb.Position])         )
        self.edit_mbr_photo_path.setText(   "{}".format( mem[frb.Photo])            )
        self.cmbo_mbr_tshirt_sz.setCurrentIndex( int( mem[frb.TShirt_SZ]) )
        self.cmbo_mbr_coat_sz.setCurrentIndex( int( mem[frb.Coat_SZ]) )

    def gui_fill_curr_mbr( self ):
        birth_list = self.frb.birthday_str_to_list( self.edit_mbr_birthday.text() )
        init_member = self.frb.init_member()

        if birth_list == None:
            print( "Birth List value is Empty")
        elif len( birth_list ) != 3:
            print( "Len of Birth List is not eqult to 3 ({})".format( len( birth_list ) ) )
        else:
            try:
                init_member[frb.MemberID] = int( self.edit_mbr_id.text()      )
            except ValueError as err:
                print( "[Exception]: {}".format( err ) )

            init_member[frb.Position]       = str( self.edit_mbr_position.text()    )
            init_member[frb.Name]           = str( self.edit_mbr_name.text()        )
            init_member[frb.IDCard]         = str( self.edit_mbr_idcard.text()      )
            init_member[frb.BirthY]         = int( birth_list[0]                    )
            init_member[frb.BirthM]         = int( birth_list[1]                    )
            init_member[frb.BirthD]         = int( birth_list[2]                    )
            init_member[frb.Area]           = str( self.edit_mbr_area.text()        )
            init_member[frb.CellPhone]      = str( self.edit_mbr_cellphone.text()   )
            init_member[frb.Phone]          = str( self.edit_mbr_phone1.text()      )
            init_member[frb.Phone2]         = str( self.edit_mbr_phone2.text()      )
            init_member[frb.Address]        = str( self.edit_mbr_address.text()     )
            init_member[frb.Photo]          = str( self.edit_mbr_photo_path.text()  )
            init_member[frb.TShirt_SZ]      = int( self.cmbo_mbr_tshirt_sz.currentIndex()   )
            init_member[frb.Coat_SZ]        = int( self.cmbo_mbr_coat_sz.currentIndex()     )

        return init_member

    def gui_mbr_info_update_photo( self, impath = frb.DEFAULT_PHOTO ):
        self.gui_qpixmap = QtGui.QPixmap( impath )
        if self.gui_qpixmap.isNull():
            self.gui_qpixmap = QtGui.QPixmap( frb.DEFAULT_PHOTO )
            print( "Photo Path is invalid, showing with default photo" )

        lblsize = self.lbl_mbr_photo.size()
        self.lbl_mbr_photo.setPixmap( self.gui_qpixmap.scaled( lblsize, QtCore.Qt.KeepAspectRatio ) )

    def gui_get_mbr_file_path( self ):
        fname = QtWidgets.QFileDialog.getOpenFileName( self, '選擇一張照片', "./Resource", "Image Files (*.png *.jpg *.bmp)" )
        if fname[0]:
            import os
            self.edit_mbr_photo_path.setText( os.path.relpath( fname[0] ) )

    def gui_save_curr_mbr_to_db( self ):
        member =  self.gui_fill_curr_mbr()
        self.frb.set_member( member, member[frb.MemberID])
        self.edit_mbr_id.setText( str( member[frb.MemberID]) )

    def gui_update_curr_mbr_to_db( self ):
        member =  self.gui_fill_curr_mbr()
        self.frb.upt_member( member, member[frb.MemberID])

    def gui_delete_curr_mbr( self ):
        retval = ui_utl.popup_msg_box("刪除會員",
                                      "確定要刪除會員 {} 嗎?".format(self.edit_mbr_id.text()),
                                      ui_utl.PU_MSG_YESNO )

        if retval == QtWidgets.QMessageBox.Yes:
            self.frb.del_member( int( self.edit_mbr_id.text() ) )

    ''' ---------------------------------------------
    Competition Tab Widgets action callback
    ----------------------------------------------'''
    def gui_cmbo_cmpt_meal_init( self ):
        self.cmbo_cmpt_worker_vegetarian.clear()
        self.cmbo_cmpt_worker_vegetarian.addItems( frb_cmpt.VEGETARIAN )

    def gui_cmbo_cmpt_job_init( self, cmbo_job_obj, items ):
        cmbo_job_obj.clear()
        cmbo_job_obj.addItem( "請選擇工作" )
        cmbo_job_obj.addItems( items )

    def gui_cmbo_cloth_sz_init( self, cmbo_sz_obj, items ):
        cmbo_sz_obj.clear()
        cmbo_sz_obj.addItem( "請選擇尺寸" )
        cmbo_sz_obj.addItems( items[1:] )
        dflt_idx = items.index( frb_cmpt.DEFAULT_SZ )
        cmbo_sz_obj.setCurrentIndex( dflt_idx )

    def gui_cmbo_wrktbl_mode_init( self, items ):
        self.cmbo_wrktbl_mode.clear()
        self.cmbo_wrktbl_mode.addItems( items )
        self.cmbo_wrktbl_mode.setCurrentIndex( frb_cmpt.WRKTBL_MODE.NORMAL  )

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

        cmptlist = self.frbc.get_all_competition()
        for name, details in cmptlist.items():
            self.cmbo_selc_competition.addItem( name )

        self.cmbo_selc_competition.currentIndexChanged.connect(
            self.gui_cmbo_selc_competition_chng
            )

        self.cmbo_wrktbl_mode.currentIndexChanged.connect(self.gui_cmbo_wrktbl_mode_chng)

    def gui_cmbo_selc_competition_chng( self, i ):
        ''' ---------------------------------------------
        Note that we should restrict file encoding as utf8
        ----------------------------------------------'''
        cmpt_slct = self.cmbo_selc_competition.currentText()
        print("[cmbo_selc_cmpt]: select {} ( {} )".format( i, cmpt_slct ) )
        if i != 0:
            ''' ---------------------------------------------
            Fill up the competition info
            ----------------------------------------------'''
            cmptinfo = self.frbc.get_competition(cmpt_slct)
            self.edit_cmpt_name.setText( "{}".format( cmptinfo['name']))
            self.edit_cmpt_location.setText( "{}".format( cmptinfo['location']))
            self.edit_cmpt_date.setText( "{}".format( cmptinfo['date']))

            ''' ---------------------------------------------
            joblist is dictionary type
            ----------------------------------------------'''
            joblist = self.frbc.get_jb_list()
            jobname_ls = [name for name, label in joblist.items()]
            self.gui_cmbo_cmpt_job_init_proc( jobname_ls )

            ''' ---------------------------------------------
            Update each component by reconnecting button of job create/delete
            ----------------------------------------------'''
            self.gui_cmpt_widget_try_disconnect(self.btn_cmpt_job_create.clicked)
            self.gui_cmpt_widget_try_disconnect(self.btn_cmpt_job_delete.clicked)
            self.gui_cmpt_widget_try_disconnect(self.btn_cmpt_job_update.clicked)
            self.gui_cmpt_widget_try_disconnect(self.btn_worker_info_create.clicked)
            self.gui_cmpt_widget_try_disconnect(self.edit_cmpt_worker_mem_id.returnPressed)
            self.gui_cmpt_widget_try_disconnect(self.edit_cmpt_worker_id.editingFinished)

            self.btn_cmpt_job_create.clicked.connect( self.gui_cmpt_job_create_proc )
            self.btn_cmpt_job_delete.clicked.connect( self.gui_cmpt_job_delete_proc )
            self.btn_cmpt_job_update.clicked.connect( self.gui_cmpt_job_update_proc )

            self.gui_cmbo_cloth_sz_init( self.cmbo_cmpt_worker_tshirt_sz, frb_cmpt.THIRT_SZ )
            self.gui_cmbo_cloth_sz_init( self.cmbo_cmpt_worker_coat_sz, frb_cmpt.COAT_SZ )
            self.gui_cmbo_cmpt_meal_init()

            self.btn_worker_info_create.clicked.connect( self.gui_save_curr_cmpt_worker_to_db )
            self.btn_worker_info_update.clicked.connect( self.gui_update_curr_cmpt_worker_to_db )
            self.btn_worker_info_delete.clicked.connect( self.gui_delete_curr_cmpt_worker_to_db )

            self.edit_cmpt_worker_mem_id.returnPressed.connect( self.gui_wrkr_read_from_mem_db )
            self.edit_cmpt_worker_id.returnPressed.connect( self.gui_wrkr_read_from_cmpt_db )

    def gui_cmpt_widget_try_disconnect( self, widget_signal ):
        try:
            widget_signal.disconnect()
        except TypeError as err:
            print( "[cmpt widget] Failed to disconnect ({})".format(err) )

    def gui_cmbo_wrktbl_mode_chng( self ):
        if frb_cmpt.WRKTBL_MODE.NORMAL == self.cmbo_wrktbl_mode.currentIndex():
            self.gui_remove_worker_data_table()
            self.gui_update_worker_data_table()
        elif frb_cmpt.WRKTBL_MODE.JOBGROUP == self.cmbo_wrktbl_mode.currentIndex():
            print("List worker table in job group")
            self.gui_remove_worker_data_table()
            self.gui_update_wrktbl_job_grp_mode()


    ''' ---------------------------------------------
    gui_cmbo_cmpt_job_init_proc
      * Initial all objects related to job.
      * job_name_list - array of each name
    ----------------------------------------------'''
    def gui_cmbo_cmpt_job_init_proc( self, job_name_list ):
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_job_list, job_name_list )
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_worker_primary_job, job_name_list )
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_worker_sec_job_1, job_name_list )
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_worker_sec_job_2, job_name_list )

    ''' ---------------------------------------------
    gui_create_competition
      - create new competition
    ----------------------------------------------'''
    def gui_create_competition( self ):
        cmpt_data = {}
        has_created = False
        cmpt_data["name"] = str( self.edit_cmpt_name.text() )
        cmpt_data["location"] = str( self.edit_cmpt_location.text() )
        cmpt_data["date"] = str( self.edit_cmpt_date.text() )

        ''' ---------------------------------------------
        Folder name = [date]_[name]
        ----------------------------------------------'''
        new_cmpt = cmpt_data["date"] + "_" + cmpt_data["name"]
        cmptlist = self.frbc.get_all_competition()

        ''' ---------------------------------------------
        Sanity check if the competition folder has been created
        ----------------------------------------------'''
        for name, details in cmptlist.items():
            print("{} {}".format(name, new_cmpt))
            if name == new_cmpt:
                ui_utl.popup_msg_box("賽事建立", "{} 已經建立過囉!".format(new_cmpt), ui_utl.PU_MSG_INFO )
                has_created = True

        if has_created == False:
            try:
                self.frbc.set_competition( cmpt_data )
                ui_utl.popup_msg_box("賽事建立", "{} 完成建立!".format(new_cmpt), ui_utl.PU_MSG_INFO )
                self.gui_cmbo_selc_competition_init()
            except:
                print("Failed to create competition")

    ''' ---------------------------------------------
    gui_update_competition
      - update competition content
    TODO: Add mechanism to allow user update the name and date
          by renaming all job list and worker dict.
    ----------------------------------------------'''
    def gui_update_competition( self ):
        ''' ---------------------------------------------
        Target name is the selected competition combo content
        ----------------------------------------------'''
        cmpt_slct = self.cmbo_selc_competition.currentText()

        cmpt_data = {}
        tmpstr = cmpt_slct.split( "-" )
        cmpt_data["name"] = tmpstr[0]
        cmpt_data["location"] = str( self.edit_cmpt_location.text() )
        cmpt_data["date"] = tmpstr[1]
        self.frbc.upt_competition( cmpt_data )

    ''' ---------------------------------------------
    gui_cmpt_job_create_proc
      - add new job item into job list
      - joblabel == 0: Unlabel object
      - job label start from 1
      - everytime add job, search the minimum unused number in job labe list
    ----------------------------------------------'''
    def gui_cmpt_job_create_proc( self ):
        text, ok = QtWidgets.QInputDialog.getText(self, '新建工作項目', '輸入工作名稱:')
        if ok:
            jbname, jblabel = self.frbc.get_jb_list( separate=True )
            ''' ---------------------------------------------
            Find the minimum unused label
            ----------------------------------------------'''
            jblbl_srt = sorted( jblabel )
            new_jb_lbl = 1
            for n in jblbl_srt:
                if n != new_jb_lbl:
                    break
                else:
                    new_jb_lbl = new_jb_lbl + 1

            ''' ---------------------------------------------
            Sanity check if target job is already in job list
            ----------------------------------------------'''
            if text not in jbname:
                ''' ---------------------------------------------
                Currently we only store label in job list dict
                ----------------------------------------------'''
                self.frbc.add_jb( text, new_jb_lbl )
                jbname.append(text)
                self.gui_cmbo_cmpt_job_init_proc( sorted(jbname) )
            else:
                print("{} has already exist".format(text))
                ui_utl.popup_msg_box("工作建立", "{} 已經建立過了!".format( text ), ui_utl.PU_MSG_INFO )


    ''' ---------------------------------------------
    gui_cmpt_job_delete_proc
    ----------------------------------------------'''
    def gui_cmpt_job_delete_proc( self ):
        if self.cmbo_cmpt_job_list.currentIndex() > 0:
            retval = ui_utl.popup_msg_box("工作設定",
                                          "確定要刪除 {} 嗎?".format( self.cmbo_cmpt_job_list.currentText() ),
                                          ui_utl.PU_MSG_YESNO )
            if retval == QtWidgets.QMessageBox.Yes:
                self.frbc.delete_jb( self.cmbo_cmpt_job_list.currentText() )
                jbname, jblabel = self.frbc.get_jb_list( separate=True )
                self.gui_cmbo_cmpt_job_init_proc( jbname )

    ''' ---------------------------------------------
    gui_cmpt_job_update_proc
    ----------------------------------------------'''
    def gui_cmpt_job_update_proc( self ):
        if self.cmbo_cmpt_job_list.currentIndex() > 0:
            text, ok = QtWidgets.QInputDialog.getText(self, '更新工作項目', '輸入工作名稱:')
            if ok:
                jbname, jblabel = self.frbc.get_jb_list( separate=True )
                job_index = self.cmbo_cmpt_job_list.currentIndex() - 1
                self.frbc.rename_jb( jbname[job_index], text )
                jbname[job_index] = text
                self.gui_cmbo_cmpt_job_init_proc( sorted(jbname) )

    ''' ---------------------------------------------
    gui_save_curr_cmpt_worker_to_db
      - Save worker information into db according to current component contents.
    ----------------------------------------------'''
    def gui_save_curr_cmpt_worker_to_db( self ):
        pri_jb_cb_idx = self.cmbo_cmpt_worker_primary_job.currentIndex()
        sec1_jb_cb_idx = self.cmbo_cmpt_worker_sec_job_1.currentIndex()
        sec2_jb_cb_idx = self.cmbo_cmpt_worker_sec_job_2.currentIndex()

        jbdict = self.frbc.get_jb_list()
        pri_jb_lbl = jbdict[self.cmbo_cmpt_worker_primary_job.currentText()] if pri_jb_cb_idx > 0 else 0
        sec1_jb_lbl = jbdict[self.cmbo_cmpt_worker_sec_job_1.currentText()] if sec1_jb_cb_idx > 0 else 0
        sec2_jb_lbl = jbdict[self.cmbo_cmpt_worker_sec_job_2.currentText()] if sec2_jb_cb_idx > 0 else 0
        print("pri_jb_lbl = {}".format(pri_jb_lbl))

        worker = self.frbc.init_worker()

        ''' ---------------------------------------------
        If the worker is also a valid club member, record it.
        ----------------------------------------------'''
        try:
            mem_id = int(self.edit_cmpt_worker_mem_id.text())
        except ValueError as err:
            print( "[Exception]: {}".format( err ) )
            mem_id = 0

        worker[frb_cmpt.Name]      = str( self.edit_cmpt_worker_name.text() )
        worker[frb_cmpt.Phone]     = str( self.edit_cmpt_worker_phone.text() )
        worker[frb_cmpt.IDCard]    = str( self.edit_cmpt_worker_idcard.text() )
        worker[frb_cmpt.Vegetarian]= int( self.cmbo_cmpt_worker_vegetarian.currentIndex() )
        worker[frb_cmpt.Primary_JB]= pri_jb_lbl
        worker[frb_cmpt.SEC_JB1]   = sec1_jb_lbl
        worker[frb_cmpt.SEC_JB2]   = sec2_jb_lbl
        worker[frb_cmpt.TShirt_SZ] = int( self.cmbo_cmpt_worker_tshirt_sz.currentIndex() )
        worker[frb_cmpt.Coat_SZ]   = int( self.cmbo_cmpt_worker_coat_sz.currentIndex() )
        worker[frb_cmpt.MemberID]  = mem_id

        self.frbc.add_worker( worker )

        ui_utl.popup_msg_box("新增工作人員",
                            "{} 新增完成!".format( str(self.edit_cmpt_worker_name.text() ) ),
                            ui_utl.PU_MSG_INFO )

    def gui_update_curr_cmpt_worker_to_db( self ):
        pri_jb_cb_idx = self.cmbo_cmpt_worker_primary_job.currentIndex()
        sec1_jb_cb_idx = self.cmbo_cmpt_worker_sec_job_1.currentIndex()
        sec2_jb_cb_idx = self.cmbo_cmpt_worker_sec_job_2.currentIndex()

        jbdict = self.frbc.get_jb_list()
        pri_jb_lbl = jbdict[self.cmbo_cmpt_worker_primary_job.currentText()] if pri_jb_cb_idx > 0 else 0
        sec1_jb_lbl = jbdict[self.cmbo_cmpt_worker_sec_job_1.currentText()] if sec1_jb_cb_idx > 0 else 0
        sec2_jb_lbl = jbdict[self.cmbo_cmpt_worker_sec_job_2.currentText()] if sec2_jb_cb_idx > 0 else 0

        try:
            mem_id = int(self.edit_cmpt_worker_mem_id.text())
        except ValueError as err:
            print( "[Exception]: {}".format( err ) )
            mem_id = 0

        try:
            wrkr_id = int( self.edit_cmpt_worker_id.text() )
        except ValueError as err:
            print( "[Exception]: {}".format( err ) )
            wrkr_id = 0

        if wrkr_id != 0:
            worker = self.frbc.init_worker()
            worker[frb_cmpt.WorkerID]  = wrkr_id
            worker[frb_cmpt.Name]      = str( self.edit_cmpt_worker_name.text() )
            worker[frb_cmpt.Phone]     = str( self.edit_cmpt_worker_phone.text() )
            worker[frb_cmpt.IDCard]    = str( self.edit_cmpt_worker_idcard.text() )
            worker[frb_cmpt.Vegetarian]= int( self.cmbo_cmpt_worker_vegetarian.currentIndex() )
            worker[frb_cmpt.Primary_JB]= pri_jb_lbl
            worker[frb_cmpt.SEC_JB1]   = sec1_jb_lbl
            worker[frb_cmpt.SEC_JB2]   = sec2_jb_lbl
            worker[frb_cmpt.TShirt_SZ] = int( self.cmbo_cmpt_worker_tshirt_sz.currentIndex() )
            worker[frb_cmpt.Coat_SZ]   = int( self.cmbo_cmpt_worker_coat_sz.currentIndex() )
            worker[frb_cmpt.MemberID]  = mem_id

            self.frbc.update_worker( wrkr_id, worker )

    def gui_delete_curr_cmpt_worker_to_db( self ):
        retval = ui_utl.popup_msg_box("刪除工作人員",
                                      "確定要刪除工作人員 {} 嗎?".format( self.edit_cmpt_worker_id.text() ),
                                      ui_utl.PU_MSG_YESNO )

        if retval == QtWidgets.QMessageBox.Yes:
            self.frbc.rm_worker( int( self.edit_cmpt_worker_id.text() ) )

    def gui_wrkr_read_from_mem_db( self ):
        try:
            query_id = int(self.edit_cmpt_worker_mem_id.text())
            member = self.frb.get_member(query_id)
            self.gui_fill_cmpt_widget_with_curr_mbr(member)
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    def gui_fill_cmpt_widget_with_curr_mbr( self, member ):
        self.edit_cmpt_worker_name.setText(member[frb.Name] )
        self.edit_cmpt_worker_phone.setText(member[frb.CellPhone])
        self.edit_cmpt_worker_idcard.setText(member[frb.IDCard])

        self.cmbo_cmpt_worker_tshirt_sz.setCurrentIndex( int(member[frb.TShirt_SZ]) )
        self.cmbo_cmpt_worker_coat_sz.setCurrentIndex( int(member[frb.Coat_SZ]) )

    ''' ---------------------------------------------
    Call after worker ID finished added
    ----------------------------------------------'''
    def gui_wrkr_read_from_cmpt_db( self ):
        self.gui_fill_cmpt_widget_with_curr_cmpt_wrkr()

    def gui_fill_cmpt_widget_with_curr_cmpt_wrkr( self ):
        try:
            query_id = int(self.edit_cmpt_worker_id.text())
            wrkr_info = self.frbc.get_worker( query_id )
            print(wrkr_info)
            if wrkr_info != None:
                self.edit_cmpt_worker_name.setText( wrkr_info[frb_cmpt.Name] )
                self.edit_cmpt_worker_phone.setText( wrkr_info[frb_cmpt.Phone] )
                self.edit_cmpt_worker_idcard.setText( wrkr_info[frb_cmpt.IDCard] )

                self.cmbo_cmpt_worker_vegetarian.setCurrentIndex( int(wrkr_info[frb_cmpt.Vegetarian]) )
                self.cmbo_cmpt_worker_primary_job.setCurrentIndex( int(wrkr_info[frb_cmpt.Primary_JB]) )
                self.cmbo_cmpt_worker_sec_job_1.setCurrentIndex( int(wrkr_info[frb_cmpt.SEC_JB1]) )
                self.cmbo_cmpt_worker_sec_job_2.setCurrentIndex( int(wrkr_info[frb_cmpt.SEC_JB2]) )
                self.cmbo_cmpt_worker_tshirt_sz.setCurrentIndex( int(wrkr_info[frb_cmpt.TShirt_SZ]) )
                self.cmbo_cmpt_worker_coat_sz.setCurrentIndex( int(wrkr_info[frb_cmpt.Coat_SZ]) )

                self.edit_cmpt_worker_mem_id.setText( str(wrkr_info[frb_cmpt.MemberID]) if wrkr_info[frb_cmpt.MemberID] > 0 else "" )

        except ValueError as err:
            print("[Exception]: {}".format( err ))

    ''' ---------------------------------------------
    Competition Worker Table procedure
    These procedures will be integrated with member table later.
    ----------------------------------------------'''
    def gui_fill_worker_data_table( self ):
        if cmpt.WRKTBL_MODE.NORMAL == self.cmbo_wrktbl_mode.currentIndex():
            self.gui_remove_worker_data_table()
            self.gui_update_worker_data_table()
        elif cmpt.WRKTBL_MODE.JOBGROUP == self.cmbo_wrktbl_mode.currentIndex():
            print("List worker table in job group")
            self.gui_remove_worker_data_table()
            self.gui_update_wrktbl_job_grp_mode()

    def gui_update_worker_data_table( self ):
        if self.frbc.curr_cmpt_hndl != "":
            ''' ---------------------------------------------
            Get all worker in database and jobs from Firebase
            ----------------------------------------------'''
            cmpt_wrkr_data = self.frbc.get_all_worker()
            jobname_ls, joblabel_ls = self.frbc.get_jb_list( separate = True)

            ''' ---------------------------------------------
            Initialize Table
            ----------------------------------------------'''
            self.cmptWorkerTbl.setColumnCount( len( CMPT_WRKR_TBLVU_HEADER ) )
            self.cmptWorkerTbl.setHorizontalHeaderLabels(CMPT_WRKR_TBLVU_HEADER)
            self.cmptWorkerTbl.verticalHeader().setVisible(False)

            ''' ---------------------------------------------
            Loop all data in Competition Database
            Note that cmpt_wrkr_data is in dict type from Firebase
            ----------------------------------------------'''
            indx = 0
            for wrkr_id, worker in cmpt_wrkr_data.items():
                self.cmptWorkerTbl.insertRow( indx )

                ''' ---------------------------------------------
                Mapping "job label in db" to "job index in json"
                for getting corresponding job name
                ----------------------------------------------'''
                try:
                    primary_jb_label = joblabel_ls.index( int(worker[frb_cmpt.Primary_JB]) )
                    pri_jb_name = jobname_ls[primary_jb_label]
                except ValueError as err:
                    pri_jb_name = ""
                    print("[CMPT_TABLE]{}".format(err))

                try:
                    sec_jb1_label = joblabel_ls.index( int(worker[frb_cmpt.SEC_JB1]) )
                    sec_jb1_name  = jobname_ls[sec_jb1_label]
                except ValueError as err:
                    sec_jb1_name = ""
                    print("[CMPT_TABLE]{}".format(err))

                try:
                    sec_jb2_label = joblabel_ls.index( int(worker[frb_cmpt.SEC_JB2]) )
                    sec_jb2_name  = jobname_ls[sec_jb2_label]
                except ValueError as err:
                    sec_jb2_name = ""
                    print("[CMPT_TABLE]{}".format(err))

                wrkr_mem_id_str = str( worker[frb_cmpt.MemberID] ) if worker[frb_cmpt.MemberID] != 0 else "None"

                self.cmptWorkerTbl.setItem( indx, 0, QtWidgets.QTableWidgetItem( str( worker[frb_cmpt.WorkerID] ) ) )                   # id
                self.cmptWorkerTbl.setItem( indx, 1, QtWidgets.QTableWidgetItem( worker[frb_cmpt.Name] ) )                              # name
                self.cmptWorkerTbl.setItem( indx, 2, QtWidgets.QTableWidgetItem( worker[frb_cmpt.Phone] ) )                             # phone
                self.cmptWorkerTbl.setItem( indx, 3, QtWidgets.QTableWidgetItem( worker[frb_cmpt.IDCard] ) )                            # idcard
                self.cmptWorkerTbl.setItem( indx, 4, QtWidgets.QTableWidgetItem( frb_cmpt.VEGETARIAN[worker[frb_cmpt.Vegetarian]] ) )   # vegetarian
                self.cmptWorkerTbl.setItem( indx, 5, QtWidgets.QTableWidgetItem( pri_jb_name ) )                                        # primary job
                self.cmptWorkerTbl.setItem( indx, 6, QtWidgets.QTableWidgetItem( sec_jb1_name ) )                                       # secoundary job 1
                self.cmptWorkerTbl.setItem( indx, 7, QtWidgets.QTableWidgetItem( sec_jb2_name ) )                                       # secoundary job 2
                self.cmptWorkerTbl.setItem( indx, 8, QtWidgets.QTableWidgetItem( frb_cmpt.THIRT_SZ[worker[frb_cmpt.TShirt_SZ]] ) )      # t-shirt sz
                self.cmptWorkerTbl.setItem( indx, 9, QtWidgets.QTableWidgetItem( frb_cmpt.COAT_SZ[worker[frb_cmpt.Coat_SZ]] ) )         # coat sz
                self.cmptWorkerTbl.setItem( indx, 10, QtWidgets.QTableWidgetItem( wrkr_mem_id_str ) )           # mem id
                indx = indx + 1

            for col in range( 0, len( CMPT_WRKR_TBLVU_HEADER ) ):
                self.cmptWorkerTbl.horizontalHeader().setSectionResizeMode( col, QtWidgets.QHeaderView.ResizeToContents )

    def gui_update_wrktbl_job_grp_mode( self ):
        if self.frbc.curr_cmpt_hndl != "":
            ''' ---------------------------------------------
            Set up header
            ----------------------------------------------'''
            HeaderLabel = [ "任務"] + [str(num) for num in range(1, N_COL_WRKRTBL_JOB_GRP + 1) ]
            self.cmptWorkerTbl.setColumnCount( len( HeaderLabel ) )
            self.cmptWorkerTbl.setHorizontalHeaderLabels(HeaderLabel)
            self.cmptWorkerTbl.verticalHeader().setVisible(False)

            ''' ---------------------------------------------
            Get all job name to worker list in dict type
            ----------------------------------------------'''
            jb_wrk_ls = self.frbc.get_jb_to_name_list()

            ''' ---------------------------------------------
            Get worker whose job is the selected job in loop
            ----------------------------------------------'''
            tblRow = -1
            for jobname, worker_ls in jb_wrk_ls.items():
                tblRow = tblRow + 1
                self.cmptWorkerTbl.insertRow( tblRow )
                self.cmptWorkerTbl.setItem( tblRow, 0, QtWidgets.QTableWidgetItem( str(jobname) ) )
                tblCol = 1
                print(worker_ls[:])
                for worker in worker_ls:
                    self.cmptWorkerTbl.setItem( tblRow, tblCol, QtWidgets.QTableWidgetItem( worker ) )
                    tblCol = tblCol + 1
                    if tblCol % N_COL_WRKRTBL_JOB_GRP == 1:
                        tblCol = 1
                        tblRow = tblRow + 1
                        self.cmptWorkerTbl.insertRow( tblRow )
        else:
            print("competition must be selected first.")

    def gui_remove_worker_data_table( self ):
        rows = self.cmptWorkerTbl.rowCount()
        for row in range( 0, rows ):
            self.cmptWorkerTbl.removeRow( 0 )

    def btn_cmpt_tbl_save_to_excel_clicked( self ):
        sheet_title = str( self.cmbo_wrktbl_mode.currentText() )
        filepath = self.frbc.curr_cmpt_hndl+ "_" + sheet_title + ".xlsx"
        myetu.ETU_cmpt_tbl_save_to_excel( self.cmptWorkerTbl, sheet_title, filepath )

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
7. QInputDialog tutorial: https://www.tutorialspoint.com/pyqt/pyqt_qinputdialog_widget.htm
8. Handle filename with UTF8 encoding: https://docs.python.org/3/howto/unicode.html
-----------------------------------------------------------'''
