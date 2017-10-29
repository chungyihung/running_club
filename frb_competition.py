#!/usr/bin/python3
# -*- coding:utf-8 -*-
import enum as enm
import pyrebase as pybs
import json

''' ---------------------------------------------
Constant
----------------------------------------------'''
INVALID_ID = 65535
INVALID_CARD_ID = '##########'
INVALID_PHONE = '09__-______'

''' --------------------------------------------
Local path structure is
    ./Resource/competition/[CompetitionName]/cmpt.json
    ./Resource/competition/[CompetitionName]/staff_member.json

Firebase remote path structure is
    ./cmpt/[CompetitionName]
    ./[CompetitionName]_worker
----------------------------------------------'''
CMPT_RSC_BASE_PATH      = "./Resource/competition/"
FRB_CMPT_PATH_BASE      = "cmpt"
FRB_CMPT_PATH           = FRB_CMPT_PATH_BASE + "/{}"
FRB_CMPT_JOB_LIST_PATH  = FRB_CMPT_PATH_BASE + "_jblst_{}"
FRB_CMPT_WRK_PATH       = FRB_CMPT_PATH_BASE + "_worker_{}"
FRB_CMPT_WRK_AVAIL_LS   = FRB_CMPT_PATH_BASE + "_worker_avail_lst_{}"

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
Worker Key
----------------------------------------------'''
WorkerID    = "wrkrid"
Name        = "name"
Phone       = "phone"
IDCard      = "idcard"
Vegetarian  = "vegetarian"
Primary_JB  = "primary_job"
SEC_JB1     = "sec_job_1"
SEC_JB2     = "sec_job_2"
TShirt_SZ   = "tshirt_sz"
Coat_SZ     = "coat_sz"
MemberID    = "mem_id"

MAX_WORKER = 65535
E_NONE      = -1

DEFAULT_TSHIRT_SZ = 0
DEFAULT_COAT_SZ = 0
INVALID_JOB_INDEX = 0

''' ---------------------------------------------
Class Implementation
----------------------------------------------'''
class frb_competition:
    def __init__( self ):
        ''' ---------------------------------------------
        Load firebase config file
        ----------------------------------------------'''
        with open("firebase_config.json", "r", encoding='utf-8' ) as frb_config_fd:
            frb_cfg = json.load( frb_config_fd )

        self.firebase = pybs.initialize_app(frb_cfg)
        self.db = self.firebase.database()
        self.stg = self.firebase.storage()

        ''' ---------------------------------------------
        Indicate current selecred competition
        ----------------------------------------------'''
        self.curr_cmpt_hndl = ""

    ''' ---------------------------------------------
    Get competition in dict type
    ----------------------------------------------'''
    def get_competition( self, cmpt_name ):
        resp = self.db.child(FRB_CMPT_PATH.format(cmpt_name)).get()
        if resp.val() != None:
            self.curr_cmpt_hndl = cmpt_name
            return dict(resp.val())
        else:
            print("No {} competition in FRB server".format(cmpt_name))
            return None

    ''' ---------------------------------------------
    Get competition in dict type
    ----------------------------------------------'''
    def get_all_competition( self ):
        resp = self.db.child(FRB_CMPT_PATH_BASE).get()
        if resp.val() != None:
            return dict(resp.val())
        else:
            print("No any competition in FRB server")
            return None

    ''' ---------------------------------------------
    Set competition in dict type
        data["name"] - competition name
        data["date"] - competition date in yyyymmdd format
    ----------------------------------------------'''
    def set_competition( self, data ):
        cmpt_name = data["date"] + "_" + data["name"]
        #self.db.child(FRB_CMPT_PATH_BASE).child(cmpt_name).set(data)
        self.db.child(FRB_CMPT_PATH.format(cmpt_name)).set(data)
        self.init_jb( cmpt_name )
        self.init_worker_avail_list( cmpt_name )
        self.curr_cmpt_hndl = cmpt_name

    ''' ---------------------------------------------
    Update competition data with dict type
    TODO: 1. Implement item specify feature
    ----------------------------------------------'''
    def upt_competition( self, data ):
        cmpt_name = data["date"] + "_" + data["name"]
        self.db.child(FRB_CMPT_PATH.format(cmpt_name)).update(data)

    ''' ---------------------------------------------
    Delete competition
    ----------------------------------------------'''
    def del_competition( self, cmpt_name ):
        self.db.child(FRB_CMPT_PATH.format(cmpt_name)).remove()

    ''' ---------------------------------------------
    Job list - get_jb_list
        job is a key value hashmap to number -> ["Job1": 1 ]
    ----------------------------------------------'''
    def get_jb_list( self, separate = False ):
        resp = self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).get()
        if resp.val() != None:
            if separate == False:
                return dict(resp.val())
            else:
                joblist = dict(resp.val())
                jobname_ls = [name for name, label in joblist.items()]
                joblabel_ls = [label for name, label in joblist.items()]
                return jobname_ls, joblabel_ls
        else:
            print("No any job in job list")
            return None

    ''' ---------------------------------------------
    Job list - init_jb
      - init job list with empty content
    ----------------------------------------------'''
    def init_jb( self ):
        self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).set("")

    ''' ---------------------------------------------
    Job list - add_jb
    ----------------------------------------------'''
    def add_jb( self, jobstr, data ):
        self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).child(jobstr).set(data)

    ''' ---------------------------------------------
    Job list - rename_jb
    ----------------------------------------------'''
    def rename_jb( self, old_jb, new_jb ):
        resp = self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).child(old_jb).get()
        self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).child(old_jb).remove()
        self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).child(new_jb).set(resp.val())

    ''' ---------------------------------------------
    Job list - update_jb
    ----------------------------------------------'''
    def upt_job( self, data ):
        self.db.child(FRB_CMPT_PATH.format(self.curr_cmpt_hndl)).update(data)

    ''' ---------------------------------------------
    Job list - delete_jb
    ----------------------------------------------'''
    def delete_jb( self, target_jb ):
        self.db.child(FRB_CMPT_JOB_LIST_PATH.format(self.curr_cmpt_hndl)).child(target_jb).remove()

    ''' ---------------------------------------------
    Worker - init_worker
    ----------------------------------------------'''
    def init_worker( self, wrkrid = INVALID_ID ):
        worker = {}
        worker[WorkerID] = wrkrid
        worker[Name] = ""
        worker[Phone] = ""
        worker[IDCard] = ""
        worker[Vegetarian] = False
        worker[Primary_JB] = 0
        worker[SEC_JB1] = 0
        worker[SEC_JB2] = 0
        worker[TShirt_SZ] = DEFAULT_TSHIRT_SZ
        worker[Coat_SZ] = DEFAULT_COAT_SZ
        worker[MemberID] = 0
        return worker

    ''' ---------------------------------------------
    Worker - add_worker
    ----------------------------------------------'''
    def add_worker( self, wrkdata ):
        wrkrid = self.get_free_worker_id( )
        wrkdata[WorkerID] = wrkrid
        if wrkrid < MAX_WORKER:
            self.db.child(FRB_CMPT_WRK_PATH.format(self.curr_cmpt_hndl)).child(wrkrid).set(wrkdata)
            self.set_worker_avail_list( wrkrid )

    ''' ---------------------------------------------
    Worker - get_worker
    ----------------------------------------------'''
    def get_worker( self, wrkrid ):
        if wrkrid < MAX_WORKER:
            resp = self.db.child(FRB_CMPT_WRK_PATH.format(self.curr_cmpt_hndl)).child(wrkrid).get()
            if resp.val() != None:
                return dict(resp.val())
        else:
            print("Worker ID larger than designed")

    ''' ---------------------------------------------
    Worker - get_all_worker
    ----------------------------------------------'''
    def get_all_worker( self ):
        resp = self.db.child(FRB_CMPT_WRK_PATH.format(self.curr_cmpt_hndl)).get()
        if resp.val() != None:
            return dict(resp.val())
        else:
            print("No competition data found")

    ''' ---------------------------------------------
    Worker - update_worker
    ----------------------------------------------'''
    def update_worker( self, wrkrid, wrkdata ):
        wrkdata[WorkerID] = wrkrid
        if wrkrid < MAX_WORKER:
            self.db.child(FRB_CMPT_WRK_PATH.format(self.curr_cmpt_hndl)).child(wrkrid).update(wrkdata)

    ''' ---------------------------------------------
    Worker - rm_worker
    ----------------------------------------------'''
    def rm_worker( self, wrkrid ):
        self.db.child(FRB_CMPT_WRK_PATH.format(self.curr_cmpt_hndl)).child(wrkrid).remove()
        self.clr_worker_avail_list( wrkrid )

    ''' ---------------------------------------------
    Worker available list - init_worker_avail_list
      - available list set at add_worker function
      - available list clear at delete_worker function
      - available list set to empty dict at create time.
      - pyrebase will convert response to be list if all key is numerical
        To make it to be dict struct, just add a prefix before nummber
    ----------------------------------------------'''
    def init_worker_avail_list( self ):
        self.db.child(FRB_CMPT_WRK_AVAIL_LS.format(self.curr_cmpt_hndl)).set("")

    def set_worker_avail_list( self, wrkid ):
        self.db.child(FRB_CMPT_WRK_AVAIL_LS.format(self.curr_cmpt_hndl)).child("a" + str(wrkid)).set(1)

    def clr_worker_avail_list( self, wrkid ):
        print("Start remove worker {}".format(wrkid))
        self.db.child(FRB_CMPT_WRK_AVAIL_LS.format(self.curr_cmpt_hndl)).child("a" + str(wrkid)).remove()

    ''' ---------------------------------------------
    Worker available list - get_free_worker_id
    Return - 0 for invalid worker ID; Start from 1.
    ----------------------------------------------'''
    def get_free_worker_id( self ):
        resp = self.db.child(FRB_CMPT_WRK_AVAIL_LS.format(self.curr_cmpt_hndl)).get()
        if resp.val() != None:
            print(resp.val())
            avail_ls = dict(resp.val())
            for wrk_id in range(1, MAX_WORKER):
                if avail_ls.get("a" + str(wrk_id), 0) == 0:
                    return wrk_id
            return MAX_WORKER
        else:
            return 1

    ''' ---------------------------------------------
    Integrated function
    ----------------------------------------------'''
    def get_jb_to_name_list( self ):
        jobname_ls, joblabel_ls = self.get_jb_list( separate = True )
        worker_ls = self.get_all_worker()

        ''' ---------------------------------------------
        Use job name as key, and each value is string array
        ----------------------------------------------'''
        jb_wrk_ls = {}
        for wrk_id, worker in worker_ls.items():
            if worker[Primary_JB] != INVALID_JOB_INDEX:
                jb_lbl = joblabel_ls.index(worker[Primary_JB])
                jb_name = jobname_ls[jb_lbl]
                if worker[Primary_JB] in jb_wrk_ls:
                    jb_wrk_ls[jb_name].append(worker[Name])
                else:
                    jb_wrk_ls[jb_name] = [worker[Name]]

            if worker[SEC_JB1] != INVALID_JOB_INDEX:
                jb_lbl = joblabel_ls.index(worker[SEC_JB1])
                jb_name = jobname_ls[jb_lbl]
                if worker[SEC_JB1] in jb_wrk_ls:
                    jb_wrk_ls[worker[SEC_JB1]].append(worker[Name])
                else:
                    jb_wrk_ls[worker[SEC_JB1]] = [worker[Name]]

            if worker[SEC_JB2] != INVALID_JOB_INDEX:
                jb_lbl = joblabel_ls.index(worker[SEC_JB2])
                jb_name = jobname_ls[jb_lbl]
                if worker[SEC_JB2] in jb_wrk_ls:
                    jb_wrk_ls[worker[SEC_JB2]].append(worker[Name])
                else:
                    jb_wrk_ls[worker[SEC_JB2]] = [worker[Name]]

        return jb_wrk_ls
