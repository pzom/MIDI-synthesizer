import mido

input_ports = mido.get_input_names()
target_port_name = input_ports[1]  # Hardcoded index for the desired MIDI input port
print(f"Opening MIDI input port: {target_port_name}")

with mido.open_input(target_port_name) as in_port:
    for msg in in_port:
        print(msg)

print("Available MIDI input ports:")
for i, port in enumerate(input_ports):
    print(f"{i}: {port}")   

