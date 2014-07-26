# -*- coding: utf-8 -*-
from maryjane.tags import BaseTag
from maryjane.helpers import split_paths, has_file_overlap
from watchdog.events import FileSystemEventHandler
import traceback
__author__ = 'vahid'


class TaskTag(BaseTag):

    def execute_actions(self):
        if hasattr(self, 'banner'):
            print self.banner
        for action in self.actions:
            action.execute()

    def __repr__(self):
        return '<TaskTag>'

class TaskEventHandler(FileSystemEventHandler):
    def __init__(self, task):
        self.task = task
        super(FileSystemEventHandler, self).__init__()

    def on_any_event(self, event):
        # noinspection PyBroadException
        try:
            self.task.execute_if_needed(event)
        except:
            traceback.print_exc()

class ObservableTaskTag(TaskTag):

    def execute_if_needed(self, event):
        paths = []
        if hasattr(event, 'src_path'):
            paths += split_paths(event.src_path)
        if hasattr(event, 'dest_path'):
            paths += split_paths(event.dest_path)

        if has_file_overlap(paths, self.watch):
            self.execute_actions()

    def create_event_handler(self):
        return TaskEventHandler(self)

    def __repr__(self):
        return '<ObservableTaskTag>'