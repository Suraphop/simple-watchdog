import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def do_something():
    print('do some thing')

class EventHandler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(self, patterns=['*.csv'],
                                             ignore_patterns=[],
                                             ignore_directories=True)
        
    file_cache = {}
    
    # def on_created(self, event):
    #     file = None
    #     while file is None:
    #         try:
    #             file = open(event.src_path)
    #             print("File created:", event.src_path)
    #         except OSError:
    #             print('Waiting for file transfer....')
    #             time.sleep(1)
    #             continue
    
    def on_modified(self, event):
            seconds = int(time.time())
            key = (seconds, event.src_path)
            if key in self.file_cache:
                return
            self.file_cache[key] = True
            
            if event.is_directory:
                print("Directory modified:", event.src_path)
            else:
                print("File modified:", event.src_path)
                do_something()
                       
path = r'C:\\Users\\nmb_m\\OneDrive\\Desktop\\watchdog\\data'
event_handler = EventHandler()

observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()