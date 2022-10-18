#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import threading
import hou
try:
    GAL_FILE = hou.findFile('gallery/CPGallery.gal')
except hou.OperationFailed:
    pass
UPDATE_INTERVAL = 10.0

class Watcher(threading.Thread):
    def __init__(self, event):
        super(Watcher, self).__init__()
        if os.path.exists(GAL_FILE):
            hou.session.gal_file_size = os.stat(GAL_FILE).st_size
        else:
            hou.session.gal_file_size = 0
        self.stop_event = event

    def run(self):
        while not self.stop_event.is_set():
            if not os.path.exists(GAL_FILE):
                continue
            cur_size = os.stat(GAL_FILE).st_size
            if cur_size > hou.session.gal_file_size:
                hou.galleries.removeGallery(GAL_FILE)
                hou.galleries.installGallery(GAL_FILE)
                # hou.ui.setStatusMessage('Gallery已更新')
            time.sleep(UPDATE_INTERVAL)