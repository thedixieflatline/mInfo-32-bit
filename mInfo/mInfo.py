"""mInfo ver 0.85  June 2014
GitHub Page: https://github.com/thedixieflatline/assettocorsa

To activate copy mInfo folder to C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python

Motorheadz present mInfo an app for the game Assetto Corsa.
Allowing compiling sequence of sounds then playback of wave files of speech or sounds in the game as alerts or reports
First alert developed is lap times for players car as they cross the line.

App developed by David Trenear
Additional Testing by Jason Madigan and Tyson Cierpial
Big thanks to Rombik who wrote the original sim info  module.

Please submit bugs or requests to the Assetto Corsa forum
http://www.assettocorsa.net/forum/index.php

TODO add volume control
TODO Fuel add ability to alert when fuel reaches set amount
TODO Need to do a better recording on the audio to sweeten it, make timing and volume more consistent. It sounds bad because I recorded on a headphone mic as a test so next version will be a nice microphone.
TODO Splits ahead or behind last split
TODO add more features, temp warnings, tires
TODO Review code and refactor when the game is released and python API and or shared memory is ver 1.0"""

import sys
import os
import os.path
import ac
import acsys
import configparser
"""Add Modules to Python path"""
sys.path.insert(0, "apps/python/mInfo/pygame")
sys.path.insert(0, "apps/python/mInfo/numpy")
sys.path.insert(0, "apps/python/mInfo/ctypes")
import numpy as np
import pygame
import pygame.mixer
import pygame.sndarray
import mmap
import functools
import ctypes
from ctypes import c_int32, c_float, c_char, c_wchar, c_bool, c_int


def CheckPythonPath():
    """Report Modules on Python path"""
    for d in sys.path:
        ac.console("{0}".format(d))

class ConfigClass:
    """Config file loader (mInfo.ini) and data process"""
    def __init__(self):
        self.config = None
        self.configpath = 'apps/python/mInfo/mInfo.ini'
        self.lapswitch = ""
        self.soundpack = ""
        self.fuelswitch = ""
        self.fuelconvert = ""
        self.bestlap = ""

    def loadConfig(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.configpath)

    def saveConfig(self):
        self.config['app']['lapswitch'] = self.lapswitch
        self.config['app']['fuelswitch'] = self.fuelswitch
        self.config['app']['fuelconvert'] = self.fuelconvert
        self.config['app']['soundfolder'] = self.soundpack
        self.config['app']['bestlap'] = self.bestlap
        self.config.write(open(self.configpath,"w"))

    def setLapSwitchEnabled(self):
        self.lapswitch = "enabled"

    def setLapSwitchDisabled(self):
        self.lapswitch = "disabled"

    def getLapSwitchStatus(self):
        return self.lapswitch

    def setFuelSwitchEnabled(self):
        self.fuelswitch = "enabled"

    def setFuelSwitchDisabled(self):
        self.fuelswitch = "disabled"

    def getFuelSwitchStatus(self):
        return self.fuelswitch

    def setBestLapEnabled(self):
        self.bestlap = "enabled"

    def setBestLapDisabled(self):
        self.bestlap = "disabled"

    def getBestLapStatus(self):
        return self.bestlap

    def setFuelConvertLiters(self):
        self.fuelconvert = "Liters"

    def setFuelConvertGallons(self):
        self.fuelconvert = "Gallons"

    def getFuelConvertStatus(self):
        return self.fuelconvert

    def setInitialStatus(self):
        self.lapswitch = self.config['app']['lapswitch']
        self.fuelswitch = self.config['app']['fuelswitch']
        self.fuelconvert = self.config['app']['fuelconvert']
        self.soundpack = self.config['app']['soundfolder']
        self.bestlap = self.config['app']['bestlap']

