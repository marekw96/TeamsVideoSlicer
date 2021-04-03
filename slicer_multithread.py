from slicer import load_video, slice_video_multithreading
import threading
import math
from timeit import default_timer as timer
from datetime import timedelta


class SlicerThread(threading.Thread):
    def __init__(self, thread_id, path, start_at, end_when):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.path = path
        self.start_at = start_at
        self.end_when = end_when

    def run(self):
        print(f"[{self.thread_id}] start at {self.start_at} until {self.end_when}")
        time_start = timer()
        slice_video_multithreading(self.path,
                                   starts_at=self.start_at,
                                   end_when=self.end_when,
                                   slicer_id=self.thread_id)
        time_end = timer()
        print(f"[{self.thread_id}] ended with time {timedelta(seconds=time_end - time_start)}")


def assign_frames_to_threads(frames, num_thread):
    frames_per_thread = math.ceil(frames / num_thread)
    groups = []

    start_from = 0
    for thread_id in range(num_thread):
        end_at = min(start_from + frames_per_thread, frames)
        groups.append((start_from, end_at))
        start_from = end_at

    return groups


def run_slicer_multithreading(path, num_of_threads):
    threads = []
    total_frames = load_video(path)['frames']
    start_time = timer()

    print(f"Total frames: {total_frames}")
    assigned_frames = assign_frames_to_threads(total_frames, num_of_threads)

    for i in range(len(assigned_frames)):
        assign = assigned_frames[i]
        (local_start_at, local_end_when) = assign
        threads.append(SlicerThread(i, path, local_start_at, local_end_when))

    for slicerThread in threads:
        slicerThread.start()

    for slicerThread in threads:
        slicerThread.join()
    print("All threads ended")

    end_time = timer()
    print(f"Whole slicing operation ended with {timedelta(seconds=end_time - start_time)}")


if __name__ == "__main__":
    video_path = "videos/2021-03-16 09-06-22.mkv.mkv"
    config_num_thread = 4
    run_slicer_multithreading(video_path, config_num_thread)
