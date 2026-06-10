# main.py

from monitoring import cpu, ram, battery, processes, diskUsage
from networking import networking
from security import logs

def main():
    # ---------- HEADER ----------
    print("Welcome to Toolkit!") 
    # maybe add a while 1 and break when 0 inputted
    print("Enter a setting number, or 0 to exit\n") 
    print("[1] CPU Usage\n[2] RAM\n[3] Battery\n[4] Running PIDs\n[5] Disk Drive Stats\n[6] Network Information\n[7] Log Parsing\n[0] Exit\n")
    
    try:
        number = int(input("Please enter your number: ")) 
    except ValueError:
        print("Invalid input.")
        return
    # Header is all good just change up the print line when another feature is added
    
    # maybe add while loop, -1 to exit
    match number: 
        case 1:
            cpu() 
        case 2:
            ram() 
        case 3:
            battery() 
        case 4:
            processes() 
        case 5: 
            diskUsage() 
        case 6: 
            networking() 
        case 7:
            logs() 
        case 0: 
            print("Goodbye!")
            return 


if __name__ == "__main__":
    main() 
