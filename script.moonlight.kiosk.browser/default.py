# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2009-2012 Stephan Raue (stephan@openelec.tv)
# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)

import os
import sys
import time
import xbmcaddon
import subprocess
import json

import xbmc

__addon__ = xbmcaddon.Addon();
__path__  = os.path.join(__addon__.getAddonInfo('path'), 'bin') + '/'

pauseXBMC = __addon__.getSetting("PAUSE_XBMC")

def pauseXbmc():
  if pauseXBMC == "true":
    xbmc.executebuiltin("PlayerControl(Stop)")
    xbmc.audioSuspend()
    xbmc.enableNavSounds(False)

def resumeXbmc():
  if pauseXBMC == "true":
    xbmc.audioResume()
    xbmc.enableNavSounds(True)

def startchrome(args):
  try:
    new_env = os.environ.copy()
    new_env['VAAPI_MODE'] = __addon__.getSetting('VAAPI_MODE')
    new_env['WINDOW_MODE'] = __addon__.getSetting('WINDOW_MODE')
    new_env['RASTER_MODE'] = __addon__.getSetting('RASTER_MODE')
    new_env['DARK_MODE'] = __addon__.getSetting('DARK_MODE')

    new_env['ALSA_DEVICE'] = ''
    if __addon__.getSetting('USE_CUST_AUDIODEVICE') == 'true':
      alsa_device = __addon__.getSetting('CUST_AUDIODEVICE_STR')
    else:
      alsa_device = getAudioDevice()
    if not alsa_device == None and not alsa_device == '':
      new_env['ALSA_DEVICE'] = alsa_device

    if args == "":
      command = 'kiosk-start ' + __addon__.getSetting('HOMEPAGE')
    else:
      command = 'kiosk-start ' + args

    subprocess.call(__path__ + command, shell=True, env=new_env)

  except Exception as e:
    xbmc.log('## Chrome Error: ' + repr(e), xbmc.LOGERROR)

def isRuning(pname):
  tmp = os.popen("ps -Af").read()
  pcount = tmp.count(pname)
  if pcount > 0:
    return True
  return False

def getAudioDevice():
  dev = json.loads(xbmc.executeJSONRPC(json.dumps({
                      "jsonrpc": "2.0",
                      "method": "Settings.GetSettingValue",
                      "params": {
                                  "setting": "audiooutput.audiodevice",
                                },
                      "id": 1,
                  })))['result']['value']
  if dev.startswith("ALSA:"):
    dev = dev.split("ALSA:")[1]
    if dev == "@":
      return None
    if dev.startswith("@:"):
      dev = dev.split("@:")[1]
  else:
    # not ALSA
    return None
  if dev.startswith("CARD="):
    dev = "plughw:" + dev
  return dev

if (not __addon__.getSetting("firstrun")):
  __addon__.setSetting("firstrun", "1")
  __addon__.openSettings()

try:
  args = ' '.join(sys.argv[1:])
except:
  args = ""


if not isRuning('chrome'):
  pauseXbmc()
  startchrome(args)
  while isRuning('chrome'):
    time.sleep(1)
  resumeXbmc()
else:
  subprocess.call(['pkill', '-f', 'chrome'])

del __addon__
