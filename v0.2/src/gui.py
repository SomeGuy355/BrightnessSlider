import os
import sys
import json
import tkinter as tk
from tkinter import ttk
from subprocess import Popen
import argparse

"""
ACTUALLY!
maybe just make it so the okay button reopens main.exe
while the cancel button just closes and does nothing
instead of this ambiguous oh maybe it will reopen but it depends on if u had it open before hahahahahahhaha
but thats for later so idfk
"""
parser = argparse.ArgumentParser(description="Example program that takes a boolean flag")
    
# Add an optional boolean argument
parser.add_argument('--reopen-when-closed', type=bool, default=False, nargs='?', const=True,
    help="Optional boolean argument (true/false). Default is False. Will reopen main.exe when closed")

# Parse the command line arguments
args = parser.parse_args()
# print(args.relaunch_when_closed)

# this part is only used for opening CMDDC, oh and also opening the json file :))))
if getattr(sys, 'frozen', False):  # Running as an executable
    # print('Running as EXE')
    # BASE_PATH = os.path.dirname(sys.executable)
    os.chdir(os.path.dirname(sys.executable)) # and idfk
else:  # Running as a script
    # print('Running as script')
    # BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(os.path.realpath(__file__))) # because apparently fucking VS Code changes the CWD???? fuck me

# print(os.path.dirname(sys.executable))
# print(os.path.dirname(os.path.realpath(__file__)))

JSON_FILE_REL = os.path.join('..', 'assets','settings.json')
CMDDC_FILE_REL = os.path.join('..', 'click_monitor','ClickMonitorDDC_7_2.exe')
MAIN_FILE_REL = os.path.join('..', 'dist','main.exe')

def on_ok():
    apply_changes(JSON_FILE_REL)
    root.destroy()

def on_apply():
    apply_button.config(state=tk.DISABLED)
    apply_changes(JSON_FILE_REL)

def on_cancel():
    root.destroy()

def apply_changes(file_path):
    data = {
        "monitor1": monitor1_var.get(),
        "monitor2": monitor2_var.get(),
        "brightness1": brightness1_var.get(),
        "brightness2": brightness2_var.get(),
        "contrast1": contrast1_var.get(),
        "contrast2": contrast2_var.get(),
        "sleep_polling_freq": sleep_polling_freq_var.get(),
        "awake_polling_freq": awake_polling_freq_var.get(),
        "awake_timeout": awake_timeout_var.get()
    }
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_variables(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        monitor1_var.set(data.get("monitor1", False))
        monitor2_var.set(data.get("monitor2", False))
        brightness1_var.set(data.get("brightness1", False))
        brightness2_var.set(data.get("brightness2", False))
        contrast1_var.set(data.get("contrast1", False))
        contrast2_var.set(data.get("contrast2", False))
        sleep_polling_freq_var.set(data.get("sleep_polling_freq", "1"))
        awake_polling_freq_var.set(data.get("awake_polling_freq", "1"))
        awake_timeout_var.set(data.get("awake_timeout", "1"))
    except FileNotFoundError:
        print(f"No file found at {file_path}")

def open_cmddc():
    Popen([CMDDC_FILE_REL])

unapplied_changed = True

# Create main window
root = tk.Tk()
root.title("Monitor Settings")
root.resizable(width=False, height=False)

# Create frames for organization
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


# Variables for checkboxes
monitor1_var    = tk.BooleanVar(value=False)
monitor2_var    = tk.BooleanVar(value=False)
brightness1_var = tk.BooleanVar(value=False)
brightness2_var = tk.BooleanVar(value=False)
contrast1_var   = tk.BooleanVar(value=False)
contrast2_var   = tk.BooleanVar(value=False)

sleep_polling_freq_var = tk.StringVar(value="1")
awake_polling_freq_var = tk.StringVar(value="1")
awake_timeout_var      = tk.StringVar(value="1")


# Monitor settings
monitor1_check = ttk.Checkbutton(main_frame, text="Monitor 1", variable=monitor1_var)
monitor1_check.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

monitor2_check = ttk.Checkbutton(main_frame, text="Monitor 2", variable=monitor2_var)
monitor2_check.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

# Brightness settings
brightness1_check = ttk.Checkbutton(main_frame, text="Brightness", variable=brightness1_var)
brightness1_check.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

brightness2_check = ttk.Checkbutton(main_frame, text="Brightness", variable=brightness2_var)
brightness2_check.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# Contrast settings
contrast1_check = ttk.Checkbutton(main_frame, text="Contrast", variable=contrast1_var)
contrast1_check.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

contrast2_check = ttk.Checkbutton(main_frame, text="Contrast", variable=contrast2_var)
contrast2_check.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)


