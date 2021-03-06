#!/usr/bin/python

import main.service as service
import socket
import time
import ssl


class Imap(service.Service):


    def get_status(self, destination, port):
        timeout = 1
        request = b"GET / HTTP/1.1\nHost: {}\n\n".format(destination)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)


        if port == 443:
            s_sock = context.wrap_socket(s, server_hostname=destination)
        else:
            s_sock = s
        try:
            start = time.time()
            s_sock.connect((destination, port))
            s_sock.sendall(request)
            resp = s_sock.recv(4096)
            print resp
            return 0, (time.time() - start) * 1000
        except socket.timeout:
            return 1, timeout
        except socket.error as e:
            return 2, timeout, e
        except Exception as error:
            print "ERROR:", error
        finally:
            s_sock.close()


if __name__ == '__main__':
    i = 0
    while i < 1:
        dest = 'www.blognone.com'
        port = 443
        xxx = Imap(1, 99, 69)
        result = xxx.get_status(dest, port)
        print result
        i += 1