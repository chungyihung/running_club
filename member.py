#!/usr/bin/python3

import sqlite3 as sql3
import openpyxl as pyxl

INVALID_ID = 65535
INVALID_CARD_ID = '##########'
INVALID_PHONE = '09__-______'

DB_FILE_NAME            = "running_club_member.db"
EXCEL_FILE_NAME         = "running_table.xlsx"
EXCEL_FILE_TS_NAME      = "running_table_test.xlsx"
EXCEL_SHEET_ALL_NAME    = "新會員(全)"

class member:
    def __init__(self, **meminfo):
        self.__name         = meminfo.get( 'name', 'Unknown'            )       # String
        self.__mem_id       = meminfo.get( 'id', INVALID_ID             )       # Unsigned Int
        self.__cell_phone   = meminfo.get( 'cell_phone', INVALID_PHONE  )       # String
        self.__position     = meminfo.get( 'position', 'Unknown'        )       # String
        self.__id_card      = meminfo.get( 'idcard', INVALID_CARD_ID    )       # String
        self.__birthday     = meminfo.get( 'birthday', ''               )       # String, will revise as list later
        self.__birthdayROC  = meminfo.get( 'birthdayROC', ''            )       # Unsigned Int
        self.__area         = meminfo.get( 'area', ''                   )       # String
        self.__address      = meminfo.get( 'address', ''                )       # String
        self.__phone        = meminfo.get( 'phone', ''                  )       # String
        self.__phone2       = meminfo.get( 'phone2', ''                 )       # String

        '''
        Create database if not exist
        '''
        self.create_tbl()

    @property
    def name(self):
        return self.__name

    @property
    def mem_id(self):
        return self.__mem_id

    @property
    def cell_phone(self):
        return self.__cell_phone

    @property
    def position(self):
        return self.__position

    @property
    def id_card(self):
        return self.__id_card

    @property
    def birthday(self):
        return self.__birthday

    @property
    def birthdayROC(self):
        return self.__birthdayROC

    @property
    def area(self):
        return self.__area

    @property
    def address(self):
        return self.__address

    @property
    def phone(self):
        return self.__phone

    @property
    def phone2(self):
        return self.__phone2

    @name.setter
    def name(self, name):
        self.__name = name

    @mem_id.setter
    def mem_id(self, mem_id):
        self.__mem_id = mem_id

    @cell_phone.setter
    def cell_phone(self, cell_phone_number):
        self.__cell_phone = cell_phone_number

    @position.setter
    def position(self, position):
        self.__position = position

    @id_card.setter
    def id_card(self, id_card):
        self.__id_card = id_card

    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    @birthdayROC.setter
    def birthdayROC(self, birthdayROC):
        self.__birthdayROC = birthdayROC

    @area.setter
    def area(self, area):
        self.__area = area

    @address.setter
    def address(self, address):
        self.__address = address

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    @phone2.setter
    def phone2(self, phone2):
        self.__phone2 = phone2

    def xstr( self, s ):
        if s is None:
            return ''
        return str(s)

    def create_tbl( self ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( ''' CREATE TABLE IF NOT EXISTS member (
                        id          INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        position    TEXT NOT NULL,
                        name        TEXT NOT NULL,
                        idcard      TEXT,
                        birthROC    INTEGER,
                        birth       TEXT,
                        area        TEXT,
                        cell_phone  TEXT,
                        phone       TEXT,
                        phone2      TEXT,
                        address     TEXT
                        )''' )

    def drop_tbl( self ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( "DROP TABLE member")

    def load_from_db( self, mem_id ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( "SELECT * FROM member WHERE id=?", (mem_id, ) )
            result = c.fetchone()
            if result != None:
                self.__mem_id       = result[0]
                self.__position     = result[1]
                self.__name         = result[2]
                self.__id_card      = result[3]
                self.__birthdayROC  = result[4]
                self.__birthday     = result[5]
                self.__area         = result[6]
                self.__cell_phone   = result[7]
                self.__phone        = result[8]
                self.__phone2       = result[9]
                self.__address      = result[10]
            else:
                print("Fetch nothing in DB")

    def save_to_db( self ):
        with sql3.connect( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( '''INSERT INTO member
                          ( position, name, idcard, birthROC, birth, area, cell_phone, phone, phone2, address )
                          VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
                          ( self.__position,
                            self.__name,
                            self.__id_card,
                            self.__birthdayROC,
                            self.__birthday,
                            self.__area,
                            self.__cell_phone,
                            self.__phone,
                            self.__phone2,
                            self.__address ) )

    def cnvt_excel_to_db( self ):
        """
        Load excel file and specific the sheet
        """
        wb = pyxl.load_workbook( EXCEL_FILE_NAME )
        sheet_all = wb.get_sheet_by_name( EXCEL_SHEET_ALL_NAME )

        """
        Delete and recreate the table of database
        """
        self.drop_tbl()
        self.create_tbl()

        with sql3.Connection( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            for item in sheet_all.iter_rows( row_offset = 1 ):
                if item[0].value != None:
                    print(int(item[0].value))
                    c.execute( '''INSERT INTO member
                                  ( position, name, idcard, birthROC, birth, area, cell_phone, phone, phone2, address )
                                  VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
                                  ( self.xstr( item[1].value ),
                                    self.xstr( item[2].value ),
                                    self.xstr( item[3].value ),
                                    self.xstr( item[4].value ),
                                    self.xstr( item[5].value ),
                                    self.xstr( item[6].value ),
                                    self.xstr( item[7].value ),
                                    self.xstr( item[8].value ),
                                    self.xstr( item[9].value ),
                                    self.xstr( item[10].value ) ) )

    def cnvt_db_to_excel( self ):
        wb = pyxl.Workbook()
        for sheet in wb.worksheets:
            wb.remove_sheet( sheet )

        ws = wb.create_sheet( title=EXCEL_SHEET_ALL_NAME )
        ws.append( ["編號", "職稱", "姓名", "身分證", "年次", "出生年月日", "地址", "手機", "電話1", "電話2", "通訊處(地址)"] )
        with sql3.Connection( DB_FILE_NAME ) as conn:
            c = conn.cursor()
            c.execute( "SELECT * FROM member" )
            for row in c:
                ws.append( [ x for x in row ] )

        wb.save( filename = EXCEL_FILE_TS_NAME )
