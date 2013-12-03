class Config :

    def __init__(self):
        self.put_throttle=0

    @property
    def put_throttle(self):
        return self.put_throttle

    def makepath(self,path):
        """Return a normalized absolute version of the path argument.

        - if the given path already exists in the filesystem
          the filesystem is not modified.

        - otherwise makepath creates directories along the given path
          using the dirname() of the path. You may append
          a '/' to the path if you want it to be a directory path.

        from holger@trillke.net 2002/03/18

        """
        import os
        dpath = os.path.normpath(os.path.dirname(path))
        if not os.path.exists(dpath):
            os.makedirs(dpath)
        return os.path.normpath(os.path.abspath(path))


    def datafilepath(self, *filename):
        """Return an absolute path to a data file in a standard location.

        Argument(s) are zero or more directory names, optionally followed by a
        data file name. The return path is offset to config.base_dir. Any
        directories in the path that do not already exist are created.

        """
        import os.path
        return makepath(os.path.join(base_dir, *filename))


    def shortpath(self, path):
        """Return a file path relative to config.base_dir."""
        import os.path
        if path.startswith(base_dir):
            return path[len(base_dir) + len(os.path.sep):]
        return path


def loadconfig ():
    return Config()

