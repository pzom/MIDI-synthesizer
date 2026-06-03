import mido
import numpy as np
import sounddevice as sd
import threading
from PySide6 import QtCore, QtWidgets
# Globals and Constants
sample_rate = 44100.0
active_notes = {}
notes_lock = threading.Lock()
gain = [0]


def convert_midi_to_frequency(msg):
    return 440 * 2 ** ((msg.note - 69) / 12)

def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    amplitude =0.2 * gain[0] / 10
    print(amplitude)
    mixed_signal = np.zeros(frames)
    
    with notes_lock:
        for note_id, (freq, phase) in list(active_notes.items()):
            t = (np.arange(frames) + phase) / sample_rate
            
            mixed_signal += amplitude * np.sin(2 * np.pi * freq * t)
            
            active_notes[note_id] = (freq, phase + frames)
            
    outdata[:] = mixed_signal.reshape(-1, 1)

def main(dial):
    input_ports = mido.get_input_names()
    target_port_name = input_ports[0]  
    try:
        with sd.OutputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
            with mido.open_input(target_port_name) as in_port:
                gain[0] = dial.value()
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



def CreateDial(minimum, maximum, start_value, label):
    knob = QtWidgets.QDial()
    knob.setMinimum(minimum)
    knob.setMaximum(maximum)
    knob.setValue(start_value)
    knob.setNotchesVisible(True)
    knob.setNotchTarget(5.0)
    knob_label = QtWidgets.QLabel()
    knob_label.setText(label)
 
    
    return knob, knob_label


def sample_widget():
    widget = QtWidgets.QWidget()
    widget.layout = QtWidgets.QVBoxLayout(widget)
    widget.layout.addWidget(QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter))
    return widget

def start_app():
    app = QtWidgets.QApplication([])
    main_window = QtWidgets.QMainWindow()
    main_window.resize(800,600)
    dial, dial_label  = CreateDial(0,100, 50, "Gain")
    dial_test = dial
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(dial)
    layout.addWidget(dial_label)    
    container = QtWidgets.QWidget()
    container.setLayout(layout)
    main_window.setCentralWidget(container)
    main_window.show()
    app.exec()
    print(dial.value())
    main(dial)

start_app()
    

