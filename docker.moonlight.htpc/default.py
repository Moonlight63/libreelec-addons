
import subprocess
import xbmc
import xbmcaddon


class Monitor(xbmc.Monitor):

   def __init__(self, *args, **kwargs):
      xbmc.Monitor.__init__(self)
      self.id = xbmcaddon.Addon().getAddonInfo('id')

   def onSettingsChanged(self):
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.bazarr.service'])
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.overseerr.service'])
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.plex.service'])
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.prowlarr.service'])
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.radarr.service'])
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.sonarr.service'])
      subprocess.call(['systemctl', 'restart', 'docker.linuxserver.transmission.service'])


if __name__ == '__main__':
   Monitor().waitForAbort()
