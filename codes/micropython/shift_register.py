import machine 


BITS_IN_BYTE = 8
CLEAR_VALUE = 0x00


class Shift_register():
    
    def __init__(self, dio_pin_id = 16, clk_pin_id = 14, stb_pin_id = 15, lsbfirst = True):                 
        self.stb = machine.Pin(stb_pin_id, machine.Pin.OUT)
        self.clk = machine.Pin(clk_pin_id, machine.Pin.OUT)
        self.dio = machine.Pin(dio_pin_id, machine.Pin.OUT)        
        self.dio_pin_id = dio_pin_id
        self.lsbfirst = lsbfirst
        
        
    def _get_bits(self, value, lsbfirst):
        return [value >> i & 1 for i in (range(0,BITS_IN_BYTE,1) if lsbfirst else range(BITS_IN_BYTE-1,-1,-1))]
        
    
    def shiftOut(self, value, lsbfirst = None, drop_stb = True, raise_stb = True):
        
        if lsbfirst is None: lsbfirst = self.lsbfirst
        bits = self._get_bits(value, lsbfirst)
        
        if drop_stb: self.stb.low()
        
        for i in range(len(bits)):
            self.clk.low()
            self.dio.value(bits[i])
            self.clk.high() 
            
        if raise_stb: self.stb.high()   
        
 
    def clear(self, value = CLEAR_VALUE):
        self.shiftOut(value)        

    
    def shiftIn(self, lsbfirst = None, drop_stb = True, raise_stb = True):         
        if lsbfirst is None: lsbfirst = self.lsbfirst         
        self.dio.high()  # need to pull high
        
        if drop_stb: self.stb.low()
            
        bits = 0    
        for i in range(BITS_IN_BYTE):
            self.clk.low()
            shift_bits = i if lsbfirst else BITS_IN_BYTE - i 
            bits = bits | self.dio.value() << shift_bits
            self.clk.high() 
            
        if raise_stb: self.stb.high()
        
        return bits
        