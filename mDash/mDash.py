##############################################################
# Motorheadz Speedo ver 1.1
# To activate copy mDash folder to C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python
#############################################################

import ac
import acsys

speedo=0

def acMain(ac_version):
    global speedo
    appWindow=ac.newApp("mDash")
    ac.setSize(appWindow,220,180)
    speedo=ac.addLabel(appWindow,"mDash")
    ac.setPosition(speedo,84,94)
    ac.setFontColor(speedo, 1.0,1.0,1.0,1)
    ac.setBackgroundTexture(appWindow,"apps/python/mDash/mDashBackground.png")
    return "mDash"

def acUpdate(deltaT):
    global speedo
    speed=ac.getCarState(0,acsys.CS.SpeedKMH)
    ac.setText(speedo,"{0} kmh".format(round(speed)))
    if(speed < 25):
        ac.setFontColor(speedo, 1.0,1.0,1.0,1)
    if(speed > 25):
        ac.setFontColor(speedo, 0.0,1.0,0.0,1)
    if(speed > 75):
        ac.setFontColor(speedo, 1.0,1.0,0.0,1)
    if(speed > 100):
        ac.setFontColor(speedo, 1.0,0.75,0.0,1)
    if(speed > 125):
        ac.setFontColor(speedo, 1.0,0.5,0.0,1)
    if(speed > 175):
        ac.setFontColor(speedo, 1.0,0.0,0.0,1)
