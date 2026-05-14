# OPC UA Practical Implementation

This repository contains a practical OPC UA monitoring demo using Prosys OPC UA Simulation Server, Python, and Node-RED.

## System Architecture

```text
Prosys OPC UA Simulation Server
        ↓ OPC UA
Python OPC UA Client / Edge Gateway
        ↓ HTTP POST + JSON
Node-RED Receiver
        ↓
Node-RED Dashboard / HMI
