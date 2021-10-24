#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time         :       2021/10/12 20:17
# @Author       :       林子然
# @File         :       db.py
# @Software     :       Pycharm

from redis import Redis
from redis_config import REDIS_HOST, REDIS_PORT, REDIS_DB,REDIS_PASSWORD


class StudentDB:

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB):
        self.redis = Redis(host, port, db, password=REDIS_PASSWORD)
    def add(self, username, password):
        self.redis.hset('STUDENT_USER', username, password)

    def search(self, username, password):
        result = self.redis.hget('STUDENT_USER', username)
        if result:
            if password == result.decode():
                return True
            else:
                return False
        else:
            return False
    def del_self(self,username,password):
        self.redis.hdel('STUDENT_USER',username,password)
    def change(self, old_username,new_username, old_password, new_password):
        if self.redis.hget('STUDENT_USER', old_username) == old_password.encode():
            self.del_self(old_username,old_password)
            self.add(new_username,new_password)
            return True
        else:
            return False
    def all(self):
        self.redis.flushdb()
if __name__ == '__main__':
    StudentDB().all()


