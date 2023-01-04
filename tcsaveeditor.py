
from enum import IntEnum
import io
from pathlib import Path
from random import randint
import sys

import snappy

_save_format_version = 6
_debug_uncompressed = False

TELEPORT_WIRE = 0b0010_0000

# Copied from save_monger
class ComponentKind(IntEnum):
    Error                   = 0
    Off                     = 1
    On                      = 2
    Buffer1                 = 3
    Not                     = 4
    And                     = 5
    And3                    = 6
    Nand                    = 7
    Or                      = 8
    Or3                     = 9
    Nor                     = 10
    Xor                     = 11
    Xnor                    = 12
    Counter8                = 13
    VirtualCounter8         = 14
    Counter64               = 15
    VirtualCounter64        = 16
    Ram8                    = 17
    VirtualRam8             = 18
    DELETED_0               = 19
    DELETED_1               = 20
    DELETED_17              = 21
    DELETED_18              = 22
    Register8               = 23
    VirtualRegister8        = 24
    Register8Red            = 25
    VirtualRegister8Red     = 26
    Register8RedPlus        = 27
    VirtualRegister8RedPlus = 28
    Register64              = 29
    VirtualRegister64       = 30
    Switch8                 = 31
    Mux8                    = 32
    Decoder1                = 33
    Decoder3                = 34
    Constant8               = 35
    Not8                    = 36
    Or8                     = 37
    And8                    = 38
    Xor8                    = 39
    Equal8                  = 40
    DELETED_2               = 41
    DELETED_3               = 42
    Neg8                    = 43
    Add8                    = 44
    Mul8                    = 45
    Splitter8               = 46
    Maker8                  = 47
    Splitter64              = 48
    Maker64                 = 49
    FullAdder               = 50
    BitMemory               = 51
    VirtualBitMemory        = 52
    DELETED_10              = 53
    Decoder2                = 54
    Timing                  = 55
    NoteSound               = 56
    DELETED_4               = 57
    DELETED_5               = 58
    Keyboard                = 59
    FileLoader              = 60
    Halt                    = 61
    WireCluster             = 62
    LevelScreen             = 63
    Program8_1              = 64
    Program8_1Red           = 65
    DELETED_6               = 66
    DELETED_7               = 67
    Program8_4              = 68
    LevelGate               = 69
    Input1                  = 70
    LevelInput2Pin          = 71
    LevelInput3Pin          = 72
    LevelInput4Pin          = 73
    LevelInputConditions    = 74
    Input8                  = 75
    Input64                 = 76
    LevelInputCode          = 77
    LevelInputArch          = 78
    Output1                 = 79
    LevelOutput1Sum         = 80
    LevelOutput1Car         = 81
    DELETED_8               = 82
    DELETED_9               = 83
    LevelOutput2Pin         = 84
    LevelOutput3Pin         = 85
    LevelOutput4Pin         = 86
    Output8                 = 87
    Output64                = 88
    LevelOutputArch         = 89
    LevelOutputCounter      = 90
    DELETED_11              = 91
    Custom                  = 92
    VirtualCustom           = 93
    Program                 = 94
    DelayLine1              = 95
    VirtualDelayLine1       = 96
    Console                 = 97
    Shl8                    = 98
    Shr8                    = 99

    Constant64              = 100
    Not64                   = 101
    Or64                    = 102
    And64                   = 103
    Xor64                   = 104
    Neg64                   = 105
    Add64                   = 106
    Mul64                   = 107
    Equal64                 = 108
    LessU64                 = 109
    LessI64                 = 110
    Shl64                   = 111
    Shr64                   = 112
    Mux64                   = 113
    Switch64                = 114

    ProbeMemoryBit          = 115
    ProbeMemoryWord         = 116

    AndOrLatch              = 117
    NandNandLatch           = 118
    NorNorLatch             = 119

    LessU8                  = 120
    LessI8                  = 121

    DotMatrixDisplay        = 122
    SegmentDisplay          = 123

    Input16                 = 124
    Input32                 = 125

    Output16                = 126
    Output32                = 127

    DELETED_12              = 128
    DELETED_13              = 129
    DELETED_14              = 130
    DELETED_15              = 131
    DELETED_16              = 132

    Buffer8                 = 133
    Buffer16                = 134
    Buffer32                = 135
    Buffer64                = 136

    ProbeWireBit            = 137
    ProbeWireWord           = 138

    Switch1                 = 139

    Output1z                = 140
    Output8z                = 141
    Output16z               = 142
    Output32z               = 143
    Output64z               = 144

    Constant16              = 145
    Not16                   = 146
    Or16                    = 147
    And16                   = 148
    Xor16                   = 149
    Neg16                   = 150
    Add16                   = 151
    Mul16                   = 152
    Equal16                 = 153
    LessU16                 = 154
    LessI16                 = 155
    Shl16                   = 156
    Shr16                   = 157
    Mux16                   = 158
    Switch16                = 159
    Splitter16              = 160
    Maker16                 = 161
    Register16              = 162
    VirtualRegister16       = 163
    Counter16               = 164
    VirtualCounter16        = 165

    Constant32              = 166
    Not32                   = 167
    Or32                    = 168
    And32                   = 169
    Xor32                   = 170
    Neg32                   = 171
    Add32                   = 172
    Mul32                   = 173
    Equal32                 = 174
    LessU32                 = 175
    LessI32                 = 176
    Shl32                   = 177
    Shr32                   = 178
    Mux32                   = 179
    Switch32                = 180
    Splitter32              = 181
    Maker32                 = 182
    Register32              = 183
    VirtualRegister32       = 184
    Counter32               = 185
    VirtualCounter32        = 186

    LevelOutput8z           = 187

    Nand8                   = 188
    Nor8                    = 189
    Xnor8                   = 190
    Nand16                  = 191
    Nor16                   = 192
    Xnor16                  = 193
    Nand32                  = 194
    Nor32                   = 195
    Xnor32                  = 196
    Nand64                  = 197
    Nor64                   = 198
    Xnor64                  = 199

    Ram                     = 200
    VirtualRam              = 201
    RamLatency              = 202
    VirtualRamLatency       = 203

    RamFast                 = 204
    VirtualRamFast          = 205
    Rom                     = 206
    VirtualRom              = 207
    SolutionRom             = 208
    VirtualSolutionRom      = 209

    DelayLine8              = 210
    VirtualDelayLine8       = 211
    DelayLine16             = 212
    VirtualDelayLine16      = 213
    DelayLine32             = 214
    VirtualDelayLine32      = 215
    DelayLine64             = 216
    VirtualDelayLine64      = 217

    RamDualLoad             = 218
    VirtualRamDualLoad      = 219

    Hdd                     = 220
    VirtualHdd              = 221

    Network                 = 222

    Rol8                    = 223
    Rol16                   = 224
    Rol32                   = 225
    Rol64                   = 226
    Ror8                    = 227
    Ror16                   = 228
    Ror32                   = 229
    Ror64                   = 230

    IndexerBit              = 231
    IndexerByte             = 232

    DivMod8                 = 233
    DivMod16                = 234
    DivMod32                = 235
    DivMod64                = 236

    SpriteDisplay           = 237
    ConfigDelay             = 238

    Clock                   = 239

    LevelInput1             = 240
    LevelInput8             = 241
    LevelOutput1            = 242
    LevelOutput8            = 243

    Ashr8                   = 244
    Ashr16                  = 245
    Ashr32                  = 246
    Ashr64                  = 247

    Bidirectional1          = 248
    VirtualBidirectional1   = 249
    Bidirectional8          = 250
    VirtualBidirectional8   = 251
    Bidirectional16         = 252
    VirtualBidirectional16  = 253
    Bidirectional32         = 254
    VirtualBidirectional32  = 255
    Bidirectional64         = 256
    VirtualBidirectional64  = 257

    def __str__(self):
        return self.name

