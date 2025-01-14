class Fruit:
    def __init__(self, id, position, ripeness=0):
        self.id = id
        self.position = position  # (x, y)
        self.ripeness = ripeness  # 0 to 100
        self.is_ripe = ripeness >= 50
        self.is_eaten = False

    def ripen(self):
        if not self.is_eaten:
            self.ripeness += 1
            if self.ripeness >= 50:
                self.is_ripe = True

    def degrade(self):
        if self.is_ripe:
            self.is_eaten = True