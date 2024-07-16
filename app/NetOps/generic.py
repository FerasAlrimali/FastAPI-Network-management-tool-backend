import os
from ..repository.device import DeviceRepository
from ..repository.devicetype import DeviceTypeRepository
import threading
from ..schema import ResponseSchema
from concurrent.futures import ThreadPoolExecutor, as_completed
import collections
# async def get_site_availability(site_id: int):
#     devices = await DeviceRepository.get_all_by_site_id(site_id=site_id, limit=1000)
#     devices = devices.content
#     devicesStatus = []
#     for a_device in devices:
#         if os.system(f"ping -c 1 {a_device['ip']}") == 0:
#             devicesStatus.append({"name":a_device["name"],"ip":a_device["ip"],"type":a_device["device_type"],"status":"UP"})
#         else:
#             devicesStatus.append({"name":a_device["name"],"ip":a_device["ip"],"type":a_device["device_type"],"status":"DOWN"})
#     return devicesStatus

async def get_site_availability_threading(site_id: int):
    devices = await DeviceRepository.get_all_by_site_id(site_id=site_id)
    results=[]
    with ThreadPoolExecutor(max_workers=100) as excuter:
        future_list = []
        for a_device in devices.content:
            future = excuter.submit(get_site_availability, a_device)
            future_list.append(future)
        # Process as completed
        for future in as_completed(future_list) :
            if future.result():
                results.append(future.result())
    return results

def get_site_availability( a_device:dict):
    if os.system(f"ping -c 1 {a_device['ip']}") == 0:
        return {"name":a_device["name"],"ip":a_device["ip"],"type":a_device["device_type"],"status":"UP"}
    else:
        return {"name":a_device["name"],"ip":a_device["ip"],"type":a_device["device_type"],"status":"DOWN"}
    

async def dashboardData(site_id: int):
    result = await get_site_availability_threading(site_id)
    device_types = await DeviceTypeRepository.get_all(limit=100)
    device_types = device_types.content
    #print(f"----------------------->{collections.}")
    dataList = []
    for _device_type in device_types:
        offline = 0
        online = 0
        for data in result:
            if data["type"] == _device_type["device_type"]:
                if data["status"] == "UP":
                    online +=1
                else: offline +=1
        dataList.append({"device_type":_device_type["device_type"], "total":offline+online,"online":online,"offline":offline}) 
    return dataList

