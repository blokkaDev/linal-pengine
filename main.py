from display_render.render import sysrlcls as Render
import math_emulator as Math
import platform

# So I'm gonna start with this code my game engine project
# The most of these features are not implemented yet but I'm gonna add them later (I wan't to print a 3d block first)
# This is made 100% from scratch whitout using external libraries so I spent really a long time to make it work

engine = Math.emulate(
    os=(platform.system(), platform.release())
    )

app = Render(
    size=(750,500),
    terminal=True,
    windowed=True,
    resizable=False
    )

status = app.status()

print(f"System state: {status.type} With code: {status.code}")

app.render(
    cli=True,
    math_emulation=engine.render,
    )
