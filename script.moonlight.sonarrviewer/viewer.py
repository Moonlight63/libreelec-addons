# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2009-2012 Stephan Raue (stephan@openelec.tv)
# Copyright (C) 2018-present Team LibreELEC (https://libreelec.tv)

import xbmcaddon
import xbmc

__addon__ = xbmcaddon.Addon();

xbmc.log('Launching Viewer: ' + __addon__.getSetting('HOMEPAGE'))
xbmc.executebuiltin('RunAddon("script.moonlight.kiosk.browser", ' + __addon__.getSetting('HOMEPAGE') + ')')

del __addon__
