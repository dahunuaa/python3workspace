# -*-coding:utf-8 -*-
import sys
import traceback
from tornado.web import url
from baosteel100.libs.loglib import get_logger

logger = get_logger("bootstrape")

def generate_handler_patterns(root_modules,handler_names,out_handlers,prefix=""):
    for name in handler_names:
        try:
            module_name = "%s.%s"%(root_modules,name)
            __import__(module_name)
            logger.debug("Import %s success"%module_name)
            module = sys.modules[module_name]
            module_handlers = getattr(module,"handlers",None)

            if module_handlers:
                _handlers = []
                for handler in module_handlers:
                    try:
                        patten = r"/%s/%s%"%(prefix,root_modules.split(".")[-1],handler[0])
                        if len(handler)==2:
                            _handlers.append(patten,
                                             handler[1])
                        elif len(handler)==3:
                            _handlers.append(url(patten,
                                                 handler[1],
                                                 {"provider":handler[2]})
                                             )
                        else:
                            pass
                    except IndexError:
                        pass
                out_handlers.extend(_handlers)
            return out_handlers
        except:
            logger.error("Import %s error" %module_name)
            logger.error(traceback.format_exc())

def autoload_models(root_module,modelnames):
    for name in modelnames:
        module_name = "%s.%s"%(root_module,name)
        __import__(module_name)
        logger.debug("Import %s success"%module_name)

