#!/usr/bin/env python3
"""nginx log"""
from pymongo import MongoClient


def print_nginx_log(mongo_collection):
    """nginx log stats"""
    print("{} logs".format(mongo_collection.count_documents({})))
    print("Methods:")
    type_of_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in type_of_methods:
        count_req = len(list(mongo_collection.find({"method": method})))
        print("\tmethod {}: {}".format(method, count_req))
    count_status_checks = len(list(mongo.collection.find({"method": "GET", "path": "/status"})))
    print("{} status check".format(count_status_checks))


def run():
    """Provides some stats about Nginx log"""
    client = MongoClient('mongodb://localhost:27017/')
    print_nginx_log(client.logs.nginx)


if __name__ == '__main__':
    run()
