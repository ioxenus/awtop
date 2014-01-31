#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import socket
from fnmatch import fnmatch

import psutil


parser = argparse.ArgumentParser(description='A simple network psutil wrapper.')
parser.add_argument('-n', dest='noresolve', action='store_const', const=True, default=False, help="don't resolve hostnames")
parser.add_argument('-l', dest='show_outgoing_localhost', action='store_const', const=True, default=False, help="show connections that go to localhost")
parser.add_argument('-p', dest='print_incoming_host', action='store_const', const=True, default=False, help="show incoming hostnames (it doesn't filter the connection list; just suppresses a bit of output)")
parser.add_argument('-c', dest='show_closed_connections', action='store_const', const=True, default=False, help="show closed connections")
parser.add_argument('-s', dest='search', type=str, default=None, help="search in outgoing hosts by wildcard")

options = vars(parser.parse_args())

def host_resolve(ip):
    try:
        result = socket.gethostbyaddr(ip)[0]
    except socket.herror as e:
        result = ip

    return result


def pprint_connection(status, c_in, c_out):
    if options['print_incoming_host']:
        return "       | |-- %-15s | %s -> %s" % (status, c_in, c_out)
    else:
        return "       | |-- %-15s | %s" % (status, c_out)

if __name__ == '__main__':
    for process in psutil.process_iter():
        try:
            pid = process.pid
            name = process.name
            connections = process.get_connections()
        except psutil._error.NoSuchProcess:
            pass
        except psutil._error.AccessDenied:
            pass

        #if len(connections) > 0:
        #    print "%6d | + %s" % (pid, name)
        #else:
        #    print "%6d | %s" % (pid, name)

        print_queue = []

        for connection in connections:
            if len(connection.laddr) == 0 or len(connection.raddr) == 0:
                continue

            in_host, in_port = connection.laddr
            out_host, out_port = connection.raddr
            in_ip, out_ip = in_host, out_host
            status = connection.status

            if options['show_outgoing_localhost'] == False and out_host == '127.0.0.1':
                continue

            if options['show_closed_connections'] == False and status == 'CLOSE':
                continue

            if options['noresolve'] == False:
                in_host = host_resolve(in_ip)
                out_host = host_resolve(out_ip)

            in_full = "%s:%s" % (in_host, in_port)
            out_full = "%s:%s" % (out_host, out_port)

            if options['search']:
                if fnmatch(out_full, options['search']):
                    print_queue.append(pprint_connection(status, in_full, out_full))
            else:
                print_queue.append(pprint_connection(status, in_full, out_full))

        if len(print_queue) > 0:
            print "%6d | + %s" % (pid, name)
            print "\n".join(print_queue)
