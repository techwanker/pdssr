sphinx-quickstart --sep  --project=pdsutil --author "Jim Schmidt, Pacific Data Services" --version "0.0.3" \
  --ext-autodoc --ext-todo
#-q, --quiet
#    Quiet mode that will skips interactive wizard to specify options. This option requires -p, -a and -v options.
#-h, --help, --version
#    Display usage summary or Sphinx version.
#Structure options
#--sep
#    If specified, separate source and build directories.
#--dot=DOT
#    Inside the root directory, two more directories will be created; 
#    “_templates” for custom HTML templates and “_static” for custom stylesheets and other static files. 
#    You can enter another prefix (such as ”.”) to replace the underscore.
#
#Project basic options
#-p PROJECT, --project=PROJECT
#    Project name will be set. (see project).
#-a AUTHOR, --author=AUTHOR
#    Author names. (see copyright).
#-v VERSION
#    Version of project. (see version).
#-r RELEASE, --release=RELEASE
#    Release of project. (see release).
#-l LANGUAGE, --language=LANGUAGE
#    Document language. (see language).
#--suffix=SUFFIX
#    Source file suffix. (see source_suffix).
#--master=MASTER
#    Master document name. (see master_doc).
#--epub
#    Use epub.
#
#

 sphinx-build -b dirhtml . sphinx-doc *.py
