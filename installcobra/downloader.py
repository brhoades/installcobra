import inspect
import os
from progressbar import ProgressBar
import shutil

class Downloader:
    """Handles all the dirty work of downloading source files. Determines if it's necessary to do so too.

    :param BaseInstaller: Takes a BaseInstaller, which this downloader is part of.
    :param kwargs: Takes a kwargs dict from BaseInstaller and extracts useful keys.
    """
    def __init__(self, installer, kwargs):
        self._installer = installer
        # This is a bit complicated as we can't just get the dir of __file__, as that's this downloader.py file
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        print(os.path.dirname(self._installer._scriptFile))
        self._dataDir = os.path.join(os.path.dirname(self._installer._scriptFile), kwargs.get('data_dir', 'data'))

        if kwargs.get('copy_source_files', False):
            #FIXME: We should only copy down if this is on a network share (or configured to copy down)
            if os.name == "nt":
                self._sourceFilesDir = os.path.join("C:", "SourceFiles", )
            elif os.name == "posix":
                self._sourceFilesDir = os.path.join("/tmp", "sourcefiles", "umrinst", "applogs")
            elif os.name == "mac":
                raise NotImplementedError("This platform is not implemented.")
            else:
                raise NotImplementedError("This platform is not implemented.")

            self._sourceFilesDir = os.path.join(self._sourceFilesDir, self._installer._identifier)
        else:
            self._sourceFilesDir = self._dataDir

    def copySourceFiles(self):
        """Initiates the copy of source files from the data directory to the sourcefiles directory.

        :returns: False if there are no source files. True if the files were copied or don't need to be copied.
        """
        if self._sourceFilesDir == self._dataDir:
            print("Not copying source files")
            return True

        if not os.path.exists(self._dataDir):
            print("Data directory doesn't exist")
            self._installer.log.error("Data directory \"{0}\" doesn't exist".format(self._dataDir))
            return False

        filecount = 0
        # The number of files to copy
        for path, dirs, files in os.walk(self._dataDir):
            filecount += len(files)

        # Remove the source files directory if it already exists
        if os.path.exists(self._sourceFilesDir):
            self._installer.log.warning("Removing old sourcefiles directory: \"{0}\"".format(self._sourceFilesDir))
            shutil.rmtree(self._sourceFilesDir)

        #print("Copying source files")
        # Create a progress bar instance. We'll use this to count files as we transfer them.
        #FIXME: Weight by file size so the percent is accurate.
        with ProgressBar(maxval=filecount) as pb:
            try:
                os.makedirs(self._sourceFilesDir)
            except:
                self._installer.log.warning("Directory already exists \"{0}\"".format(self._sourceFilesDir))

            for path, dirs, filenames in os.walk(self._dataDir):
                for directory in dirs:
                    dest = path.replace(self._dataDir, self._sourceFilesDir)
                    directory = os.path.join(dest, directory)
                    try:
                        os.makedirs(directory)
                    except:
                        self._installer.log.warning("Directory already exists \"{0}\"".format(directory))
                
                for sfile in filenames:
                     srcFile = os.path.join(path, sfile)
                     destFile = os.path.join(path.replace(self._dataDir, self._sourceFilesDir), sfile)
                     if not shutil.copy(srcFile, destFile):
                         self._installer.log.error("Error copying the file:\n  From: \"{0}\"\n  To:\"{1}\"".format(srcFile, destFile))
                     pb += 1
