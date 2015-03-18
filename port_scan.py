import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

def conn_scan(tgt_host, tgt_port):
    try:
        conn_skt = socket(AF_INET, SOCK_STREAM)
        conn_skt.connect((tgt_host, tgt_port))
        conn_skt.send('asdfasdfadsfa\n\r')
        results = conn_skt.recv(100)
        screenLock.acquire()
        print '[+] {0}/tcp open'.format(tgt_port)
        print '[+] {0}'.format(results)
    except:
        screenLock.acquire()
        print '[-] {0}/tcp closed'.format(tgt_port)
    finally:
        screenLock.release()
        conn_skt.close()

def port_scan(tgt_host, tgt_ports):
    try:
        tgt_ip = gethostbyname(tgt_host)
    except:
        print '[-] Cannot resolve {0}: Unknown host'\
          .format(tgt_host)
        return

    try:
        tgt_name = gethostbyaddr(tgt_ip)
        print '\n[+] Scan results for: {0}'.format(tgt_name[0])
    except:
        print '\n[-] Scan Results for: {0}'.format(tgt_ip)

    setdefaulttimeout(1)

    for tgt_port in tgt_ports:
        print 'Scanning port {0}'.format(tgt_port)
        t = Thread(target=conn_scan, args=(tgt_host, tgt_port))
        t.start()

def main():
    parser = optparse.OptionParser('usage %prog '+\
        '-H <target host> -p <target port>')

    parser.add_option('-H', dest='tgt_host', type='string',\
        help='specify target host')
    parser.add_option('-p', dest='tgt_port', type='string',\
        help='specify target port[s] separated by comma')

    (options, args) = parser.parse_args()

    tgt_host = options.tgt_host
    tgt_ports = str(options.tgt_port).split(',')

    if (tgt_host == None) | (tgt_ports[0] == None):
        print '[-] You must specify a target host and port[s].'
        exit(0)

    port_scan(tgt_host, tgt_ports)


if __name__ == '__main__':
    main()
