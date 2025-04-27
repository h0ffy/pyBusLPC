#!/usr/local/env python3


class LPC-Capture:
  
  recording = False
  last_clk = 0
  cur_nibble = []

  def __init__(self,file_path="record.csv"):
    self._out_file = file_path

    
  def __run__(self):

  def __exit__(self):
    return
    
  def __end__(self):
    self.exit()

  
  
  
  def detect_trigger(self):
    #signal_file = 'signal_record.csv'
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
    
            # Detect falling edge de LFRAME#
            if lframe == 0:
                recording = True
    
            if recording:
                # if CLK is UP
                if last_clk == 0 and clk == 1:
                    # Reading the nibble during CLK is up
                    nibble = (lad3 << 3) | (lad2 << 2) | (lad1 << 1) | lad0
                    cur_nibble.append((timestamp, nibble))
    
                last_clk = clk
    
    
    def interpretar_frame(nibbles):
        if len(nibbles) < 3:
            return "Error frame is broken"
    
        out = []
    
        start_code = nibbles[0][1]
        sync_code = nibbles[1][1]
        command = nibbles[2][1]
    
        if start_code != 0x0:
            out.append("Error: No Start Frame")
        if sync_code != 0xF:
            out.append("Error: No Sync")
    
        if command == 0x1:
            out.append("Command: I/O Read")
        elif command == 0x2:
            out.append("Command: I/O Write")
        else:
            out.append(f"Command:  Unknow value 0x{command:X}")
    
        # OFFSET (nextb 4 nibbles)
        if len(nibbles) >= 7:
            offset = (nibbles[3][1] << 12) | (nibbles[4][1] << 8) | (nibbles[5][1] << 4) | nibbles[6][1]
            out.append(f"Offset: 0x{offset:04X}")
    
        # Data ( is exists
        if len(nibbles) >= 11:
            data = (nibbles[7][1] << 12) | (nibbles[8][1] << 8) | (nibbles[9][1] << 4) | nibbles[10][1]
            out.append(f"Data: 0x{data:04X}")
    
        return out
