import os
import socket
import struct
import select

class connection:
    def __init__(self) -> None:
        self._connected = False

        display = os.environ.get("DISPLAY", ":0")
        display_num = display.split(":")[-1].split(".")[0]
        socket_path = f"/tmp/.X11-unix/X{display_num}"

        # Connect to the x11 server with socket
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.connect(socket_path)

        self._extra_data = None
        self._window_id = None

    def _send_packet(
        self,
        packet: bytes,
        expected_reply=False
    ) -> bool:

        self.s.sendall(packet)

        if expected_reply:
            response = self.s.recv(8)

            status, _, major, minor, length = struct.unpack(
                "<BBHHH", response
            )

            if status == 1:
                self._extra_data = self.s.recv(length * 4)
                return True

            print("X11 error:", major)
            return False

        ready, _, _ = select.select([self.s], [], [], 0.1)

        if ready:
            response = self.s.recv(32)
            if response[0] == 0:
                print("X11 error:", response[1])
                print("Sequence:", struct.unpack("<H", response[2:4])[0])
                print("Major opcode:", response[10])
                return False

        return True




        return True

    def _recv_all(self, size):
        data = b""

        while len(data) < size:
            data += self.s.recv(size - len(data))
        return data



    def close(self) -> bool:
        try:
            # Let's close the connection
            self.s.close()
            return True
        except Exception:
            return False


    def connect(self) -> bool:
        byte_order = 0x6C

         # Let's set the packet to send the cpu
        packet = struct.pack(
            "<BBHHHHxx",
            byte_order,         # Byte order
            0,                  # Unused bytes
            11,                 # Protocol major version
            0,                  # Protocol minor version
            0,                  # Lenght of authentication
            0,                  # Length of authentication protocol data
        )

        self.s.sendall(packet)
        response_header = self._recv_all(8)

        # Check the server response
        if not response_header:
            print("No response from X11")
            return False

        status, _, major, minor, additional_length = struct.unpack(
            "<BBHHH",
            response_header
        )

        self._extra_data = self._recv_all(additional_length * 4)

        if status == 1:
            self._connected = True
            print("Connected to x11 server")
            return True

        print("Connection failed")
        return False
#


    def create_window(
        self,
        size: tuple= (250, 100)
    ) -> tuple:


        # Data to load in the packet
        opcode_create = 1
        depth = 0
        request_length = 9

        # Screen size
        vendor_length = struct.unpack("<H", self._extra_data[16:18])[0]
        num_formats = self._extra_data[21]
        vendor_pad = (4 - (vendor_length % 4)) % 4
        screen_start = (
            32
            + vendor_length
            + vendor_pad
            + num_formats * 8
        )


        # Create window
        resource_id_base = struct.unpack("<I", self._extra_data[4:8])[0]
        self._window_id = resource_id_base + 1
        root_window_id = struct.unpack("<I", self._extra_data[screen_start : screen_start + 4])[
            0
        ]

        print("ROOT:", hex(root_window_id))
        print("WINDOW:", hex(self._window_id))


        # Customize the window
        value_mask = 1 << 1
        background_pixel = 0xFFFFFF


        packet = struct.pack(
            "<BBHIIhhhhHHIII",
            opcode_create,      # Create window
            depth,              # Color
            request_length,     # Packet lenght
            self._window_id,    # Window ID
            root_window_id,     # Parent window ID
            100,
            100,                # x,y screen position
            size[0],
            size[1],            # x,y window size
            0,                  # Border
            1,                  # Window type
            0,                  # Visual ID
            value_mask,         # Value mask
            background_pixel    # Background color

        )

        # Let's check if the x11 server is connected to python
        if self._send_packet(packet, expected_reply=False):
            print("Window created successfully")
            return (True, "Window created successfully")
        else:
            print("Error creating window")
            return (False, "Error creating window")

    def show_window(self) -> tuple:
        opcode_map = 8
        map_length = 2

        packet = struct.pack(
            "<BBHI",
            opcode_map,         # Map window command
            0,                  # Empty pad
            map_length,         # Packet lenght
            self._window_id,    # Window ID
        )


        if self._send_packet(packet, expected_reply=False):
            print("Window loaded successfully")
            return (True, "Window loaded successfully")
        else:
            print("Error loading window")
            return (False, "Error loading window")

    def create_gc(self):

        opcode = 55
        request_length = 5

        resource_id_base = struct.unpack(
            "<I",
            self._extra_data[4:8]
        )[0]

        self._gc_id = resource_id_base + 2

        value_mask = 1 << 2
        foreground = 0x000000

        print("opcode:", opcode, type(opcode))
        print("length:", request_length, type(request_length))
        print("gc:", self._gc_id, type(self._gc_id))
        print("window:", self._window_id, type(self._window_id))
        print("mask:", value_mask, type(value_mask))
        print("foreground:", foreground, type(foreground))

        packet = struct.pack(
            "<BBHIIII",
            opcode,
            0,
            request_length,
            self._gc_id,
            self._window_id,
            value_mask,
            foreground
        )

        return self._send_packet(packet)

    def clear_window(self):
        opcode = 61
        request_length = 4

        packet = struct.pack(
            "<BBH I hh HH",
            opcode,
            0,
            request_length,
            self._window_id,
            0,                  # x
            0,                  # y
            0,                  # Window width
            0                   # Window height
        )

        print(self.s.sendall(packet))

        return True


    def draw_line(
        self,
        coo: tuple = ((50, 50), (300, 200))
    ) -> bool:

        print(coo)

        opcode = 65
        coordinate_mode = 0
        request_length = 5

        x1 = coo[0][0]
        y1 = coo[0][1]
        x2 = coo[1][0]
        y2 = coo[1][1]

        packet = struct.pack(
            "<BBHIIhhhh",
            opcode,             # Execute PolyLine
            coordinate_mode,    # Next coordinates
            request_length,     # Request bytes
            self._window_id,    # Window ID
            self._gc_id,        # Draw type
            x1,
            y1,                 # Drawable coordinates
            x2,
            y2
        )

        print("Packet:", packet.hex())

        return self._send_packet(packet)


if __name__ == "__main__":
    import time

    cn = connection()
    cn.connect()


    cn.create_window()
    cn.show_window()
    print("ID:", hex(cn._window_id))

    time.sleep(100)
    cn.close()