class SoundClass:
    """Define sound paths and sound object containers define pygame mixer and channel define variables for sound manipulation and playback."""
    def __init__(self):
        self.maindir = os.path.split(os.path.abspath(__file__))[0]
        self.mixer = pygame.mixer
        self.chan = None
        self.test = 0
        self.currentsoundpack_name = ""
        self.currentsoundpack_folder = ""
        self.currentsoundpack_folder_root = "sounds/"
        self.hasplayedLastLaptime = 0
        self.hasplayedLastFuel = 0
        self.soundlist = {}
        self.playlist_laptime = []
        self.joinsounds_laptime = None
        self.playsounds_laptime =  None
        self.playlist_fuel = []
        self.joinsounds_fuel = None
        self.playsounds_fuel = None
        self.sound_silence = None
        self.filepathsound_silence = None
        self.sound_and = None
        self.filepathsound_and = None
        self.sound_point = None
        self.filepathsound_point = None
        self.sound_minute = None
        self.filepathsound_minute = None
        self.sound_minutes = None
        self.filepathsound_minutes = None
        self.sound_fuel = None
        self.filepathsound_fuel = None
        self.sound_fuel_liters = None
        self.filepathsound_fuel_liters = None
        self.sound_fuel_gallons = None
        self.filepathsound_fuel_gallons = None
        self.sound_bestlap = None
        self.filepathsound_bestlap = None
        self.sound_zero = None
        self.filepathsound_zero = None
        self.sound_one = None
        self.filepathsound_one = None
        self.sound_two = None
        self.filepathsound_two = None
        self.sound_three = None
        self.filepathsound_three = None
        self.sound_four = None
        self.filepathsound_four  = None
        self.sound_five = None
        self.filepathsound_five = None
        self.sound_six = None
        self.filepathsound_six = None
        self.sound_seven = None
        self.filepathsound_seven = None
        self.sound_eight = None
        self.filepathsound_eight = None
        self.sound_nine = None
        self.filepathsound_nine = None
        self.sound_ten = None
        self.filepathsound_ten = None
        self.sound_eleven = None
        self.filepathsound_eleven = None
        self.sound_twelve = None
        self.filepathsound_twelve = None
        self.sound_thirteen = None
        self.filepathsound_thirteen = None
        self.sound_fourteen = None
        self.filepathsound_fourteen = None
        self.sound_fifteen = None
        self.filepathsound_fifteen = None
        self.sound_sixteen = None
        self.filepathsound_sixteen = None
        self.sound_seventeen = None
        self.filepathsound_seventeen = None
        self.sound_eighteen = None
        self.filepathsound_eighteen = None
        self.sound_nineteen = None
        self.filepathsound_nineteen = None
        self.sound_twenty = None
        self.filepathsound_twenty = None
        self.sound_thirty = None
        self.filepathsound_thirty = None
        self.sound_forty = None
        self.filepathsound_forty = None
        self.sound_fifty = None
        self.filepathsound_fifty = None
        self.sound_sixty = None
        self.filepathsound_sixty = None
        self.sound_seventy = None
        self.filepathsound_seventy = None
        self.sound_eighty = None
        self.filepathsound_eighty = None
        self.sound_ninety = None
        self.filepathsound_ninety = None
        self.sound_hundred = None
        self.filepathsound_hundred = None

    def setCurrentSoundPack(self):
        self.currentsoundpack_name = configuration.soundpack
        self.currentsoundpack_folder = self.currentsoundpack_folder_root + configuration.soundpack

    def loadSounds(self):
        """ init mixer freq set channels and volume, load sounds into contained from disk and set volume."""
        self.currentsoundpack_name = configuration.soundpack
        self.currentsoundpack_folder = self.currentsoundpack_folder_root + configuration.soundpack
        self.filepathsound_silence = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_silence.wav')
        self.filepathsound_and = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_and.wav')
        self.filepathsound_point = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_point.wav')
        self.filepathsound_minute = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_minute.wav')
        self.filepathsound_minutes = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_minutes.wav')
        self.filepathsound_fuel = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_fuel.wav')
        self.filepathsound_fuel_liters = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_fuel_liters.wav')
        self.filepathsound_fuel_gallons = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_fuel_gallons.wav')
        self.filepathsound_bestlap = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_bestlap.wav')
        self.filepathsound_zero = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_zero.wav')
        self.filepathsound_one = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_one.wav')
        self.filepathsound_two = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_two.wav')
        self.filepathsound_three = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_three.wav')
        self.filepathsound_four  = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_four.wav')
        self.filepathsound_five = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_five.wav')
        self.filepathsound_six = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_six.wav')
        self.filepathsound_seven = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_seven.wav')
        self.filepathsound_eight = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_eight.wav')
        self.filepathsound_nine = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_nine.wav')
        self.filepathsound_ten = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_ten.wav')
        self.filepathsound_eleven = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_eleven.wav')
        self.filepathsound_twelve = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_twelve.wav')
        self.filepathsound_thirteen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_thirteen.wav')
        self.filepathsound_fourteen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_fourteen.wav')
        self.filepathsound_fifteen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_fifteen.wav')
        self.filepathsound_sixteen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_sixteen.wav')
        self.filepathsound_seventeen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_seventeen.wav')
        self.filepathsound_eighteen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_eighteen.wav')
        self.filepathsound_nineteen = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_nineteen.wav')
        self.filepathsound_twenty = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_twenty.wav')
        self.filepathsound_thirty = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_thirty.wav')
        self.filepathsound_forty = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_forty.wav')
        self.filepathsound_fifty = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_fifty.wav')
        self.filepathsound_sixty = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_sixty.wav')
        self.filepathsound_seventy = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_seventy.wav')
        self.filepathsound_eighty = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_eighty.wav')
        self.filepathsound_ninety = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_ninety.wav')
        self.filepathsound_hundred = os.path.join(self.maindir, self.currentsoundpack_folder, 'sound_hundred.wav')
        self.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
        self.mixer.set_num_channels(2)
        self.chan = pygame.mixer.Channel(0)
        self.chan.set_volume(1.0)
        self.joinsounds_laptime = self.mixer.Sound(self.filepathsound_point)
        self.joinsounds_laptime.set_volume(1.0)
        self.playsounds_laptime = self.mixer.Sound(self.filepathsound_point)
        self.playsounds_laptime.set_volume(1.0)
        self.joinsounds_fuel = self.mixer.Sound(self.filepathsound_point)
        self.joinsounds_fuel.set_volume(1.0)
        self.playsounds_fuel = self.mixer.Sound(self.filepathsound_point)
        self.playsounds_fuel.set_volume(1.0)
        self.sound_silence = self.mixer.Sound(self.filepathsound_silence)
        self.sound_silence.set_volume(1.0)
        self.sound_and = self.mixer.Sound(self.filepathsound_and)
        self.sound_and.set_volume(1.0)
        self.sound_point = self.mixer.Sound(self.filepathsound_point)
        self.sound_point.set_volume(1.0)
        self.sound_minute = self.mixer.Sound(self.filepathsound_minute)
        self.sound_minute.set_volume(1.0)
        self.sound_minutes = self.mixer.Sound(self.filepathsound_minutes)
        self.sound_minutes.set_volume(1.0)
        self.sound_fuel = self.mixer.Sound(self.filepathsound_fuel)
        self.sound_fuel.set_volume(1.0)
        self.sound_fuel_liters = self.mixer.Sound(self.filepathsound_fuel_liters)
        self.sound_fuel_liters.set_volume(1.0)
        self.sound_fuel_gallons = self.mixer.Sound(self.filepathsound_fuel_gallons)
        self.sound_fuel_gallons.set_volume(1.0)
        self.sound_bestlap = self.mixer.Sound(self.filepathsound_bestlap)
        self.sound_bestlap.set_volume(1.0)
        self.sound_zero = self.mixer.Sound(self.filepathsound_zero)
        self.sound_zero.set_volume(1.0)
        self.sound_one = self.mixer.Sound(self.filepathsound_one)
        self.sound_one.set_volume(1.0)
        self.sound_two = self.mixer.Sound(self.filepathsound_two)
        self.sound_two.set_volume(1.0)
        self.sound_three = self.mixer.Sound(self.filepathsound_three)
        self.sound_three.set_volume(1.0)
        self.sound_four = self.mixer.Sound(self.filepathsound_four)
        self.sound_four.set_volume(1.0)
        self.sound_five = self.mixer.Sound(self.filepathsound_five)
        self.sound_five.set_volume(1.0)
        self.sound_six = self.mixer.Sound(self.filepathsound_six)
        self.sound_six.set_volume(1.0)
        self.sound_seven = self.mixer.Sound(self.filepathsound_seven)
        self.sound_seven.set_volume(1.0)
        self.sound_eight = self.mixer.Sound(self.filepathsound_eight)
        self.sound_eight.set_volume(1.0)
        self.sound_nine = self.mixer.Sound(self.filepathsound_nine)
        self.sound_nine.set_volume(1.0)
        self.sound_ten = self.mixer.Sound(self.filepathsound_ten)
        self.sound_ten.set_volume(1.0)
        self.sound_eleven = self.mixer.Sound(self.filepathsound_eleven)
        self.sound_eleven.set_volume(1.0)
        self.sound_twelve = self.mixer.Sound(self.filepathsound_twelve)
        self.sound_twelve.set_volume(1.0)
        self.sound_thirteen = self.mixer.Sound(self.filepathsound_thirteen)
        self.sound_thirteen.set_volume(1.0)
        self.sound_fourteen = self.mixer.Sound(self.filepathsound_fourteen)
        self.sound_fourteen.set_volume(1.0)
        self.sound_fifteen = self.mixer.Sound(self.filepathsound_fifteen)
        self.sound_fifteen.set_volume(1.0)
        self.sound_sixteen = self.mixer.Sound(self.filepathsound_sixteen)
        self.sound_sixteen.set_volume(1.0)
        self.sound_seventeen = self.mixer.Sound(self.filepathsound_seventeen)
        self.sound_seventeen.set_volume(1.0)
        self.sound_eighteen = self.mixer.Sound(self.filepathsound_eighteen)
        self.sound_eighteen.set_volume(1.0)
        self.sound_nineteen = self.mixer.Sound(self.filepathsound_nineteen)
        self.sound_nineteen.set_volume(1.0)
        self.sound_twenty = self.mixer.Sound(self.filepathsound_twenty)
        self.sound_twenty.set_volume(1.0)
        self.sound_twenty_one_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_one))
        self.sound_twenty_one = pygame.sndarray.make_sound(self.sound_twenty_one_array)
        self.sound_twenty_one.set_volume(1.0)
        self.sound_twenty_two_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_two))
        self.sound_twenty_two = pygame.sndarray.make_sound(self.sound_twenty_two_array)
        self.sound_twenty_two.set_volume(1.0)
        self.sound_twenty_three_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_three))
        self.sound_twenty_three = pygame.sndarray.make_sound(self.sound_twenty_three_array)
        self.sound_twenty_three.set_volume(1.0)
        self.sound_twenty_four_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_four))
        self.sound_twenty_four = pygame.sndarray.make_sound(self.sound_twenty_four_array)
        self.sound_twenty_four.set_volume(1.0)
        self.sound_twenty_five_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_five))
        self.sound_twenty_five = pygame.sndarray.make_sound(self.sound_twenty_five_array)
        self.sound_twenty_five.set_volume(1.0)
        self.sound_twenty_six_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_six))
        self.sound_twenty_six = pygame.sndarray.make_sound(self.sound_twenty_six_array)
        self.sound_twenty_six.set_volume(1.0)
        self.sound_twenty_seven_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_seven))
        self.sound_twenty_seven = pygame.sndarray.make_sound(self.sound_twenty_seven_array)
        self.sound_twenty_seven.set_volume(1.0)
        self.sound_twenty_eight_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_eight))
        self.sound_twenty_eight = pygame.sndarray.make_sound(self.sound_twenty_eight_array)
        self.sound_twenty_eight.set_volume(1.0)
        self.sound_twenty_nine_array = np.concatenate((self.sound_twenty,self.sound_silence,self.sound_nine))
        self.sound_twenty_nine = pygame.sndarray.make_sound(self.sound_twenty_nine_array)
        self.sound_twenty_nine.set_volume(1.0)
        self.sound_thirty = self.mixer.Sound(self.filepathsound_thirty)
        self.sound_thirty.set_volume(1.0)
        self.sound_thirty_one_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_one))
        self.sound_thirty_one = pygame.sndarray.make_sound(self.sound_thirty_one_array)
        self.sound_thirty_one.set_volume(1.0)
        self.sound_thirty_two_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_two))
        self.sound_thirty_two = pygame.sndarray.make_sound(self.sound_thirty_two_array)
        self.sound_thirty_two.set_volume(1.0)
        self.sound_thirty_three_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_three))
        self.sound_thirty_three = pygame.sndarray.make_sound(self.sound_thirty_three_array)
        self.sound_thirty_three.set_volume(1.0)
        self.sound_thirty_four_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_four))
        self.sound_thirty_four = pygame.sndarray.make_sound(self.sound_thirty_four_array)
        self.sound_thirty_four.set_volume(1.0)
        self.sound_thirty_five_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_five))
        self.sound_thirty_five = pygame.sndarray.make_sound(self.sound_thirty_five_array)
        self.sound_thirty_five.set_volume(1.0)
        self.sound_thirty_six_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_six))
        self.sound_thirty_six = pygame.sndarray.make_sound(self.sound_thirty_six_array)
        self.sound_thirty_six.set_volume(1.0)
        self.sound_thirty_seven_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_seven))
        self.sound_thirty_seven = pygame.sndarray.make_sound(self.sound_thirty_seven_array)
        self.sound_thirty_seven.set_volume(1.0)
        self.sound_thirty_eight_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_eight))
        self.sound_thirty_eight = pygame.sndarray.make_sound(self.sound_thirty_eight_array)
        self.sound_thirty_eight.set_volume(1.0)
        self.sound_thirty_nine_array = np.concatenate((self.sound_thirty,self.sound_silence,self.sound_nine))
        self.sound_thirty_nine = pygame.sndarray.make_sound(self.sound_thirty_nine_array)
        self.sound_thirty_nine.set_volume(1.0)
        self.sound_forty = self.mixer.Sound(self.filepathsound_forty)
        self.sound_forty.set_volume(1.0)
        self.sound_forty_one_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_one))
        self.sound_forty_one = pygame.sndarray.make_sound(self.sound_forty_one_array)
        self.sound_forty_one.set_volume(1.0)
        self.sound_forty_two_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_two))
        self.sound_forty_two = pygame.sndarray.make_sound(self.sound_forty_two_array)
        self.sound_forty_two.set_volume(1.0)
        self.sound_forty_three_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_three))
        self.sound_forty_three = pygame.sndarray.make_sound(self.sound_forty_three_array)
        self.sound_forty_three.set_volume(1.0)
        self.sound_forty_four_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_four))
        self.sound_forty_four = pygame.sndarray.make_sound(self.sound_forty_four_array)
        self.sound_forty_four.set_volume(1.0)
        self.sound_forty_five_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_five))
        self.sound_forty_five = pygame.sndarray.make_sound(self.sound_forty_five_array)
        self.sound_forty_five.set_volume(1.0)
        self.sound_forty_six_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_six))
        self.sound_forty_six = pygame.sndarray.make_sound(self.sound_forty_six_array)
        self.sound_forty_six.set_volume(1.0)
        self.sound_forty_seven_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_seven))
        self.sound_forty_seven = pygame.sndarray.make_sound(self.sound_forty_seven_array)
        self.sound_forty_seven.set_volume(1.0)
        self.sound_forty_eight_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_eight))
        self.sound_forty_eight = pygame.sndarray.make_sound(self.sound_forty_eight_array)
        self.sound_forty_eight.set_volume(1.0)
        self.sound_forty_nine_array = np.concatenate((self.sound_forty,self.sound_silence,self.sound_nine))
        self.sound_forty_nine = pygame.sndarray.make_sound(self.sound_forty_nine_array)
        self.sound_forty_nine.set_volume(1.0)
        self.sound_fifty = self.mixer.Sound(self.filepathsound_fifty)
        self.sound_fifty.set_volume(1.0)
        self.sound_fifty_one_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_one))
        self.sound_fifty_one = pygame.sndarray.make_sound(self.sound_fifty_one_array)
        self.sound_fifty_one.set_volume(1.0)
        self.sound_fifty_two_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_two))
        self.sound_fifty_two = pygame.sndarray.make_sound(self.sound_fifty_two_array)
        self.sound_fifty_two.set_volume(1.0)
        self.sound_fifty_three_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_three))
        self.sound_fifty_three = pygame.sndarray.make_sound(self.sound_fifty_three_array)
        self.sound_fifty_three.set_volume(1.0)
        self.sound_fifty_four_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_four))
        self.sound_fifty_four = pygame.sndarray.make_sound(self.sound_fifty_four_array)
        self.sound_fifty_four.set_volume(1.0)
        self.sound_fifty_five_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_five))
        self.sound_fifty_five = pygame.sndarray.make_sound(self.sound_fifty_five_array)
        self.sound_fifty_five.set_volume(1.0)
        self.sound_fifty_six_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_six))
        self.sound_fifty_six = pygame.sndarray.make_sound(self.sound_fifty_six_array)
        self.sound_fifty_six.set_volume(1.0)
        self.sound_fifty_seven_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_seven))
        self.sound_fifty_seven = pygame.sndarray.make_sound(self.sound_fifty_seven_array)
        self.sound_fifty_seven.set_volume(1.0)
        self.sound_fifty_eight_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_eight))
        self.sound_fifty_eight = pygame.sndarray.make_sound(self.sound_fifty_eight_array)
        self.sound_fifty_eight.set_volume(1.0)
        self.sound_fifty_nine_array = np.concatenate((self.sound_fifty,self.sound_silence,self.sound_nine))
        self.sound_fifty_nine = pygame.sndarray.make_sound(self.sound_fifty_nine_array)
        self.sound_fifty_nine.set_volume(1.0)
        self.sound_sixty = self.mixer.Sound(self.filepathsound_sixty)
        self.sound_sixty.set_volume(1.0)
        self.sound_sixty_one_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_one))
        self.sound_sixty_one = pygame.sndarray.make_sound(self.sound_sixty_one_array)
        self.sound_sixty_one.set_volume(1.0)
        self.sound_sixty_two_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_two))
        self.sound_sixty_two = pygame.sndarray.make_sound(self.sound_sixty_two_array)
        self.sound_sixty_two.set_volume(1.0)
        self.sound_sixty_three_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_three))
        self.sound_sixty_three = pygame.sndarray.make_sound(self.sound_sixty_three_array)
        self.sound_sixty_three.set_volume(1.0)
        self.sound_sixty_four_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_four))
        self.sound_sixty_four = pygame.sndarray.make_sound(self.sound_sixty_four_array)
        self.sound_sixty_four.set_volume(1.0)
        self.sound_sixty_five_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_five))
        self.sound_sixty_five = pygame.sndarray.make_sound(self.sound_sixty_five_array)
        self.sound_sixty_five.set_volume(1.0)
        self.sound_sixty_six_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_six))
        self.sound_sixty_six = pygame.sndarray.make_sound(self.sound_sixty_six_array)
        self.sound_sixty_six.set_volume(1.0)
        self.sound_sixty_seven_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_seven))
        self.sound_sixty_seven = pygame.sndarray.make_sound(self.sound_sixty_seven_array)
        self.sound_sixty_seven.set_volume(1.0)
        self.sound_sixty_eight_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_eight))
        self.sound_sixty_eight = pygame.sndarray.make_sound(self.sound_sixty_eight_array)
        self.sound_sixty_eight.set_volume(1.0)
        self.sound_sixty_nine_array = np.concatenate((self.sound_sixty,self.sound_silence,self.sound_nine))
        self.sound_sixty_nine = pygame.sndarray.make_sound(self.sound_sixty_nine_array)
        self.sound_sixty_nine.set_volume(1.0)
        self.sound_seventy = self.mixer.Sound(self.filepathsound_seventy)
        self.sound_seventy.set_volume(1.0)
        self.sound_seventy_one_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_one))
        self.sound_seventy_one = pygame.sndarray.make_sound(self.sound_seventy_one_array)
        self.sound_seventy_one.set_volume(1.0)
        self.sound_seventy_two_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_two))
        self.sound_seventy_two = pygame.sndarray.make_sound(self.sound_seventy_two_array)
        self.sound_seventy_two.set_volume(1.0)
        self.sound_seventy_three_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_three))
        self.sound_seventy_three = pygame.sndarray.make_sound(self.sound_seventy_three_array)
        self.sound_seventy_three.set_volume(1.0)
        self.sound_seventy_four_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_four))
        self.sound_seventy_four = pygame.sndarray.make_sound(self.sound_seventy_four_array)
        self.sound_seventy_four.set_volume(1.0)
        self.sound_seventy_five_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_five))
        self.sound_seventy_five = pygame.sndarray.make_sound(self.sound_seventy_five_array)
        self.sound_seventy_five.set_volume(1.0)
        self.sound_seventy_six_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_six))
        self.sound_seventy_six = pygame.sndarray.make_sound(self.sound_seventy_six_array)
        self.sound_seventy_six.set_volume(1.0)
        self.sound_seventy_seven_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_seven))
        self.sound_seventy_seven = pygame.sndarray.make_sound(self.sound_seventy_seven_array)
        self.sound_seventy_seven.set_volume(1.0)
        self.sound_seventy_eight_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_eight))
        self.sound_seventy_eight = pygame.sndarray.make_sound(self.sound_seventy_eight_array)
        self.sound_seventy_eight.set_volume(1.0)
        self.sound_seventy_nine_array = np.concatenate((self.sound_seventy,self.sound_silence,self.sound_nine))
        self.sound_seventy_nine = pygame.sndarray.make_sound(self.sound_seventy_nine_array)
        self.sound_seventy_nine.set_volume(1.0)
        self.sound_eighty = self.mixer.Sound(self.filepathsound_eighty)
        self.sound_eighty.set_volume(1.0)
        self.sound_eighty_one_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_one))
        self.sound_eighty_one = pygame.sndarray.make_sound(self.sound_eighty_one_array)
        self.sound_eighty_one.set_volume(1.0)
        self.sound_eighty_two_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_two))
        self.sound_eighty_two = pygame.sndarray.make_sound(self.sound_eighty_two_array)
        self.sound_eighty_two.set_volume(1.0)
        self.sound_eighty_three_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_three))
        self.sound_eighty_three = pygame.sndarray.make_sound(self.sound_eighty_three_array)
        self.sound_eighty_three.set_volume(1.0)
        self.sound_eighty_four_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_four))
        self.sound_eighty_four = pygame.sndarray.make_sound(self.sound_eighty_four_array)
        self.sound_eighty_four.set_volume(1.0)
        self.sound_eighty_five_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_five))
        self.sound_eighty_five = pygame.sndarray.make_sound(self.sound_eighty_five_array)
        self.sound_eighty_five.set_volume(1.0)
        self.sound_eighty_six_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_six))
        self.sound_eighty_six = pygame.sndarray.make_sound(self.sound_eighty_six_array)
        self.sound_eighty_six.set_volume(1.0)
        self.sound_eighty_seven_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_seven))
        self.sound_eighty_seven = pygame.sndarray.make_sound(self.sound_eighty_seven_array)
        self.sound_eighty_seven.set_volume(1.0)
        self.sound_eighty_eight_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_eight))
        self.sound_eighty_eight = pygame.sndarray.make_sound(self.sound_eighty_eight_array)
        self.sound_eighty_eight.set_volume(1.0)
        self.sound_eighty_nine_array = np.concatenate((self.sound_eighty,self.sound_silence,self.sound_nine))
        self.sound_eighty_nine = pygame.sndarray.make_sound(self.sound_eighty_nine_array)
        self.sound_eighty_nine.set_volume(1.0)
        self.sound_ninety = self.mixer.Sound(self.filepathsound_ninety)
        self.sound_ninety.set_volume(1.0)
        self.sound_ninety_one_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_one))
        self.sound_ninety_one = pygame.sndarray.make_sound(self.sound_ninety_one_array)
        self.sound_ninety_one.set_volume(1.0)
        self.sound_ninety_two_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_two))
        self.sound_ninety_two = pygame.sndarray.make_sound(self.sound_ninety_two_array)
        self.sound_ninety_two.set_volume(1.0)
        self.sound_ninety_three_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_three))
        self.sound_ninety_three = pygame.sndarray.make_sound(self.sound_ninety_three_array)
        self.sound_ninety_three.set_volume(1.0)
        self.sound_ninety_four_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_four))
        self.sound_ninety_four = pygame.sndarray.make_sound(self.sound_ninety_four_array)
        self.sound_ninety_four.set_volume(1.0)
        self.sound_ninety_five_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_five))
        self.sound_ninety_five = pygame.sndarray.make_sound(self.sound_ninety_five_array)
        self.sound_ninety_five.set_volume(1.0)
        self.sound_ninety_six_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_six))
        self.sound_ninety_six = pygame.sndarray.make_sound(self.sound_ninety_six_array)
        self.sound_ninety_six.set_volume(1.0)
        self.sound_ninety_seven_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_seven))
        self.sound_ninety_seven = pygame.sndarray.make_sound(self.sound_ninety_seven_array)
        self.sound_ninety_seven.set_volume(1.0)
        self.sound_ninety_eight_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_eight))
        self.sound_ninety_eight = pygame.sndarray.make_sound(self.sound_ninety_eight_array)
        self.sound_ninety_eight.set_volume(1.0)
        self.sound_ninety_nine_array = np.concatenate((self.sound_ninety,self.sound_silence,self.sound_nine))
        self.sound_ninety_nine = pygame.sndarray.make_sound(self.sound_ninety_nine_array)
        self.sound_ninety_nine.set_volume(1.0)
        self.sound_hundred = self.mixer.Sound(self.filepathsound_hundred)
        self.sound_hundred.set_volume(1.0)
        self.sound_hundred_one_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_one))
        self.sound_hundred_one = pygame.sndarray.make_sound(self.sound_hundred_one_array)
        self.sound_hundred_one.set_volume(1.0)
        self.sound_hundred_two_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_two))
        self.sound_hundred_two = pygame.sndarray.make_sound(self.sound_hundred_two_array)
        self.sound_hundred_two.set_volume(1.0)
        self.sound_hundred_three_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_three))
        self.sound_hundred_three = pygame.sndarray.make_sound(self.sound_hundred_three_array)
        self.sound_hundred_three.set_volume(1.0)
        self.sound_hundred_four_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_four))
        self.sound_hundred_four = pygame.sndarray.make_sound(self.sound_hundred_four_array)
        self.sound_hundred_four.set_volume(1.0)
        self.sound_hundred_five_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_five))
        self.sound_hundred_five = pygame.sndarray.make_sound(self.sound_hundred_five_array)
        self.sound_hundred_five.set_volume(1.0)
        self.sound_hundred_six_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_six))
        self.sound_hundred_six = pygame.sndarray.make_sound(self.sound_hundred_six_array)
        self.sound_hundred_six.set_volume(1.0)
        self.sound_hundred_seven_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_seven))
        self.sound_hundred_seven = pygame.sndarray.make_sound(self.sound_hundred_seven_array)
        self.sound_hundred_seven.set_volume(1.0)
        self.sound_hundred_eight_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_eight))
        self.sound_hundred_eight = pygame.sndarray.make_sound(self.sound_hundred_eight_array)
        self.sound_hundred_eight.set_volume(1.0)
        self.sound_hundred_nine_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_nine))
        self.sound_hundred_nine = pygame.sndarray.make_sound(self.sound_hundred_nine_array)
        self.sound_hundred_nine.set_volume(1.0)
        self.sound_hundred_ten_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_ten))
        self.sound_hundred_ten = pygame.sndarray.make_sound(self.sound_hundred_ten_array)
        self.sound_hundred_ten.set_volume(1.0)
        self.sound_hundred_eleven_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_eleven))
        self.sound_hundred_eleven = pygame.sndarray.make_sound(self.sound_hundred_eleven_array)
        self.sound_hundred_eleven.set_volume(1.0)
        self.sound_hundred_twelve_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_twelve))
        self.sound_hundred_twelve = pygame.sndarray.make_sound(self.sound_hundred_twelve_array)
        self.sound_hundred_twelve.set_volume(1.0)
        self.sound_hundred_thirteen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_thirteen))
        self.sound_hundred_thirteen = pygame.sndarray.make_sound(self.sound_hundred_thirteen_array)
        self.sound_hundred_thirteen.set_volume(1.0)
        self.sound_hundred_fourteen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_fourteen))
        self.sound_hundred_fourteen = pygame.sndarray.make_sound(self.sound_hundred_fourteen_array)
        self.sound_hundred_fourteen.set_volume(1.0)
        self.sound_hundred_fifteen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_fifteen))
        self.sound_hundred_fifteen = pygame.sndarray.make_sound(self.sound_hundred_fifteen_array)
        self.sound_hundred_fifteen.set_volume(1.0)
        self.sound_hundred_sixteen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_sixteen))
        self.sound_hundred_sixteen = pygame.sndarray.make_sound(self.sound_hundred_sixteen_array)
        self.sound_hundred_sixteen.set_volume(1.0)
        self.sound_hundred_seventeen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_seventeen))
        self.sound_hundred_seventeen = pygame.sndarray.make_sound(self.sound_hundred_seventeen_array)
        self.sound_hundred_seventeen.set_volume(1.0)
        self.sound_hundred_eighteen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_eighteen))
        self.sound_hundred_eighteen = pygame.sndarray.make_sound(self.sound_hundred_eighteen_array)
        self.sound_hundred_eighteen.set_volume(1.0)
        self.sound_hundred_nineteen_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_nineteen))
        self.sound_hundred_nineteen = pygame.sndarray.make_sound(self.sound_hundred_nineteen_array)
        self.sound_hundred_nineteen.set_volume(1.0)
        self.sound_hundred_twenty_array = np.concatenate((self.sound_hundred,self.sound_silence,self.sound_twenty))
        self.sound_hundred_twenty = pygame.sndarray.make_sound(self.sound_hundred_twenty_array)
        self.sound_hundred_twenty.set_volume(1.0)
        self.playlist_laptime = [self.sound_point,self.sound_point, self.sound_point, self.sound_point, self.sound_point, self.sound_point, self.sound_point, self.sound_point]
        self.playlist_fuel = [self.sound_point,self.sound_point, self.sound_point, self.sound_point, self.sound_point, self.sound_point, self.sound_point]
        self.soundlist = {
            's': self.sound_silence,
            'p': self.sound_point,
            'm': self.sound_minute,
            'ms': self.sound_minutes,
            'f': self.sound_fuel,
            'l': self.sound_fuel_liters,
            'g': self.sound_fuel_gallons,
            'b': self.sound_bestlap,
            '0': self.sound_zero,
            '1': self.sound_one,
            '2': self.sound_two,
            '3': self.sound_three,
            '4': self.sound_four,
            '5': self.sound_five,
            '6': self.sound_six,
            '7': self.sound_seven,
            '8': self.sound_eight,
            '9': self.sound_nine,
            '10': self.sound_ten,
            '11': self.sound_eleven,
            '12': self.sound_twelve,
            '13': self.sound_thirteen,
            '14': self.sound_fourteen,
            '15': self.sound_fifteen,
            '16': self.sound_sixteen,
            '17': self.sound_seventeen,
            '18': self.sound_eighteen,
            '19': self.sound_nineteen,
            '20': self.sound_twenty,
            '21': self.sound_twenty_one,
            '22': self.sound_twenty_two,
            '23': self.sound_twenty_three,
            '24': self.sound_twenty_four,
            '25': self.sound_twenty_five,
            '26': self.sound_twenty_six,
            '27': self.sound_twenty_seven,
            '28': self.sound_twenty_eight,
            '29': self.sound_twenty_nine,
            '30': self.sound_thirty,
            '31': self.sound_thirty_one,
            '32': self.sound_thirty_two,
            '33': self.sound_thirty_three,
            '34': self.sound_thirty_four,
            '35': self.sound_thirty_five,
            '36': self.sound_thirty_six,
            '37': self.sound_thirty_seven,
            '38': self.sound_thirty_eight,
            '39': self.sound_thirty_nine,
            '40': self.sound_forty,
            '41': self.sound_forty_one,
            '42': self.sound_forty_two,
            '43': self.sound_forty_three,
            '44': self.sound_forty_four,
            '45': self.sound_forty_five,
            '46': self.sound_forty_six,
            '47': self.sound_forty_seven,
            '48': self.sound_forty_eight,
            '49': self.sound_forty_nine,
            '50': self.sound_fifty,
            '51': self.sound_fifty_one,
            '52': self.sound_fifty_two,
            '53': self.sound_fifty_three,
            '54': self.sound_fifty_four,
            '55': self.sound_fifty_five,
            '56': self.sound_fifty_six,
            '57': self.sound_fifty_seven,
            '58': self.sound_fifty_eight,
            '59': self.sound_fifty_nine,
            '60': self.sound_sixty,
            '61': self.sound_sixty_one,
            '62': self.sound_sixty_two,
            '63': self.sound_sixty_three,
            '64': self.sound_sixty_four,
            '65': self.sound_sixty_five,
            '66': self.sound_sixty_six,
            '67': self.sound_sixty_seven,
            '68': self.sound_sixty_eight,
            '69': self.sound_sixty_nine,
            '70': self.sound_seventy,
            '71': self.sound_seventy_one,
            '72': self.sound_seventy_two,
            '73': self.sound_seventy_three,
            '74': self.sound_seventy_four,
            '75': self.sound_seventy_five,
            '76': self.sound_seventy_six,
            '77': self.sound_seventy_seven,
            '78': self.sound_seventy_eight,
            '79': self.sound_seventy_nine,
            '80': self.sound_eighty,
            '81': self.sound_eighty_one,
            '82': self.sound_eighty_two,
            '83': self.sound_eighty_three,
            '84': self.sound_eighty_four,
            '85': self.sound_eighty_five,
            '86': self.sound_eighty_six,
            '87': self.sound_eighty_seven,
            '88': self.sound_eighty_eight,
            '89': self.sound_eighty_nine,
            '90': self.sound_ninety,
            '91': self.sound_ninety_one,
            '92': self.sound_ninety_two,
            '93': self.sound_ninety_three,
            '94': self.sound_ninety_four,
            '95': self.sound_ninety_five,
            '96': self.sound_ninety_six,
            '97': self.sound_ninety_seven,
            '98': self.sound_ninety_eight,
            '99': self.sound_ninety_nine,
            '100': self.sound_hundred,
            '101': self.sound_hundred_one,
            '102': self.sound_hundred_two,
            '103': self.sound_hundred_three,
            '104': self.sound_hundred_four,
            '105': self.sound_hundred_five,
            '106': self.sound_hundred_six,
            '107': self.sound_hundred_seven,
            '108': self.sound_hundred_eight,
            '109': self.sound_hundred_nine,
            '110': self.sound_hundred_ten,
            '111': self.sound_hundred_eleven,
            '112': self.sound_hundred_twelve,
            '113': self.sound_hundred_thirteen,
            '114': self.sound_hundred_fourteen,
            '115': self.sound_hundred_fifteen,
            '116': self.sound_hundred_sixteen,
            '117': self.sound_hundred_seventeen,
            '118': self.sound_hundred_eighteen,
            '119': self.sound_hundred_nineteen,
            '120': self.sound_hundred_twenty,
            }

    def playSoundLaptime(self):
        if(configuration.bestlap == "enabled" ):
            if(timesystem.bestlapmilliseconds == timesystem.lastlapmilliseconds):
                self.playlist_laptime[0] = self.sound_bestlap
            else:
                self.playlist_laptime[0] = self.sound_silence
        if(timesystem.lastlapminutes==0):
            self.playlist_laptime[1] = self.sound_silence
            self.playlist_laptime[2] = self.sound_silence
        else:
            if(timesystem.lastlapminutes == 1):
                self.playlist_laptime[1] = self.soundlist.get(str(timesystem.lastlapminutes))
                self.playlist_laptime[2] = self.soundlist.get("m")
            else:
                self.playlist_laptime[1] = self.soundlist.get(str(timesystem.lastlapminutes))
                self.playlist_laptime[2] = self.soundlist.get("ms")
        self.playlist_laptime[3] = self.soundlist.get(str(timesystem.lastlapsecondsint))
        self.playlist_laptime[4] = self.soundlist.get("p")
        self.playlist_laptime[5] = self.soundlist.get(timesystem.lastlapmilliseconds1)
        self.playlist_laptime[6] = self.soundlist.get(timesystem.lastlapmilliseconds2)
        self.playlist_laptime[7] = self.soundlist.get(timesystem.lastlapmilliseconds3)
        # self.playlist_laptime[0] = self.sound_bestlap
        # self.playlist_laptime[1] = self.sound_one
        # self.playlist_laptime[2] = self.sound_minute
        # self.playlist_laptime[3] = self.sound_twenty_one
        # self.playlist_laptime[4] = self.sound_point
        # self.playlist_laptime[5] = self.sound_three
        # self.playlist_laptime[6] = self.sound_three
        # self.playlist_laptime[7] = self.sound_two
        self.joinsounds_laptime = np.concatenate((self.playlist_laptime[0],self.playlist_laptime[1], self.playlist_laptime[2],self.playlist_laptime[3], self.playlist_laptime[4],self.playlist_laptime[5], self.playlist_laptime[6],self.playlist_laptime[7]), axis=0)
        self.playsounds_laptime = pygame.sndarray.make_sound(self.joinsounds_laptime)
        self.chan.play(self.playsounds_laptime)
        self.hasplayedLastFuel = 1

    def playSoundFuel(self):
        if(configuration.fuelconvert == "Liters"):
            if(fuelsystem.currentfuel<10.00):
                self.playlist_fuel[0] = self.sound_fuel
                self.playlist_fuel[1] = self.sound_silence
                self.playlist_fuel[2] = self.soundlist.get(fuelsystem.currentfuel_10)
                self.playlist_fuel[3] = self.sound_point
                self.playlist_fuel[4] = self.soundlist.get(fuelsystem.currentfuel_0)
                self.playlist_fuel[5] = self.soundlist.get(fuelsystem.currentfuel_00)
                self.playlist_fuel[6] = self.sound_fuel_liters
                self.joinsounds_fuel = np.concatenate((self.playlist_fuel[0],self.playlist_fuel[1], self.playlist_fuel[2],self.playlist_fuel[3], self.playlist_fuel[4],self.playlist_fuel[5], self.playlist_fuel[6]), axis=0)
                self.playsounds_fuel = pygame.sndarray.make_sound(self.joinsounds_fuel)
                self.chan.queue(self.playsounds_fuel)
            elif(fuelsystem.currentfuel>10.00 and fuelsystem.currentfuel < 100.00):
                self.playlist_fuel[0] = self.sound_fuel
                self.playlist_fuel[1] = self.sound_silence
                self.playlist_fuel[2] = self.soundlist.get(fuelsystem.currentfuel_100+fuelsystem.currentfuel_10)
                self.playlist_fuel[3] = self.sound_point
                self.playlist_fuel[4] = self.soundlist.get(fuelsystem.currentfuel_0)
                self.playlist_fuel[5] = self.soundlist.get(fuelsystem.currentfuel_00)
                self.playlist_fuel[6] = self.sound_fuel_liters
                self.joinsounds_fuel = np.concatenate((self.playlist_fuel[0],self.playlist_fuel[1], self.playlist_fuel[2],self.playlist_fuel[3], self.playlist_fuel[4],self.playlist_fuel[5], self.playlist_fuel[6]), axis=0)
                self.playsounds_fuel = pygame.sndarray.make_sound(self.joinsounds_fuel)
                self.chan.queue(self.playsounds_fuel)
            elif(fuelsystem.currentfuel>100.00):
                self.playlist_fuel[0] = self.sound_silence
                self.playlist_fuel[1] = self.sound_fuel
                self.playlist_fuel[2] = self.soundlist.get(fuelsystem.currentfuel_100+fuelsystem.currentfuel_10)
                self.playlist_fuel[3] = self.sound_point
                self.playlist_fuel[4] = self.soundlist.get(fuelsystem.currentfuel_0)
                self.playlist_fuel[5] = self.soundlist.get(fuelsystem.currentfuel_00)
                self.playlist_fuel[6] = self.sound_fuel_liters
                self.joinsounds_fuel = np.concatenate((self.playlist_fuel[0],self.playlist_fuel[1], self.playlist_fuel[2],self.playlist_fuel[3], self.playlist_fuel[4],self.playlist_fuel[5], self.playlist_fuel[6]), axis=0)
                self.playsounds_fuel = pygame.sndarray.make_sound(self.joinsounds_fuel)
                self.chan.queue(self.playsounds_fuel)
        elif(configuration.fuelconvert == "Gallons"):
            if(fuelsystem.currentfuelgallons<10.00):
                self.playlist_fuel[0] = self.sound_fuel
                self.playlist_fuel[1] = self.sound_silence
                self.playlist_fuel[2] = self.soundlist.get(fuelsystem.currentfuel_10)
                self.playlist_fuel[3] = self.sound_point
                self.playlist_fuel[4] = self.soundlist.get(fuelsystem.currentfuel_0)
                self.playlist_fuel[5] = self.soundlist.get(fuelsystem.currentfuel_00)
                self.playlist_fuel[6] = self.sound_fuel_gallons
                self.joinsounds_fuel = np.concatenate((self.playlist_fuel[0],self.playlist_fuel[1], self.playlist_fuel[2],self.playlist_fuel[3], self.playlist_fuel[4],self.playlist_fuel[5], self.playlist_fuel[6]), axis=0)
                self.playsounds_fuel = pygame.sndarray.make_sound(self.joinsounds_fuel)
                self.chan.queue(self.playsounds_fuel)
            elif(fuelsystem.currentfuelgallons>10.00 and fuelsystem.currentfuelgallons < 100.00):
                self.playlist_fuel[0] = self.sound_fuel
                self.playlist_fuel[1] = self.sound_silence
                self.playlist_fuel[2] = self.soundlist.get(fuelsystem.currentfuel_100+fuelsystem.currentfuel_10)
                self.playlist_fuel[3] = self.sound_point
                self.playlist_fuel[4] = self.soundlist.get(fuelsystem.currentfuel_0)
                self.playlist_fuel[5] = self.soundlist.get(fuelsystem.currentfuel_00)
                self.playlist_fuel[6] = self.sound_fuel_gallons
                self.joinsounds_fuel = np.concatenate((self.playlist_fuel[0],self.playlist_fuel[1], self.playlist_fuel[2],self.playlist_fuel[3], self.playlist_fuel[4],self.playlist_fuel[5], self.playlist_fuel[6]), axis=0)
                self.playsounds_fuel = pygame.sndarray.make_sound(self.joinsounds_fuel)
                self.chan.queue(self.playsounds_fuel)
            elif(fuelsystem.currentfuelgallons>100.00):
                self.playlist_fuel[0] = self.sound_silence
                self.playlist_fuel[1] = self.sound_fuel
                self.playlist_fuel[2] = self.soundlist.get(fuelsystem.currentfuel_100+fuelsystem.currentfuel_10)
                self.playlist_fuel[3] = self.sound_point
                self.playlist_fuel[4] = self.soundlist.get(fuelsystem.currentfuel_0)
                self.playlist_fuel[5] = self.soundlist.get(fuelsystem.currentfuel_00)
                self.playlist_fuel[6] = self.sound_fuel_gallons
                self.joinsounds_fuel = np.concatenate((self.playlist_fuel[0],self.playlist_fuel[1], self.playlist_fuel[2],self.playlist_fuel[3], self.playlist_fuel[4],self.playlist_fuel[5], self.playlist_fuel[6]), axis=0)
                self.playsounds_fuel = pygame.sndarray.make_sound(self.joinsounds_fuel)
                self.chan.queue(self.playsounds_fuel)

    def playSound(self):
        """ join sounds to form laptime sound in container self.joinsounds_laptime format and copy to playback container self.playsounds then play thru channel in mixer."""
        self.joinsounds_laptime = np.concatenate((self.playlist_laptime[0],self.playlist_laptime[1], self.playlist_laptime[2],self.playlist_laptime[3], self.playlist_laptime[4],self.playlist_laptime[5],self.playlist_laptime[6], self.playlist_laptime[7]), axis=0)
        self.playsounds_laptime = pygame.sndarray.make_sound(self.joinsounds_laptime)
        self.chan.play(self.playsounds_laptime)
        #ac.console("playSound")

