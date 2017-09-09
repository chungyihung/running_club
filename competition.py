#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sqlite3 as sql3
import enum as enm

''' ---------------------------------------------
Constant
----------------------------------------------'''
INVALID_ID = 65535
INVALID_CARD_ID = '##########'
INVALID_PHONE = '09__-______'

CMPT_RSC_BASE_PATH      = "./Resource/competition/"
CMPT_DB_FILE_NAME       = "cmpt.db"

VEGETARIAN = [ '葷', '素' ]

DEFAULT_SZ = 'M'
THIRT_SZ   = [ 'N/A', '8#', '10#', 'XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '5XL' ]
COAT_SZ    = [ 'N/A', '8#', '10#', 'XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '5XL' ]

WRKTBL_MODE_NAME = [ '正常模式', '工作群組模式' ]
''' ---------------------------------------------
Worker Table items sequence
----------------------------------------------'''
class WRKTBL_MODE( enm.IntEnum ):
    NORMAL                  = 0
    JOBGROUP                = 1
    MODE_CNT                = enm.auto()

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
        self.__wrkrid       = worker.get( 'wrkrid', INVALID_ID         )       # Unsigned Int
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
        self.__cmpt_hndl      = ""
        self.__cmpt_db_path   = ""

    @property
    def cmpt_hndl(self):
        return self.__cmpt_hndl

    @property
    def cmpt_db_path(self):
        return self.__cmpt_db_path

    @cmpt_hndl.setter
    def cmpt_hndl(self, cmpt_name):
        self.__cmpt_hndl = cmpt_name

    @cmpt_db_path.setter
    def cmpt_db_path(self, path):
        self.__cmpt_db_path = path


    def target_cmpt_set( self, cmpt_fldr_name ):
        self.__cmpt_hndl = cmpt_fldr_name
        self.__cmpt_db_path = CMPT_RSC_BASE_PATH + cmpt_fldr_name + "/" + CMPT_DB_FILE_NAME
        print(self.__cmpt_hndl)

    def json_fname( self ):
        filepath = CMPT_RSC_BASE_PATH + self.__cmpt_hndl + "/cmpt.json"
        return filepath

    """
    Create competition database.
    The create timing is
      1. If not exist after user select the competition from combo box.
      2. After create a new competition.
    """
    def create_tbl( self ):
        with sql3.connect( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( ''' CREATE TABLE IF NOT EXISTS competition (
                        wrkrid      INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name        TEXT NOT NULL,
                        phone       TEXT,
                        idcard      TEXT,
                        vegetarian  INTEGER,
                        primary_job TEXT,
                        sec_job_1   TEXT,
                        sec_job_2   TEXT,
                        tshirt_sz   INTEGER,
                        coat_sz     INTEGER,
                        member_id   INTEGER NOT NULL
                        )''' )

    def drop_tbl( self ):
        with sql3.connect( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( "DROP TABLE competition")

    def load_from_db( self, worker_id ):
        with sql3.connect( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( "SELECT * FROM competition WHERE wrkrid=?", (worker_id, ) )
            result = c.fetchone()
            if result != None:
                self.__wrkrid      = result[0]
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
                print("Now current worker ID is {}".format(self.__wrkrid))
                return result
            else:
                print("Fetch nothing in DB")

    def save_to_db( self ):

        with sql3.connect( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( '''SELECT MAX(wrkrid) FROM competition''' )

            max_id = c.fetchone()[0]
            if max_id == None:
                max_id = 0
            else:
                max_id += 1
                if max_id % 10 == 4:
                    max_id += 1

            self.__wrkrid = max_id
            c.execute( '''INSERT INTO competition
                          (
                          wrkrid,
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
                          ( self.__wrkrid,
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

    def update_to_db( self ):
        with sql3.connect( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( '''UPDATE competition SET
                      name=:name,
                      phone=:phone,
                      idcard=:idcard,
                      vegetarian=:vegetarian,
                      primary_job=:primary_job,
                      sec_job_1=:sec_job_1,
                      sec_job_2=:sec_job_2,
                      tshirt_sz=:tshirt_sz,
                      coat_sz=:coat_sz,
                      member_id=:member_id
                      WHERE wrkrid=:wrkrid''',
                      { "wrkrid"         : self.__wrkrid,
                        "name"           : self.__name,
                        "phone"          : self.__phone,
                        "idcard"         : self.__idcard,
                        "vegetarian"     : self.__vegetarian,
                        "primary_job"    : self.__primary_job,
                        "sec_job_1"      : self.__sec_job_1,
                        "sec_job_2"      : self.__sec_job_2,
                        "tshirt_sz"      : self.__tshirt_sz,
                        "coat_sz"        : self.__coat_sz,
                        "member_id"      : self.__member_id
                        } )

    def delete_item( self, del_id ):
        with sql3.connect( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute( '''DELETE FROM competition WHERE wrkrid = ?''', ( del_id, ) )

    def retrieve_all_data( self ):
        with sql3.Connection( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM competition ''')
            rows = c.fetchall()
            return rows

    def get_wrk_lst_in_job( self, joblabel ):
        with sql3.Connection( self.__cmpt_db_path ) as conn:
            c = conn.cursor()
            c.execute('''SELECT name FROM competition where primary_job = ? OR sec_job_1 = ? OR sec_job_2 = ? ''', ( joblabel, joblabel, joblabel) )
            rows = c.fetchall()
            return rows

    ''' ---------------------------------------------
    Use for update current worker information
    ----------------------------------------------'''
    def worker_info_update( self, wrkr_info ):
        [ self.__wrkrid      ,
          self.__name        ,
          self.__phone       ,
          self.__idcard      ,
          self.__vegetarian  ,
          self.__primary_job ,
          self.__sec_job_1   ,
          self.__sec_job_2   ,
          self.__tshirt_sz   ,
          self.__coat_sz     ,
          self.__member_id ] = wrkr_info
