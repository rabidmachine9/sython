import mido
import tkinter as tk
from tkinter import messagebox, scrolledtext
from sython_extended import SythonExtended
import sys

class MidiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Device Selector and Sython Editor")

        # Interpreter
        self.interpreter = SythonExtended()

        # Variables
        self.midi_out = None
        self.message_log_text = tk.StringVar()

        # Create the MIDI device dropdown
        self.selected_device = tk.StringVar(self.root)
        self.selected_device.set("Select MIDI Device")

        self.midi_devices = mido.get_output_names() or ["No devices found"]
        self.device_dropdown = tk.OptionMenu(self.root, self.selected_device, *self.midi_devices)
        self.device_dropdown.pack(pady=5)

        # Button to connect to MIDI device
        self.connect_button = tk.Button(self.root, text="Connect to MIDI", command=self.connect_midi)
        self.connect_button.pack(pady=5)

        # Simple text editor with line numbers
        self.create_editor_with_line_numbers()

        # Play button
        self.play_button = tk.Button(self.root, text="Play", command=self.play_code)
        self.play_button.pack(pady=10)

        # Message log at the bottom
        self.message_log = scrolledtext.ScrolledText(self.root, height=5)
        self.message_log.pack(pady=5)
        self.log_message("Welcome to the Sython Editor. Connect to a MIDI device to start.")

    def create_editor_with_line_numbers(self):
        """Creates a text editor with line numbers on the left."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Text editor (code area)
        self.editor = tk.Text(frame, wrap=tk.NONE, width=60, height=20)
        self.editor.pack(side=tk.RIGHT)

        # Line numbers on the left
        self.line_numbers = tk.Text(frame, width=4, padx=5, takefocus=0, border=0,
                                    background='lightgrey', state='disabled', wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.update_line_numbers()
        self.editor.bind("<KeyRelease>", self.update_line_numbers)

    def update_line_numbers(self, event=None):
        """Updates the line numbers when text is entered."""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)

        current_lines = int(self.editor.index('end').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, current_lines))
        self.line_numbers.insert(tk.END, line_numbers_string)

        self.line_numbers.config(state=tk.DISABLED)

    def connect_midi(self):
        """Handle MIDI device connection."""
        selected_device = self.selected_device.get()

        if selected_device == "Select MIDI Device" or selected_device == "No devices found":
            messagebox.showerror("Error", "Please select a valid MIDI device.")
            return

        try:
            self.interpreter.set_midi_output(selected_device)
        except Exception as e:
            self.log_message(f"Failed to connect to MIDI device: {e}")

    def play_code(self):
        """Evaluates the code in the editor and sends MIDI messages."""
        code = self.editor.get('1.0', tk.END).strip()

        if code:
            result = self.interpreter.run(code)
            self.log_message(result)
        else:
            self.log_message("No code to evaluate.")

    def log_message(self, message):
        """Logs messages to the message log."""
        self.message_log.insert(tk.END, message + "\n")
        self.message_log.yview(tk.END)

# Create and run the app
root = tk.Tk()
app = MidiApp(root)
root.mainloop()
