from display_render.render.x11 import connection as x11_render

class sysrlcls:
    def __init__(
        self,
        size: list | tuple=(150, 200),  # Size format: (n,n)= (100,200)= (x,y)
        terminal: bool= False,  # Toggle terminal
        windowed: bool= True,    # Toggle Windowed mode on the application/terminal
        resizable: bool= True # Toggle window Resizable mode

    ) -> None:

        global main_self

        self._math_emulation: object = None

        # Rendering status (not updated every time)
        # Status codes: 0 idle, 1 working, 2 warning, 3 error, 4 code crashed
        self._status = 0

        if len(size) > 2 and type(size) == list and type(size) == tuple:
            self._status = 2
            print(f"Warning: loading window_size, Expected: 2 elements got: {len(size)} elements instead")
        elif type(size) == list or type(size) == tuple: # Check the screen size
            self.window_size = size
        else:
            self._status = 2
            print(f"Warning: loading window_size, Expected: (value, value) Got: {size}")
            self.window_size = (150, 200)

        # This code leaves these vars whitout any check because this will work anyway
        self.terminal = terminal
        self.windowed = windowed
        self.resizable = resizable

        # Main class self
        main_self = self

        # Let's connect the x11 server to the code to render things
        self.x11 = x11_render()
        self.x11.connect()

        #self.x11.close()


    def render(
        self,
        cli: bool = False,
        math_emulation: object = None
    ) -> None:

        self._math_emulation = math_emulation(
            render=self
            )

        try: # Start the rendering process
            self._status = 1
            self.x11.create_window(size=self.window_size)

            self.x11.create_gc()
            self.x11.show_window()

            # Go read README.md for some code snippets

            while True:
                pass
        except Exception as e: # Give an error if something wrong with the rendering process
            self._status = 3
            print(f"Error loading")
        finally: # Finish the rendering process with a message
            self._status = 0
            print(f"Process finished: {self._status} {self.status().type}")


    class status:
        def __init__(self) -> None:

            self.code = 3
            self.type = "error"

            # Let's load the status data
            self.status()

        def status(self) -> dict:
            status_code = main_self._status

            status_type = None

            # Check every possible code state
            if status_code == 0:
                status_type = "idle"
            elif status_code == 1:
                status_type = "working"
            elif status_code == 2:
                status_type = "warning"
            elif status_code == 3:
                status_type = "error"
            elif status_code == 4:
                status_type = "code crashed"

            # If the status_code is not recognized the code gives an error
            if not status_type:
                print("Error: loading service status")
                status_type = "error"
                self.status, status_code = 3, 3

            # Update the code, type vars
            self.code, self.type = status_code, status_type

            return {"code": status_code, "type": status_type}

