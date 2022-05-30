#########
# these are temp imports for development
from unittest.mock import Mock
from scanner import Symbol, Scanner
from names import Names

#########
## TODO: implement errors and returns from them

"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """
    # def __init__(self, names, devices, network, monitors, scanner):
    def __init__(self, names, scanner):
        """Initialise constants."""
        self.names = names
        self.scanner = scanner
        self.success = 1
        self.symbol  = ""
        self.error_count = 0

    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        # Read first character
        self.scanner.advance()

        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.DEVICES_ID
        ):
            print('<--- Find DEVICES --->')
            self.symbol = self.scanner.get_symbol()
            if (self.symbol.type == self.scanner.CURLY_BRACKET 
                and self.symbol.id == self.scanner.LEFT_CURLY_BRACKET_ID
            ):
                pass
            self.symbol = self.scanner.get_symbol()
            self.device()
            self.symbol = self.scanner.get_symbol()

            while (self.symbol.type != 
                self.scanner.CURLY_BRACKET ) and   (self.symbol.id != 
                self.scanner.RIGHT_CURLY_BRACKET_ID):
                print('-- Another device found')
                self.device()
                self.symbol = self.scanner.get_symbol()

        
        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.CONNECT_ID
        ):
            print('<--- Find CONNECT --->')
            self.symbol = self.scanner.get_symbol()
            if (self.symbol.type == self.scanner.CURLY_BRACKET 
                and self.symbol.id == self.scanner.LEFT_CURLY_BRACKET_ID
            ):
                pass
            
            print('-Start first connection')
            self.symbol = self.scanner.get_symbol()
            self.create_conn()
            self.symbol = self.scanner.get_symbol()

            while (self.symbol.type != 
                self.scanner.CURLY_BRACKET ) and   (self.symbol.id != 
                self.scanner.RIGHT_CURLY_BRACKET_ID):
                print('-- Another connection found')
                self.create_conn()
                self.symbol = self.scanner.get_symbol()

        self.symbol = self.scanner.get_symbol()
        if (
            self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.MONITOR_ID
        ):
            print('<--- Find MONITOR --->')
            self.symbol = self.scanner.get_symbol()
            if (self.symbol.type == self.scanner.CURLY_BRACKET 
                and self.symbol.id == self.scanner.LEFT_CURLY_BRACKET_ID
            ):
                pass
            
            self.symbol = self.scanner.get_symbol()
            print('-Start first monitor point')
            self.make_monitor()
            self.symbol = self.scanner.get_symbol()

            while (int(self.symbol.id) != 
                self.scanner.RIGHT_CURLY_BRACKET_ID):
                print('-- Another monitor point found')
                self.make_monitor()
                self.symbol = self.scanner.get_symbol()
        self.symbol = self.scanner.get_symbol()
        print(self.symbol.type, self.names.get_name_string(self.symbol.id))
        if (self.symbol.type == self.scanner.KEYWORD
            and self.symbol.id == self.scanner.END_ID):
            print('<--- End of file found --->')


    def make_monitor(self):
        """
        Fucntion to parse the monitor line as per the EBNF spec
        """
        if self.symbol.type == self.scanner.DEVICE_NAME:
            pass
        self.symbol = self.scanner.get_symbol()

        if int(self.symbol.type) == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.scanner.OUTPUT_PIN:
                self.symbol = self.scanner.get_symbol()
        
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
        print('-Monitor point ended')
        

    def create_conn(self):
        """
        Method to parse connection creation as per EBNF spec
        """
        if self.symbol.type == self.scanner.DEVICE_NAME:
            pass
        self.symbol = self.scanner.get_symbol()

        if self.symbol.type == self.scanner.DOT:
            self.symbol = self.scanner.get_symbol()
            if self.symbol.type == self.output_pin:
                pass

        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.RIGHT_ARROW:
            pass

        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.DOT:
            pass
        
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.INPUT_NUMBER 
                or self.symbol.type == self.scanner.INPUT_PIN
            ):
                pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.SEMICOLON):
            pass
        print('-Connection Ended')

    def device(self):
        """
        Method to parse devices
        TODO this
        """

        if self.symbol.id == self.scanner.CLOCK_ID:
            print('-CLOCK found, start to parse CLOCK')
            self.clock_devices()
        elif self.symbol.id == self.scanner.SWITCH_ID:
            print('-SWITCH found, start to parse SWITCH')
            self.switch_devices()
        elif self.symbol.id == self.scanner.DTYPE_ID:
            print('-DTYPE found, start to parse DTYPE')
            self.dtype_devices()
        elif self.symbol.id == (self.gate_devices or
            self.AND_ID or
            self.NAND_ID or
            self.OR_ID or
            self.NOR_ID or
            self.DTYPE_ID or
            self.XOR_ID):
            print('-GATE found, start to parse GATE')
            self.gate_devices()
        else: 
            pass


    def gate_devices(self):
        """
        Method to parse gates
        """
        self.device_name()
        
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.BRACKET 
            and self.symbol.id == self.scanner.LEFT_BRACKET_ID):
            pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.NUMBER 
                and (self.symbol.id in range(1,17))):
            pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.BRACKET 
            and self.symbol.id == self.scanner.RIGHT_BRACKET_ID):
            pass
        
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            while self.symbol.type == self.scanner.COMMA:
                self.device_name()
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.BRACKET 
                    and self.symbol.id == self.scanner.LEFT_BRACKET_ID):
                    pass
                self.symbol = self.scanner.get_symbol()
                self.input_number()
                if (self.symbol.type == self.scanner.BRACKET 
                    and self.symbol.id == self.scanner.RIGHT_BRACKET_ID):
                    pass
                self.symbol = self.scanner.get_symbol() # comma check
        
        if self.symbol.type == self.scanner.SEMICOLON:
            pass

        print('-End of GATE statement')


    def dtype_devices(self):
        """
        Method to parse dtype latches
        """
        if self.symbol.id == self.scanner.DTYPE_ID:
            pass
        self.device_name()
        self.symbol = self.scanner.get_symbol()
        while self.symbol.type == self.scanner.COMMA:
            self.device_name()
            self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.SEMICOLON:
            print('-End of DTYPE statement')
            pass


    def switch_devices(self):
        """
        Method to parse switch defenitions
        """
        self.device_name()
        
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.BRACKET 
            and self.symbol.id == self.scanner.LEFT_BRACKET_ID):
            pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.NUMBER  
                and self.symbol.id in range(0,2)):
            pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.BRACKET 
            and self.symbol.id == self.scanner.RIGHT_BRACKET_ID):
            pass
        
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            while self.symbol.type == self.scanner.COMMA:
                self.device_name()
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.BRACKET 
                    and self.symbol.id == self.scanner.LEFT_BRACKET_ID):
                    pass
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.NUMBER
                    and (self.symbol.id in range(0,2))
                ):
                    pass
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.BRACKET 
                    and self.symbol.id == self.scanner.RIGHT_BRACKET_ID):
                    pass
                self.symbol = self.scanner.get_symbol() # comma check
        
        if self.symbol.type == self.scanner.SEMICOLON:
            pass
            
        print('-End of SWITCH statement')


    def clock_devices(self):
        """
        Method to parse clock devices
        """
        self.device_name()
        
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.BRACKET 
            and self.symbol.id == self.scanner.LEFT_BRACKET_ID):
            pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.NUMBER 
            and int(self.symbol.id) > 0):
            pass
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.BRACKET 
            and self.symbol.id == self.scanner.RIGHT_BRACKET_ID):
            pass
        
        self.symbol = self.scanner.get_symbol()
        if self.symbol.type == self.scanner.COMMA:
            while self.symbol.type == self.scanner.COMMA:
                self.device_name()
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.BRACKET 
                    and self.symbol.id == self.scanner.LEFT_BRACKET_ID):
                    pass
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.NUMBER
                    and int(self.symbol.id) > 0
                ):
                    pass
                self.symbol = self.scanner.get_symbol()
                if (self.symbol.type == self.scanner.BRACKET 
                    and self.symbol.id == self.scanner.RIGHT_BRACKET_ID):
                    pass
                self.symbol = self.scanner.get_symbol() # comma check
        
        if self.symbol.type == self.scanner.SEMICOLON:
            pass

        print('-End of CLOCK statement')

    def output_pin(self):
        """
        Method to parse output pins
        """
        if self.symbol == self.scanner.Q:
            self.symbol = self.scanner.getsymbol()
            return 1
        elif self.symbol == self.scanner.QBAR:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # output pin specified but not describes
            self.error("OUTPUT_PIN_NOT_DESCRIBED")

    def input_pin(self):
        if self.symbol == self.scanner.I:
            self.symbol = self.scanner.getsymbol()
            self.input_number()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.DATA_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.CLK_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.SET_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        elif (
            self.symbol.type == self.scanner.KEYWORDS
            and self.symbol.id == self.scanner.CLEAR_ID
        ):
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # unknown symbol or not specified
            self.error("UNKOWN_SYMBOL")

    def input_number(self):
        if (self.symbol.type == self.scanner.NUMBER
                    and (self.symbol.id in range(1,17))
        ):
            self.symbol = self.scanner.get_symbol()
        else:
            # error of invalid input
            self.error("NUMBER_OF_INPUTS_INVALID")

    def on_off(self):
        """
        Method to parse on/off parameter
        """
        if self.symbol == self.scanner.ZERO:
            self.symbol = self.scanner.getsymbol()
            return 1
        elif self.symol == self.scanner.ONE:
            self.symbol = self.scanner.getsymbol()
            return 1
        else:
            # error: 0 or 1 expected
            self.error("0_OR_1_EXPECTED")

    def device_name(self):
        """
        Method to parse device names
        """
        # Identifier EBNF statement implicity defined by DEVICE_NAME type
        self.symbol = self.scanner.get_symbol()
        if (self.symbol.type == self.scanner.DEVICE_NAME):
            pass
        else:
            self.error("DEVICE_NAME_EXPECTED")



    def error(self, error_type):
        self.error_count += 1


path_definition = "definitions/circuit.def"

names_instance = Names()

scanner_instance = Scanner(path_definition, names_instance)

parser_1 = Parser(names_instance, scanner_instance)

a = parser_1.parse_network()
