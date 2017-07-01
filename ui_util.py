#!/usr/local/bin/python3
# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets
import enum as enm

''' ---------------------------------------------
Excel items sequence
----------------------------------------------'''
PU_MSG_INFO     = 1
PU_MSG_YESNO    = 2

def popup_msg_box( title, strinfo, popup_msg_type ):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle( title )

    if popup_msg_type == PU_MSG_INFO:
        icon = QtWidgets.QMessageBox.Information
        btn_type = QtWidgets.QMessageBox.Ok
    elif popup_msg_type == PU_MSG_YESNO:
        icon = QtWidgets.QMessageBox.Information
        btn_type = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No

    msg.setIcon( icon )
    msg.setStandardButtons( btn_type )
    msg.setText( strinfo )
    return msg.exec_()
