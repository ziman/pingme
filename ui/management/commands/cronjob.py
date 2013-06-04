import os
import Image as pil
from ui.models import Image

from django.utils import timezone
from django.core.management.base import BaseCommand

import simport
import sync
from sharedutils.http import HttpClient, HttpException
from sharedutils.misc import mkdirp

THUMB_SIZE = 200

def createThumb(src, dst, size):
    img = pil.open(src)
    img.thumbnail((size, size), pil.ANTIALIAS)
    img.save(dst)

class Command(BaseCommand):
    args = '--none--'
    
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.http = HttpClient(retries=1, timeout=5.0)
        self.log = sync.Logger('***', logDirectly=True)
        
    def downloadImage(self, dbi):
        mkdirp(os.path.join(simport.settings.MEDIA_ROOT, 'images', dbi.user.slug))
        mkdirp(os.path.join(simport.settings.MEDIA_ROOT, 'thumbs', dbi.user.slug))
        
        fullPath = os.path.join(simport.settings.MEDIA_ROOT, 'images', dbi.user.slug, dbi.localname)
        thumbPath = os.path.join(simport.settings.MEDIA_ROOT, 'thumbs', dbi.user.slug, dbi.localname)
        if os.path.exists(fullPath):
            self.log.debug(u'already exists: ' + fullPath)
            if not dbi.downloaded:
                dbi.downloaded = timezone.now()
            return False
        
        self.log.debug(u"downloading " + dbi.url)

        try:
            data = self.http.getBinary(dbi.url.replace('https', 'http'))
            if len(data) < 1024:
                self.log.debug(u'skipping %s because size = %d' % (dbi.url, len(data)))
                return
            
            with open(fullPath, "wb") as f:         
                f.write(data)
                
            createThumb(fullPath, thumbPath, THUMB_SIZE)
            dbi.downloaded = timezone.now()
            return True
        except HttpException as e:
            if e.code and e.code in [403, 404]:
                dbi.dead = True
                self.log.debug('%s is dead (HTTP %d)' % (dbi, e.code))
            else:
                self.log.debug('%s: %s' % (dbi, e))                
                
        return False

    def handle(self, *args, **_kwargs):
        for dbi in Image.objects.filter(dead=False, downloaded__isnull=True, rejected=False):
            self.downloadImage(dbi)
            dbi.save()