class TimerClass:
    """ Controls time recording storage combination output of laptimes input to getTime() is milliseconds from siminfo class obj instance timesystem. """
    def __init__(self):
        self.currentlap = 0
        self.completedlaps = 0
        self.bestlapminutes = 0.0
        self.bestlapsecondsint = 0.0
        self.bestlapmilliseconds = 0.0
        self.bestlapmillisecondsStr = ""
        self.bestlapmilliseconds1 = ""
        self.bestlapmilliseconds2 = ""
        self.bestlapmilliseconds3 = ""
        self.insertzeroatminutesbest = ""

        self.lastlapminutes = 0.0
        self.lastlapsecondsint = 0.0
        self.lastlapmilliseconds = 0.0
        self.lastlapmillisecondsStr = ""
        self.lastlapmilliseconds1 = ""
        self.lastlapmilliseconds2 = ""
        self.lastlapmilliseconds3 = ""
        self.insertzeroatminuteslast = ""

        self.currentlapminutes = 0.0
        self.currentlapsecondsint = 0.0
        self.currentlapmilliseconds = 0.0
        self.currentlapmillisecondsStr = ""
        self.currentlapmilliseconds1 = "0"
        self.currentlapmilliseconds2 = "0"
        self.currentlapmilliseconds3 = "0"
        self.insertzeroatminutescurrent = ""

    def updateLapTime(self,thelap,thetime1,thetime2,thetime3):
        self.currentlap = thelap
        self.bestlapmilliseconds = thetime1
        self.lastlapmilliseconds = thetime2
        self.currentlapmilliseconds = thetime3

    def getCurrentLap(self):
        return self.currentlap

    def getBestLapTime(self):
        if(self.bestlapmilliseconds):
            if(self.bestlapmilliseconds<60000):
                self.bestlapminutes = 0
                self.bestlapsecondsint = int((self.bestlapmilliseconds/1000) // 1 * 1)
                self.bestlapmillisecondsStr = format(self.bestlapmilliseconds/1000, '.3f')
                self.bestlapmilliseconds1 = self.bestlapmillisecondsStr[-3:-2]
                self.bestlapmilliseconds2 = self.bestlapmillisecondsStr[-2:-1]
                self.bestlapmilliseconds3 = self.bestlapmillisecondsStr[-1]
                if(self.bestlapsecondsint<10):
                    self.insertzeroatminutesbest = "0{0}".format(self.bestlapsecondsint)
                    return "{0}:{1}:{2}{3}{4}".format(self.bestlapminutes,self.insertzeroatminutesbest,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
                else:
                    self.bestlapsecondsint = int((self.bestlapmilliseconds/1000) - (self.bestlapminutes*60))
                    return "{0}:{1}:{2}{3}{4}".format(self.bestlapminutes,self.bestlapsecondsint,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
            else:
                self.bestlapminutes = int((self.bestlapmilliseconds/1000)/60)
                self.bestlapsecondsint = int((self.bestlapmilliseconds/1000) - (self.bestlapminutes*60))
                self.bestlapmillisecondsStr = format(self.bestlapmilliseconds/1000, '.3f')
                self.bestlapmilliseconds1 = self.bestlapmillisecondsStr[-3:-2]
                self.bestlapmilliseconds2 = self.bestlapmillisecondsStr[-2:-1]
                self.bestlapmilliseconds3 = self.bestlapmillisecondsStr[-1]
                if(self.bestlapsecondsint<10):
                    self.insertzeroatminutesbest = "0{0}".format(self.bestlapsecondsint)
                    return "{0}:{1}:{2}{3}{4}".format(self.bestlapminutes,self.insertzeroatminutesbest,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
                else:
                    self.bestlapsecondsint = int((self.bestlapmilliseconds/1000) - (self.bestlapminutes*60))
                    return "{0}:{1}:{2}{3}{4}".format(self.bestlapminutes,self.bestlapsecondsint,self.bestlapmilliseconds1,self.bestlapmilliseconds2,self.bestlapmilliseconds3)
        else:
            return "-:--:---"

    def getLastLapTime(self):
        if(self.lastlapmilliseconds):
            if(self.lastlapmilliseconds<60000):
                self.lastlapminutes = 0
                self.lastlapsecondsint = int((self.lastlapmilliseconds/1000) // 1 * 1)
                self.lastlapmillisecondsStr = format(self.lastlapmilliseconds/1000, '.3f')
                self.lastlapmilliseconds1 = self.lastlapmillisecondsStr[-3:-2]
                self.lastlapmilliseconds2 = self.lastlapmillisecondsStr[-2:-1]
                self.lastlapmilliseconds3 = self.lastlapmillisecondsStr[-1]
                if(self.lastlapsecondsint<10):
                    self.insertzeroatminuteslast = "0{0}".format(self.lastlapsecondsint)
                    return "{0}:{1}:{2}{3}{4}".format(self.lastlapminutes,self.insertzeroatminuteslast,self.lastlapmilliseconds1,self.lastlapmilliseconds2,self.lastlapmilliseconds3)
                else:
                    self.lastlapsecondsint = int((self.lastlapmilliseconds/1000) - (self.lastlapminutes*60))
                    return "{0}:{1}:{2}{3}{4}".format(self.lastlapminutes,self.lastlapsecondsint,self.lastlapmilliseconds1,self.lastlapmilliseconds2,self.lastlapmilliseconds3)
            else:
                self.lastlapminutes = int((self.lastlapmilliseconds/1000)/60)
                self.lastlapsecondsint = int((self.lastlapmilliseconds/1000) - (self.lastlapminutes*60))
                self.lastlapmillisecondsStr = format(self.lastlapmilliseconds/1000, '.3f')
                self.lastlapmilliseconds1 = self.lastlapmillisecondsStr[-3:-2]
                self.lastlapmilliseconds2 = self.lastlapmillisecondsStr[-2:-1]
                self.lastlapmilliseconds3 = self.lastlapmillisecondsStr[-1]
                if(self.lastlapsecondsint<10):
                    self.insertzeroatminuteslast = "0{0}".format(self.lastlapsecondsint)
                    return "{0}:{1}:{2}{3}{4}".format(self.lastlapminutes,self.insertzeroatminuteslast,self.lastlapmilliseconds1,self.lastlapmilliseconds2,self.lastlapmilliseconds3)
                else:
                    self.lastlapsecondsint = int((self.lastlapmilliseconds/1000) - (self.lastlapminutes*60))
                    return "{0}:{1}:{2}{3}{4}".format(self.lastlapminutes,self.lastlapsecondsint,self.lastlapmilliseconds1,self.lastlapmilliseconds2,self.lastlapmilliseconds3)
        else:
            return "-:--:---"

    def getCurrentLapTime(self):
        if(self.currentlapmilliseconds):
            if(self.currentlapmilliseconds<60000):
                self.currentlapminutes = 0
                self.currentlapsecondsint = int((self.currentlapmilliseconds/1000) // 1 * 1)
                self.currentlapmillisecondsStr = format(self.currentlapmilliseconds/1000, '.3f')
                self.currentlapmilliseconds1 = self.currentlapmillisecondsStr[-3:-2]
                self.currentlapmilliseconds2 = self.currentlapmillisecondsStr[-2:-1]
                self.currentlapmilliseconds3 = self.currentlapmillisecondsStr[-1]
                if(self.currentlapsecondsint<10):
                    self.insertzeroatminutescurrent = "0{0}".format(self.currentlapsecondsint)
                    return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.insertzeroatminutescurrent,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
                else:
                    self.currentlapsecondsint = int((self.currentlapmilliseconds/1000) - (self.currentlapminutes*60))
                    return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.currentlapsecondsint,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
            else:
                self.currentlapminutes = int((self.currentlapmilliseconds/1000)/60)
                self.currentlapsecondsint = int((self.currentlapmilliseconds/1000) - (self.currentlapminutes*60))
                self.currentlapmillisecondsStr = format(self.currentlapmilliseconds/1000, '.3f')
                self.currentlapmilliseconds1 = self.currentlapmillisecondsStr[-3:-2]
                self.currentlapmilliseconds2 = self.currentlapmillisecondsStr[-2:-1]
                self.currentlapmilliseconds3 = self.currentlapmillisecondsStr[-1]
                if(self.currentlapsecondsint<10):
                    self.insertzeroatminutescurrent = "0{0}".format(self.currentlapsecondsint)
                    return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.insertzeroatminutescurrent,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
                else:
                    self.currentlapsecondsint = int((self.currentlapmilliseconds/1000) - (self.currentlapminutes*60))
                    return "{0}:{1}:{2}{3}{4}".format(self.currentlapminutes,self.currentlapsecondsint,self.currentlapmilliseconds1,self.currentlapmilliseconds2,self.currentlapmilliseconds3)
        else:
            return "-:--:---"

class FuelClass:
    """ Controls fuel record value storage output of fuel input to getTime() is float from siminfo class instance fuelsystem"""
    def __init__(self):
        self.currentfuel = 0.0
        self.currentfuelgallons = 0.0
        self.currentfuelstr = ""
        self.currentfuel_100 = ""
        self.currentfuel_10 = ""
        self.currentfuel_0 = ""
        self.currentfuel_00 = ""
        self.currentfuel_display = ""
        self.totalfuel = 0.0
        self.usedfuel = 0.0

    def updateFuel(self,fuel):
        self.currentfuel = fuel
        self.currentfuelgallons = fuel*0.264172
        if(configuration.fuelconvert == "Liters"):
            self.currentfuelstr = format(self.currentfuel, '.3f')
            if(self.currentfuel<10.00):
                self.currentfuel_10 = self.currentfuelstr[0]
                self.currentfuel_0 = self.currentfuelstr[2]
                self.currentfuel_00 = self.currentfuelstr[3]
                self.currentfuel_display = self.currentfuel_10 + "." + self.currentfuel_0 + self.currentfuel_00
            elif(self.currentfuel > 10.00 and self.currentfuel < 100.00):
                self.currentfuel_100 = self.currentfuelstr[0]
                self.currentfuel_10 = self.currentfuelstr[1]
                self.currentfuel_0 = self.currentfuelstr[3]
                self.currentfuel_00 =  self.currentfuelstr[4]
                self.currentfuel_display = self.currentfuel_100 + self.currentfuel_10 + "." + self.currentfuel_0 + self.currentfuel_00
            elif(self.currentfuel>100.00):
                self.currentfuel_100 = self.currentfuelstr[0] + self.currentfuelstr[1]
                self.currentfuel_10 = self.currentfuelstr[2]
                self.currentfuel_0 = self.currentfuelstr[4]
                self.currentfuel_00 =  self.currentfuelstr[5]
                self.currentfuel_display = self.currentfuel_100 + self.currentfuel_10 + "." + self.currentfuel_0 + self.currentfuel_00
        elif(configuration.fuelconvert == "Gallons"):
            self.currentfuelstr = format(self.currentfuelgallons, '.3f')
            if( self.currentfuelgallons<10.00):
                self.currentfuel_10 = self.currentfuelstr[0]
                self.currentfuel_0 = self.currentfuelstr[2]
                self.currentfuel_00 = self.currentfuelstr[3]
                self.currentfuel_display = self.currentfuel_10 + "." + self.currentfuel_0 + self.currentfuel_00
            elif(self.currentfuelgallons > 10.00 and  self.currentfuelgallons < 100.00):
                self.currentfuel_100 = self.currentfuelstr[0]
                self.currentfuel_10 = self.currentfuelstr[1]
                self.currentfuel_0 = self.currentfuelstr[3]
                self.currentfuel_00 =  self.currentfuelstr[4]
                self.currentfuel_display = self.currentfuel_100 + self.currentfuel_10 + "." + self.currentfuel_0 + self.currentfuel_00
            elif(self.currentfuelgallons>100.00):
                self.currentfuel_100 = self.currentfuelstr[0] + self.currentfuelstr[1]
                self.currentfuel_10 = self.currentfuelstr[2]
                self.currentfuel_0 = self.currentfuelstr[4]
                self.currentfuel_00 =  self.currentfuelstr[5]
                self.currentfuel_display = self.currentfuel_100 + self.currentfuel_10 + "." + self.currentfuel_0 + self.currentfuel_00

    def getCurrentFuel(self):
        if(configuration.fuelconvert == "Liters"):
            return self.currentfuel_display
        elif(configuration.fuelconvert == "Gallons"):
            return self.currentfuel_display

#------------------------------------------------------------------------------------------------------------------------------------------
# SIM INFO by @Rombik
# Big thanks to @Rombik who wrote this sim info  module. Saved me maybe a week of thrashing to get it going and testing
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
        ('packetId', c_int32),
        ('gas', c_float),
        ('brake', c_float),
        ('fuel', c_float),
        ('gear', c_int32),
        ('rpms', c_int32),
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
        ('numberOfTyresOut', c_int32),
        ('pitLimiterOn', c_int32),
        ('abs', c_float),
    ]

class SPageFileGraphic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('packetId', c_int32),
        ('status', AC_STATUS),
        ('session', AC_SESSION_TYPE),
         # NOTE: if you want str instead bytes, access it without '_'
        ('_currentTime', c_char * 15),
        ('_lastTime', c_char * 15),
        ('_bestTime', c_char * 15),
        ('_split', c_char * 15),
        ('completedLaps', c_int32),
        ('position', c_int32),
        ('iCurrentTime', c_int32),
        ('iLastTime', c_int32),
        ('iBestTime', c_int32),
        ('sessionTimeLeft', c_float),
        ('distanceTraveled', c_float),
        ('isInPit', c_int32),
        ('currentSectorIndex', c_int32),
        ('lastSectorTime', c_int32),
        ('numberOfLaps', c_int32),
        ('_tyreCompound', c_char * 33),

        ('replayTimeMultiplier', c_float),
        ('normalizedCarPosition', c_float),
        ('carCoordinates', c_float * 3),
    ]

class SPageFileStatic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('_smVersion', c_char * 15),
        ('_acVersion', c_char * 15),
        # session static info
        ('numberOfSessions', c_int32),
        ('numCars', c_int32),
        ('_carModel', c_char * 33),
        ('_track', c_char * 33),
        ('_playerName', c_char * 33),
        ('_playerSurname', c_char * 33),
        ('_playerNick', c_char * 33),
        ('sectorCount', c_int32),

        # car static info
        ('maxTorque', c_float),
        ('maxPower', c_float),
        ('maxRpm', c_int32),
        ('maxFuel', c_float),
        ('suspensionMaxTravel', c_float * 4),
        ('tyreRadius', c_float * 4),
    ]

#make _char_p properties return unicode strings
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
        self._acpmf_physics = mmap.mmap(0, ctypes.sizeof(SPageFilePhysics), "acpmf_physics")
        self._acpmf_graphics = mmap.mmap(0, ctypes.sizeof(SPageFileGraphic), "acpmf_graphics")
        #self._acpmf_static = mmap.mmap(0, ctypes.sizeof(SPageFileStatic), "acpmf_static")
        self.physics = SPageFilePhysics.from_buffer(self._acpmf_physics)
        self.graphics = SPageFileGraphic.from_buffer(self._acpmf_graphics)
        #self.static = SPageFileStatic.from_buffer(self._acpmf_static)

    def close(self):
        self._acpmf_physics.close()
        self._acpmf_graphics.close()
        #self._acpmf_static.close()

    def __del__(self):
        self.close()

class DisplayClass:
    """display elements labels buttons and callback functions """
    def __init__(self):
        self.lapswitch = None
        self.fuelswitch = None
        self.fuelconvert = configuration.fuelconvert
        self.bestlap = None
        self.appWindow = None
        self.currentlaplabel = None
        self.besttimelabel = None
        self.lasttimelabel = None
        self.currenttimelabel = None
        self.currentfuellabel = None
        self.spinner = None
        self.spinnerEvent = self.spinnerEventFunction
        self.checkboxContainerLaptime = None
        self.checkboxLabelLaptime = None
        self.checkboxEventLaptime = self.checkboxEventFunctionLaptime
        self.checkboxContainerFuel = None
        self.checkboxLabelFuel = None
        self.checkboxEventFuel = self.checkboxEventFunctionFuel
        self.checkboxContainerFuelConvert = None
        self.checkboxLabelFuelConvert = None
        self.checkboxEventFuelConvert = self.checkboxEventFunctionFuelConvert
        self.checkboxContainerBestLap = None
        self.checkboxLabelBestLap = None
        self.checkboxEventBestLap = self.checkboxEventFunctionBestLap

        self.AppActivated = self.AppActivatedFunction
        self.AppDismissed = self.AppDismissedFunction

    def spinnerEventFunction(self,x):
        ac.console("hit")

    def checkboxEventFunctionBestLap(self,x,y):
        if(mInfoDisplay.bestlap):
            configuration.setBestLapDisabled()
            mInfoDisplay.bestlap = False
            ac.setText(mInfoDisplay.checkboxLabelBestLap, "Disabled")
            ac.setFontColor(mInfoDisplay.checkboxLabelBestLap, 1.0, 0.0, 0.0, 1)
        else:
            configuration.setBestLapEnabled()
            mInfoDisplay.bestlap = True
            ac.setText(mInfoDisplay.checkboxLabelBestLap, "Best Lap")
            ac.setFontColor(mInfoDisplay.checkboxLabelBestLap, 0.0, 1.0, 0.1, 1)

    def checkboxEventFunctionFuel(self,x,y):
        if(mInfoDisplay.fuelswitch):
            configuration.setFuelSwitchDisabled()
            mInfoDisplay.fuelswitch = False
            ac.setText(mInfoDisplay.checkboxLabelFuel, "Disabled")
            ac.setFontColor(mInfoDisplay.checkboxLabelFuel, 1.0, 0.0, 0.0, 1)
        else:
            configuration.setFuelSwitchEnabled()
            mInfoDisplay.fuelswitch = True
            ac.setText(mInfoDisplay.checkboxLabelFuel, "Enabled")
            ac.setFontColor(mInfoDisplay.checkboxLabelFuel, 0.0, 1.0, 0.1, 1)

    def checkboxEventFunctionFuelConvert(self,x,y):
        if(mInfoDisplay.fuelconvert == "Liters"):
            mInfoDisplay.fuelconvert = "Gallons"
            configuration.setFuelConvertGallons()
            ac.setText(mInfoDisplay.checkboxLabelFuelConvert, "Gallons")
            ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 0.0, 1.0, 0.1, 1)
        else:
            mInfoDisplay.fuelconvert = "Liters"
            configuration.setFuelConvertLiters()
            ac.setText(mInfoDisplay.checkboxLabelFuelConvert, "Liters")
            ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 0.0, 1.0, 0.1, 1)

    def checkboxEventFunctionLaptime(self,x,y):
        if(mInfoDisplay.lapswitch):
            mInfoDisplay.lapswitch = False
            configuration.setLapSwitchDisabled()
            ac.setText(mInfoDisplay.checkboxLabelLaptime, "Disabled")
            ac.setFontColor(mInfoDisplay.checkboxLabelLaptime, 1.0, 0.0, 0.0, 1)
            configuration.setBestLapDisabled()
            mInfoDisplay.bestlap = False
            ac.setText(mInfoDisplay.checkboxLabelBestLap, "Disabled")
            ac.setFontColor(mInfoDisplay.checkboxLabelBestLap, 1.0, 0.0, 0.0, 1)
        else:
            mInfoDisplay.lapswitch = True
            configuration.setLapSwitchEnabled()
            ac.setText(mInfoDisplay.checkboxLabelLaptime, "Enabled")
            ac.setFontColor(mInfoDisplay.checkboxLabelLaptime, 0.0, 1.0, 0.1, 1)
            configuration.setBestLapEnabled()
            mInfoDisplay.bestlap = True
            ac.setText(mInfoDisplay.checkboxLabelBestLap, "Best Lap")
            ac.setFontColor(mInfoDisplay.checkboxLabelBestLap, 0.0, 1.0, 0.1, 1)


    def AppActivatedFunction(self,val):
        #must have a pass completion or crash!!!
        timesystem.updateLapTime(infosystem.graphics.completedLaps,infosystem.graphics.iBestTime,infosystem.graphics.iLastTime, infosystem.graphics.iCurrentTime)
        fuelsystem.updateFuel(infosystem.physics.fuel)
        configuration.setLapSwitchEnabled()
        configuration.setFuelSwitchEnabled()
        soundsystem.hasplayedLastFuel = 0
        #pygame.init()
        #soundsystem.loadSounds()

    def AppDismissedFunction(self,val):
        #must have a pass completion or crash!!!
        configuration.setLapSwitchDisabled()
        configuration.setFuelSwitchDisabled()
        configuration.saveConfig()
        #pygame.quit()


#---------------------------------------------------------
# declare class instance objects and secondary init

configuration = ConfigClass()
configuration.loadConfig()
configuration.setInitialStatus()
infosystem = SimInfo()
timesystem = TimerClass()
fuelsystem = FuelClass()
soundsystem = SoundClass()
mInfoDisplay = DisplayClass()

#---------------------------------------------------------


def acMain(ac_version):
    """main init function which runs on game startup."""
    if(configuration.getLapSwitchStatus()=="enabled"):
        mInfoDisplay.lapswitch = True
    elif(configuration.getLapSwitchStatus()=="disabled"):
        mInfoDisplay.lapswitch = False
    if(configuration.getFuelSwitchStatus() =="enabled"):
        mInfoDisplay.fuelswitch = True
    elif(configuration.getFuelSwitchStatus()=="disabled"):
        mInfoDisplay.fuelswitch = False
    if(configuration.getBestLapStatus() =="enabled"):
        mInfoDisplay.bestlap = True
    elif(configuration.getBestLapStatus()=="disabled"):
        mInfoDisplay.bestlap = False

    mInfoDisplay.appWindow = ac.newApp("mInfo")
    ac.addRenderCallback(mInfoDisplay.appWindow, onFormRender)
    ac.addOnAppActivatedListener(mInfoDisplay.appWindow, mInfoDisplay.AppActivated)
    ac.addOnAppDismissedListener(mInfoDisplay.appWindow, mInfoDisplay.AppDismissed)
    ac.setSize(mInfoDisplay.appWindow, 250, 400)

    if(mInfoDisplay.fuelswitch is True):
        mInfoDisplay.currentfuellabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.currentfuellabel, 11, 220)
        ac.setFontColor(mInfoDisplay.currentfuellabel, 1.0, 1.0, 1.0, 1)
        ac.setFontAlignment(mInfoDisplay.currentfuellabel,'left')

        mInfoDisplay.checkboxContainerFuel = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerFuel, 230, 164)
        ac.setSize(mInfoDisplay.checkboxContainerFuel,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerFuel,mInfoDisplay.checkboxEventFuel)

        mInfoDisplay.checkboxLabelFuel = ac.addLabel(mInfoDisplay.appWindow, "Enabled")
        ac.setPosition(mInfoDisplay.checkboxLabelFuel, 26, 161)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuel, 0.0, 1.0, 0.1, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelFuel,'right')

        mInfoDisplay.checkboxContainerFuelConvert = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerFuelConvert, 230, 190)
        ac.setSize(mInfoDisplay.checkboxContainerFuelConvert,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerFuelConvert,mInfoDisplay.checkboxEventFuelConvert)

        mInfoDisplay.checkboxLabelFuelConvert = ac.addLabel(mInfoDisplay.appWindow, mInfoDisplay.fuelconvert)
        ac.setPosition(mInfoDisplay.checkboxLabelFuelConvert, 24, 186)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelFuelConvert,'right')

        # mInfoDisplay.spinner = ac.addSpinner(mInfoDisplay.appWindow, "soundpack")
        # ac.setPosition(mInfoDisplay.spinner,116,170)
        # ac.setSize(mInfoDisplay.spinner,70,24)
        # ac.setRange(mInfoDisplay.spinner,1,1)
        # ac.setValue(mInfoDisplay.spinner,1)
        # ac.addOnValueChangeListener(mInfoDisplay.spinner,mInfoDisplay.spinnerEvent)
    else:
        mInfoDisplay.currentfuellabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.currentfuellabel, 11, 220)
        ac.setFontColor(mInfoDisplay.currentfuellabel, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.currentfuellabel,'left')

        mInfoDisplay.checkboxContainerFuel = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerFuel, 230,164)
        ac.setSize(mInfoDisplay.checkboxContainerFuel,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerFuel,mInfoDisplay.checkboxEventFuel)

        mInfoDisplay.checkboxLabelFuel = ac.addLabel(mInfoDisplay.appWindow, "Disabled")
        ac.setPosition(mInfoDisplay.checkboxLabelFuel, 26, 161)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuel, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelFuel,'right')
        ac.setText(mInfoDisplay.currentfuellabel, "Fuel Remaining : ----- Liters")

        mInfoDisplay.checkboxContainerFuelConvert = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerFuelConvert, 230, 190)
        ac.setSize(mInfoDisplay.checkboxContainerFuelConvert,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerFuelConvert,mInfoDisplay.checkboxEventFuelConvert)

        mInfoDisplay.checkboxLabelFuelConvert = ac.addLabel(mInfoDisplay.appWindow, mInfoDisplay.fuelconvert)
        ac.setPosition(mInfoDisplay.checkboxLabelFuelConvert, 24, 186)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelFuelConvert,'right')

        # mInfoDisplay.spinner = ac.addSpinner(mInfoDisplay.appWindow, "soundpack")
        # ac.setPosition(mInfoDisplay.spinner,116,170)
        # ac.setSize(mInfoDisplay.spinner,70,24)
        # ac.setRange(mInfoDisplay.spinner,1,1)
        # ac.setValue(mInfoDisplay.spinner,1)
        # ac.addOnValueChangeListener(mInfoDisplay.spinner,mInfoDisplay.spinnerEvent)

    if(mInfoDisplay.lapswitch is True):
        mInfoDisplay.currentlaplabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.currentlaplabel, 16, 65)
        ac.setFontColor(mInfoDisplay.currentlaplabel, 1.0, 1.0, 1.0, 1)
        ac.setFontAlignment(mInfoDisplay.currentlaplabel,'left')

        mInfoDisplay.besttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.besttimelabel, 26, 85)
        ac.setFontColor(mInfoDisplay.besttimelabel, 1.0, 1.0, 1.0, 1)
        ac.setFontAlignment(mInfoDisplay.besttimelabel,'left')

        mInfoDisplay.lasttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.lasttimelabel, 31, 105)
        ac.setFontColor(mInfoDisplay.lasttimelabel, 1.0, 1.0, 1.0, 1)
        ac.setFontAlignment(mInfoDisplay.lasttimelabel,'left')

        mInfoDisplay.currenttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.currenttimelabel, 7, 125)
        ac.setFontColor(mInfoDisplay.currenttimelabel, 1.0, 1.0, 1.0, 1)
        ac.setFontAlignment(mInfoDisplay.currenttimelabel,'left')

        mInfoDisplay.checkboxContainerLaptime = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerLaptime, 230, 38)
        ac.setSize(mInfoDisplay.checkboxContainerLaptime,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerLaptime,mInfoDisplay.checkboxEventLaptime)

        mInfoDisplay.checkboxLabelLaptime = ac.addLabel(mInfoDisplay.appWindow, "Enabled")
        ac.setPosition(mInfoDisplay.checkboxLabelLaptime, 26, 35)
        ac.setFontColor(mInfoDisplay.checkboxLabelLaptime, 0.0, 1.0, 0.1, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelLaptime,'right')

        mInfoDisplay.checkboxContainerBestLap = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerBestLap, 230, 88)
        ac.setSize(mInfoDisplay.checkboxContainerBestLap,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerBestLap,mInfoDisplay.checkboxEventBestLap)

        mInfoDisplay.checkboxLabelBestLap = ac.addLabel(mInfoDisplay.appWindow, "Best Lap")
        ac.setPosition(mInfoDisplay.checkboxLabelBestLap, 26, 85)
        ac.setFontColor(mInfoDisplay.checkboxLabelBestLap, 0.0, 1.0, 0.1, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelBestLap,'right')
    else:
        mInfoDisplay.currentlaplabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.currentlaplabel, 16, 65)
        ac.setFontColor(mInfoDisplay.currentlaplabel, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.currentlaplabel,'left')

        mInfoDisplay.besttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.besttimelabel, 26, 85)
        ac.setFontColor(mInfoDisplay.besttimelabel, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.besttimelabel,'left')

        mInfoDisplay.lasttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.lasttimelabel, 31, 105)
        ac.setFontColor(mInfoDisplay.lasttimelabel, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.lasttimelabel,'left')

        mInfoDisplay.currenttimelabel = ac.addLabel(mInfoDisplay.appWindow, "mInfo")
        ac.setPosition(mInfoDisplay.currenttimelabel, 7, 125)
        ac.setFontColor(mInfoDisplay.currenttimelabel, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.currenttimelabel,'left')

        mInfoDisplay.checkboxContainerLaptime = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerLaptime, 230, 38)
        ac.setSize(mInfoDisplay.checkboxContainerLaptime,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerLaptime,mInfoDisplay.checkboxEventLaptime)

        mInfoDisplay.checkboxLabelLaptime = ac.addLabel(mInfoDisplay.appWindow, "Best Lap")
        ac.setPosition(mInfoDisplay.checkboxLabelLaptime, 26, 35)
        ac.setFontColor(mInfoDisplay.checkboxLabelLaptime, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelLaptime,'right')

        mInfoDisplay.checkboxContainerBestLap = ac.addCheckBox(mInfoDisplay.appWindow, "")
        ac.setPosition(mInfoDisplay.checkboxContainerBestLap, 230, 88)
        ac.setSize(mInfoDisplay.checkboxContainerBestLap,15,15)
        ac.addOnCheckBoxChanged(mInfoDisplay.checkboxContainerBestLap,mInfoDisplay.checkboxEventBestLap)

        mInfoDisplay.checkboxLabelBestLap = ac.addLabel(mInfoDisplay.appWindow, "Best Lap")
        ac.setPosition(mInfoDisplay.checkboxLabelBestLap, 26, 85)
        ac.setFontColor(mInfoDisplay.checkboxLabelBestLap, 1.0, 0.0, 0.0, 1)
        ac.setFontAlignment(mInfoDisplay.checkboxLabelBestLap,'right')

        ac.setText(mInfoDisplay.currentlaplabel, "current lap : -")
        ac.setText(mInfoDisplay.besttimelabel, "best time : -:--:---")
        ac.setText(mInfoDisplay.lasttimelabel, "last time : -:--:---")
        ac.setText(mInfoDisplay.currenttimelabel, "current time : -:--:---")
    ac.setBackgroundTexture(mInfoDisplay.appWindow, "apps/python/mInfo/images/mInfoBackground.png")
    pygame.init()
    soundsystem.loadSounds()
    return "mInfo"

