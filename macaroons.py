#!/usr/bin/env python3
import lightning
import json
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc.exceptions import JSONRPCMethodNotFound
from jsonrpc.jsonrpc2 import JSONRPC20Response


# Initialise the plugin
plugin = lightning.Plugin()


plugin.add_option(
    name="json-rpc-port",
    default=None,
    description="A port for the JSON-RPC macaroon interface to use",
    opt_type="int",
)


@plugin.method("method_name")
def method_name(plugin=None):
    """A dummy method
    """
    ...


@Request.application
def application(request):
    # First we get the macaroon

    # Load the request and setup the function call
    ln_request = json.loads(request.data.decode("utf-8"))
    func = getattr(plugin.rpc, ln_request["method"])

    # Next we check the call is valid per this macaroon

    # If valid, attempt the call
    try:
        if ln_request["params"]:
            response = func(ln_request["params"])
        else:
            response = func()
    except lightning.RpcError:
        print(f"Method not found")
        response = JSONRPC20Response(
            error=JSONRPCMethodNotFound()._data, request=ln_request
        )
        return Response(response.json, mimetype="application/json")

    # Undo "helpful" millisat conversions
    for k, v in response.items():
        if type(v) == lightning.Millisatoshi:
            response[k] = v.millisatoshis

    return Response(json.dumps(response), mimetype="application/json")


@plugin.init()
def init(options, configuration, plugin):
    print("Starting macaroon plugin")

    # Show the user new RPCs available from the plugin
    commands = list(plugin.methods.keys())
    commands.remove("init")
    commands.remove("getmanifest")
    print(f"New RPC commands available: {commands}")
    print(f"Macaroon plugin config file options: {options}")

    # Start the basic server
    run_simple("localhost", int(options["json-rpc-port"]), application)


plugin.run()
