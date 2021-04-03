from slicer_multithread import run_slicer_multithreading
from removeDuplicates import remove_duplicates

if __name__ == "__main__":
    path = "videos/2021-03-30 09-02-48.mkv"
    output_path = f"{path}_output"
    num_of_threads = 4

    run_slicer_multithreading(path, num_of_threads)
    remove_duplicates(output_path)
