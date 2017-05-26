#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sqlite3 as sql3

INVALID_ID = 65535
INVALID_CARD_ID = '##########'
INVALID_PHONE = '09__-______'

CMPT_RSC_BASE_PATH      = "./Resource/competition/"
CMPT_DB_FILE_NAME       = "cmpt.db"

''' ---------------------------------------------
TODO:
After finish the prototype, try combining member
and competition module in one.
----------------------------------------------'''

''' ---------------------------------------------
Main member class
----------------------------------------------'''
class competition:

    def __init__(self, **worker):
        '''
        Create database if not exist
        '''
        self.__id           = worker.get( 'id', INVALID_ID             )       # Unsigned Int
        self.__name         = worker.get( 'name', 'Unknown'            )       # String
        self.__phone        = worker.get( 'phone', INVALID_PHONE       )       # String
        self.__idcard       = worker.get( 'idcard', INVALID_CARD_ID    )       # String
        self.__vegetarian   = worker.get( 'vegetarian', 0              )       # 0 for non-vegetarian
        self.__primary_job  = worker.get( 'primary_job', ''            )
        self.__sec_job_1    = worker.get( 'sec_job_1', ''              )
        self.__sec_job_2    = worker.get( 'sec_job_2', ''              )
        self.__tshirt_sz    = worker.get( 'tshirt_sz', ''              )
        self.__coat_sz      = worker.get( 'coat_sz', ''                )
        self.__member_id    = worker.get( 'mem_id', ''                 )       # If 0 means it is just a volunteer

        '''
        Use competition name (folder name) as handler. Default NONE
        '''
        self.cmpt_hndl      = ""
        self.cmpt_db_path   = ""


    def target_cmpt_set( self, cmpt_name ):
        self.cmpt_hndl = cmpt_name
        self.cmpt_db_path = CMPT_RSC_BASE_PATH + cmpt_name + "/" + CMPT_DB_FILE_NAME


    """
    Create competition database.
    The create timing is
      1. If not exist after user select the competition from combo box.
      2. After create a new competition.
    """
    def create_tbl( self ):
        with sql3.connect( self.cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( ''' CREATE TABLE IF NOT EXISTS competition (
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
                        member_id   INTEGER NOT NULL
                        )''' )

    def drop_tbl( self ):
        with sql3.connect( self.cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( "DROP TABLE competition")

    def load_from_db( self, worker_id ):
        with sql3.connect( self.cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( "SELECT * FROM competition WHERE id=?", (worker_id, ) )
            result = c.fetchone()
            if result != None:
                self.__id          = result[0]
                self.__name        = result[1]
                self.__phone       = result[2]
                self.__idcard      = result[3]
                self.__vegetarian  = result[4]
                self.__primary_job = result[5]
                self.__sec_job_1   = result[6]
                self.__sec_job_2   = result[7]
                self.__tshirt_sz   = result[8]
                self.__coat_sz     = result[9]
                self.__member_id   = result[10]
                print("Now current worker ID is {}".format(self.__id))
            else:
                print("Fetch nothing in DB")

    def save_to_db( self ):

        with sql3.connect( self.cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( '''SELECT MAX(id) FROM competition''' )

            max_id = c.fetchone()[0]
            if max_id == None:
                max_id = 0
            else:
                max_id += 1
                if max_id % 10 == 4:
                    max_id += 1

            self.__id = max_id
            c.execute( '''INSERT INTO competition
                          (
                          id,
                          name,
                          phone,
                          idcard,
                          vegetarian,
                          primary_job,
                          sec_job_1,
                          sec_job_2,
                          tshirt_sz,
                          coat_sz,
                          member_id
                          )
                          VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
                          ( self.__id,
                            self.__name,
                            self.__phone,
                            self.__idcard,
                            self.__vegetarian,
                            self.__primary_job,
                            self.__sec_job_1,
                            self.__sec_job_2,
                            self.__tshirt_sz,
                            self.__coat_sz,
                            self.__member_id ) )

    def delete_item( self, del_id ):
        with sql3.connect( self.cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( '''DELETE FROM competition WHERE id = ?''', ( del_id, ) )

    def retrieve_all_data( self ):
        with sql3.Connection( self.cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM competition ''')
            rows = c.fetchall()
            return rows
