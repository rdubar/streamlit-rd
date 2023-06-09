from dataclasses import dataclass
import re
from datetime import datetime
from tools.utils import show_file_size


def object_clean(obj, remove):
    """ Hack to clean object information for easy plain text search """
    text = str(obj)
    text = re.sub('[^A-Za-z0-9 ]+', ' ', text).replace(remove, '').replace(", ", "")
    return text


@dataclass(order=True)
class MediaRecord:
    """ Record to store desired information from a Plex object or other media as text in an object """
    title: str = None
    year: int = None
    source: str = None
    extras: bool = False
    quality: str = None
    added: datetime = None
    size: int = None
    plex: str = None
    entry: str = None
    file: str = None
    art: str = None
    thumb: str = None
    summary: str = None
    tagline: str = None
    duration: int = None
    directors: str = None
    roles: str = None
    writers: str = None
    codec: str = None
    bitrate: int = None
    width: int = None
    height: int = None
    uncompressed: bool = False
    search: str = None

    def __post_init__(self):
        self.set_entry()
        self.set_search()

    def __str__(self):
        return self.display()

    def set_entry(self):
        self.entry = self.title.lower()
        if self.year:
            self.entry += f' ({self.year})'
        return self.entry

    def set_plex_info(self, plex):
        p = plex
        if not p:
            return
        self.plex = str(p.ratingKey)
        self.title = p.title
        empty = ''
        self.year = p.year if hasattr(p, 'year') else empty
        self.set_entry()
        self.source = 'Plex'
        self.art = p.art if hasattr(p, 'art') else empty
        self.thumb = p.thumb if hasattr(p, 'thumb') else empty
        self.summary = p.summary if hasattr(p, 'summary') else empty
        self.tagline = p.tagline if hasattr(p, 'tagline') else empty
        self.duration = p.duration if hasattr(p, 'duration') else empty
        self.added = p.addedAt if hasattr(p, 'addedAt') else empty
        self.directors = object_clean(p.directors, 'Director') if hasattr(p, 'directors') else empty
        self.roles = object_clean(p.roles, 'Role') if hasattr(p, 'roles') else empty
        self.writers = object_clean(p.writers, 'Writer') if hasattr(p, 'writers') else empty
        m = p.media[0] if hasattr(p, 'media') else None
        self.codec = m.videoCodec if hasattr(m, 'videoCodec') else empty
        self.bitrate = m.bitrate if hasattr(m, 'bitrate') else empty
        self.height = m.height if hasattr(m, 'height') else empty
        self.quality = str(self.height) if hasattr(m, 'height') else empty
        self.width = m.width if hasattr(m, 'width') else empty
        f = m.parts[0] if hasattr(m, 'parts') else empty
        self.size = f.size if hasattr(f, 'size') else empty
        self.file = f.file if hasattr(f, 'file') else empty
        self.uncompressed = True if self.codec == 'mpeg2video' else False
        self.set_search()

    def set_search(self):
        content = vars(self)
        # make sure we don't duplicate the previous search information
        if 'search' in content:
            del content['search']
        s = str(content).lower()
        while "' " in s or '  ' in s:
            s = s.replace("'", '').replace('  ', ' ')
        self.search = s
        return self.search

    def display(self):
        source = self.source[:5].lower() if hasattr(self, 'source') and self.source is not None else ''
        s = show_file_size(self.size) if hasattr(self, 'source') and self.size is not None else ''
        h = self.height if hasattr(self, 'height') and self.height is not None else ''
        if hasattr(self, 'codec') and self.codec == 'mpeg2video':
            h = f'*{h}'
        b = self.bitrate if hasattr(self, 'bitrate') and self.bitrate is not None else ''
        return f'{source:>5}{s:>10} {h:>6} {b:>6}   {self.entry}'

    def get(self, attrib, default=None, force=False):
        """ Get a value from the object, if it doesn't exist, return the default """
        if not force:
            if attrib == 'added':
                default = datetime.min
            if attrib == 'year':
                default = 0
        v = getattr(self, attrib) if hasattr(self, attrib) and getattr(self, attrib) is not None else default
        return v
