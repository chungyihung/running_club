#!/usr/bin/python3

import member as mem

member_info = { 'name':         'Joseph',
                'position':     'CEO^^||',
                'memid':        1,
                'idcard':       'F123456789',
                'birthday':     '2017.01.01',
                'area':         'Taoyuan',
                'address':      'Test Address',
                'cell_phone':   '0975123456',
                'phone':        '02-222222222',
                'phone2':       '02-33334444'
              }

new_mem = mem.member( **member_info )

print('The new member\'s name is {}'.format(new_mem.name))
print('The new member\'s ID is {}'.format(new_mem.mem_id))
