# thread 1
# Connect Server MQTT and Retry if fail
    # retry
    # request setting until success , interval
    # send services status


# thread 2
# Connect to i2c connection and Retry if fail



# global singletone variable
# i2c_connection
# mqtt_connection`
import json
count = 0
skip = ['5,4','5,5','5,1','5,2']
data = []
for x in range(5,0,-1):
    for y in range(5,0,-1):
        for z in range(5,2,-1):
            cur = f'{x},{y}'
            if cur in skip :
                continue
            count += 1
            # print(x,y,z)
            print(count)
            data.append(dict(x=x,y=y,z=z,uid=count))

print(data)

print(json.dumps(data))