def report_error(msg, owner='Anonymous', log=None, e=None):
    """report error messages, also handle reporting errors during exception handling."""
    try:
        if not log:
            import logging, logging.handlers
            log = logging.getLogger(owner)
            handler = logging.handlers.SocketHandler('localhost',
                        logging.handlers.DEFAULT_TCP_LOGGING_PORT)
            log.addHandler(handler)
            log.info("Initialized")

        import syslog
        msg = "%s:%s" % (owner, msg)
        log.critical(msg)
        syslog.syslog(syslog.LOG_ERR, msg)
        print msg

        if e:
            try:
                import sys, os
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                errdetails = "%s:%s:%s %s" % (owner, fname, exc_tb.tb_lineno, exc_type)
                log.critical(errdetails)
                syslog.syslog(syslog.LOG_ERR, errdetails)
                print errdetails
            except Exception as e:
                print e, e.__doc__

            err = "%s:%s" % (owner, e.__doc__)
            log.critical(err)
            syslog.syslog(syslog.LOG_ERR, err)
            print err
    except:
        errmsg = "report_error self-destructed handling msg:[%s]" % msg
        try:
            log.error(errmsg)
        except:
            try:
                log.error(errmsg, extra={'uut':None})
            except:
                try:
                    print errmsg
                except:
                    pass


def get_date():
    """return formatted date string"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

