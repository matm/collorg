# -*- coding: utf-8 -*-
import socket
import json

class Client():
    def __init__(self, ctrl):
        params = ctrl.db._cog_params
        self.__db = ctrl.db.name
        self.__host = params['session_cache_host']
        self.__port = int(params['session_cache_port'])
        self.__buff_size = int(params['session_cache_buff_size'])
        self.__address = (self.__host, self.__port)
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def request(self,  *args):
        data = json.dumps([self.__db, args])
        print("client request{}".format(data))
        self.__client.settimeout(0.01)
        self.__client.sendto(data, self.__address)
        recv_data, addr = self.__client.recvfrom(self.__buff_size)
        return json.loads(recv_data)

    def set_(self, cmd, session, data = None):
        try:
            json.dumps(data)
        except:
            data = str(data)
        res = self.request("set", cmd, str(session), data)
        return res

    def del_(self, cmd, key):
        self.request("del", cmd, key, None)

    def get_(self, cmd, session, key = None):
        try:
            return self.request("get", cmd, str(session), key)
        except:
            return None

    def check(self):
        return self.request("check", None, None, None)
