from AlinLog.models import ProRunTimeLog
import traceback
import sys


def except_handle(e):
    print e
    _, _, exc_tb = sys.exc_info()
    origin_mes = traceback.format_exc()
    eline = ''
    efile = ''
    elinenum = ''
    for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
        efile = filename
        elinenum = linenum
        eline += "%s:line num : %s '%s' in %s\n" % (filename, linenum, source, funcname)
    newprolog = ProRunTimeLog(error_file=efile, error_line=elinenum, origin_message=origin_mes, err_message=eline)
    print newprolog.err_message
    print newprolog.error_file
    newprolog.save()