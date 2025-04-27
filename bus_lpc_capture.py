#!/usr/bin/env python3

import csv
import sys

class LPCCapture:
  
    def __init__(self, file_path="record.csv"):
        self._out_file = file_path
        self.recording = False
        self.last_clk = 0
        self.current_nibbles = []
        self.all_frames = []

    def run(self):
        signal_file = self._out_file
        
        with open(signal_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                timestamp = float(row[0])
                lad0 = int(row[1])
                lad1 = int(row[2])
                lad2 = int(row[3])
                lad3 = int(row[4])
                lframe = int(row[5])
                clk = int(row[6])

                # Detect falling edge on LFRAME#
                if lframe == 0 and not self.recording:
                    if self.current_nibbles:
                        self.all_frames.append(self.current_nibbles)
                    self.current_nibbles = []
                    self.recording = True

                # Capture nibbles on rising edge of CLK
                if self.recording:
                    if self.last_clk == 0 and clk == 1:
                        nibble = (lad3 << 3) | (lad2 << 2) | (lad1 << 1) | lad0
                        self.current_nibbles.append((timestamp, nibble))

                self.last_clk = clk

            # Save last frame if any
            if self.current_nibbles:
                self.all_frames.append(self.current_nibbles)

    def interpret_frame(self, nibbles):
        if len(nibbles) < 3:
            return ["Incomplete frame"]

        output = []

        start_code = nibbles[0][1]
        sync_code = nibbles[1][1]
        command = nibbles[2][1]

        if start_code != 0x0:
            output.append("Error: No Start Frame detected")
        if sync_code != 0xF:
            output.append("Error: No Sync Confirm detected")

        if command == 0x1:
            output.append("Command: I/O Read")
        elif command == 0x2:
            output.append("Command: I/O Write")
        else:
            output.append(f"Unknown Command: 0x{command:X}")

        if len(nibbles) >= 7:
            address = (nibbles[3][1] << 12) | (nibbles[4][1] << 8) | (nibbles[5][1] << 4) | nibbles[6][1]
            output.append(f"Address: 0x{address:04X}")

        if len(nibbles) >= 11:
            data = (nibbles[7][1] << 12) | (nibbles[8][1] << 8) | (nibbles[9][1] << 4) | nibbles[10][1]
            output.append(f"Data: 0x{data:04X}")

        return output

    def interpret_all_frames(self):
        for frame in self.all_frames:
            decoded = self.interpret_frame(frame)
            for line in decoded:
                print(line)
            print("---")


def banner():
    print(f"Usage: {sys.argv[0]} <file_recorded.csv>")

# main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        banner()
        sys.exit(1)

    recorder = LPCCapture(sys.argv[1])
    recorder.run()
    recorder.interpret_all_frames()
