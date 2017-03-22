#!/usr/bin/python3

INVALID_ID = 65535
INVALID_CARD_ID = '##########'

class member:
    def __init__(self, **meminfo):
        self.__name = meminfo.get('name', 'Unknown')                # String
        self.__position = meminfo.get('position', 'Unknown')        # String
        self.__mem_id = meminfo.get('memid', INVALID_ID)            # Unsigned Int
        self.__id_card = meminfo.get('idcard', INVALID_CARD_ID)     # String
        self.__birthday = meminfo.get('birthday', '')               # String, will revise as list later
        self.__area = meminfo.get('area', '')                       # String
        self.__address = meminfo.get('address', '')                 # String
        self.__cell_phone = meminfo.get('cell_phone', '' )          # String
        self.__phone = meminfo.get('phone', '' )                    # String
        self.__phone2 = meminfo.get('phone2', '' )                  # String

    @property
    def name(self):
        return self.__name

    @property
    def position(self):
        return self.__position

    @property
    def mem_id(self):
        return self.__mem_id

    @property
    def cell_phone(self):
        return self.__cell_phone

    @cell_phone.setter
    def cell_phone(self, cell_phone_number):
        self.__cell_phone = cell_phone_number


