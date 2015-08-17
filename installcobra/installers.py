import os
import logging

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
    """
    def __init__(self, name, version, **kwargs):
        if name is None or len(name) < 3:
            raise ValueError("Passed name is None or less than three characters")
        
        if version is None or len(version) < 1: 
            raise ValueError("Passed version is None or zero-length.")
        
        self._loglevel = kwargs.get('loglevel', logging.DEBUG)
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

        self._logfile = os.path.join(self._logpath, name+'.'+version)

        # Open the file with logger
        self.log = logging.getLogger(self._logfile)
        self.log.setLevel(self._loglevel)

    def prerequisite(self):
        raise NotImplementedError("This method is not implemented.")

    def _copySourceFiles(self):
        """Source files are always in ./data/ from the script being ran.
        """
        print("COPY SOURCE FILES")

    def preinstall(self):
        pass

    def install(self):
        pass

    def postinstall(self):
        pass

    def run(self):
        self.prerequisite()
        self._copySourceFiles()
        self.preinstall()
        self.install()
        self.postinstall()

class ScriptInstaller(BaseInstaller):
    pass
