import asyncio
from asyncua import Client

OPC_ENDPOINT = "opc.tcp://localhost:53530/OPCUA/SimulationServer"

NODES = {
    "Counter": "ns=3;i=1002",
    "Sinusoid": "ns=3;i=1004",
    "Triangle": "ns=3;i=1006",
}


async def main():
    print("Connecting to OPC UA server...")
    print("Endpoint:", OPC_ENDPOINT)

    async with Client(url=OPC_ENDPOINT) as client:
        print("Connected successfully!\n")

        while True:
            print("----- OPC UA Live Values -----")

            for name, node_id in NODES.items():
                try:
                    node = client.get_node(node_id)
                    value = await node.read_value()
                    print(f"{name}: {value}")
                except Exception as error:
                    print(f"{name}: ERROR -> {error}")

            print()
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user.")
