from multiprocessing import Process
import subprocess

def run_process_1():
    subprocess.run(["python", "dual_volume_test_pygame_subprocess.py"])

def run_process_2():
    subprocess.run(["python", "dual_volume_test_pygame_subprocess.py"])

if __name__ == "__main__":
    p1 = Process(target=run_process_1)
    p2 = Process(target=run_process_2)

    # Start both processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()
