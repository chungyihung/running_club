#!/usr/bin/python3

import sqlite3 as sql3

INVALID_ID = 65535
INVALID_CARD_ID = '##########'
INVALID_PHONE = '09__-______'

DB_FILE_NAME = "running_club_member.db"

class member:
    def __init__(self, **meminfo):
        self.__name = meminfo.get('name', 'Unknown')                    # String
        self.__mem_id = meminfo.get('memid', INVALID_ID)                # Unsigned Int
        self.__cell_phone = meminfo.get('cell_phone', INVALID_PHONE )   # String
        self.__position = meminfo.get('position', 'Unknown')            # String
        self.__id_card = meminfo.get('idcard', INVALID_CARD_ID)         # String
        self.__birthday = meminfo.get('birthday', '')                   # String, will revise as list later
        self.__area = meminfo.get('area', '')                           # String
        self.__address = meminfo.get('address', '')                     # String
        self.__phone = meminfo.get('phone', '' )                        # String
        self.__phone2 = meminfo.get('phone2', '' )                      # String

        '''
        Create database if not exist
        '''
        self.create_db()

    @property
    def name(self):
        return self.__name

    @property
    def mem_id(self):
        return self.__mem_id

    @property
    def cell_phone(self):
        return self.__cell_phone

    @name.setter
    def name(self, name):
        self.__name = name

    @mem_id.setter
    def mem_id(self, mem_id):
        self.__mem_id = mem_id

    @cell_phone.setter
    def cell_phone(self, cell_phone_number):
        self.__cell_phone = cell_phone_number

    def create_db( self ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( ''' CREATE TABLE IF NOT EXISTS member (
                        id          INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name        TEXT NOT NULL,
                        cell_phone  TEXT NOT NULL
                        )''' )

    def load_from_db( self, mem_id ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( "SELECT * FROM member WHERE id=?", (mem_id, ) )
            result = c.fetchone()
            if result != None:
                self.__mem_id = result[0]
                self.__name = result[1]
                self.__cell_phone = result[2]
            else:
                print("Fetch nothing in DB")

    def save_to_db( self ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( "INSERT INTO member VALUES (?, ?, ?)", ( self.__mem_id, self.__name, self.__cell_phone ) )

