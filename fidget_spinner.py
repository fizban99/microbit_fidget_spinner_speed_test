from microbit import pin0, running_time


def calculateCurrentRPM(lasteventtime, currenteventtime):
    # work out the time between the last two low light levels events
    # and assuming spinner has 3 arms so three low levels events per revolution
    return round((oneminuteinmilliseconds / ((currenteventtime - lasteventtime) * 3)))

minlightvalue, maxlightvalue = 2, 4
lasttriggertime, lastreportime = 0, 0
hashitminlightlevel = False
oneminuteinmilliseconds = 60000
print("ready to start")
while True:
    # get current reading then devide value by a number
    # that brings it into single digits, in our case %
    # 100 this makes it easier to detect high and low
    # light values as there are fewer steps in light
    # level available
    currentlightreading = round(pin0.read_analog() / 100)
    # uncomment line below to calibrate min and max light
    # values but be sure to comment out again before
    # trying to calculate RPM
    # print("light reading:", currentlightreading)
    # check if light has
    # dimmed to lowest value BUT has been to the highest
    # value first this reduces / elimenates false
    # positive readings
    if (currentlightreading <= minlightvalue and not hashitminlightlevel):
        hashitminlightlevel = True
        currenttime = running_time()
        if (currenttime - lastreportime > 1000):
            # write our result at most once per second otherwise
            # serial.write slows down the reading of the light
            # sensor too much
            lastreportime = currenttime
            print("RPM:",  calculateCurrentRPM(lasttriggertime, currenttime))
        lasttriggertime = currenttime
    # check if light has reached highest value and if so
    # reset hashitminlightlevel ready for  detection of
    # next lowest light value
    if (currentlightreading >= maxlightvalue):
        hashitminlightlevel = False
