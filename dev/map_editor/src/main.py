import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# Constants
ROWS, COLS = 12, 16
TILE_SIZE = 40

GRASS = 0
PATH = 1

COLORS = {
    GRASS: "green",
    PATH: "tan"
}

MAP_LAYOUT = [[GRASS for _ in range(COLS)] for _ in range(ROWS)]
MAP_DIR = "assets/maps"

class MapEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Map Editor")
        self.geometry(f"{COLS*TILE_SIZE}x{ROWS*TILE_SIZE}")

        self.canvas = tk.Canvas(self, width=COLS*TILE_SIZE, height=ROWS*TILE_SIZE, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.bind("<Control-s>", self.save_map)
        self.bind("<Control-l>", self.load_map)

        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                x1, y1 = col*TILE_SIZE, row*TILE_SIZE
                x2, y2 = x1+TILE_SIZE, y1+TILE_SIZE
                tile_type = MAP_LAYOUT[row][col]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS[tile_type], outline="black")

    def on_click(self, event):
        col = event.x // TILE_SIZE
        row = event.y // TILE_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            MAP_LAYOUT[row][col] = PATH if MAP_LAYOUT[row][col] == GRASS else GRASS
            self.draw_map()

    def save_map(self, event=None):
        os.makedirs(MAP_DIR, exist_ok=True)
        map_name = simpledialog.askstring("Save Map", "Enter map name:")
        if not map_name:
            return
        filename = os.path.join(MAP_DIR, f"{map_name}.json")
        if os.path.exists(filename):
            if not messagebox.askyesno("Overwrite?", f"Map '{map_name}' already exists. Overwrite?"):
                return

        # Build pretty JSON with single-line rows for layout
        meta = {
            "rows": ROWS,
            "cols": COLS,
            "tile_size": TILE_SIZE,
            "legend": {"GRASS": GRASS, "PATH": PATH}
        }
        meta_str = json.dumps(meta, indent=4, separators=(",", ": "))

        # Manually format layout rows
        layout_lines = []
        for r in MAP_LAYOUT:
            row_str = "[{}]".format(",".join(str(v) for v in r))
            layout_lines.append("        " + row_str)  # 8 spaces to align with indent=4 in object

        json_text = (
            "{\n"
            + meta_str[1:-1]  # strip outer braces of meta to merge
            + ",\n"
            + '    "layout": [\n'
            + ",\n".join(layout_lines)
            + "\n    ]\n"
            + "}"
        )

        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_text)

        messagebox.showinfo("Saved", f"Map saved to {filename}")

    def load_map(self, event=None):
        map_name = simpledialog.askstring("Load Map", "Enter map name:")
        if not map_name:
            return
        filename = os.path.join(MAP_DIR, f"{map_name}.json")
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"No map found with name '{map_name}'.")
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            layout = data.get("layout")
            if layout and len(layout) == ROWS and all(len(row) == COLS for row in layout):
                global MAP_LAYOUT
                MAP_LAYOUT = layout
                self.draw_map()
                messagebox.showinfo("Loaded", f"Map loaded from {filename}")
            else:
                messagebox.showerror("Error", "Invalid map file format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {e}")

if __name__ == "__main__":
    app = MapEditor()
    app.mainloop()
