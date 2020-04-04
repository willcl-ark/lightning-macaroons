import requests
import json

ECHO_STR = "C-Lightning Macaroon RPC!"


def main():
    url = "http://localhost:19745/jsonrpc"

    payload = {
        "method": "getbalance",
        "params": [],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.get(url, json=payload).json()
    print(response)

    payload = {
        "method": "listfunds",
        "params": [],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.get(url, json=payload).json()
    print(response)


if __name__ == "__main__":
    main()
