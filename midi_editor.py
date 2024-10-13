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

        frame = tk.Frame(root)
        frame.pack(pady=20)

        # Create the MIDI device dropdown
        self.selected_device = tk.StringVar(self.root)
        self.selected_device.set("Select MIDI Device")

        self.midi_devices = mido.get_output_names() or ["No devices found"]
        self.device_dropdown = tk.OptionMenu(frame, self.selected_device, *self.midi_devices)
        self.device_dropdown.pack(side=tk.LEFT, padx=10)

        # Button to connect to MIDI device
        self.connect_button = tk.Button(frame, text="Connect to MIDI", command=self.connect_midi)
        self.connect_button.pack(side=tk.LEFT, padx=10)

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
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Line numbers on the left
        self.line_numbers = tk.Text(frame, width=4, padx=5, takefocus=0, border=0,
                                    background='lightgrey', state='disabled', wrap=tk.NONE)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Text editor (code area)
        self.editor = tk.Text(frame, wrap=tk.NONE, width=60, height=20)
        self.editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Attach scrollbar
        scrollbar = tk.Scrollbar(self.editor)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.on_scroll)

        # Initial update of line numbers
        self.update_line_numbers()

        # Bind events to update line numbers when typing or scrolling
        self.editor.bind("<KeyRelease>", self.update_line_numbers)
        self.editor.bind("<MouseWheel>", self.update_line_numbers)

    def on_scroll(self, *args):
        """Handle synchronized scrolling for both editor and line numbers."""
        self.editor.yview(*args)
        self.line_numbers.yview(*args)

    def update_line_numbers(self, event=None):
        """Update the line numbers in the side text widget."""
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)

        # Get the index of the first and last visible lines in the text editor
        first_visible_line = int(self.editor.index("@0,0").split('.')[0])
        last_visible_line = int(self.editor.index(f"@0,{self.editor.winfo_height()}").split('.')[0])

        # Insert the line numbers in the line_numbers widget
        line_number_string = "\n".join(str(i) for i in range(first_visible_line, last_visible_line + 1))
        self.line_numbers.insert(tk.END, line_number_string)

        # Disable editing of the line numbers widget
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
