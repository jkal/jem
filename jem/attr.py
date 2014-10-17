from xattr import getxattr
from biplist import readPlistFromString

def finder_tags(fname):
    """
    OS X Finder tags are stored in an extended attribute named
    com.apple.metadata:_kMDItemUserTags. Its value is a binary property list
    that contains a single array of strings.
    """
    pl = getxattr(fname, 'com.apple.metadata:_kMDItemUserTags')
    return readPlistFromString(pl)
