import mido
import time


class SythonMidiMixin:
    NOTE_TO_MIDI = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 
        'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }

    def __init__(self):
        print("Initializing SythonMidiMixin")
        self.midi_output = None
        self.tempo = 120  # Default BPM
        self.tempo_ms = self.calculate_tempo_ms()
        self.is_playing = False

    def play_pause(self):
        # Toggle the playing state
        self.is_playing = not self.is_playing
        print("Playback started." if self.is_playing else "Playback paused.")

    def add_midi_library(self, env):
        """Add MIDI-related methods to the Sython environment."""
        env['sendNote'] = self.send_note
        env['setTempo'] = self.set_tempo
        env['sequencer'] = self.sequencer
        env['playPause'] = self.play_pause

    def set_midi_output(self, port_name):
        """Set the MIDI output by specifying the port name."""
        try:
            self.midi_output = mido.open_output(port_name)
            print(f"Connected to MIDI output: {port_name}")
        except IOError:
            print(f"Could not connect to MIDI output: {port_name}")

    def calculate_tempo_ms(self):
        """Calculate the time in milliseconds for one beat based on the current tempo."""
        return 60.0 / self.tempo

    def send_note(self, pitch, velocity, duration, channel=0):
        """Send a MIDI note message."""
        if isinstance(pitch, str):
            pitch = self.parse_note_name(pitch)
        if pitch is None:
            raise ValueError(f"Invalid note: {pitch}")

        # Send note on message
        msg_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_on)
        time.sleep(duration)  # Wait for the specified duration
        # Send note off message
        msg_off = mido.Message('note_off', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_off)
    
    def note_on(self, pitch, velocity, channel=0):
        if isinstance(pitch, str):
            pitch = self.parse_note_name(pitch)
        if pitch is None:
            raise ValueError(f"Invalid note: {pitch}")

        # Send note on message
        msg_on = mido.Message('note_on', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_on)
    
    def note_off(self, pitch, velocity, channel=0):
        # Send note off message
        msg_off = mido.Message('note_off', note=pitch, velocity=velocity, channel=channel)
        self.midi_output.send(msg_off)

    def set_tempo(self, bpm):
        """Set the tempo in beats per minute."""
        self.tempo = bpm
        self.tempo_ms = self.calculate_tempo_ms()  # Recalculate tempo in milliseconds
        return f"Tempo set to {bpm} BPM"

    def parse_note_name(self, note):
        """Convert a note name like 'C#3' into a MIDI note number."""
        note_name = note[:-1]
        octave = note[-1]

        if note_name in self.NOTE_TO_MIDI and octave.isdigit():
            octave = int(octave)
            return self.NOTE_TO_MIDI[note_name] + (octave + 1) * 12
        return None

    def sequencer(self, *args):
        i = 0
        notes = list(args)
        while self.is_playing:
            
            
            try:
                self.note_on(notes[i%2], 100 )
                time.sleep(self.tempo_ms)
                self.note_off(notes[i%2], 100)

            except Exception as e:
                print(f"[DEBUG] Error while evaluating step: {e}")
                continue
            
            i += 1