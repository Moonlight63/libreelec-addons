#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2019 Zomboided
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    This module displays the current entered password

import xbmcaddon
import xbmcgui
from libs.utility import debugTrace, errorTrace, infoTrace, getID, getName

xbmc.log("-- Entered passwordpopup.py")
    
addon = xbmcaddon.Addon("docker.moonlight.htpc")
pw = addon.getSetting("vpn_password")
if not pw == "":
    xbmcgui.Dialog().ok("Transmission VPN", "Your password is '[B]" + pw + "[/B]'.")
else:
    xbmcgui.Dialog().ok("Transmission VPN", "No password has been entered.")
command = "Addon.OpenSettings(docker.moonlight.htpc)"
xbmc.executebuiltin(command)
    
xbmc.log("-- Exit passwordpopup.py --")
