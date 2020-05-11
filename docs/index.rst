.. pdssrpdssr documentation master file, created by
   sphinx-quickstart on Sat Apr 29 07:50:57 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Indices and tables
==================

* :ref:`search`
* :ref:`genindex`
* :ref:`modindex`

Pacific Data Services - Sales Reporting
=======================================


This project, pdssr (Pacific Data Services - Sales Reporting), 
is an example showcase
for pdsutil (Pacific Data Services Utilities)

Any distributor currently writing files in the CDS reporting format can easily load files 
into a local database in order to analyze the data.

We have provided many analyses that report data worthy of further inspection.

This approach is our "answers to questions you should have asked".

Features
========

* Load standard reporting files into ETL (Extract Transform and Load) tables in a relational database

* Process Condition Identification against the loads for inconsistencies such as
* Post the load information
* Extract load files into
  * CDS reporting format
  * CSV
  * JSON
  * XML
  * Python Objects
    * List of Lists
    * List of Tuples
    * List of Dictionary
  * Excel Spreadsheets
* Data Analysis
  * Top Customers
  * Customer Call Reporting
  * ARIMA
* Custom Spreadsheets
* Compute Rebates
* Generate ACH Files for rebate payment
  This saves the cost of printing and mailing checks.
* JSON RPC Server and Client
* Address Validation, Standardization and Correction
* Geo Location
* VCF
* Database Support

  * Oracle
  * Postgres
  * MySql
  * sqlite


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   pdssr
   cds_record_layout
