#####################################################################################################################################
# mInfo ver 0.75  June 2014
# To activate copy mInfo folder to C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python
# Motorheadz present mInfo an app for the game Assetto Corsa.
# Allowing compiling sequence of sounds then playback of wave files of speech or sounds in the game as alerts or reports
# First alert developed is lap times for players car as they cross the line.
# This is an alpha proof of concept if people like it I will develop this concept further
# TODO clean up some of the code to be more efficent. Create enable/disable switch. Add ability for config fie to remember settings.
# TODO Review code and refactor when the game is released and python API and or shared memory is ver 1.0
# TODO add additional languages and voice sets and volume control
# TODO Perhaps add more features, report other drivers times, fuel report, temp warnings, average speed, lap countdowns  etc
# App developed by David Trenear
# Additional Testing by Jason Madigan and Tyson Cierpial
# Big thanks to whoever wrote this sim info  module. Saved me maybe a week of thrashing to get it going and testing
# Contact me so I can give thanks and acknowledge you on the Assetto Corsa forums and in the credits
#####################################################################################################################################

import sys
import os
import os.path
# sys.path.insert(0, "apps/python/mInfo/pygame")
# sys.path.insert(0, "apps/python/mInfo/numpy")
# sys.path.insert(0, "apps/python/mInfo/ctypes")
import numpy as np
import ac
import acsys
import mmap
import functools
import ctypes
from ctypes import c_int32, c_float, c_char, c_wchar, c_bool, c_int
import pygame
import pygame.mixer
import pygame.sndarray

# for d in sys.path:
#     ac.console("{0}".format(d))


#------------------------------------------------------------------------------------------------------------------------------------------
# SIM INFO
# Big thanks to whoever wrote this sim info  module. Saved me maybe a week of thrashing to get it going and testing
# Contact me so I can give thanks and acknowledge you on the assetto corsa forums and in the credits
# I adapted to run internally and not as a module. Also temporarily switched off what I do not need from shared memory link at the moment
# This following set of variables and class setup the reading of shared memore with the game which enables us to get correct vales
# that are currently not working in the python API, namely the last lap times
# This stuff might go once we gat a final release api etc

#vars for the following classes
AC_STATUS = c_int32
AC_OFF = 0
AC_REPLAY = 1
AC_LIVE = 2
AC_PAUSE = 3
AC_SESSION_TYPE = c_int32
AC_UNKNOWN = -1
AC_PRACTICE = 0
AC_QUALIFY = 1
AC_RACE = 2
AC_HOTLAP = 3
AC_TIME_ATTACK = 4
AC_DRIFT = 5
AC_DRAG = 6

class SPageFilePhysics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('packetId' , c_int32),
        ('gas', c_float),
        ('brake', c_float),
        ('fuel', c_float),
        ('gear' , c_int32),
        ('rpms' , c_int32),
        ('steerAngle', c_float),
        ('speedKmh', c_float),
        ('velocity', c_float * 3),
        ('accG', c_float * 3),
        ('wheelSlip', c_float * 4),
        ('wheelLoad', c_float * 4),
        ('wheelsPressure', c_float * 4),
        ('wheelAngularSpeed', c_float * 4),
        ('tyreWear', c_float * 4),
        ('tyreDirtyLevel', c_float * 4),
        ('tyreCoreTemperature', c_float * 4),
        ('camberRAD', c_float * 4),
        ('suspensionTravel', c_float * 4),
        ('drs', c_float),
        ('tc', c_float),
        ('heading', c_float),
        ('pitch', c_float),
        ('roll', c_float),
        ('cgHeight', c_float),
        ('carDamage', c_float * 5),
        ('numberOfTyresOut' , c_int32),
        ('pitLimiterOn' , c_int32),
        ('abs', c_float),
    ]

