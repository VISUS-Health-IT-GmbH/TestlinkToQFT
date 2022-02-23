#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cherrypy

import app.TestlinkApplication as TestlinkApplication
import app.TestlinkFileWriter as XMLWriter
import app.TestlinkConfig as TestlinkConfig
import util.TestlinkStringHelper as Helper
import data.TestlinkTestcase as TestCase
import data.TestlinkTeststep as TestStep


# ======================================================================================================================
#   Server-Tools
# ======================================================================================================================
def secure_headers():
    """
    Security headers

    1) Strict-Transport-Security            -> HTTPS only
    2) X-Frame-Options                      -> NO embedding 
    3) X-XSS-Protection                     -> NO Cross Site Scripting
    4) Content-Security-Policy              -> Shield from attacks
    5) Server                               -> empty cherry-py server field
    6) X-Permitted-Cross-Domain-Policies    -> Forbid cross-domain shenanigans
    """

    cherrypy.response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    cherrypy.response.headers["X-Frame-Options"] = "DENY"
    cherrypy.response.headers["X-XSS-Protection"] = "1; mode=block"
    cherrypy.response.headers["Content-Security-Policy"] = "default-app 'self'"
    cherrypy.response.headers["Server"] = "none"
    cherrypy.response.headers["X-Permitted-Cross-Domain-Policies"] = "none"


def CORS():
    """ Handles CORS (Cross-Origin-Resource-Sharing) for Frontend(JavaScript)-Requests
        and permits use of "Name"-Header"""

    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    cherrypy.response.headers["Access-Control-Expose-Headers"] = "Name"


# ======================================================================================================================
#   Server-Configuration
# ======================================================================================================================
root_path = os.path.dirname(os.path.abspath(__file__))

# Config across REST-API
rest_config = {
    "/": {
        "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
        "tools.CORS.on": True,
	"tools.response_headers.on": True
    }
}


# ======================================================================================================================
#   MAIN-Routine
# ======================================================================================================================
if __name__ == "__main__":
    # 0) init config and app objects
    config = TestlinkConfig.TestlinkConfig()
    app = TestlinkApplication.TestlinkApplication(config)

    # 1) Expose url
    # ==========================
    cherrypy.tree.mount(app, "/tl2qft", config=rest_config)

    # 2) Advanced config
    # ===========================
    cherrypy.tools.secureheaders = cherrypy.Tool("before_finalize", secure_headers, priority=60)
    cherrypy.tools.CORS = cherrypy.Tool("before_handler", CORS)

    cherrypy.config.update({
        "server.socket_port": 3110,
        "server.socket_host": "0.0.0.0"
    })

    # 3) Start server
    # =================
    cherrypy.engine.start()
    cherrypy.engine.block()
