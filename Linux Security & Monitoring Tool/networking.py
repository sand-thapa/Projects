# networking.py

import psutil
import nmap
import socket

def networking():
    # ---------- NUMBER 6, NETWORKING ----------

    # network stats 
    print("[1] Check Connection\n[2] Check Interface IP Addr\n[3] Active Connections & Ports\n[4] Port Scanner") 
    useCase = int(input("Please enter a number: ")) 

    # USE CASE 1, CONNECTION CHECK
    if (useCase == 1):
        # CHECK FOR CONNECTION
        print("-"*15,"Network Connection Status", "-"*15)
        print() 


        # queries for dictionary of net interfaces (eth0 or wlan0) + status
        connection = psutil.net_if_stats() 

        # use net_io_counters to get network in/out stats and pernic=True to 
        # have them in a dictionary where interface is the key
        ioData = psutil.net_io_counters(pernic=True)
        for interface, stats in connection.items(): 
            status = "CONNECTED" if stats.isup else "DISCONNECTED"

            # get the bytes for the interface (if exists) in the traffic data
            
            if interface in ioData: 
                bytesSent = ioData[interface].bytes_sent 
                bytesRecv = ioData[interface].bytes_recv 
                print(f"Interface: {interface} | Status: {status} | Sent: {bytesSent:,} B | Recv: {bytesRecv:,} B")
            else: 
                print(f"Interface {interface} | Status: {status}") 
            

    # USE CASE 2, INTERFACE IP ADDR 
    if (useCase == 2):
        # INTERFACE IP ADDRESS
        print("-"*15, "Interface IP Addresses", "-"*15)
        address = psutil.net_if_addrs() 
        for interface, addrs in address.items(): 
            for addr in addrs: 
                if addr.family == socket.AF_INET: 
                    print(f"Interface: {interface} | IPv4 Address: {addr.address}") 

    # USE CASE 3 ACTIVE CONNECTIONS AND LISTENING PORTS
    if (useCase == 3): 

        print("-"*15, "Active Connections & Listening Ports", "-"*15)
        print()

        # set up the table using these bottom two lines
        print( f"{'Protocol':<10} {'Local Address':<22} {'Remote Address':<22} {'Status':<15} {'PID/Name'}" ) 
        print('-'*80)

        # get all the connections
        connections = psutil.net_connections(kind='inet') 

        # loop through all the connections
        for conn in connections[:10]:
            # formatting the endpoints
            localAddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A" 
            remoteAddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"

            procInfo = "N/A" 
            if conn.pid:
                try: 
                    procInfo = f"{conn.pid}/{psutil.Process(conn.pid).name()}"
                except (psutil.NoSuchProcess, psutil.AccessDenied): 
                    procInfo = f"{conn.pid}/Unknown" 
            
            proto = "TCP" if conn.type == 1 else "UDP" 

            print(f"{proto:<10} {localAddr:<22} {remoteAddr:<22} {conn.status:<15} {procInfo}") 

    # USE CASE 4: PORT SCANNER
    if (useCase == 4):
        print("-"*15, "Port Scanner", "-"*15)
        print()

        targetIP = input("Please provide a target IP to scan, or 0 to scan yourself: ").strip()

        # ports to scan - 21, 22, 23, 25, 53, 80, 110, 139/445, 143, 443, 3306, 3389, 8080, 

        if targetIP == "0":
            targetIP = "127.0.0.1" 
        
        portList = ["21", "22", "23", "25", "53", "80", "110", "139", "143", "443", "3306", "3389", "8080"] 
        scanningPorts = ",".join(portList) 

        print(f"Starting scan on {targetIP}\n")
        nm = nmap.PortScanner()
        nm.scan(targetIP, scanningPorts, arguments='-Pn -sT -sV')

        print(f"Hostname: {nm[targetIP].hostname()}")
        print("-"*20)
        
        for port in nm[targetIP]['tcp']:
            info = nm[targetIP]['tcp'][port] 
            state = info['state'] 
            service = info.get('name','unknown') 
            running = info.get('product','')
            version = info.get('version', '') 

            # clean spacing
            print(f"{f'Port: {port}':<15} {f'State: {state}':<18} {f'Service: {service}':<22} Running: {running} {version}")            