# Polling and Timeout inputs
def validate_number_input(action, value):
    """
    Callback function to validate that the input is a number.
    """
    if action == '1':  # '1' means text is being inserted
        if value.isdigit():
            variable_changed()
        return value.isdigit()  # Allow only digits
    return True  # Allow other actions like deletion

vcmd = (root.register(validate_number_input), '%d', '%S')

sleep_polling_label = ttk.Label(main_frame, text="Sleeping Polling Frequency (Hz):")
sleep_polling_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

sleep_polling_entry = ttk.Entry(main_frame, width=5, textvariable=sleep_polling_freq_var, validate="key", validatecommand=vcmd)
sleep_polling_entry.grid(row=0, column=3, padx=5, pady=5)

awake_polling_label = ttk.Label(main_frame, text="Awake Polling Frequency (Hz):")
awake_polling_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

awake_polling_entry = ttk.Entry(main_frame, width=5, textvariable=awake_polling_freq_var, validate="key", validatecommand=vcmd)
awake_polling_entry.grid(row=1, column=3, padx=5, pady=5)

timeout_label = ttk.Label(main_frame, text="Awake Timeout (Seconds):")
timeout_label.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)

timeout_entry = ttk.Entry(main_frame, width=5, textvariable=awake_timeout_var, validate="key", validatecommand=vcmd)
timeout_entry.grid(row=2, column=3, padx=5, pady=5)


# Action buttons
bottom_button_frame = ttk.Frame(root)
bottom_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Configure column weights
root.columnconfigure(0, weight=1)
bottom_button_frame.columnconfigure(0, weight=1)  # First column (empty space)
bottom_button_frame.columnconfigure(1, weight=0)  # Second column for right_button_frame

# Add a placeholder button to the left
cmddc_button = ttk.Button(bottom_button_frame, text="Open Click Monitor DDC", command=open_cmddc)
cmddc_button.grid(row=0, column=0, padx=15, pady=5, stick=tk.W)

# Right button frame
right_button_frame = ttk.Frame(bottom_button_frame, padding="10")
right_button_frame.grid(row=0, column=1, sticky=(tk.E))

# Buttons in the right frame
okay_button = ttk.Button(right_button_frame, text="Ok", command=on_ok)
okay_button.grid(row=0, column=0, padx=5, pady=5)

apply_button = ttk.Button(right_button_frame, text="Apply", command=on_apply)
apply_button.grid(row=0, column=1, padx=5, pady=5)

cancel_button = ttk.Button(right_button_frame, text="Exit", command=on_cancel)
cancel_button.grid(row=0, column=2, padx=5, pady=5)


def variable_changed(var=None, index=None, mode=None):
    unapplied_changed = False
    apply_button.config(state=tk.NORMAL)

# Trace functions
def monitor1_update(var=None, index=None, mode=None):
    variable_changed()
    if monitor1_var.get():
        brightness1_check.config(state=tk.NORMAL)
        contrast1_check.config(state=tk.NORMAL)
    else:
        brightness1_check.config(state=tk.DISABLED)
        contrast1_check.config(state=tk.DISABLED)

def monitor2_update(var=None, index=None, mode=None):
    variable_changed()
    if monitor2_var.get():
        brightness2_check.config(state=tk.NORMAL)
        contrast2_check.config(state=tk.NORMAL)
    else:
        brightness2_check.config(state=tk.DISABLED)
        contrast2_check.config(state=tk.DISABLED)

# Traces
monitor1_var.trace_add('write', monitor1_update)
monitor2_var.trace_add('write', monitor2_update)
brightness1_var.trace_add('write', variable_changed)
brightness2_var.trace_add('write', variable_changed)
contrast1_var.trace_add('write', variable_changed)
contrast2_var.trace_add('write', variable_changed)

# Misc setup
monitor1_update()
monitor2_update()
apply_button.config(state=tk.DISABLED)
load_variables(JSON_FILE_REL)

root.mainloop()

if args.reopen_when_closed:
    Popen([MAIN_FILE_REL])