class ComponentRotation(IntEnum):
    '''
    Component rotation, based on the in-game clockwise rotation. Default is ROT_0.
    '''
    ROT_0   = 0,
    ROT_90  = 1,
    ROT_180 = 2,
    ROT_270 = 3

    def __str__(self):
        return self.name[4:] + '°'

class WireKind(IntEnum):
    '''
    The size of the wire, in bits. So `WK_64` is the 64-bit wire, etc.
    '''
    WK_1  = 0,
    WK_8  = 1,
    WK_16 = 2,
    WK_32 = 3,
    WK_64 = 4

    def __str__(self):
        return self.name[3:]

class WireColor(IntEnum):
    DEFAULT    = 0,
    YELLOW     = 1,
    KIWI_GREEN = 2,
    GREEN_CYAN = 3,
    CYAN       = 4,
    DARK_BLUE  = 5,
    PURPLE     = 6,
    PINK       = 7,
    ORANGE     = 8,
    WHITE      = 9,
    GREY       = 10,

    def __str__(self):
        return self.name

class TCPoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'({self.x}, {self.y})'

class TCSynced(IntEnum):
    unsynced = 0,
    synced = 1,
    changed_after_sync = 2

    def __str__(self):
        return self.name

class TCComponent:
    def __init__(self, kind: ComponentKind, position: TCPoint, rotation = ComponentRotation.ROT_0, permanent_id = randint(0, 2**64-1), custom_string = "", setting_1 = 0,
            setting_2 = 0, ui_order = 0, custom_id = 0, custom_displacement = TCPoint(0, 0), selected_programs: dict[int, str] = {}):
        self.kind = kind
        self.position = position
        self.rotation = rotation
        self.permanent_id = permanent_id
        self.custom_string = custom_string
        self.setting_1 = setting_1
        self.setting_2 = setting_2
        self.ui_order = ui_order
        self.custom_id = custom_id
        self.custom_displacement = custom_displacement
        self.selected_programs = selected_programs
    
    def __str__(self):
        return '{:30}  Position: ({:3}, {:3})  Rotation: {}'.format(str(self.kind) + f' [{str(int(self.kind))}]', self.position.x, self.position.y, self.rotation)

