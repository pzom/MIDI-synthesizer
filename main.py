import mido
import numpy as np
import sounddevice as sd
import threading
# Globals and Constants
sample_rate = 44100.0
active_notes = {}
notes_lock = threading.Lock()

def convert_midi_to_frequency(msg):
    return 440 * 2 ** ((msg.note - 69) / 12)

def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    amplitude =0.2
    mixed_signal = np.zeros(frames)
    
    with notes_lock:
        for note_id, (freq, phase) in list(active_notes.items()):
            t = (np.arange(frames) + phase) / sample_rate
            
            mixed_signal += amplitude * np.sin(2 * np.pi * freq * t)
            
            active_notes[note_id] = (freq, phase + frames)
            
    outdata[:] = mixed_signal.reshape(-1, 1)

def main():
    input_ports = mido.get_input_names()
    target_port_name = input_ports[1]  

    try:
        with sd.OutputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
            with mido.open_input(target_port_name) as in_port:
                for msg in in_port:
                    if msg.type == 'note_on' and msg.velocity > 0:
                        freq = convert_midi_to_frequency(msg)
                        with notes_lock:
                            active_notes[msg.note] = (freq, 0)
                    
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        with notes_lock:
                            if msg.note in active_notes:
                                del active_notes[msg.note]

    except KeyboardInterrupt:
        print("Exiting...")
main()