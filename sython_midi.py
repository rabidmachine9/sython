import mido
import time


class SythonMidiMixin:
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
        """Send a MIDI note message."""
        msg = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
        # Send the message via MIDI
        # Assuming you have a midi output port initialized
        self.midi_output.send(msg)
        # Optionally add a delay for the duration
        time.sleep(duration)
        msg_off = mido.Message('note_off', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_off)

    def set_tempo(self, bpm):
        """Set the tempo in beats per minute."""
        self.tempo = bpm
        # Use this tempo for sequencing notes