class TCWirePath:
    def __init__(self, start: TCPoint, body: list[int], end = TCPoint(0, 0)):
        self.start = start
        self.body = body
        self.end = end

class TCWire:
    def __init__(self, kind: WireKind, color = WireColor.DEFAULT, comment: str = "", path = TCWirePath(TCPoint(0, 0), [0b0001_1111])):
        self.kind = kind
        self.color = color
        self.comment = comment
        self.path = path
    
    def __str__(self):
        return 'Wire ({:3}, {:3}) {:>2}-bit {}'.format(self.path.start.x, self.path.start.y, self.kind, self.color)

class TCSave:
    def __init__(self, save_id = 0, hub_id = 0, gate = 0, delay = 0, menu_visible = False, clock_speed = 0, dependencies: list[int] = [], camera_position = TCPoint(0, 0),
            synced = TCSynced.unsynced, campaign_bound = False, player_data: list[int] = [], hub_description = "", components: list[TCComponent] = [],
            wires: list[TCWire] = []):
        self.save_id = save_id
        self.hub_id = hub_id
        self.gate = gate
        self.delay = delay
        self.menu_visible = menu_visible
        self.clock_speed = clock_speed
        self.dependencies = dependencies
        self.camera_position = camera_position
        self.synced = synced
        self.campaign_bound = campaign_bound
        self.player_data = player_data
        self.hub_description = hub_description
        self.components = components
        self.wires = wires

    def from_file(self, source_file: str) -> 'TCSave':
        # Read bytes, check save version
        f = open(source_file, 'rb')
        save_format_v = int.from_bytes(f.read(1), 'little')
        if save_format_v != _save_format_version:
            print(f'Error: Expected save format v{_save_format_version}, instead got v{save_format_v}!')
            sys.exit()
        f_compressed_bytes = f.read()
        f.close()

        # Decompress
        self._bytes_io = io.BytesIO(snappy.uncompress(data=f_compressed_bytes))

        if _debug_uncompressed: # For debugging uncompressed data
            self._uncompressed_data = self._bytes_io.read()
            self._bytes_io.seek(0)

        # Read the data
        self.save_id = self._get_int(8)
        self.hub_id = self._get_int(4)
        self.gate = self._get_int(8)
        self.delay = self._get_int(8)
        self.menu_visible = self._get_bool()
        self.clock_speed = self._get_int(4)
        self.dependencies = []
        for _ in range(0, self._get_int(2)):
            self.dependencies.append(self._get_int(8))
        self.description = self._get_string()
        self.camera_position = self._get_point()
        self.synced = TCSynced(self._get_bool())
        self.campaign_bound = self._get_bool()
        self._bytes_io.read(2) # Discard (currently) unused
        self.player_data = []
        for _ in range(0, self._get_int(2)):
            self.player_data.append(self._get_byte())
        self.hub_description = self._get_string()
        self.components = []
        for _ in range(0, self._get_int(8)):
            c_kind = ComponentKind(self._get_int(2))
            self.components.append(TCComponent(
                kind=c_kind,
                position=self._get_point(),
                rotation=ComponentRotation(self._get_int(1)),
                permanent_id=self._get_int(8),
                custom_string=self._get_string(),
                setting_1=self._get_int(8),
                setting_2=self._get_int(8),
                ui_order=self._get_signed_int(2),
                custom_id=self._get_int(8) if c_kind == ComponentKind.Custom else 0,
                custom_displacement=self._get_point() if c_kind == ComponentKind.Custom else TCPoint(0, 0),
                selected_programs=self._get_selected_programs() if (c_kind == ComponentKind.Program8_1 or c_kind == ComponentKind.Program8_4 or
                    c_kind == ComponentKind.Program) else {},
            ))
        self.wires = []
        for _ in range(0, self._get_int(8)):
            wire = TCWire(
                kind=WireKind(self._get_int(1)),
                color=WireColor(self._get_int(1)),
                comment=self._get_string(),
                path=TCWirePath(start=self._get_point(), body=self._get_wire_body())
            )
            if wire.path.body[-1] == TELEPORT_WIRE:
                wire.path.end = self._get_point()
            self.wires.append(wire)
        return self
    
    def save(self, save_location: str):
        self._bytes_io = io.BytesIO()
        self._write(self.save_id, 8)
        self._write(self.hub_id, 4)
        self._write(self.gate, 8)
        self._write(self.delay, 8)
        self._write(self.menu_visible, 1)
        self._write(self.clock_speed, 4)
        self._write(len(self.dependencies), 2)
        for dep in self.dependencies:
            self._write(dep, 8)
        self._write_string(self.description)
        self._write_point(self.camera_position)
        self._write(int(self.synced), 1)
        self._write(self.campaign_bound, 1)
        self._write(0, 2) # Write (currently) unused
        self._write(len(self.player_data), 2)
        for player_d in self.player_data:
            self._write_byte(player_d)
        self._write_string(self.hub_description)
        self._write(len(self.components), 8)
        for comp in self.components:
            self._write(int(comp.kind), 2)
            self._write_point(comp.position)
            self._write(int(comp.rotation), 1)
            self._write(comp.permanent_id, 8)
            self._write_string(comp.custom_string)
            self._write(comp.setting_1, 8)
            self._write(comp.setting_2, 8)
            self._write_signed(comp.ui_order, 2)
            if comp.kind == ComponentKind.Custom:
                self._write(comp.custom_id, 8)
                self._write_point(comp.custom_displacement)
            elif (comp.kind == ComponentKind.Program8_1 or comp.kind == ComponentKind.Program8_4 or comp.kind == ComponentKind.Program):
                self._write_selected_programs(comp.selected_programs)
        self._write(len(self.wires), 8)

        for wire in self.wires:
            self._write(int(wire.kind), 1)
            self._write(int(wire.color), 1)
            self._write_string(wire.comment)
            self._write_point(wire.path.start)
            for body in wire.path.body:
                self._write(body, 1)
            if wire.path.body[-1] == TELEPORT_WIRE:
                self._write_point(wire.path.end)

        # Debug uncompressed data, verifies that the data being saved is identical to the data loaded from file. Ensures that the writer is working as intended.
        if _debug_uncompressed:
            self._bytes_io.seek(0)
            _saving_data = self._bytes_io.read()
            for i in range(0, len(self._uncompressed_data)):
                if i >= len(_saving_data):
                    print(f'Unexpectedly reached the end of saving data at index {i}!')
                    sys.exit()
                if self._uncompressed_data[i] != _saving_data[i]:
                    print(f'Encountered corrupt data at index [{i}], data loaded from file:\n{self._uncompressed_data[i:]}\nCorrupt data attempted to save:\n{_saving_data[i:]}')
                    sys.exit()
            if len(self._uncompressed_data) != len(_saving_data):
                print(f'Unexpectedly reached the end of load data, remaining save data possibly corrupt:\n{_saving_data[len(self._uncompressed_data):]}')
                sys.exit()

        # Compress data
        self._bytes_io.seek(0)
        self._bytes_io = snappy.compress(data=self._bytes_io.read())
        
        # Write data to file
        Path(save_location).parent.mkdir(exist_ok=True, parents=True) # Make directory if does not exist
        f = open(save_location, 'wb')
        f.write(_save_format_version.to_bytes(1, 'little'))
        f.write(self._bytes_io)
        f.close()
    
    def create_teleport_wire(self, start: TCPoint, end: TCPoint, kind = WireKind.WK_1, color = WireColor.DEFAULT, comment = ""):
        self.wires.append(TCWire(kind, color, comment, TCWirePath(start, [TELEPORT_WIRE], end)))
    
    def _get_string(self) -> str:
        return self._bytes_io.read(int.from_bytes(self._bytes_io.read(2), 'little')).decode('ascii')
    
    def _get_int(self, n_bytes: int) -> int:
        return int.from_bytes(self._bytes_io.read(n_bytes), 'little')
    
    def _get_signed_int(self, n_bytes: int) -> int:
        return int.from_bytes(self._bytes_io.read(n_bytes), 'little', signed=True)
    
    def _get_byte(self) -> bytes:
        return self._bytes_io.read(1)
    
    def _get_bool(self):
        return bool(int.from_bytes(self._bytes_io.read(1), 'little'))
    
    def _get_point(self) -> TCPoint:
        return TCPoint(int.from_bytes(self._bytes_io.read(2), 'little', signed=True), int.from_bytes(self._bytes_io.read(2), 'little', signed=True))
    
    def _get_selected_programs(self) -> dict[int, str]:
        result: dict[int, str] = {}
        for _ in range(0, int.from_bytes(self._bytes_io.read(2), 'little')):
            key = int.from_bytes(self._bytes_io.read(8), 'little') # Must come first
            result[key] = self._get_string()
        return result

    def _get_wire_body(self) -> list[int]:
        body_data = []
        while True:
            body_data.append(int.from_bytes(self._bytes_io.read(1), 'little'))

            if body_data[-1] == TELEPORT_WIRE or (body_data[-1] & 0b0001_1111) == 0:
                return body_data
    
    def _write(self, data, bytes: int):
        self._bytes_io.write(data.to_bytes(bytes, 'little'))
    
    def _write_byte(self, data: bytes):
        self._bytes_io.write(data)
    
    def _write_signed(self, data, bytes: int):
        self._bytes_io.write(data.to_bytes(bytes, 'little', signed=True))

    def _write_string(self, string: str):
        self._bytes_io.write(len(string).to_bytes(2, 'little'))
        self._bytes_io.write(bytes(string, 'ascii'))

    def _write_point(self, tc_point: TCPoint):
        self._bytes_io.write(tc_point.x.to_bytes(2, 'little', signed=True))
        self._bytes_io.write(tc_point.y.to_bytes(2, 'little', signed=True))

    def _write_selected_programs(self, selected_programs: dict[int, str]):
        self._bytes_io.write(len(selected_programs).to_bytes(2, 'little'))
        for key, value in selected_programs.items():
            self._bytes_io.write(key.to_bytes(8, 'little'))
            self._write_string(value)

    def __str__(self):
        return  f'Save Id:         {self.save_id}\n' + \
                f'Hub Id:          {self.hub_id}\n' + \
                f'Gate:            {self.gate}\n' + \
                f'Delay:           {self.delay}\n' + \
                f'Menu Visible:    {self.menu_visible}\n' + \
                f'Clock Speed:     {self.clock_speed}\n' + \
                f'Description:     \"{self.description}\"\n' + \
                f'Camera Position: {self.camera_position}\n' + \
                f'Synced:          {str(self.synced)}\n' + \
                f'Campaign Bound:  {self.campaign_bound}\n' + \
                f'Hub Description: \"{self.hub_description}\"\n' + \
                f'Components:      {len(self.components)}\n' + \
                f'Wires:           {len(self.wires)}'
