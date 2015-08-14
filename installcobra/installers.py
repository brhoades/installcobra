from utils import spit

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
        
        if version is None or len(version) < 3: 
            raise ValueError("Passed version is None or less than three characters")
        
        self._setupLogging(name, version)

    def _setupLogging(self, name, version):
        

    def prerequisite(self):
        raise NotImplementedError("This method is not implemented.")

    def _copySourceFiles(self):
        """Source files are always in ./data/ from the script being ran.
        """
        raise NotImplementedError("This method is not implemented.")

    def preinstall(self):
        raise NotImplementedError("This method is not implemented.")

    def install(self):
        raise NotImplementedError("This method is not implemented.")

    def postinstall(self):
        raise NotImplementedError("This method is not implemented.")

    def run(self):
        self.prerequisite()
        self._copySourceFiles()
        self.preinstall()
        self.install()
        self.postinstall()
