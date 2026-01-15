import platform
import os
from subprocess import Popen, PIPE
import pathlib
import requests
import bs4
import re

GITHUB_URL = 'https://github.com'
PRODIGAL_RELEASE_URL = 'https://github.com/hyattpd/Prodigal/releases/latest' # updated line 7/31/22
_LINUX = 'linux'
_WINDOWS = 'windows'
_OSX = 'osx'


class ProdigalRelease:
    """
    Class of operations to get the latest Prodigal Release
    """

    SUPPORTED_SYSTEMS = [_WINDOWS, _LINUX, _OSX]

    def __init__(self):
        self._releaseRequest = None
        self._releaseSoup = None
        self._version = ''
        self.releaseUrls = {system: None for system in self.SUPPORTED_SYSTEMS}
        self._getReleaseInfo()

    @property
    def version(self):
        return self._version

    def getBinary(self, system: str, location: str) -> str:
        """
        Download the latest Prodigal binary
        :param system: the target operating system
        :param location: directory of where to save the binary
        :return full path of file location
        """
        # check if path exists
        if not os.path.exists(location):
            raise IsADirectoryError('\"{} is not a valid directory\"'.format(location))

        system = system.lower()
        if system == 'darwin':
            system = _OSX

        # check if specified system is supported
        if system not in self.SUPPORTED_SYSTEMS:
            raise ValueError('Prodigal does not support this system: {}'.format(system))

        # download file
        with requests.get(self.releaseUrls[system]) as r:
            r.raise_for_status()
            fileName = f'prodigal-{self.version}-{system}'
            if system == _WINDOWS:
                fileName += '.exe'
            
            location = pathlib.Path(location)
            fullPath = location / fileName
            
            with open(fullPath, 'wb') as file:
                for chunk in r.iter_content(chunk_size=10 * 1024):
                    if chunk:
                        file.write(chunk)

        # make linux and mac versions executable
        if system == _LINUX or system == _OSX:
            proc = Popen(f'chmod +x "{fullPath}"', stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()

        return str(fullPath)

    def _getReleaseInfo(self):
        """
        FIXED: Hardcoded links to bypass broken GitHub scraping.
        """
        self._version = 'v2.6.3'
        base_url = 'https://github.com/hyattpd/Prodigal/releases/download/v2.6.3'
        self.releaseUrls[_WINDOWS] = f'{base_url}/prodigal.windows.exe'
        self.releaseUrls[_LINUX] = f'{base_url}/prodigal.linux'
        self.releaseUrls[_OSX] = f'{base_url}/prodigal.osx.10.9.5'

if __name__ == '__main__':
    release = ProdigalRelease()
    binary = release.getBinary(platform.system(), r'C:\Users\mdlaz\Desktop')
    print(binary)
