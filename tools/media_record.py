from dataclasses import dataclass
import re, datetime
from tools.utils import show_file_size

def object_clean(object, remove):
    """ Hack to clean object information for easy plain text search """
    text = str(object)
    text = re.sub('[^A-Za-z0-9 ]+', ' ', text).replace(remove,'')
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

    def __post_init__(self):
        pass

    def __str__(self):
        return self.entry()

    def set_plex_info(self, plex):
        p = plex
        if not p: return
        self.plex = str(p.ratingKey)
        self.title = p.title
        empty = ''
        self.year = p.year if hasattr(p, 'year') else empty
        self.source = 'Plex'
        self.art = p.art if hasattr(p,'art') else empty
        self.thumb = p.thumb if hasattr(p,'thumb') else empty
        self.summary = p.summary if hasattr(p,'summary') else empty
        self.tagline = p.tagline if hasattr(p,'tagline') else empty
        self.duration = p.duration if hasattr(p,'duration') else empty
        self.added = p.addedAt if hasattr(p,'addedAt') else empty
        self.directors = object_clean(p.directors,'Director') if hasattr(p, 'directors') else empty
        self.roles = object_clean(p.roles,'Role') if hasattr(p, 'roles') else empty
        self.writers = object_clean(p.writers,'Writer') if hasattr(p, 'writers') else empty
        m = p.media[0] if hasattr(p,'media') else None
        self.codec = m.videoCodec if hasattr(m,'videoCodec') else empty
        self.bitrate = m.bitrate if hasattr(m,'bitrate') else empty
        self.height = m.height if hasattr(m,'height') else empty
        self.quality = self.height
        self.width = m.width if hasattr(m,'width') else empty
        f = m.parts[0] if hasattr(m,'parts') else empty
        self.size = f.size if hasattr(f, 'size') else empty
        self.file = f.file if hasattr(f, 'file') else empty
        self.uncompressed = True if self.codec=='mpeg2video' else False
        self.set_search()

    def set_search(self):
        self.search = str(vars(self)).lower()
        return self.search

    def entry(self):
        entry = self.title.lower()
        #if hasattr(self, 'year') and self.year and self.year != '': entry += f' ({self.year})'
        return str(entry)

    def display(self):
        source = self.source[:5].lower() if hasattr(self,'source') else ''
        s = show_file_size(self.size) if hasattr(self,'source') else ''
        h = self.height if hasattr(self,'height') else ''
        b = self.bitrate if hasattr(self,'bitrate') else ''
        return f'{source:>5}  {s:>10} {h:>6} {b:>6}  {self.entry()}'