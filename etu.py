#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import competition as cmpt
import openpyxl as pyxl
import ui_util as ui_utl

''' ---------------------------------------------
Excel Transformation Utility (ETU) module
----------------------------------------------'''
def ETU_cmpt_tbl_save_to_excel( QtTable, sheet_name, filename ):
    ''' ---------------------------------------------
    Get table header string
    ----------------------------------------------'''
    header_ls = []
    header_idx = 0
    while True:
        qtwitem = QtTable.horizontalHeaderItem(header_idx)
        if qtwitem == None:
            break
        else:
            header_ls.append(qtwitem.text())
            header_idx += 1
    etu_save_to_excel( QtTable, sheet_name, header_ls, filename )
    return True

def etu_save_to_excel( targetTbl, sheet_title, header, filepath ):
    wb = pyxl.Workbook()
    for sheet in wb.worksheets:
        wb.remove_sheet( sheet )

    ws = wb.create_sheet( title = sheet_title )
    ws.append(header)

    for row in range( 0, targetTbl.rowCount() ):
        append_list = []
        for col in range( 0 , targetTbl.columnCount() ):
            qtblitem = targetTbl.item(row, col)
            append_list.append( qtblitem.text() if qtblitem != None else "" )
        ws.append( append_list )

    wb.save( filename = filepath )
    ui_utl.popup_msg_box("匯出Excel", "已成功匯出至{}".format(filepath), ui_utl.PU_MSG_TYPE.INFO )

    return True
