#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import threading
import hou

UPDATE_INTERVAL = 900.0

class Watcher(threading.Thread):
    def __init__(self, event):
        super(Watcher, self).__init__()
        self.stop_event = event

    def run(self):
		while not self.stop_event.is_set():
			hou.hipFile.saveAsBackup()
			time.sleep(UPDATE_INTERVAL)