def acUpdate(deltaT):
    """main loop.only update lap once and play sound once required as we are in a loop."""
    if(mInfoDisplay.lapswitch is True):
        soundsystem.hasplayedLastLaptime = 0
        if(timesystem.currentlap==0):
            timesystem.completedlaps = timesystem.currentlap
        if(timesystem.completedlaps < timesystem.currentlap):
            timesystem.completedlaps = timesystem.currentlap
            soundsystem.hasplayedLastLaptime = 1
            if(soundsystem.hasplayedLastLaptime==1):
                #ac.console("play sound")
                soundsystem.playSoundLaptime()
                soundsystem.hasplayedLastLaptime = 0
        timesystem.updateLapTime(infosystem.graphics.completedLaps,infosystem.graphics.iBestTime,infosystem.graphics.iLastTime, infosystem.graphics.iCurrentTime)
        ac.setFontColor(mInfoDisplay.currentlaplabel, 1.0, 1.0, 1.0, 1)
        ac.setFontColor(mInfoDisplay.besttimelabel, 1.0, 1.0, 1.0, 1)
        ac.setFontColor(mInfoDisplay.lasttimelabel, 1.0, 1.0, 1.0, 1)
        ac.setFontColor(mInfoDisplay.currenttimelabel, 1.0, 1.0, 1.0, 1)
        #ac.setFontColor(mInfoDisplay.spinner, 1.0, 1.0, 1.0, 1)
        ac.setText(mInfoDisplay.currentlaplabel, "current lap : {0}".format(timesystem.getCurrentLap()))
        ac.setText(mInfoDisplay.besttimelabel, "best time : {0}".format(timesystem.getBestLapTime()))
        ac.setText(mInfoDisplay.lasttimelabel, "last time : {0}".format(timesystem.getLastLapTime()))
        ac.setText(mInfoDisplay.currenttimelabel, "current time : {0}".format(timesystem.getCurrentLapTime()))
    else:
        timesystem.updateLapTime(infosystem.graphics.completedLaps,infosystem.graphics.iBestTime,infosystem.graphics.iLastTime, infosystem.graphics.iCurrentTime)
        ac.setFontColor(mInfoDisplay.currentlaplabel, 1.0, 0.0, 0.0, 1)
        ac.setFontColor(mInfoDisplay.besttimelabel, 1.0, 0.0, 0.0, 1)
        ac.setFontColor(mInfoDisplay.lasttimelabel, 1.0, 0.0, 0.0, 1)
        ac.setFontColor(mInfoDisplay.currenttimelabel, 1.0, 0.0, 0.0, 1)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 1.0, 0.0, 0.0, 1)
        #ac.setFontColor(mInfoDisplay.spinner, 1.0, 0.0, 0.0, 1)
        ac.setText(mInfoDisplay.currentlaplabel, "current lap : -")
        ac.setText(mInfoDisplay.besttimelabel, "best time : -:--:---")
        ac.setText(mInfoDisplay.lasttimelabel, "last time : -:--:---")
        ac.setText(mInfoDisplay.currenttimelabel, "current time : -:--:---")
    if(mInfoDisplay.fuelswitch is True):
        fuelsystem.updateFuel(infosystem.physics.fuel)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuel, 0.0, 1.0, 0.1, 1)
        ac.setFontColor(mInfoDisplay.currentfuellabel, 1.0, 1.0, 1.0, 1)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 0.0, 1.0, 0.1, 1)
        ac.setText(mInfoDisplay.currentfuellabel, "Fuel Remaining : {0} {1}".format(fuelsystem.getCurrentFuel(),mInfoDisplay.fuelconvert))
        if(mInfoDisplay.lapswitch is False):
            if(timesystem.currentlap==0):
                timesystem.completedlaps = timesystem.currentlap
            if(timesystem.completedlaps < timesystem.currentlap):
                timesystem.completedlaps = timesystem.currentlap
                soundsystem.hasplayedLastFuel = 1
                if(soundsystem.hasplayedLastFuel == 1):
                    soundsystem.playSoundFuel()
                    soundsystem.hasplayedLastFuel = 0
        else:
            if(soundsystem.hasplayedLastFuel == 1):
                soundsystem.playSoundFuel()
                soundsystem.hasplayedLastFuel = 0
    else:
        fuelsystem.updateFuel(infosystem.physics.fuel)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuel, 1.0, 0.0, 0.0, 1)
        ac.setFontColor(mInfoDisplay.currentfuellabel, 1.0, 0.0, 0.0, 1)
        ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 1.0, 0.0, 0.0, 1)
        ac.setText(mInfoDisplay.currentfuellabel, "Fuel Remaining : ----- {0}".format(mInfoDisplay.fuelconvert))

