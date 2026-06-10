# security.py

import subprocess                       # needed for logs since fedora uses systemd journal
from collections import defaultdict     # needed to initialize the failed IPs
import re                               # in order to check for "BUG" in logs


def logs():
    # ---------- LOGS ----------
    numLogs = input("Please enter number of logs to parse: ")
    logs = subprocess.check_output(
        ["journalctl", "-n", numLogs, "--no-pager"], 
        text = True
    )
    
    failedLogins = 0 
    suspiciousIP = set()  
    sshLogs = []

    # use lambda to initialize a new entry with count and set 
    # to keep track of attempts and usernames for each ip
    failedIP = defaultdict(lambda: [0, set()])
    for line in logs.splitlines(): 
        if "Failed password" in line or "Invalid user" in line: 
            failedLogins += 1
            sshLogs.append(line) 
            words = line.split() 

            # grab the attempt IP and append it to the failed IPs
            if "from" in words:
                attemptIP = words[words.index('from') + 1]
            else: 
                attemptIP = "Unknown" 

            # handle usernames for invalid or valid case
            if "invalid user" in line.lower():
                username = words[words.index('user') + 1] 
            elif "for" in words: 
                username = words[words.index('for') + 1]
            else:
                username = "Unknown" 

            # update attempt number for IP
            failedIP[attemptIP][0] += 1
            # add the username to the set of them
            failedIP[attemptIP][1].add(username)
            #mark suspicious
            if (failedIP[attemptIP][0] > 2 and attemptIP not in suspiciousIP):
                suspiciousIP.add(attemptIP) 

            
    
    sudoCount = 0 
    for line in logs.splitlines(): 
        if "sudo:" in line: 
            sudoCount += 1 

    # one way to create that if statement
    sshCount = 0 
    for line in logs.splitlines(): 
        if "Accepted password" in line or \
        "Accepted publickey" in line:
            sshCount += 1
            sshLogs.append(line) 


    
    # different way to do it
    crashCount = 0
    crashLogs = []
    for line in logs.splitlines(): 
        if any(term in line for term in [
            "segfault", 
            "core dumped",
            "crashed"
        ]): 
            crashCount += 1 
            crashLogs.append(line)

    kernelErrors = 0 
    kernelLogs = []
    for line in logs.splitlines():
        if (
            any(term in line for term in [
                "kernel panic",
                "I/O error",
                "Oops:",
                "Call Trace:",
                "hardware error",
                "MCE:"
            ]) 
            or re.search(r"\bBUG\b", line)
        ): 
            kernelErrors += 1
            kernelLogs.append(line)

    securityScore = 100 
    securityScore -= failedLogins * 2 
    securityScore -= crashCount * 5 
    securityScore -= kernelErrors * 10 

    securityScore = max(securityScore, 0) 

    print('-'*10, " Security Analysis ", '-'*10)
    print() 
    print(f"Failed Logins:   {failedLogins}") 
    print(f"SSH Logins:   {sshCount}")
    print(f"Sudo Events:   {sudoCount}") 
    print(f"Kernel Errors:   {kernelErrors}")

    print(f"Security Score:  {securityScore}/100")
    if (failedLogins > 0):
        print("\nLogin Alert:")
        for key in failedIP:
            if key not in suspiciousIP:
                print(f"IP {key} attempted to log in {failedIP[key][0]} time(s) under username(s) {failedIP[key][1]}")
            else: 
                print(f"SUSPICIOUS: IP {key} attempted to log in {failedIP[key][0]} times(s) under username(s) {failedIP[key][1]}")
    
    
    if (failedLogins > 0 or crashCount > 0 or kernelErrors > 0):
        number = 0 
        sshNumber = -1
        crashNumber = -1
        kernelNumber = -1
        print("\nPlease choose any logs you would like to view from below:")
        print("0: None")
        if failedLogins > 0:
            number += 1
            sshNumber = number 
            print(f"{number}: SSH/Login Attempt Logs")
        if crashCount > 0: 
            number += 1
            crashNumber = number 
            print(f"{number}: Crash Logs")
        if kernelErrors > 0:
            number += 1
            kernelNumber = number 
            print(f"{number}: Kernel Errors")
        logNumber = int(input("\nPlease enter a number: "))
        print() 
        if logNumber == sshNumber:
            for lines in sshLogs:
                print(lines)
        elif logNumber == crashNumber:
            for lines in crashLogs: 
                print(lines) 
        elif logNumber == kernelNumber:
            for lines in kernelLogs: 
                print(lines) 
