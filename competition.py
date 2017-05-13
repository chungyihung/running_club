#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sqlite3 as sql3

INVALID_ID = 65535
INVALID_PHONE = '09__-______'

CMPT_RSC_BASE_PATH      = "./Resource/competition/"
CMPT_DB_FILE_NAME       = "cmpt.db"

''' ---------------------------------------------
Main member class
----------------------------------------------'''
class competition:
    def __init__(self, **meminfo):
        '''
        Create database if not exist
        '''
        self.__folk_id      = meminfo.get( 'id', INVALID_ID             )       # Unsigned Int
        self.__name         = meminfo.get( 'name', 'Unknown'            )       # String
        self.__phone        = meminfo.get( 'phone', INVALID_PHONE       )       # String
        self.__id_card      = meminfo.get( 'idcard', INVALID_CARD_ID    )       # String
        self.__vegetarian   = meminfo.get( 'vegetarian', 0              )       # 0 for non-vegetarian
        self.__primary_job  = meminfo.get( 'primary_job', ''            )
        self.__address      = meminfo.get( 'address', ''                )       # String

    def create_tbl( self, filename ):
        with sql3.connect( filename ) as conn:
            c = conn.cursor()
            c.execute( ''' CREATE TABLE IF NOT EXISTS member (
                        id          INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name        TEXT NOT NULL,
                        phone       TEXT,
                        idcard      TEXT,
                        vegetarian  INTEGER,
                        primary_job TEXT,
                        sec_job_1   TEXT,
                        sec_job_2   TEXT,
                        tshirt_sz   INTEGER,
                        coat_sz     INTEGER
                        member_id   INTEGER NOT NULL,
                        )''' )
