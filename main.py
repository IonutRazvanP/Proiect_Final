import subprocess
import threading

# Run the files in separate threads
def run_file(filename):
    subprocess.run(['python', filename])

threading.Thread(target=run_file, args=('app.py',)).start()
threading.Thread(target=run_file, args=('prelucrare_fisiere.py',)).start()
threading.Thread(target=run_file, args=('prelucrare_ore.py',)).start()
