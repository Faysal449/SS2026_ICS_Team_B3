
import asyncio
import json
import urllib.request
from datetime import datetime

from asyncua import Client


OPC_ENDPOINT = "opc.tcp://localhost:53530/OPCUA/SimulationServer"
NODE_RED_URL = "http://127.0.0.1:1880/opcua-data"

NODES = {
    "counter": "ns=3;i=1002",
    "sinusoid": "ns=3;i=1004",
    "triangle": "ns=3;i=1006",
}


def send_to_node_red(data):
    json_data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        NODE_RED_URL,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            return response.status
    except Exception as error:
        print("Node-RED send error:", error)
        return None


async def main():
    print("Connecting to OPC UA server...")
    print("Endpoint:", OPC_ENDPOINT)

    async with Client(url=OPC_ENDPOINT) as client:
        print("Connected successfully!")
        print("Sending OPC UA values to Node-RED...\n")

        while True:
            data = {
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }

            for name, node_id in NODES.items():
                try:
                    node = client.get_node(node_id)
                    value = await node.read_value()
                    data[name] = float(value)
                except Exception as error:
                    data[name] = None
                    print(f"{name}: ERROR -> {error}")

            status = send_to_node_red(data)

            print("----- OPC UA Live Values -----")
            print(data)
            print("Node-RED HTTP status:", status)
            print()

            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")
