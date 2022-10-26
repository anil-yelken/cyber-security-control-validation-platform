from spyne import Application, rpc, ServiceBase, Iterable, Integer, String
import sqlite3
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import subprocess

class webservis(ServiceBase):
    @rpc(String , _returns=String)
    def query(ctx, name):
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("select * from test where username = '%s'" % name )
        data=str(cur.fetchall())
        con.close()
        import logging
        logging.basicConfig(filename="soap_server.log", filemode='w', level=logging.DEBUG)
        logging.debug(data)
        return(data)

    @rpc(String, _returns=String)
    def get_users(ctx,name):
        try:
            command="grep "+name+" /etc/passwd"
            data= subprocess.check_output(command,shell=True)
            import logging
            logging.basicConfig(filename="soap_server.log", filemode='w', level=logging.DEBUG)
            logging.debug(str(data))
            return(str(data))
        except:
            data=str(name)+" username didn't found"
            logging.debug(data)
            return(data)

    @rpc( _returns=String)
    def get_log(ctx):
        try:
            command="cat soap_server.log"
            data=subprocess.check_output(command,shell=True)
            return(str(data))
        except:
            return("Command didn't run")

    @rpc(_returns=String)
    def deserialization(ctx):
        try:
            import socket, pickle
            HOST = "0.0.0.0"
            PORT = 8001
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                connection, address = s.accept()
                with connection:
                    received_data = connection.recv(1024)
                    pickle.loads(received_data)
                    return("connection ok")
        except:
            return("You must connect 8001 port")

    @rpc(String, _returns=String)
    def read_file(ctx,file):
        file = open(file, "r")
        data = file.read()
        file.close()
        import logging
        logging.basicConfig(filename="soap_server.log", filemode='w', level=logging.DEBUG)
        logging.debug(data)
        return(data)

    @rpc(String, _returns=String)
    def get_admin_mail(ctx,control):
        if control=="admin":
            data="admin@cybersecurity.intra"
            import logging
            logging.basicConfig(filename="soap_server.log", filemode='w', level=logging.DEBUG)
            logging.debug(data)
            return(data)
        else:
            return("Control didn't set admin")

    @rpc(String,String, _returns=String)
    def create_file(ctx,filename,text):
        try:
            file=open(filename,"w")
            file.write(text)
            file.close()
            return("File created")
        except:
            return("File didn't create")

    @rpc(String,_returns=String)
    def run_file(ctx, filename):
        try:
            command="/bin/bash "+filename
            data=subprocess.check_output(command,shell=True)
            return(data)
        except:
            return("File failed to run")

application = Application([webservis], 'spyne.examples.web.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server
    import logging
    logging.basicConfig(filename="soap_server.log",filemode='w',level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    server = make_server('0.0.0.0', 8000, wsgi_application)
    server.serve_forever()
