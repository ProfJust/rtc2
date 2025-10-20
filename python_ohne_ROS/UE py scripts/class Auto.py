class Auto:
    def __init__(self, farbe, geschwindigkeit):
        self.farbe = farbe
        self.geschwindigkeit = geschwindigkeit

    def fahren(self):
        print(f"Das {self.farbe} Auto fährt {self.geschwindigkeit} km/h.")


if __name__ == "__main__":
    a1 = Auto("rot", 120)
    a2 = Auto("blau", 180)

    a1.fahren()  # → Das rot Auto fährt 120 km/h.
    a2.fahren()  # → Das blau Auto fährt 180 km/h