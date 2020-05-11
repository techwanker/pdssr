#!/usr/bin/env python
import argparse



import logging
from pdssr.SalesReportingAdmin import SalesReportingAdmin

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("sra_main")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--connection_name", required=True, default="it",
                        help="name of database connection")

    SUBPARSERS = PARSER.add_subparsers(dest="command",help='commands')
    SUBPARSERS.required = True

    INITIALIZATION_PARSER = SUBPARSERS.add_parser('initialize',
                                                  help='initialize the database')
    INITIALIZATION_PARSER.set_defaults(method='initialize')

    #
    LOAD_PARSER = SUBPARSERS.add_parser('load', help='loads a fixed length file')
    LOAD_PARSER.add_argument("file_name",
                             help="name of CDS reporting format file")
    LOAD_PARSER.add_argument("--distributor_cd", required=True,
                             help="distributor code")

    #
    LOAD_CONDITION_PARSER = SUBPARSERS.add_parser("load_condition")
    LOAD_CONDITION_PARSER.add_argument("--command", default="load_condition")
    LOAD_CONDITION_PARSER.add_argument("etl_file_id",
                                       help="load identifier (etl_file_id)")
    LOAD_CONDITION_PARSER.add_argument('--rerun', action='store_true')
    LOAD_CONDITION_PARSER.set_defaults(rerun=False)
    #
    #
    POST_PARSER = SUBPARSERS.add_parser("post", help="post a load")
    POST_PARSER.add_argument("etl_file_id",
                             help="load identifier to be posted")


    #
    UNLOAD_PARSER = SUBPARSERS.add_parser("unload", help="extract a load")
    UNLOAD_PARSER.add_argument("etl_file_id", help="load identifier to be unloaded")
    UNLOAD_PARSER.add_argument("--file", required=True, help="destination file for unload")
    #UNLOAD_PARSER.add_argument("--connection_name", required=False, default="test",
    #                    help="name of database connection")
    #
    TO_CSV_PARSER = SUBPARSERS.add_parser("to_csv", help="convert a load file to a set of csv files")

    TO_CSV_PARSER.add_argument("--output_dir",
                               help="output directory")
    TO_CSV_PARSER.add_argument("--input_file", required=True, help="input file to be split")

    #
    # This is all relative stuff TODO make this work
    # webserver_parser = subparsers.add_parser("webserver")
    # webserver_parser.add_argument("--command", default="webserver")
    #  TODO find a way to make this immutable
    # webserver_parser.add_argument("--port", required=False,
    # default=8090, help="ip port to listen on")

    #
    WEBSERVICES_PARSER = SUBPARSERS.add_parser("webservices", help="start webservices")
    # TODO find a way to make this immutable
    WEBSERVICES_PARSER.add_argument("--port", required=False,
                                    default=8091, help="ip port to listen on")
    WEBSERVICES_PARSER.set_defaults(command="webservices")

    ARGS = PARSER.parse_args()
    ###
    ADMIN = SalesReportingAdmin(ARGS.connection_name)
    LOGGER.debug("ARGS %s" % ARGS)
    if ARGS.command == "initialize":  # TODO create map of command to function
        ADMIN.initialize(connection_name=ARGS.connection_name)
    elif ARGS.command == "load":
        ADMIN.load_file(ARGS.file_name, ARGS.distributor_cd)
    elif ARGS.command == "load_condition":
        ADMIN.dataload_conditions(int(ARGS.etl_file_id),rerun=ARGS.rerun)
    elif ARGS.command == "post":
        ADMIN.post(int(ARGS.etl_file_id))
    elif ARGS.command == "to_csv":
        ADMIN.to_csv(ARGS.input_file,ARGS.output_dir)
    elif ARGS.command == "unload":
        LOGGER.info("about to unload")
        ADMIN.unload(int(ARGS.etl_file_id),ARGS.file)
        LOGGER.info("done unload")
    elif ARGS.command == "webservices":
        ADMIN.web_services(ARGS.port)
    else:
        raise Exception("Logic error")


