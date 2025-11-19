from enum import Enum

class xp_msg_t(Enum):
    CMD = 0
    ACC = 1
    TEMP1 = 2
    TEMP2 = 3
    TEMP3 = 4
    TEMP4 = 5
    PRESSURE1 = 6
    PRESSURE2 = 7
    PRESSURE3 = 8
    PRESSURE4 = 9
    PRESSURE5 = 10
    PRESSURE6 = 11
    PRESSURE7 = 12
    PRESSURE8 = 13
    PRESSURE9 = 14
    PRESSURE10 = 15
    PRESSURE11 = 16
    PRESSURE12 = 17

class xp_packet_t:
    def __init__(self):
        self.type = -1
        self.data = 0
        self.sender_id = 0x00
        self.END_BYTE = 0x00


class XPLink:
    def __init__(self):
        self.END_BYTE = 0x00
        self.PREV_END = 0
        self.buffer = []

    def COBS_UNPACK(self, input_bytes, end_byte):
        output = []
        read_head = 0

        while read_head < len(input_bytes):
            read_step = input_bytes[read_head]
            if read_step == end_byte:
                break

            # copy next (read_step - 1) bytes
            for i in range(1, read_step):
                output.append(input_bytes[read_head + i])

            # insert zero after the block
            output.append(0)

            read_head += read_step

        return output  
                
    def XPLINK_UNPACK(self, byte):
        try:
            #reset buffer if previously got an end byte
            if(self.PREV_END):
                self.PREV_END = 0
                self.buffer = []

            #add byte to buffer    
            self.buffer.append(byte)

            #collect buffer if end byte
            if(byte == self.END_BYTE):
                self.PREV_END = 1
                raw = self.COBS_UNPACK(self.buffer, self.END_BYTE)[0:-1]

                packet = xp_packet_t()
                packet.sender_id = raw[0]
                packet.type = raw[1]
                packet.data = raw[2:9]

                ##check the checksum
                actual = sum(raw[0:9])%256
                expected = raw[9]
                if(actual!= expected):
                    print("CHECKSUM DOES NOT MATCH\n")
                    return 0
                
                return packet
        except:
            print("[XPLink] Error Parsing Byte\n")
        return 0
    
    def XPLINK_PACK(self, xppack: xp_packet_t) -> list[12]:

        packet = [0] * 10
        
        # SENDER ID
        packet[0] = xppack.sender_id

        # PACKET TYPE
        packet[1] = xppack.type

        for i in range(7):
            packet[2+i] = (xppack.data >> (i*8)) & 0xFF
        
        sum1 = sum(packet[0:9])

        packet[9] = sum1 % 256

        return self.COBS_PACK(packet)

    
    def COBS_PACK(self, input: list[10]) -> list[12]:
        curr_idx = 0
        output = [0]*13
        
        for i in range(len(input)):

            if(input[i] == self.END_BYTE):
                output[curr_idx] = (i-curr_idx) + 1
                curr_idx = i+1
            else:
                output[i+1] = input[i]
            
            if(i == len(input) - 1):
                output[curr_idx] = (i-curr_idx) + 2
            
        output[len(input) + 1] = self.END_BYTE

        return output