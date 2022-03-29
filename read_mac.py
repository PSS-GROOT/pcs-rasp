from uuid import getnode as get_mac


client_id = hex(get_mac())

print("Mac address of current device",client_id)
