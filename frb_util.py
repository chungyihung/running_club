#!/usr/bin/python3
# -*- coding:utf-8 -*-
import enum as enm
import pyrebase as pybs
import json

''' ---------------------------------------------
Class Implementation
----------------------------------------------'''
class frb_util:
    def __init__( self ):
        ''' ---------------------------------------------
        Load firebase config file
        ----------------------------------------------'''
        with open("firebase_config.json", "r", encoding='utf-8' ) as frb_config_fd:
            frb_cfg = json.load( frb_config_fd )

        self.firebase = pybs.initialize_app(frb_cfg)
        self.rtdb = self.firebase.database()
        self.stg = self.firebase.storage()

    def get_instance( self ):
        return self.firebase

    def get_db_instance( self ):
        return self.rtdb, self.stg

