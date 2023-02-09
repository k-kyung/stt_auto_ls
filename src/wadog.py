import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


class Target:
    watchDir = os.getcwd()
    # watchDir에 감시하려는 디렉토리를 명시한다.

    def __init__(self):
        self.observer = Observer()  # observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir,
                               recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()


class Handler(FileSystemEventHandler):
    # FileSystemEventHandler 클래스를 상속받음.
    # 아래 핸들러들을 오버라이드 함

    # 파일, 디렉터리가 move 되거나 rename 되면 실행
    def on_moved(self, event):
        print(event)

    def on_created(self, event):  # 파일, 디렉터리가 생성되면 실행
        print(event)
        if event.is_directory:
            print("디렉토리 생성")
        else:  # not event.is_directory
            """
            Fname : 파일 이름
            Extension : 파일 확장자 
            """
            Fname, Extension = os.path.splitext(
                os.path.basename(event.src_path))
            '''
                1. zip 파일
                2. exe 파일
                3. lnk 파일
            '''
            if Extension == '.wma':
                print(".wma 파일 입니다.")
                print(event.src_path)
            elif Extension == '.txt':
                print(".txt 파일 입니다.")
                print(event.src_path)
                # os.remove(Fname + Extension)   # _파일 삭제 event 발생

    def on_deleted(self, event):  # 파일, 디렉터리가 삭제되면 실행
        print(event)

    def on_modified(self, event):  # 파일, 디렉터리가 수정되면 실행
        print(event)


if __name__ == '__main__':  # 본 파일에서 실행될 때만 실행되도록 함
    w = Target()
    w.run()