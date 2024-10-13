import mido
import time


class SythonMidiMixin:
    # Map for note names to MIDI note numbers
    NOTE_TO_MIDI = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 
        'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }

    def __init__(self):
        self.midi_output = None

    def add_midi_library(self, env):
        env['sendNote'] = self.send_note
        env['setTempo'] = self.set_tempo

    def set_midi_output(self, port_name):
        """Set the MIDI output by specifying the port name."""
        try:
            self.midi_output = mido.open_output(port_name)
            print(f"Connected to MIDI output: {port_name}")
        except IOError:
            print(f"Could not connect to MIDI output: {port_name}")

    def send_note(self, pitch, velocity, duration, channel=0):
        """Send a MIDI note message, supports both note names (e.g. C#3) and MIDI numbers."""
        if isinstance(pitch, str):
            pitch = self.parse_note_name(pitch)
        if pitch is None:
            raise ValueError(f"Invalid note: {pitch}")
        
        msg_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_on)
        time.sleep(duration)
        msg_off = mido.Message('note_off', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_off)

    def set_tempo(self, bpm):
        """Set the tempo in beats per minute."""
        self.tempo = bpm

    def parse_note_name(self, note):
        """Convert a note name like 'C#3' into a MIDI note number."""
        note_name = note[:-1]  # Extract note name (e.g., "C#")
        octave = note[-1]      # Extract octave (e.g., "3")
        
        if note_name in self.NOTE_TO_MIDI and octave.isdigit():
            octave = int(octave)
            midi_note_number = self.NOTE_TO_MIDI[note_name] + (octave + 1) * 12
            return midi_note_number
        return None
