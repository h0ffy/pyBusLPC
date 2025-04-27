
This script decodes LPC (Low Pin Count) bus signals from a CSV file and interprets the frames 
based on the LPC protocol. It is designed to work with a specific format of CSV files generated 
by a logic analyzer.

## Classes:
    LPCDecode:
        A class to interpret LPC frames captured from a CSV file. It processes the signal data, 
        detects the start of frames, captures nibbles, and interprets the frames according to 
        the LPC protocol.

## Methods:
    LPCDecode.__init__(file_path="record.csv"):
        Initializes the LPCDecode instance with the specified CSV file path.

    LPCDecode.run():
        Reads the CSV file, processes the signal data, detects frames, and captures nibbles 
        based on the LPC protocol.

    LPCDecode.interpret_frame(nibbles):
        Interprets a single LPC frame based on the captured nibbles. It validates the frame 
        structure and decodes the command, address, and data fields.

    LPCDecode.interpret_all_frames():
        Iterates through all captured frames, decodes them, and prints the interpreted results.

## Usage:
    The script is executed by passing the path to the CSV file as a command-line argument. 
    It processes the file, decodes the LPC frames, and prints the interpreted results.

## Example:
    $ python3 lpcdecode.py path/to/signal.csv

