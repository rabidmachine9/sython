import mido
import time

# Open MIDI output port
midi_out = mido.open_output()  # Automatically selects the default output device

# Create a 'note_on' message
note_on = mido.Message('note_on', note=60, velocity=64)

# Send the 'note_on' message
midi_out.send(note_on)
print("Note On sent")

# Wait for 1 second
time.sleep(1)

# Send 'note_off' message to stop the note
note_off = mido.Message('note_off', note=60)
midi_out.send(note_off)
print("Note Off sent")