class SPageFileGraphic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('packetId' , c_int32),
        ('status', AC_STATUS),
        ('session', AC_SESSION_TYPE),
         # NOTE: if you want str instead bytes, access it without '_'
        ('_currentTime', c_char * 10),
        ('_lastTime', c_char * 10),
        ('_bestTime', c_char * 10),
        ('_split', c_char * 10),
        ('completedLaps' , c_int32),
        ('position' , c_int32),
        ('iCurrentTime' , c_int32),
        ('iLastTime' , c_int32),
        ('iBestTime' , c_int32),
        ('sessionTimeLeft', c_float),
        ('distanceTraveled', c_float),
        ('isInPit' , c_int32),
        ('currentSectorIndex' , c_int32),
        ('lastSectorTime' , c_int32),
        ('numberOfLaps' , c_int32),
        ('_tyreCompound', c_char * 32),

        ('replayTimeMultiplier', c_float),
        ('normalizedCarPosition', c_float),
        ('carCoordinates', c_float * 3),
    ]

class SPageFileStatic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('_smVersion', c_char * 10),
        ('_acVersion', c_char * 10),
        # session static info
        ('numberOfSessions' , c_int32),
        ('numCars' , c_int32),
        ('_carModel', c_char * 32),
        ('_track', c_char * 32),
        ('_playerName', c_char * 32),
        ('_playerSurname', c_char * 32),
        ('_playerNick', c_char * 32),
        ('sectorCount' , c_int32),

        # car static info
        ('maxTorque', c_float),
        ('maxPower', c_float),
        ('maxRpm' , c_int32),
        ('maxFuel', c_float),
        ('suspensionMaxTravel', c_float * 4),
        ('tyreRadius', c_float * 4),
    ]

#make _char_p properties return unicode strings not needed now here maybe later

for cls in (SPageFilePhysics, SPageFileGraphic, SPageFileStatic):
    for name, typ in cls._fields_:
        if name.startswith("_"):
            def getter(self, name=None):
                value = getattr(self, name)
                # TODO: real encoding is very strange, it's not utf-8
                return value.decode("utf-8")
            setattr(cls, name.lstrip("_"),
                    property(functools.partial(getter, name=name)))

class SimInfo:
    def __init__(self):
        #self._acpmf_physics = mmap.mmap(0, ctypes.sizeof(SPageFilePhysics), "acpmf_physics")
        self._acpmf_graphics = mmap.mmap(0, ctypes.sizeof(SPageFileGraphic), "acpmf_graphics")
        #self._acpmf_static = mmap.mmap(0, ctypes.sizeof(SPageFileStatic), "acpmf_static")
        #self.physics = SPageFilePhysics.from_buffer(self._acpmf_physics)
        self.graphics = SPageFileGraphic.from_buffer(self._acpmf_graphics)
        #self.static = SPageFileStatic.from_buffer(self._acpmf_static)

    def close(self):
        #self._acpmf_physics.close()
        self._acpmf_graphics.close()
        #self._acpmf_static.close()

    def __del__(self):
        self.close()

# def demo(self):
#     infoDemo = SimInfo()
#     for _ in range(400):
#         ac.console(Demo.static.track, Demo.graphics.tyreCompound, Demo.physics.rpms, Demo.graphics.currentTime)

# END SIM INFO
#------------------------------------------------------------------------------------------------------------------------------------------



