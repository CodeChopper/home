#!/usr/bin/env python

import os
import sys, optparse
import random
import time
import datetime
import subprocess

from optparse import OptionParser

def run_process(cmd_args_list):
    process = subprocess.Popen(cmd_args_list, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.stdout.readlines()

    return output

def parse_temperature(l):

    english = None

    if l.startswith('Temperature:'):
        fields = l.split(' ')
        temperature = fields[1]
        english = "\nTemperature is %s degrees." % temperature
        
    return english

def parse_humidity(l):

    english = ""
    
    if l.startswith('Relative Humidity:'):
        fields = l.split(' ')
        humidity = fields[2]
        english += "\nRelative humidity is %s." % humidity

    return english

def parse_sky_conditions(l):

    english = ""

    if l.startswith('Sky conditions:'):
        fields = l.split(' ')
        conditions = fields[2]
        english += "\nSky conditions are %s." % conditions

    return english

def parse_direction(abbrev):

    english = ""

    if abbrev == "N":
        english = "North"
    elif abbrev == "E":
        english = "East"
    elif abbrev == "W":
        english = "West"
    elif abbrev == "S":
        english = "South"
    elif abbrev == "NE":
        english = "North east"
    elif abbrev == "NW":
        english = "North west"
    elif abbrev == "SE":
        english = "South east"
    elif abbrev == "SW":
        english = "South west"
    else:
        english = abbrev

    return english

def parse_wind(l):

    english = ""
    
    if l.startswith('Wind:'):
        fields = l.split(' ')
        the_index = -1
        mph_index = -1
        
        for i in range(len(fields)):
            if fields[i] == 'the':
                the_index = i
            if fields[i].upper() == 'MPH':
                mph_index = i

        if mph_index != -1:
            wind_speed     = fields[mph_index - 1]
        else:
            wind_speed = "unknown"

        if the_index != -1:
            wind_direction = fields[the_index + 1]
        else:
            wind_direction = ""

        english += "\nWind is %s miles per hour." % wind_speed
                                                   
    return english

def parse_weather(weather_lines):

    temperature = None
    humidity    = None
    wind        = None
    
    english = ""

    for l in weather_lines:
        temperature = parse_temperature(l)
        if temperature is not None:
            english += temperature
            
        humidity = parse_humidity(l)
        if humidity is not None:
            english += humidity

        wind = parse_wind(l)
        if wind is not None:
            english += wind

        sky = parse_sky_conditions(l)
        if sky is not None:
            english += sky

    return english
    

def main():

    dialogue = "Hi Rick."

    cmd_list = ['/bin/date', '+it is %M minutes after %I']
    time_out = run_process(cmd_list)

    cmd_list = ['/usr/bin/weather', '-q', '-i', 'ksaf']
    weather_out = run_process(cmd_list)
        
    for line in time_out:
        dialogue += line

    weather_report = parse_weather(weather_out)
    dialogue += weather_report

    print dialogue

    f = open('/home/rick/tmp/festival-time.tmp', 'w')
    print >>f, dialogue
    f.close()

    cmd = "/usr/bin/text2wave /home/rick/tmp/festival-time.tmp -o /home/rick/tmp/festival-time.wav"
    os.system(cmd)
    time.sleep(1)
    cmd = "play /home/rick/tmp/festival-time.wav"
    os.system(cmd)

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print "Exception in main: %s" % e

