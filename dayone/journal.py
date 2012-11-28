
import sys, os, stat
import plistlib, datetime, glob

class Entry(object):
    def __init__(self, journal, filename=None):
        self._entry = {}
        self.journal = journal
        self.filename = filename
        if filename is not None:
            self.load()

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        self._entry = plistlib.readPlist(filename)

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        plistlib.writePlist(self._entry, filename)

    @property
    def uuid(self): return self._entry["UUID"]
    @uuid.setter
    def uuid(self, x):
        self._entry["UUID"] = str(x)

    @property
    def text(self): return self._entry["Entry Text"]
    @text.setter
    def text(self, x):
        self._entry["Entry Text"] = str(x)

    @property
    def date(self): return self._entry["Creation Date"]
    @date.setter
    def date(self, x):
        if not isinstance(x, datetime):
            raise ValueError, "date must be a datetime object"
        self._entry["Creation Date"] = x
    
    @property
    def starred(self): return self._entry["Starred"]
    @starred.setter
    def starred(self, x):
        self._entry["Starred"] = bool(x)

    # Tags
    @property
    def tags(self): return self._entry.get("Tags",[])
    @tags.setter
    def tags(self, x):
        self._entry["Tags"] = list(x)
    def addtag(self, tag):
        if tag not in self._entry["Tags"]:
            self._entry["Tags"].append(tag)
    def rmtag(self, tag):
        if tag in self._entry["Tags"]:
            self._entry["Tags"].remove(tag)
    def has_tag(self, tag):
        return tag in self._entry["Tags"]
        
    # Location not implemented yet
    @property
    def location(self): return self._entry.get("Location",{})
    
    # Weather not implemented yet
    @property
    def weather(self): return self._entry.get("Weather",{})

    # Return the picture if there is one, not implemented yet
    @property
    def picture(self):
        return None



# This class could have more intelligence about when to load entries, checking
# mtimes of cached entries to see if they've been changed externally, etc.
# But for now, none of that is really necessary.
        
class Journal(object):
    def __init__(self, path="~/Dropbox/Apps/Day One/Journal.dayone"):
        self.path = os.path.expanduser(path)
        self._cache = {}
        
    def filename_for_uuid(self, uuid):
        return os.path.join(self.path, "entries", "%s.doentry" % (str(uuid).upper(),))

    def get(self, uuid):
        fn = self.filename_for_uuid(uuid)
        if uuid not in self._cache:
            self._cache[uuid] = Entry(self, fn)

        return self._cache[uuid]

    def load(self):
        self._cache = {}
        for fn in glob.iglob(os.path.join(self.path, "entries", "*.doentry")):
            uuid = os.path.splitext(os.path.basename(fn))[0]
            self._cache[uuid] = Entry(self, fn)
        
    def iter_entries(self):
        if not self._cache:
            self.load()
            
        for entry in self._cache.itervalues():
            yield entry
            
    def entries(self):
        return list(self.iter_entries())

    def entries_by_date(self):
        e = self.entries()
        e.sort(lambda x,y: cmp(x.date, y.date))
        return e
        
