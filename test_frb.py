#!/usr/bin/python3
# -*- coding:utf-8 -*-
import frb_member as frbm
import time

myfrbm = frbm.frb_member()
#data = myfrbm.get_member(1)
#
#print(data)
#print(data["name"])
#data["name"] = "test2"
#myfrbm.set_member(data, 1)
##myfrbm.upt_member(data, 1)
#myfrbm.del_member(data, 2)

#myfrbm.cnvt_excel_to_db()
#myfrbm.cnvt_db_to_excel()
#data = myfrbm.get_all_member()
#
#print(data.val())

#print(data[0])
#print(data[1])
#print(data[2])
#print(data[3])
#print(data[4])
#print(data[10])

myfrbm.updt_timestamp()
mytime = myfrbm.get_timestamp()
print("mytime = {}".format(mytime))
