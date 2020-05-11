#!/usr/bin/env python
# coding: utf-8
# https://pypi.python.org/pypi/python-jsonrpc
import pyjsonrpc


# TODO consolidate with SalesReportingAdmin
class WebServices(pyjsonrpc.HttpRequestHandler):
    """
    Provices json rpc servcies
    """

    # @pyjsonrpc.rpcmethod
    # def add(self, a, b):
    #     print str(self)
    #     """Test method"""
    #     return a + b

    @pyjsonrpc.rpcmethod
    def validate_load(self, etl_file_id):
        """
        validate a load file
        :param etl_file_id:
        :return:
        """
        from pdssr.CdsDataloadConditions import CdsDataloadConditions
        import pdsutil.DbUtil
        conn = pdsutil.DbUtil.get_named_connection("current")  # TODO externalize
        co = CdsDataloadConditions()
        print (co.process_load(conn, etl_file_id))
        buffer = ""
        for msg in co.get_messages():
            buffer += msg + "\n"

        return buffer

        # Threading HTTP-Server


if __name__ == "__main__":
    http_server = pyjsonrpc.ThreadingHttpServer(
        server_address=('localhost', 8081),
        RequestHandlerClass=WebServices
    )
    print ("Starting HTTP server ...")
    print ("URL: http://localhost:8081")  # TODO  get from settings
    http_server.serve_forever()
