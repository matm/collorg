# -*- coding: utf-8 -*-
import os
from multiprocessing import Process
import signal
import socket
import json

class Handler():
    def __init__(self):
        self.dict_ = {}

    def __set_session(self, session):
        if not session in self.dict_:
            self.dict_[session] = {}
        return self.dict_[session]

    def check(self, **kwargs):
        return "ok"

    def do_get_cog_ref_oid(self, sub_cmd, session, key):
        return self.dict_[session][sub_cmd][key]

    def do_set_cog_ref_oid(self, sub_cmd, session, value):
        """
        value is in json...
        """
        obj_oid, ref_obj_oid = json.loads(value)
        dict_ = self.__set_session(session)
        if not sub_cmd in dict_:
            dict_[sub_cmd] = {}
        dict_ = dict_[sub_cmd]
        if not obj_oid in dict_:
            dict_[obj_oid] = []
        if not ref_obj_oid in dict_[obj_oid]:
            dict_[obj_oid].append(ref_obj_oid)
        return dict_[obj_oid]

    def do_get(self, sub_cmd, session, key = None):
        value = self.dict_[session][sub_cmd] or ""
        if key is not None:
            value = self.dict_[session][sub_cmd][key]
        return value

    def do_set(self, sub_cmd, session, value):
        if sub_cmd == ['ref_obj_oid']:
            return self.do_set_cog_ref_oid(sub_cmd, session, value)
        self.__set_session(session)[sub_cmd] = value
        return "ok"

    def do_del(self, sub_cmd, session, key):
        open("/tmp/cog_cache_log", "a+").write("delete: {}\n".format(session))
        if session in self.dict_:
            self.dict_.pop(session)

class Server():
    server = None
    __init_failed = False
    __connect_failed = False
    __id = None
    def __init__(self, ctrl):
        self.__ctrl = ctrl
        params = ctrl.db._cog_params
        self.__host = params['session_cache_host']
        self.__port = int(params['session_cache_port'])
        self.__buff_size = int(params['session_cache_buff_size'])
        self.__address = (self.__host, self.__port)
        self.__pid_file = "{}/pid".format(params['upload_dir'])
        self.__id = id(self)
        self.__d_handlers = {}

    def __serve(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server.bind(self.__address)
        while(1):
            try:
                recv_data, addr = self.__server.recvfrom(self.__buff_size)
                data = json.loads(recv_data)
                db_name = data[0]
                cmd, sub_cmd, session, data_ = data[1]
                if session is None or session == "None":
                    self.__server.sendto(json.dumps(None), addr)
                    continue
                if not db_name in self.__d_handlers:
                    self.__d_handlers[db_name] = Handler()
                handler = self.__d_handlers[db_name]
                if cmd == "set":
                    res = handler.do_set(sub_cmd, session, data_)
                elif cmd == "get":
                    res = handler.do_get(sub_cmd, session, key = None)
                elif cmd == "del":
                    res = handler.do_del(sub_cmd, session, key = None)
                elif cmd == "check":
                    res = handler.check()
                res_string = json.dumps(res)
                self.__server.sendto(res_string, addr)
            except Exception, err:
                open("/tmp/cog_cache_log", "a+").write(
                    "Error: {}\n{}\n".format(recv_data, err))

    def start(self):
        p = Process(target = self.__serve)
        p.start()
        pid = str(p.pid)
        open(self.__pid_file, "w").write("{}\n".format(pid))
        open("/tmp/cog_cache_log", "a+").write("{}\n".format(70*"-"))
        os.popen("chmod 777 /tmp/cog_cache_log")
        open("/tmp/cog_cache_log", "a+").write(
            "Starting server with PID: {}\n".format(pid))
        open("/tmp/cog_cache_log", "a+").write("server ok\n")

    def stop(self):
        pid = int(open(self.__pid_file).read().strip())
        print("stopping server with pid: {}".format(pid))
        os.kill(pid, signal.SIGINT)
        os.unlink(self.__pid_file)
