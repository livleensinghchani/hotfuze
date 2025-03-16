from hotfuze.utils import Color
import time
import sys
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Custom Event Handler

class CFileSystemEventHandler(FileSystemEventHandler):
  # Counter to tack changes made (TIME)
  last_update = 0

  def on_modified(self, event):
    event_path = event.src_path.replace("\\", "/")
    if not event_path == FILE_PATH:
      return
    
    current_time = time.time()
    if (current_time - self.last_update) < COMPILE_COOLDOWN:
      # If multiple changes made within short time (1 Sec)
      return
    
    self.last_update = current_time
    print(Color.GREY, "Changes Saved!", Color.RESET)
    compile_run_file()

# UTIL FUNCTIONS

def loop_header_text():
  subprocess.run("cls", shell=True)
  print("Tracking changes on:", Color.GREY, PATH_TO_FILE, Color.RESET)
  print("File: ", Color.GREEN, FILE_NAME[0]+"."+FILE_NAME[1], Color.RESET)
  print("------------->\n")

def footer_text():
  print("\n\n------------->")
  print(Color.GREY, "Waiting for changes /", Color.RESET)

# UTIL FUNCTIONS ~END

# Main application loop
def main_loop():
  # Makes sure all the required data is set
  startup()

  event_handler = CFileSystemEventHandler()

  global WATCHDOG_OBSERVER
  WATCHDOG_OBSERVER.schedule(event_handler, PATH_TO_FILE)
  
  loop_header_text()
  WATCHDOG_OBSERVER.start()
  footer_text()

  try:
    while (1):
      # Keep the app running!
      time.sleep(1)
  except KeyboardInterrupt:
    exit_app()

# Handels Path of File to track (Formats data)
def startup():
  global FILE_PATH, FILE_NAME, PATH_TO_FILE, TEMP_DIR

  TEMP_DIR = set_temp_dir_path()
  if not (check_temp_dir_exist()):
    create_temp_dir()
  FILE_PATH = check_file_exist(process_input())

  FILE_PATH = FILE_PATH.replace("\\", "/")
  path_split = FILE_PATH.split("/")
  if(len(path_split) < 2):
    path_split = ["./"]+path_split
    FILE_PATH = path_split[0]+path_split[-1]
  FILE_NAME = path_split[-1].split(".")

  if not check_valid_extension():
    print(Color.ERROR, "Invalid File extension!", end="\t")
    print(FILE_NAME[0]+"."+Color.INVLAID, FILE_NAME[-1])
    exit_app()

  PATH_TO_FILE = "/".join(path_split[:-1])
    

# Formats path for TEMP location of compiled .exe files
def set_temp_dir_path() -> str:
  current_path_file = sys.argv[0].replace("\\", "/").split("/")
  current_path = "/".join(current_path_file[:-1])
  current_path += "/"+(TEMP_DIR_NAME)
  return current_path

# Returns True if dir exist else False
def check_temp_dir_exist() -> bool:
  if not os.path.isdir(TEMP_DIR):
    return False
  else:
    return True

# Creates Temp dir for the compiled .exe
def create_temp_dir():
  os.mkdir(TEMP_DIR)

# Processes User Inputed File Path
def process_input() -> str:
  if not len(sys.argv) > 1:
    print(color("File to watch not specified!", "RED"), end="\n\n")
    get_file_path_interactive()
  return sys.argv[1]

# Get user input (FILE PATH) from user in CLI
def get_file_path_interactive():
  try:
    path = input("Enter .C File Path: ")
  except KeyboardInterrupt:
    exit_app()
  sys.argv.append(path)

# Checking if the file exists in path specified!
def check_file_exist(path_to_file: str):
  if not (os.path.isfile(path_to_file)):
    print(color("File does not exist!", "RED"), end="\t")
    print(color(path_to_file, "GREY"))
    exit_app()
  return path_to_file

# Check if the file is valid .c file
def check_valid_extension() -> bool:
  if not (FILE_NAME[-1] == "c"):
    return False
  else:
    return True

# Compiles and run the .c File
def compile_run_file():
  subprocess.run(["cls"], shell=True)
  out_path = TEMP_DIR + "/" + FILE_NAME[0]
  
  try:
    # Making sure file is being compiled
    subprocess.run(["gcc", FILE_PATH, "-o", out_path], check=True)
  except subprocess.CalledProcessError:
    print(color("Error in Compile", "RED"))
    footer_text()
    return
  
  # Running the .c => .exe file
  run_command = out_path
  try:
    loop_header_text()
    subprocess.run(run_command)
    footer_text()
  except:
    print(color("Runtime Error!", "RED"))
  
# Removes Temp_Dir
def remove_temp_dir():
  shutil.rmtree(TEMP_DIR)

# Clean Exit
def exit_app():
  print(color("\n----------------", "GREY"))
  print(color("Ending Watch!", "RED"))
  WATCHDOG_OBSERVER.stop()
  remove_temp_dir()
  sys.exit()


# Global Variables 
# ALERT Be careful any dir of this name will be deleted on app exit!
TEMP_DIR_NAME = "hot_reload_tool-temp_storage"
TEMP_DIR = ""

FILE_PATH = ""
FILE_NAME = ""
PATH_TO_FILE = ""

COMPILE_COOLDOWN = 2

WATCHDOG_OBSERVER = Observer()



# Global Variables ~END

# Starting Point
print("~ Hot Reload C ~",  color("\t#CHANI", "PURPLE"))
main_loop()
