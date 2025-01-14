import tkinter as tk


class SimulationGUI:
    def __init__(self, field, canvas_width=800, canvas_height=600):
        self.field = field
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.cell_width = canvas_width / field.size[0]
        self.cell_height = canvas_height / field.size[1]
        self.update_interval = 0.5  # Default update interval in seconds

        # Initialize the root window and canvas
        self.root = tk.Tk()
        self.root.title("Stink Bug Simulator")
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        # Add slider to control the update interval
        self.slider = tk.Scale(self.root, from_=0.1, to=2.0, resolution=0.1,
                               orient=tk.HORIZONTAL, label="Update Speed (seconds)")
        self.slider.set(self.update_interval)
        self.slider.pack()

    def draw_field(self):
        self.canvas.delete("all")
        # Draw field border
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, outline="black")

    def update(self, bugs, pesticides):
        # Clear the canvas and redraw the field
        self.draw_field()

        # Draw trees
        for tree in self.field.trees:
            x, y = self._scale_position(tree.position)
            self._draw_circle(x, y, 10, "green")

        # Draw fruits
        for fruit in self.field.get_fruits():
            x, y = self._scale_position(fruit.position)
            if not fruit.is_eaten:
                color = "yellow" if fruit.is_ripe else "orange"
                self._draw_circle(x, y, 5, color)

        # Draw bugs
        for bug in bugs:
            if bug.alive:
                x, y = self._scale_position(bug.position)
                self._draw_circle(x, y, 5, "brown")

        # Draw pesticides
        for pesticide in pesticides:
            x, y = self._scale_position(pesticide.repulsion_force)
            self._draw_circle(x, y, 10, "purple")

        self.root.update()

    def _scale_position(self, position):
        """Convert real-world coordinates to canvas coordinates."""
        x = position[0] * self.cell_width
        y = position[1] * self.cell_height
        return x, y

    def _draw_circle(self, x, y, radius, color):
        """Draw a circle centered at (x, y) with the given radius and color."""
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color, outline="black"
        )

    def get_update_interval(self):
        """Retrieve the current update interval from the slider."""
        return self.slider.get()

    def run(self):
        self.root.mainloop()