class SoundClass:
    """Define sound paths and sound object containers define pygame mixer and channel define variables for sound manipulation and playback."""
    def __init__(self):
        self.maindir = os.path.split(os.path.abspath(__file__))[0]
        self.mixer = pygame.mixer
        self.chan = None

        self.hasplayed = 0

        self.joinsounds = None
        self.playsounds =  None

        self.sound_point = None
        self.filepathsound_point = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_point.wav')

        self.sound_one = None
        self.filepathsound_one = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_one.wav')

        self.sound_two = None
        self.filepathsound_two = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_two.wav')

        self.sound_three = None
        self.filepathsound_three = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_three.wav')

        self.sound_four = None
        self.filepathsound_four  = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_four.wav')

        self.sound_five = None
        self.filepathsound_five = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_five.wav')

        self.sound_six = None
        self.filepathsound_six = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_six.wav')

        self.sound_seven = None
        self.filepathsound_seven = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_seven.wav')

        self.sound_eight = None
        self.filepathsound_eight = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_eight.wav')

        self.sound_nine = None
        self.filepathsound_nine = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_nine.wav')

        self.sound_ten = None
        self.filepathsound_ten = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_ten.wav')

        self.sound_eleven = None
        self.filepathsound_eleven = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_eleven.wav')

        self.sound_twelve = None
        self.filepathsound_twelve = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_twelve.wav')

        self.sound_thirteen = None
        self.filepathsound_thirteen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_thirteen.wav')

        self.sound_fourteen = None
        self.filepathsound_fourteen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_fourteen.wav')

        self.sound_fifteen = None
        self.filepathsound_fifteen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_fifteen.wav')

        self.sound_sixteen = None
        self.filepathsound_sixteen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_sixteen.wav')

        self.sound_seventeen = None
        self.filepathsound_seventeen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_seventeen.wav')

        self.sound_eighteen = None
        self.filepathsound_eighteen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_eighteen.wav')

        self.sound_nineteen = None
        self.filepathsound_nineteen = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_nineteen.wav')

        self.sound_twenty = None
        self.filepathsound_twenty = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_twenty.wav')

        self.sound_thirty = None
        self.filepathsound_thirty = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_thirty.wav')

        self.sound_forty = None
        self.filepathsound_forty = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_forty.wav')

        self.sound_fifty = None
        self.filepathsound_fifty = os.path.join(self.maindir, 'sounds/Soundset-David', 'sound_fifty.wav')


    def loadSounds(self):
        """ init mixer freq set channels and volume, load sounds into contained from disk and set volume."""
        self.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
        self.mixer.set_num_channels(2)
        self.chan = pygame.mixer.Channel(0)
        self.chan.set_volume(1.0)

        self.playsounds = self.mixer.Sound(self.filepathsound_point)
        self.playsounds.set_volume(1.0)

        self.sound_point = self.mixer.Sound(self.filepathsound_point)
        self.sound_point.set_volume(1.0)
        self.sound_point_array = pygame.sndarray.array(self.sound_point)

        self.sound_one = self.mixer.Sound(self.filepathsound_one)
        self.sound_one.set_volume(1.0)
        self.sound_one_array = pygame.sndarray.array(self.sound_one)

        self.sound_two = self.mixer.Sound(self.filepathsound_two)
        self.sound_two.set_volume(1.0)
        self.sound_two_array = pygame.sndarray.array(self.sound_two)

        self.sound_three = self.mixer.Sound(self.filepathsound_three)
        self.sound_three.set_volume(1.0)
        self.sound_three_array = pygame.sndarray.array(self.sound_three)

        self.sound_four = self.mixer.Sound(self.filepathsound_four)
        self.sound_four.set_volume(1.0)
        self.sound_four_array = pygame.sndarray.array(self.sound_four)

        self.sound_five = self.mixer.Sound(self.filepathsound_five)
        self.sound_five.set_volume(1.0)
        self.sound_five_array = pygame.sndarray.array(self.sound_five)

        self.sound_six = self.mixer.Sound(self.filepathsound_six)
        self.sound_six.set_volume(1.0)
        self.sound_six_array = pygame.sndarray.array(self.sound_six)

        self.sound_seven = self.mixer.Sound(self.filepathsound_seven)
        self.sound_seven.set_volume(1.0)
        self.sound_seven_array = pygame.sndarray.array(self.sound_seven)

        self.sound_eight = self.mixer.Sound(self.filepathsound_eight)
        self.sound_eight.set_volume(1.0)
        self.sound_eight_array = pygame.sndarray.array(self.sound_eight)

        self.sound_nine = self.mixer.Sound(self.filepathsound_nine)
        self.sound_nine.set_volume(1.0)
        self.sound_nine_array = pygame.sndarray.array(self.sound_nine)

        self.sound_ten = self.mixer.Sound(self.filepathsound_ten)
        self.sound_ten.set_volume(1.0)
        self.sound_ten_array = pygame.sndarray.array(self.sound_ten)

        self.sound_eleven = self.mixer.Sound(self.filepathsound_eleven)
        self.sound_eleven.set_volume(1.0)
        self.sound_eleven_array = pygame.sndarray.array(self.sound_eleven)

        self.sound_twelve = self.mixer.Sound(self.filepathsound_twelve)
        self.sound_twelve.set_volume(1.0)
        self.sound_twelve_array = pygame.sndarray.array(self.sound_twelve)

        self.sound_thirteen = self.mixer.Sound(self.filepathsound_thirteen)
        self.sound_thirteen.set_volume(1.0)
        self.sound_thirteen_array = pygame.sndarray.array(self.sound_thirteen)

        self.sound_fourteen = self.mixer.Sound(self.filepathsound_fourteen)
        self.sound_fourteen.set_volume(1.0)
        self.sound_fourteen_array = pygame.sndarray.array(self.sound_fourteen)

        self.sound_fifteen = self.mixer.Sound(self.filepathsound_fifteen)
        self.sound_fifteen.set_volume(1.0)
        self.sound_fifteen_array = pygame.sndarray.array(self.sound_fifteen)

        self.sound_sixteen = self.mixer.Sound(self.filepathsound_sixteen)
        self.sound_sixteen.set_volume(1.0)
        self.sound_sixteen_array = pygame.sndarray.array(self.sound_sixteen)

        self.sound_seventeen = self.mixer.Sound(self.filepathsound_seventeen)
        self.sound_seventeen.set_volume(1.0)
        self.sound_seventeen_array = pygame.sndarray.array(self.sound_seventeen)

        self.sound_eighteen = self.mixer.Sound(self.filepathsound_eighteen)
        self.sound_eighteen.set_volume(1.0)
        self.sound_eighteen_array = pygame.sndarray.array(self.sound_eighteen)

        self.sound_nineteen = self.mixer.Sound(self.filepathsound_nineteen)
        self.sound_nineteen.set_volume(1.0)
        self.sound_nineteen_array = pygame.sndarray.array(self.sound_nineteen)

        self.sound_twenty = self.mixer.Sound(self.filepathsound_twenty)
        self.sound_twenty.set_volume(1.0)
        self.sound_twenty_array = pygame.sndarray.array(self.sound_twenty)

        self.sound_thirty = self.mixer.Sound(self.filepathsound_thirty)
        self.sound_thirty.set_volume(1.0)
        self.sound_thirty_array = pygame.sndarray.array(self.sound_thirty)

        self.sound_forty = self.mixer.Sound(self.filepathsound_forty)
        self.sound_forty.set_volume(1.0)
        self.sound_forty_array = pygame.sndarray.array(self.sound_forty)

        self.sound_fifty = self.mixer.Sound(self.filepathsound_fifty)
        self.sound_fifty.set_volume(1.0)
        self.sound_fifty_array = pygame.sndarray.array(self.sound_fifty)


    def playSound(self):
        """ join sounds to form laptime sound in container self.joinsounds format and copy to playback container self.playsounds then play thru channel in mixer."""
        self.joinsounds = np.concatenate((self.sound_one, self.sound_twenty, self.sound_two,self.sound_point_array, self.sound_three,self.sound_three,self.sound_two), axis=0)
        self.playsounds = pygame.sndarray.make_sound(self.joinsounds)
        self.chan.play(self.playsounds)
        #ac.console("playSound")


