# Linux Security & Monitoring Tool

Python based CLI Linux tool focused on monitoring and security analysis. Provides
hardware monitoring, assists in system troubleshooting, running processes, network
activity, port scanning, and log parsing with an integrated security score. 
Developed to practice with Linux, Python, networking, and security monitoring.  	

--------------------

## Features:

### SYSTEM MONITORING:
CPU Utilization Monitoring and Troubleshooting - 
 - Measures CPU usage for each core
 - When usage is high an alert is given and the heaviest processes
   (sorted top down) are shown with the pid, name, and usage percentage
CPU Stress testing to ensure functionality
RAM Utilization Monitoring - 
 - Total amount, bytes available, and usage

Battery Status Monitoring - 
 - Battery percentage and charging status

Disk Usage Analysis - 
 - Goes through disk partitions and gets the total storage, usage, and available GB

Display of Running Processes - 
 - Prints all running processes and their PIDs


### NETWORKING:
 - Check Connection with status, interface, bytes sent and received
 - Check interface IP address
 - Check active connections and listening ports (protocol, local address with 
   port, remote address, status (listening, none, established, pid/name)
 - Port scanner to either scan yourself or a different ip (scans specific ports,
   shows states, shows services, product, and version being ran)


### LOGS ANALYSIS:
 - Go through the amount of logs inputted by the user
 - Gives a security score out of 100 based on number of failed logins, crash count,
   and kernel errors
 - For failed ssh logins: prints the request IP and number of attempts with host
   names used, for 3 or more failed ssh attempts, the IP is labeled as suspicious
 - If there are events that lower the overall security score, the user can choose
   choose one of the events to see the logs associated with it 

--------------------

## INSTALLATION:
Clone repository
Install dependencies using: pip install -r requirements.txt
Run the toolkit: pythoon main.py

--------------------

## TECHNOLOGIES USED: 
Python 3
Linux (Fedora) (main device)
Windows 11 (testing/attacking device)
python-nmap
psutil
journalctl
regex

--------------------

## PROJECT STRUCTURE: 
|- main.py
|- monitoring.py
|- networking.py
|- security.py
|- requirements.txt
|- README.md

--------------------

## USAGE: 
Run the toolkit using 
python main.py

Select one of the options from the menu: 

[1] CPU Usage
[2] RAM
[3] Battery
[4] Running PIDs
[5] Disk Drive Stats
[6] Network Information
[7] Log Parsing
[0] Exit

--------------------

## TESTING:

CPU Stress Testing - 
Stress tested the CPU in order to get high usage levels. Then ran the program during
this and was able to successfully get an error message as well as heavy 
processes list.

Failed SSH Authentication - 
A second machine was used to attempt invalid SSH logins against the Fedora host in
order to generate failure logs.

For example:
ssh fakeuser@hostip

Once these logs were generated, the program was able to identify them and pull the
information that we needed.

Successful SSH Authentication - 
Successful SSH logins were also performed to verify the proper auditing of these 
events.

Sudo Activity Testing - 
Administrative commands were executed in the terminal, these events were properly
detected when the logs were parsed.

Log Injection Testing -
Custom log events were generated to ensure that kernel errors were being caught

Ex. 
logger "kernel panic" 
logger "BUG"

Network Testing - 
Port scanning and active connection monitoring were tested. Ports such as port 22
was opened for ssh testing on the host machine. The port was shown to be listening
for connections when the host device scanned itself. Port 22 was then opened on
the Windows machine and the Linux host was able to properly display that the port
was listening. 

--------------------

## LEARNED: 
During the development process I gained experience in 
 - Linux system administration
 - Process monitoring
 - Network analysis
 - Port scanning
 - Security event detection
 - Journal log investigation
 - Python automation
 - Regular expressions
 - Blue teaming
 - Troubleshooting and testing

--------------------

## FUTURE IMPROVEMENTS: 
 - Real time monitoring
 - UI/UX development with dashboard integration
 - Report storage
 - SIEM Integration
