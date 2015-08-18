import os
import logging
from installcobra.downloader import Downloader
from installcobra.phase import Phase
from itertools import starmap

class Installer:
    """Installer interface. All other Installers should inherit from this.
    """
    def prerequisite(self):
        raise NotImplementedError("This method is not implemented.")

    def preinstall(self):
        raise NotImplementedError("This method is not implemented.")

    def install(self):
        raise NotImplementedError("This method is not implemented.")

    def postinstall(self):
        raise NotImplementedError("This method is not implemented.")


class BaseInstaller(Installer):
    """Basic installer boilerplate. No implementation should ever use this, this is used by other installers.
        
        :param file: The full path and name of the script running. Just path __file__.
        :param name: The name of this script, used when printing. Forms the first part of the identifier.
        :param version: The version of this script, used for the logfiles and source directory. Forms the second portion of the identifier.
        
        :Kwargs:
            * **identifier** (*name.version*): The identifier used for sourcefiles and the log file name.
            * **log_level** (*logging.DEBUG*): The level at which to write to the log.
            * **copy_source_files** (*False*): If source files are copied to a local folder and then ran. If not, the script uses the sourcefiles
                directly from data.
            * **data_dir** (*data*): The name of the source files directory.
    """
    def __init__(self, scriptfile, name, version, **kwargs):
        if name is None or len(name) < 3:
            raise ValueError("Passed name is None or less than three characters")
        
        if version is None or len(version) < 1: 
            raise ValueError("Passed version is None or zero-length.")

        self._scriptFile = os.path.abspath(scriptfile)
        self._name = name
        self._version = version
        self._identifier = kwargs.get('identifier', name+'.'+version)
        self._loglevel = kwargs.get('log_level', logging.DEBUG)

        # Initialize our internal downloader instance
        # This is something like private inheritance
        self.__downloader = Downloader(self, kwargs)

        self._setupLogging(name, version)

    def _setupLogging(self, name, version):
        """Sets up the logging txt file, whereever the OS stores it.
        """
        if os.name == "nt":
            self._logpath = os.path.join("C:", "Windows", "System32", "UMRInst", "AppLogs")
        elif os.name == "posix":
            self._logpath = os.path.join("var", "log", "umrinst", "applogs")
        elif os.name == "mac":
            raise NotImplementedError("This platform is not implemented.")
        else:
            raise NotImplementedError("This platform is not implemented.")

        if os.path.exists(self._logpath):
            os.mkdirs(self._logpath)

        self._logfile = os.path.join(self._logpath, self._identifier)

        # Open the file with logger
        self.log = logging.getLogger(self._logfile)
        self.log.setLevel(self._loglevel)
    
    def prerequisite(self):
        return None

    def copySourceFiles(self):
        return self.__downloader.copySourceFiles();

    def preinstall(self):
        return None

    def install(self):
        return None

    def postinstall(self):
        return None

    def run(self):
        phases = starmap(Phase,
                      [[self.prerequisite, "Prerequisite"],
                      [self.copySourceFiles, "Copy Source Files"],
                      [self.preinstall, "Preinstall"],
                      [self.install, "Install"],
                      [self.postinstall, "Postinstall"]])

        for p in phases:
            if p.hides(self, BaseInstaller):
                self.log.info('\n')
                self.log.info('='*40)
                self.log.info("Beginning {0} Phase".format(p.name()))
                self.log.info('='*40)
                self.log.info('\n')
                p.method()()
            else:
                self.log.debug("Skipping {0} Phase".format(p.name()))

        

class ScriptInstaller(BaseInstaller):
    pass