class TimerClass:
    """ Controls time recording storage combination output of laptimes input to getTime() is milliseconds from siminfo class obj instance laptimer. """
    def __init__(self,):

        self.currentlap = 0
        self.completedlaps = 0

        self.bestlapminutes = 0.0
        self.bestlapsecondsint = 0.0
        self.bestlapmilliseconds = 0.0
        self.bestlapmillisecondsStr = ""
        self.bestlapmilliseconds1 = ""
        self.bestlapmilliseconds2 = ""
        self.bestlapmilliseconds3 = ""

        self.lastlapminutes = 0.0
        self.lastlapsecondsint = 0.0
        self.lastlapmilliseconds = 0.0
        self.lastlapmillisecondsStr = ""
        self.lastlapmilliseconds1 = ""
        self.lastlapmilliseconds2 = ""
        self.lastlapmilliseconds3 = ""

        self.currentlapminutes = 0.0
        self.currentlapsecondsint = 0.0
        self.currentlapmilliseconds = 0.0
        self.currentlapmillisecondsStr = ""
        self.currentlapmilliseconds1 = "0"
        self.currentlapmilliseconds2 = "0"
        self.currentlapmilliseconds3 = "0"

    def updateTime(self,thelap,thetime1,thetime2,thetime3):
        self.currentlap = thelap
        self.bestlapmilliseconds = thetime2
        self.lastlapmilliseconds = thetime1
        self.currentlapmilliseconds = thetime3

    def getCurrentLap(self,):
        return self.currentlap

    def getBestLapTime(self,):
        if(self.bestlapmilliseconds):
            if(self.bestlapmilliseconds<60000):
                self.bestlapminutes = 0
                self.bestlapsecondsint = int((self.bestlapmilliseconds/1000) // 1 * 1)
                self.bestlapmillisecondsStr = str(self.bestlapmilliseconds/1000)
                self.bestlapmilliseconds1 = str(self.bestlapmillisecondsStr[-3:-2])
                self.bestlapmilliseconds2 = str(self.bestlapmillisecondsStr[-2:-1])
                self.bestlapmilliseconds3 = str(self.bestlapmillisecondsStr[-1])
                if(self.bestlapsecondsint <10 ):
                    return "{0}:0{1}:{2}{3}{4}".format(self.bestlapminutes,self.bestlapsecondsint,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
                else:
                    return "{0}:{1}:{2}{3}{4}".format(self.bestlapminutes,self.bestlapsecondsint,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
            else:
                self.bestlapminutes = int((self.bestlapmilliseconds/1000)/60)
                self.bestlapsecondsint = int((self.bestlapmilliseconds/1000) - (self.bestlapminutes*60))
                self.bestlapmillisecondsStr = str(self.bestlapmilliseconds/1000)
                self.bestlapmilliseconds1 = str(self.bestlapmillisecondsStr[-3:-2])
                self.bestlapmilliseconds2 = str(self.bestlapmillisecondsStr[-2:-1])
                self.bestlapmilliseconds3 = str(self.bestlapmillisecondsStr[-1])
                return "{0}:{1}:{2}{3}{4}".format(self.bestlapminutes,self.bestlapsecondsint,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
        else:
            return "-:--:---"

    def getLastLapTime(self,):
        if(self.lastlapmilliseconds):
            if(self.lastlapmilliseconds<60000):
                self.lastlapminutes = 0
                self.lastlapsecondsint = int((self.lastlapmilliseconds/1000) // 1 * 1)
                self.lastlapmillisecondsStr = str(self.lastlapmilliseconds/1000)
                self.lastlapmilliseconds1 = str(self.lastlapmillisecondsStr[-3:-2])
                self.lastlapmilliseconds2 = str(self.lastlapmillisecondsStr[-2:-1])
                self.lastlapmilliseconds3 = str(self.lastlapmillisecondsStr[-1])
                return "{0}:{1}:{2}{3}{4}".format(self.lastlapminutes,self.lastlapsecondsint,self.lastlapmilliseconds1,self.lastlapmilliseconds2,self.lastlapmilliseconds3)
            else:
                self.lastlapminutes = int((self.lastlapmilliseconds/1000)/60)
                self.lastlapsecondsint = int((self.lastlapmilliseconds/1000) - (self.lastlapminutes*60))
                self.lastlapmillisecondsStr = str(self.lastlapmilliseconds/1000)
                self.lastlapmilliseconds1 = str(self.lastlapmillisecondsStr[-3:-2])
                self.lastlapmilliseconds2 = str(self.lastlapmillisecondsStr[-2:-1])
                self.lastlapmilliseconds3 = str(self.lastlapmillisecondsStr[-1])
                return "{0}:{1}:{2}{3}{4}".format(self.lastlapminutes,self.lastlapsecondsint,self.lastlapmilliseconds1,self.lastlapmilliseconds2,self.lastlapmilliseconds3)
        else:
            return "-:--:---"

    def getCurrentLapTime(self,):
        if(self.currentlapmilliseconds):
            if(self.currentlapmilliseconds<60000):
                self.currentlapminutes = 0
                self.currentlapsecondsint = int((self.currentlapmilliseconds/1000) // 1 * 1)
                self.currentlapmillisecondsStr = str(self.currentlapmilliseconds/1000)
                self.currentlapmilliseconds1 = str(self.currentlapmillisecondsStr[-3:-2])
                self.currentlapmilliseconds2 = str(self.currentlapmillisecondsStr[-2:-1])
                self.currentlapmilliseconds3 = str(self.currentlapmillisecondsStr[-1])
                #return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.currentlapsecondsint,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
                if(self.currentlapsecondsint <10 ):
                    return "{0}:0{1}:{2}{3}{4}".format(self.currentlapminutes,self.currentlapsecondsint,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
                else:
                    return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.currentlapsecondsint,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
            else:
                self.currentlapminutes = int((self.currentlapmilliseconds/1000)/60)
                self.currentlapsecondsint = int((self.currentlapmilliseconds/1000) - (self.currentlapminutes*60))
                self.currentlapmillisecondsStr = str(self.currentlapmilliseconds/1000)
                self.currentlapmilliseconds1 = str(self.currentlapmillisecondsStr[-3:-2])
                self.currentlapmilliseconds2 = str(self.currentlapmillisecondsStr[-2:-1])
                self.currentlapmilliseconds3 = str(self.currentlapmillisecondsStr[-1])
                return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.currentlapsecondsint,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
        else:
            return "-:--:---"

class DisplayClass:
    """eventually move all of the display elements into this class like labels buttons and settings """
    def __init__(self,):
        self.appWindow = 0
        self.currentlaplabel = 0
        self.besttimelabel = 0
        self.lasttimelabel = 0
        self.currenttimelabel = 0


#---------------------------------------------------------
# declare class instance objects

infosystem = SimInfo()
soundsystem = SoundClass()
laptimer = TimerClass()
mInfoDisplay = DisplayClass()
#---------------------------------------------------------

def acMain(ac_version):
    """main init function which runs on game startup."""

    mInfoDisplay.appWindow = ac.newApp("mInfo")
    ac.addRenderCallback(mInfoDisplay.appWindow, onFormRender)
    ac.setSize(mInfoDisplay.appWindow, 220, 180)

    mInfoDisplay.currentlaplabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
    ac.setPosition(mInfoDisplay.currentlaplabel, 49, 65)
    ac.setFontColor(mInfoDisplay.currentlaplabel, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(mInfoDisplay.currentlaplabel,'left')

    mInfoDisplay.besttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
    ac.setPosition(mInfoDisplay.besttimelabel, 59, 90)
    ac.setFontColor(mInfoDisplay.besttimelabel, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(mInfoDisplay.besttimelabel,'left')

    mInfoDisplay.lasttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
    ac.setPosition(mInfoDisplay.lasttimelabel, 65, 115)
    ac.setFontColor(mInfoDisplay.lasttimelabel, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(mInfoDisplay.lasttimelabel,'left')

    mInfoDisplay.currenttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
    ac.setPosition(mInfoDisplay.currenttimelabel, 40, 140)
    ac.setFontColor(mInfoDisplay.currenttimelabel, 1.0, 1.0, 1.0, 1)
    ac.setFontAlignment(mInfoDisplay.currenttimelabel,'left')
    ac.setBackgroundTexture(mInfoDisplay.appWindow, "apps/python/mInfo/images/mInfoBackground.png")

    pygame.init()
    soundsystem.loadSounds()
    return "mInfo"

def acUpdate(deltaT):
    """main loop."""

    # """ only update lap once and play sound once required as we are in a loop."""
    soundsystem.hasplayed = 0
    if (laptimer.completedlaps < laptimer.currentlap):
        laptimer.completedlaps = laptimer.currentlap
        soundsystem.hasplayed = 1
        if(soundsystem.hasplayed==1):
            #ac.console(laptimer.getLastLapTime())
            soundsystem.playSound()
            soundsystem.hasplayed = 0

    """update timer."""
    laptimer.updateTime(infosystem.graphics.completedLaps,infosystem.graphics.iBestTime,infosystem.graphics.iLastTime, infosystem.graphics.iCurrentTime)

def onFormRender(deltaT):
    """only update app when app form is visible then update only the following note call back method for this function defined in acMain above."""
    #global appWindow
    global besttimelabel
    global besttimeset
    global lasttimelabel
    global currenttimelabel
    global currenttimeset
    ac.setText(mInfoDisplay.currentlaplabel, "current lap : {0}".format(laptimer.getCurrentLap()))
    ac.setText(mInfoDisplay.besttimelabel, "best time : {0}".format(laptimer.getBestLapTime()))
    ac.setText(mInfoDisplay.lasttimelabel, "last time : {0}".format(laptimer.getLastLapTime()))
    ac.setText(mInfoDisplay.currenttimelabel, "current time : {0}".format(laptimer.getCurrentLapTime()))


def acShutdown():
    """on shut down quit pygame so no crash or lockup."""
    pygame.quit()