def onFormRender(deltaT):
    """only update app when app form is visible then update only the following note call back method for this function defined in acMain above."""
    ac.setFontColor(mInfoDisplay.currentlaplabel, 1.0, 1.0, 1.0, 1)
    ac.setFontColor(mInfoDisplay.besttimelabel, 1.0, 1.0, 1.0, 1)
    ac.setFontColor(mInfoDisplay.lasttimelabel, 1.0, 1.0, 1.0, 1)
    ac.setFontColor(mInfoDisplay.currenttimelabel, 1.0, 1.0, 1.0, 1)
    ac.setFontColor(mInfoDisplay.checkboxLabelFuelConvert, 0.0, 1.0, 0.1, 1)
    ac.setFontColor(mInfoDisplay.currentfuellabel, 1.0, 1.0, 1.0, 1)
    #ac.setFontColor(mInfoDisplay.spinner, 1.0, 1.0, 1.0, 1)
    ac.setText(mInfoDisplay.currentlaplabel, "current lap : {0}".format(timesystem.getCurrentLap()))
    ac.setText(mInfoDisplay.besttimelabel, "best time : {0}".format(timesystem.getBestLapTime()))
    ac.setText(mInfoDisplay.lasttimelabel, "last time : {0}".format(timesystem.getLastLapTime()))
    ac.setText(mInfoDisplay.currenttimelabel, "current time : {0}".format(timesystem.getCurrentLapTime()))
    ac.setText(mInfoDisplay.currentfuellabel, "Fuel Remaining : {0} {1}".format(fuelsystem.getCurrentFuel(),mInfoDisplay.fuelconvert))

def acShutdown():
    """on shut down quit pygame so no crash or lockup."""
    configuration.saveConfig()
    pygame.quit()