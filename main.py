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
TAB_CMPT_MENU_WRKR_TBL  = 1
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

        self.tab_member_menu.currentChanged.connect( self.gui_tab_member_menu_change_hndl )

        #Combo widget init
        self.gui_cmbo_cloth_sz_init( self.cmbo_mbr_tshirt_sz, cmpt.THIRT_SZ )
        self.gui_cmbo_cloth_sz_init( self.cmbo_mbr_coat_sz, cmpt.COAT_SZ )

        ''' ---------------------------------------------
        Tab of Competition Init
        ----------------------------------------------'''
        self.tab_competition_menu.currentChanged.connect( self.gui_tab_cmpt_menu_change_hndl )
        self.btn_cmpt_create.clicked.connect( self.gui_create_competition )

        self.gui_cmbo_selc_competition_init()

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
        mbrdata = self.curr_mbr.retrieve_all_data()

        HeaderLabel = [
            "編號", "職稱", "姓名", "身分證",  "出生年月日", "地區",
            "手機", "電話1", "電話2", "地址", "T-Shirt尺寸", "風衣尺寸" ]
        self.mbrTable.setColumnCount( len( HeaderLabel ) )
        self.mbrTable.setHorizontalHeaderLabels(HeaderLabel)
        self.mbrTable.verticalHeader().setVisible(False)

        for row in mbrdata:
            indx = mbrdata.index( row )
            birthstr = "{}.{}.{}".format( row[mbr.DBItem.DB_birthday_Y.value],
                                          row[mbr.DBItem.DB_birthday_M.value],
                                          row[mbr.DBItem.DB_birthday_D.value] )

            mbr_thsirt_sz = cmpt.THIRT_SZ[ row[mbr.DBItem.DB_tshirt_sz.value] ]
            mbr_coat_sz   = cmpt.COAT_SZ[ row[mbr.DBItem.DB_coat_sz.value] ]

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
            self.mbrTable.setItem( indx, 10, QtWidgets.QTableWidgetItem( mbr_thsirt_sz ) )                      # TShirt sz
            self.mbrTable.setItem( indx, 11, QtWidgets.QTableWidgetItem( mbr_coat_sz ) )                        # coat sz

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
            self.gui_fill_widget_with_curr_mbr()
            self.gui_mbr_info_update_photo()
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    def gui_fill_widget_with_curr_mbr( self ):
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
        self.cmbo_mbr_tshirt_sz.setCurrentIndex( int( self.curr_mbr.tshirt_sz ) )
        self.cmbo_mbr_coat_sz.setCurrentIndex( int( self.curr_mbr.coat_sz ) )

    def gui_fill_curr_mbr( self ):
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
            self.curr_mbr.tshirt_sz     = int( self.cmbo_mbr_tshirt_sz.currentIndex()   )
            self.curr_mbr.coat_sz       = int( self.cmbo_mbr_coat_sz.currentIndex()     )
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
        if True == self.gui_fill_curr_mbr():
            self.curr_mbr.save_to_db()
            self.edit_mbr_id.setText( str( self.curr_mbr.mem_id ) )

    def gui_update_curr_mbr_to_db( self ):
        if True == self.gui_fill_curr_mbr():
            self.curr_mbr.update_to_db()

    def gui_delete_curr_mbr( self ):
        self.curr_mbr.delete_item( int( self.edit_mbr_id.text() ) )

    ''' ---------------------------------------------
    Competition Tab Widgets action callback
    ----------------------------------------------'''
    def gui_cmbo_cmpt_meal_init( self ):
        self.cmbo_cmpt_worker_vegetarian.clear()
        self.cmbo_cmpt_worker_vegetarian.addItems( cmpt.VEGETARIAN )

    def gui_cmbo_cmpt_job_init( self, cmbo_job_obj, items ):
        cmbo_job_obj.clear()
        cmbo_job_obj.addItem( "請選擇工作" )
        cmbo_job_obj.addItems( items )

    def gui_cmbo_cloth_sz_init( self, cmbo_sz_obj, items ):
        cmbo_sz_obj.clear()
        cmbo_sz_obj.addItem( "請選擇尺寸" )
        cmbo_sz_obj.addItems( items[1:] )
        dflt_idx = items.index( cmpt.DEFAULT_SZ )
        cmbo_sz_obj.setCurrentIndex( dflt_idx )

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
        print("[cmbo_selc_cmpt]: select {} ( {} )".format( i, self.cmbo_selc_competition.currentText() ) )
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
                joblist = cmpt_data['job']
                self.curr_cmpt.target_cmpt_set( self.cmbo_selc_competition.currentText() )

                jobname_ls = [name for name, label in joblist]

                self.gui_cmbo_cmpt_job_init_proc( jobname_ls )

                ''' ---------------------------------------------
                Reconnect Button of job create/delete
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

                self.gui_cmbo_cloth_sz_init( self.cmbo_cmpt_worker_tshirt_sz, cmpt.THIRT_SZ )
                self.gui_cmbo_cloth_sz_init( self.cmbo_cmpt_worker_coat_sz, cmpt.COAT_SZ )
                self.gui_cmbo_cmpt_meal_init()

                self.btn_worker_info_create.clicked.connect( self.gui_save_curr_cmpt_worker_to_db )
                #self.btn_mbr_info_update.clicked.connect( self.gui_update_curr_mbr_to_db )
                #self.btn_mbr_info_delete.clicked.connect( self.gui_delete_curr_mbr )

                self.edit_cmpt_worker_mem_id.returnPressed.connect( self.gui_wrkr_read_from_mem_db )
                self.edit_cmpt_worker_id.editingFinished.connect( self.gui_wrkr_read_from_cmpt_db )

    def gui_cmpt_widget_try_disconnect( self, widget_signal ):
        try:
            widget_signal.disconnect()
        except TypeError as err:
            print( "[cmpt widget] Failed to disconnect ({})".format(err) )

    def gui_cmbo_cmpt_job_init_proc( self, job_name_list ):
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_job_list, job_name_list )
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_worker_primary_job, job_name_list )
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_worker_sec_job_1, job_name_list )
        self.gui_cmbo_cmpt_job_init( self.cmbo_cmpt_worker_sec_job_2, job_name_list )

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
            data = { "name": cmpt_name, "location": cmpt_locl, "date": cmpt_date, "jobLabelCnt":0,"job": [] }

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

    def gui_cmpt_job_create_proc( self ):
        filepath = cmpt.CMPT_RSC_BASE_PATH + self.curr_cmpt.cmpt_hndl + "/cmpt.json"

        with open( filepath, "r+", encoding='utf-8' ) as cmpt_info:
            cmpt_data = json.load( cmpt_info )
            joblist = cmpt_data['job']
            jobLblCnt = cmpt_data['jobLabelCnt'] + 1

            text, ok = QtWidgets.QInputDialog.getText(self, '新建工作項目', '輸入工作名稱:')
            if ok:
                ''' ---------------------------------------------
                Sanity check if the same job has been created.
                ----------------------------------------------'''
                if ( len(joblist) > 0 and text not in joblist[:][0] ) or ( len(joblist) == 0 ):
                    ''' ---------------------------------------------
                    For convenience, the job list is sorted after each
                    create/update process
                    ----------------------------------------------'''
                    joblist.append([text, jobLblCnt])
                    joblist = sorted( joblist, key = lambda job:job[0] )
                    cmpt_data['job'] = joblist
                    cmpt_data['jobLabelCnt'] = jobLblCnt
                    cmpt_info.seek(0)
                    json.dump( cmpt_data, cmpt_info, ensure_ascii=False, indent=4, separators=(',', ': ') )
                    cmpt_info.truncate()

                    jobname_ls = [name for name, label in joblist]
                    self.gui_cmbo_cmpt_job_init_proc( jobname_ls )
                else:
                    print("{} has already exist".format(text))
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("新建工作")
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok )
                    msg.setText("{} 已經建立過了!".format( text ) )
                    retval = msg.exec_()

    def gui_cmpt_job_delete_proc( self ):
        if self.cmbo_cmpt_job_list.currentIndex() > 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("賽事設定")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No )
            msg.setText("確定要刪除 {} 嗎?".format( self.cmbo_cmpt_job_list.currentText() ) )

            retval = msg.exec_()

            if retval == QtWidgets.QMessageBox.Yes:
                filepath = cmpt.CMPT_RSC_BASE_PATH + self.curr_cmpt.cmpt_hndl + "/cmpt.json"

                with open( filepath, "r+", encoding='utf-8' ) as cmpt_info:
                    cmpt_data = json.load( cmpt_info )
                    joblist = cmpt_data['job']
                    del joblist[ self.cmbo_cmpt_job_list.currentIndex() - 1 ]
                    cmpt_data['job'] = joblist
                    cmpt_info.seek(0)
                    json.dump( cmpt_data, cmpt_info, ensure_ascii=False, indent=4, separators=(',', ': ') )
                    cmpt_info.truncate()

                    jobname_ls = [name for name, label in joblist]
                    self.gui_cmbo_cmpt_job_init_proc( jobname_ls )

    def gui_cmpt_job_update_proc( self ):
        if self.cmbo_cmpt_job_list.currentIndex() > 0:
            text, ok = QtWidgets.QInputDialog.getText(self, '更新工作項目', '輸入工作名稱:')
            if ok:
                filepath = cmpt.CMPT_RSC_BASE_PATH + self.curr_cmpt.cmpt_hndl + "/cmpt.json"
                with open( filepath, "r+", encoding='utf-8' ) as cmpt_info:
                    cmpt_data = json.load( cmpt_info )
                    joblist = cmpt_data['job']
                    job_index = self.cmbo_cmpt_job_list.currentIndex() - 1
                    joblist[ job_index ] = [ text, joblist[ job_index ][1] ]

                    ''' ---------------------------------------------
                    For convenience, the job list is sorted after each
                    create/update process
                    ----------------------------------------------'''
                    joblist = sorted( joblist, key = lambda job:job[0] )

                    cmpt_data['job'] = joblist
                    cmpt_info.seek(0)
                    json.dump( cmpt_data, cmpt_info, ensure_ascii=False, indent=4, separators=(',', ': ') )
                    cmpt_info.truncate()

                    jobname_ls = [name for name, label in joblist]
                    self.gui_cmbo_cmpt_job_init_proc( jobname_ls )

    def gui_save_curr_cmpt_worker_to_db( self ):
        filepath = cmpt.CMPT_RSC_BASE_PATH + self.curr_cmpt.cmpt_hndl + "/cmpt.json"

        pri_jb_cb_idx = self.cmbo_cmpt_worker_primary_job.currentIndex() - 1
        sec1_jb_cb_idx = self.cmbo_cmpt_worker_sec_job_1.currentIndex() - 1
        sec2_jb_cb_idx = self.cmbo_cmpt_worker_sec_job_2.currentIndex() - 1

        with open( filepath, "r", encoding='utf-8' ) as cmpt_info:
            cmpt_data = json.load( cmpt_info )
            joblist = cmpt_data['job']
            pri_jb_lbl = joblist[ pri_jb_cb_idx][1] if pri_jb_cb_idx >= 0 else 0
            sec1_jb_lbl = joblist[ sec1_jb_cb_idx ][1] if sec1_jb_cb_idx >= 0 else 0
            sec2_jb_lbl = joblist[ sec2_jb_cb_idx ][1] if sec2_jb_cb_idx >= 0 else 0

            #print(pri_jb_lbl)
            #print(sec1_jb_lbl)
            #print(sec1_jb_lbl)

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

        wrkr_info = [ wrkr_id,
                      str( self.edit_cmpt_worker_name.text() ),
                      str( self.edit_cmpt_worker_phone.text() ),
                      str( self.edit_cmpt_worker_idcard.text() ),
                      int( self.cmbo_cmpt_worker_vegetarian.currentIndex() ),
                      pri_jb_lbl,
                      sec1_jb_lbl,
                      sec2_jb_lbl,
                      int( self.cmbo_cmpt_worker_tshirt_sz.currentIndex() ),
                      int( self.cmbo_cmpt_worker_coat_sz.currentIndex() ),
                      mem_id
                    ]
        self.curr_cmpt.worker_info_update(wrkr_info)
        self.curr_cmpt.save_to_db()

    def gui_wrkr_read_from_mem_db( self ):
        try:
            query_id = int(self.edit_cmpt_worker_mem_id.text())
            self.curr_mbr.load_from_db( query_id )
            self.gui_fill_cmpt_widget_with_curr_mbr()
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    def gui_fill_cmpt_widget_with_curr_mbr( self ):
        self.edit_cmpt_worker_name.setText( self.curr_mbr.name )
        self.edit_cmpt_worker_phone.setText( self.curr_mbr.cell_phone )
        self.edit_cmpt_worker_idcard.setText( self.curr_mbr.id_card )

        self.cmbo_cmpt_worker_tshirt_sz.setCurrentIndex( int(self.curr_mbr.tshirt_sz) )
        self.cmbo_cmpt_worker_coat_sz.setCurrentIndex( int(self.curr_mbr.coat_sz) )

    def gui_wrkr_read_from_cmpt_db( self ):
        self.gui_fill_cmpt_widget_with_curr_cmpt_wrkr()

    def gui_fill_cmpt_widget_with_curr_cmpt_wrkr( self ):
        try:
            query_id = int(self.edit_cmpt_worker_id.text())
            wrkr_info = self.curr_cmpt.load_from_db( query_id )

            self.edit_cmpt_worker_name.setText( wrkr_info[1] )
            self.edit_cmpt_worker_phone.setText( wrkr_info[2] )
            self.edit_cmpt_worker_idcard.setText( wrkr_info[3] )

            self.cmbo_cmpt_worker_vegetarian.setCurrentIndex( int(wrkr_info[4]) )
            self.cmbo_cmpt_worker_primary_job.setCurrentIndex( int(wrkr_info[5]) )
            self.cmbo_cmpt_worker_sec_job_1.setCurrentIndex( int(wrkr_info[6]) )
            self.cmbo_cmpt_worker_sec_job_2.setCurrentIndex( int(wrkr_info[7]) )
            self.cmbo_cmpt_worker_tshirt_sz.setCurrentIndex( int(wrkr_info[8]) )
            self.cmbo_cmpt_worker_coat_sz.setCurrentIndex( int(wrkr_info[9]) )

            self.edit_cmpt_worker_mem_id.setText( str(wrkr_info[10]) if wrkr_info[10] >0 else "" )
        except ValueError as err:
            print("[Exception]: {}".format( err ))

    ''' ---------------------------------------------
    Competition Worker Table procedure
    These procedures will be integrated with member table later.
    ----------------------------------------------'''
    def gui_fill_worker_data_table( self ):
        self.gui_remove_worker_data_table()
        self.gui_update_worker_data_table()

    def gui_update_worker_data_table( self ):
        if self.curr_cmpt.cmpt_hndl != "":
            cmpt_wrkr_data = self.curr_cmpt.retrieve_all_data()

            HeaderLabel = [
                "編號", "姓名", "電話",  "身分證", "葷素",
                "主任務", "次任務1", "次任務2", "T-Shirt尺寸", "風衣尺寸", "會員ID"  ]
            self.cmptWorkerTbl.setColumnCount( len( HeaderLabel ) )
            self.cmptWorkerTbl.setHorizontalHeaderLabels(HeaderLabel)
            self.cmptWorkerTbl.verticalHeader().setVisible(False)

            filepath = cmpt.CMPT_RSC_BASE_PATH + self.curr_cmpt.cmpt_hndl + "/cmpt.json"
            with open( filepath, "r", encoding='utf-8' ) as cmpt_info:
                cmpt_data = json.load( cmpt_info )
                joblist = cmpt_data['job']
                jobname_ls = [name for name, label in joblist]
                joblabel_ls = [label for name, label in joblist]
                print(jobname_ls)
                print(joblabel_ls)

            for row in cmpt_wrkr_data:
                indx = cmpt_wrkr_data.index( row )
                self.cmptWorkerTbl.insertRow( indx )

                try:
                    primary_jb_label = joblabel_ls.index( int(row[5]) )
                    pri_jb_name = jobname_ls[primary_jb_label]
                except ValueError as err:
                    pri_jb_name = ""
                    print("[CMPT_TABLE]{}".format(err))

                try:
                    sec_jb1_label = joblabel_ls.index( int(row[6]) )
                    sec_jb1_name  = jobname_ls[sec_jb1_label]
                except ValueError as err:
                    sec_jb1_name = ""
                    print("[CMPT_TABLE]{}".format(err))

                try:
                    sec_jb2_label = joblabel_ls.index( int(row[7]) )
                    sec_jb2_name  = jobname_ls[sec_jb2_label]
                except ValueError as err:
                    sec_jb2_name = ""
                    print("[CMPT_TABLE]{}".format(err))

                wrkr_mem_id_str = str( row[10] ) if row[10] != 0 else "None"

                self.cmptWorkerTbl.setItem( indx, 0, QtWidgets.QTableWidgetItem( str( row[ 0 ] ) ) )            # id
                self.cmptWorkerTbl.setItem( indx, 1, QtWidgets.QTableWidgetItem( row[1] ) )                     # name
                self.cmptWorkerTbl.setItem( indx, 2, QtWidgets.QTableWidgetItem( row[2] ) )                     # phone
                self.cmptWorkerTbl.setItem( indx, 3, QtWidgets.QTableWidgetItem( row[3] ) )                     # idcard
                self.cmptWorkerTbl.setItem( indx, 4, QtWidgets.QTableWidgetItem( cmpt.VEGETARIAN[row[4]] ) )    # vegetarian
                self.cmptWorkerTbl.setItem( indx, 5, QtWidgets.QTableWidgetItem( pri_jb_name ) )                # primary job
                self.cmptWorkerTbl.setItem( indx, 6, QtWidgets.QTableWidgetItem( sec_jb1_name ) )               # secoundary job 1
                self.cmptWorkerTbl.setItem( indx, 7, QtWidgets.QTableWidgetItem( sec_jb2_name ) )               # secoundary job 2
                self.cmptWorkerTbl.setItem( indx, 8, QtWidgets.QTableWidgetItem( cmpt.THIRT_SZ[row[8]] ) )      # t-shirt sz
                self.cmptWorkerTbl.setItem( indx, 9, QtWidgets.QTableWidgetItem( cmpt.COAT_SZ[row[9]] ) )       # coat sz
                self.cmptWorkerTbl.setItem( indx, 10, QtWidgets.QTableWidgetItem( wrkr_mem_id_str ) )           # mem id

            for col in range( 0, len( HeaderLabel ) ):
                self.cmptWorkerTbl.horizontalHeader().setSectionResizeMode( col, QtWidgets.QHeaderView.ResizeToContents )

    def gui_remove_worker_data_table( self ):
        rows = self.cmptWorkerTbl.rowCount()
        for row in range( 0, rows ):
            self.cmptWorkerTbl.removeRow( 0 )


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
