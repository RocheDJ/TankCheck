def v3_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    
   # if buttonValue=="1":
    # GPIO.output(10, True)
    #else:
    # GPIO.output(10, False)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds


def publish_Blynk(iLevel,iTemp):
    blynk.virtual_write(1, round(iTemp,2)) 
    blynk.virtual_write(2,round(get_uptime(),0))
    blynk.virtual_write(3, round(iLevel,2))

# infinite loop that waits for event
while True:
    blynk.run()
    sleep(.5)

