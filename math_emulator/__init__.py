class emulate:
    def __init__(self, os: tuple=("Linux", "7.2.2-arch1-1")) -> None:
        pass

    class render:
        def __init__(
            self,
            render: object = None
        ) -> None:
            self.__render = render

        def draw(
            self,
            coo: list = [((50, 50), (300, 200))]
        ) -> None:
            render = self.__render
            for i in coo:
                render.x11.draw_line(coo=i)

        def square(
            self,
            coo: tuple=(100,100), #x,y position
            side: int = 200

        ) -> list:
            x = coo[0]
            y = coo[1]

            return {
                ((x, y), (x + side, y)),
                ((x + side, y), (x + side, y + side)),
                ((x + side, y + side), (x, y + side)),
                ((x, y + side), (x, y))

                }
