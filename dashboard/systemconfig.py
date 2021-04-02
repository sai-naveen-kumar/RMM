import GPUtil
import platform
import psutil


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
def Sysinfo():
    finaldict={}
    FINAL_OUT=""
    name=platform.system()
    version=platform.version()
    os={'name':name,'version':version}
    finaldict['os']=os
    try:
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = f"{gpu.load*100}%"
            # get free memory in MB format
            gpu_free_memory = f"{gpu.memoryFree}MB"
            # get used memory
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            # get total memory
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            # get GPU temperature in Celsius
            gpu_temperature = f"{gpu.temperature} °C"
            gpu_uuid = gpu.uuid
##            list_gpus.append((
##                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
##                gpu_total_memory, gpu_temperature, gpu_uuid
##            ))
##
##        

        gpu={'gpu_id':gpu_id,'gpu_name':gpu_name,'gpu_load':gpu_load,'gpu_free_memory':gpu_free_memory,'gpu_used_memory':gpu_used_memory,'gpu_temperature':gpu_temperature}
        finaldict["GPU"]=gpu
    except:
        finaldict["GPU"]={"Gpu":"No Gpu Detected"}
        

  


    # let's print CPU information
    
##    # number of cores
##    print("Physical cores:", psutil.cpu_count(logical=False))
##    print("Total cores:", psutil.cpu_count(logical=True))
##    # CPU frequencies
    cpufreq = psutil.cpu_freq()
##    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
##    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
##    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
##    # CPU usage
    cores={}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cores[f"Core {i}"]= f"{percentage}%"
##    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

    cpu={"Physical cores":psutil.cpu_count(logical=False),"Total cores":psutil.cpu_count(logical=True),"Max_Frequency": f"{cpufreq.max:.2f}Mhz","Min Frequency": f"{cpufreq.min:.2f}Mhz","Current Frequency": f"{cpufreq.current:.2f}Mhz",
        "cores":cores,"Total CPU Usage": f"{psutil.cpu_percent()}"
         }
    finaldict["CPU"]=cpu

    # Memory Information

    # get the memory details
    svme={}
    svmem = psutil.virtual_memory()
    svme["Total"]= f"{get_size(svmem.total)}"
    svme["Available"]= f" {get_size(svmem.available)}"
    svme["Used"]= f" {get_size(svmem.used)}"
    svme["Percentage"]= f" {svmem.percent}%"
    # get the swap memory details (if exists)
    swp ={}
    swap= psutil.swap_memory()
    swp["Total"]= f" {get_size(swap.total)}"
    swp["Free"]= f"{get_size(swap.free)}"
    swp["Used"]= f"{get_size(swap.used)}"
    swp["Percentage"]= f" {swap.percent}%"
    
    finaldict["svme"]=svme
    finaldict["swp"]=swp




    # Disk Information
    disk={}
##    print("="*40, "Disk Information", "="*40)
##    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
##        
##        print(f"  Mountpoint: {partition.mountpoint}")
##        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
##        print(f"  Total Size: {get_size(partition_usage.total)}")
##        print(f"  Used: {get_size(partition_usage.used)}")
##w       print(f"  Free: {get_size(partition_usage.free)}")
##        print(f"  Percentage: {partition_usage.percent}%")
        disk[f"Device:{partition.device}"]={"Mountpoint": f"{partition.mountpoint}","File system type":f"{partition.fstype}","Total Size":f"{get_size(partition_usage.total)}","Used":f"{get_size(partition_usage.used)}","Free":f"{get_size(partition_usage.free)}","Percentage":f"{get_size(partition_usage.percent)}"}
    # getIO statistics since boot
    disk_io = psutil.disk_io_counters()
##    print(f"Total read: {get_size(disk_io.read_bytes)}")
##    print(f"Total write: {get_size(disk_io.write_bytes)}")
    disk["total"]={"Total read":f"{get_size(disk_io.read_bytes)}","Total write":f"{get_size(disk_io.write_bytes)}"}




    finaldict["DISK"]=disk


    # Network information
    network={}
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
##            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
##                print(f"  IP Address: {address.address}")
##                print(f"  Netmask: {address.netmask}")
##                print(f"  Broadcast IP: {address.broadcast}")
                network[f"Interface: {interface_name}"]={"IP Address":f"{address.address}","Netmask":f"{address.netmask}","Broadcast IP":f"{address.broadcast}"}
            elif str(address.family) == 'AddressFamily.AF_PACKET':
##                print(f"  MAC Address: {address.address}")
##                print(f"  Netmask: {address.netmask}")
##                print(f"  Broadcast MAC: {address.broadcast}")
                network[f"Interface: {interface_name}"]={"MAC Address":f"{address.address}","Netmask":f"{address.netmask}","Broadcast MAC":f"{address.broadcast}"}
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
##    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
##    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")


    finaldict["network"]=network
    
    return finaldict
    
# Sysinfo()
