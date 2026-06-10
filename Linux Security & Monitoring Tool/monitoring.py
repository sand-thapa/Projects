# monitoring.py

import psutil
import time     # CPU -> sleep and measure the cpu usage in CPU


def cpu():
    # ---------- NUMBER 1, GET CPU INFORMATION ----------
    print("CPU")

    # get the percent usage for each core over a 1 second interval
    corePercentages = psutil.cpu_percent(interval = 1, percpu=True)

    # header
    print("CPU Core Usage Over 1 Second") 
    print("-"*20)

    # "count" to keep track of the core #, "highAlert" to display if usage is too high
    count = 0 
    highAlert = False 
    for percentages in corePercentages: 
        count += 1  

        print(f"Core {count:<5} {percentages}%")
        if percentages >= 90: 
            highAlert = True 
    
    totalUsage = sum(corePercentages)/len(corePercentages)
    print(f"Total Usage: {totalUsage:.3}%")    # call cpu_percent(None) for each process, acts as a stopwatch to measure
    
    
    # if usage is too high, print out the heaviest processes 
    if highAlert:

        #header
        print() 
        print("ALERT: At least one core has high utilization!")
        print("Note high utilization could be due to browser tabs, driver issues, hung processes or background indexing ex. syncing cloud storage.")  
        print("If you do not recognize these high utilization processes and they persist be wary of possible malware/ransomware") 
        print("High Utilization Processes:")

        # the cpu usage, this first call would start the stopwatch and we sleep for a second
        for p in psutil.process_iter(): 
            p.cpu_percent(None) 
        time.sleep(1) 

        # try except is more secure in the case that a process exits while we are iterating
        # iterate through each process and store its information into top
        top = [] 
        for p in psutil.process_iter(): 
            try: 
                top.append(
                    (
                        p.pid,
                        p.name(),
                        p.cpu_percent(None)
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied): 
                pass

        # sort top properly based on its cpu_percent after iteration
        # and reverse it so the list goes greatest to least
        top.sort(key = lambda x: x[2], reverse = True) 

        # slice so that we are only looking at 10 processes max
        top = top[:10]

        # print out the processes
        for pid, name, cpu in top: 
            if cpu > 0:
                print(f"{cpu:5.1f}% {pid:6} {name}")
    
    # if there is no high usage but the user wants to view the heaviest processes anyways
    # use the same logic as high utilization with user input at the beginning
    seeProcesses = input("Do you want to view the heaviest processes? Yes=1 No=0 ")
    
    if seeProcesses == '1':
        # the cpu usage, this first call would start the stopwatch and we sleep for a second
        for p in psutil.process_iter(): 
            p.cpu_percent(None) 
        time.sleep(1) 

        top = [] 
        for p in psutil.process_iter(): 
            try: 
                top.append(
                    (
                        p.pid,
                        p.name(),
                        p.cpu_percent(None)
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied): 
                pass
        
        top.sort(key = lambda x: x[2], reverse = True) 
        top = top[:10]

        for pid, name, cpu in top: 
            if cpu > 0:
                print(f"{cpu:5.1f}% {pid:6} {name}")


def ram():
    # ---------- NUMBER 2, GET RAM INFO ----------
    # get RAM info 
    print("RAM")
    ram = psutil.virtual_memory() 
    print(f"Total RAM (bytes): {ram.total}\nApprox GB: {ram.total/1000000000:.2f}") 
    print(f"Ram Available (bytes): {ram.available}\nApprox Available GB: {ram.available/1000000000:.2f}")
    print(f"Ram Usage: {ram.percent}%\n") 


def battery():
    # ---------- NUMBER 3, CHECK BATTERY AND IF CHARGING ----------
    #Battery Percentage
    battery = psutil.sensors_battery() 
    print("BATTERY") 
    print(f"Battery Percentage: {battery.percent:.2f}%") 
    print(f"Currently Charging: {battery.power_plugged}") 


def processes():
    # ---------- NUMBER FOUR, RUNNING PROCESSES ----------
    # Store all pids in pids variable, then loop through 10 of them and print the number and name 
    # unless the access to that process is denied
    pids = psutil.pids() 
    # Print running process pids (up to 10)
    for pid in pids:
        proc = psutil.Process(pid)
        try: 
            print(f"{pid:<5} | {proc.name()}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print(f"{pid:<5} | [Access Denied / Stopped]")


def diskUsage():
    # ---------- NUMBER 5, DISK USAGE ---------
    # get all the partitions (/, /home, /boot, etc) and loop through
    partitions = psutil.disk_partitions(all=False)
    for p in partitions:
        # get the disk usage for the current partition
        usage = psutil.disk_usage(p.mountpoint)


        print(f"Device: {p.device}\tMountpoint: {p.mountpoint}\tType: {p.fstype}")
        print(f"Total Storage GB: {usage.total/1000000000:.2f}") 
        print(f"Used GB: {usage.used/1000000000:.2f}")
        print(f"Available GB: {usage.free/1000000000:.2f}\n") 
