# Linal-Pengine (LP-graphics)
linal-pengine meaning: linear algebra (math) python game engine

## Some code snippets v0.0.1
### Center and smaller cube every time

```python
x = 100
y = 100
side = 215

change = 4

while side > 0:
    self._math_emulation.draw(
        coo=self._math_emulation.square(
            coo=(x, y),
            side=side
            )
        )

    x += change
    y += change
    side -= change*2
```

### Diagonal walking objects
```python
x = 100
y = 100
side = 215

step_blocks = 20

while True:
    self._math_emulation.draw(
            coo=self._math_emulation.square(
                coo=(x, y),
                side=side
                )
        )
    self.x11.clear_window()

    y += step_blocks
    x -= step_blocks
    side += int(step_blocks/2)
```
