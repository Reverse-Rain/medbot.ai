import multiprocessing
import subprocess

# Define the functions to run each Python file 
def run_file1():
    subprocess.run(['python', 'receive.py'])

 
def run_file3():
    subprocess.run(['python', 'reminder.py'])

if __name__ == '__main__':
    # Create two processes, one for each file
    process1 = multiprocessing.Process(target=run_file1)
    process3 = multiprocessing.Process(target=run_file3)
    # Start both processes
    process1.start()
    process3.start()
    # Wait for both processes to finish
    process1.join()
    process3.join()

    
