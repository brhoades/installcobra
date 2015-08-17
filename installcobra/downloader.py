import inspect
import os

class Downloader:
    """Handles all the dirty work of downloading source files. Determines if it's necessary to do so too.

    :param BaseInstaller: Takes a BaseInstaller, which this downloader is part of.
    :param kwargs: Takes a kwargs dict from BaseInstaller and extracts useful keys.
    """
    def __init__(self, installer, kwargs):
        self._installer = installer
        # This is a bit complicated as we can't just get the dir of __file__, as that's this downloader.py file
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        self._dataDir = os.path.join(os.path.dirname(os.path.abspath(filename)), kwargs.get('data_dir', 'data'))

        if kwargs.get('copy_source_files', False):
            #FIXME: We should only copy down if this is on a network share (or configured to copy down)
            if os.name == "nt":
                self._sourceFilesDir = os.path.join("C:", "SourceFiles", )
            elif os.name == "posix":
                self._sourceFilesDir = os.path.join("tmp", "sourcefiles", "umrinst", "applogs")
            elif os.name == "mac":
                raise NotImplementedError("This platform is not implemented.")
            else:
                raise NotImplementedError("This platform is not implemented.")
        else:
            self._sourceFilesDir = self._dataDir
