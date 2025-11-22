import os
import tkinter as tk
from tkinter import simpledialog, messagebox, colorchooser, filedialog
from PIL import Image, ImageTk

SCALE = 10

class TextureEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Texture Editor")

        # Base folders
        self.base_input = "assets/textures"
        self.base_output = "assets/generated"

        os.makedirs(self.base_input, exist_ok=True)
        os.makedirs(self.base_output, exist_ok=True)

        # State
        self.current_color = "#000000"
        self.tool = "brush"

        # Images (backing pixel data)
        self.main_img = Image.new("RGBA", (32, 32), (255, 255, 255, 0))
        self.edge_img = Image.new("RGBA", (32, 6), (255, 255, 255, 0))
        self.corner_img = Image.new("RGBA", (6, 6), (255, 255, 255, 0))

        # UI layout
        self.build_toolbar()
        self.build_palette()
        self.build_canvases()
        self.build_preview_panel()


    def build_toolbar(self):
        bar = tk.Frame(self.root)
        bar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(bar, text="Brush", command=lambda: self.set_tool("brush")).pack(side=tk.LEFT)
        tk.Button(bar, text="Eraser", command=lambda: self.set_tool("eraser")).pack(side=tk.LEFT)
        tk.Button(bar, text="Fill", command=lambda: self.set_tool("fill")).pack(side=tk.LEFT)
        tk.Button(bar, text="Choose RGB", command=self.choose_rgb).pack(side=tk.LEFT, padx=6)

        # Current color indicator
        tk.Label(bar, text="Current:").pack(side=tk.LEFT, padx=(12, 2))
        self.current_color_view = tk.Canvas(bar, width=24, height=16, bg=self.current_color, highlightthickness=1, highlightbackground="black")
        self.current_color_view.pack(side=tk.LEFT)

        # Save button
        tk.Button(bar, text="Save", command=self.save_textures).pack(side=tk.RIGHT)
        tk.Button(bar, text="Load", command=self.load_textures).pack(side=tk.RIGHT)

    def choose_rgb(self):
        # Open color chooser dialog
        color = colorchooser.askcolor(title="Pick a color")
        if color and color[1]:  # color[1] is the hex string
            self.set_color(color[1])

    def build_palette(self):
        palette = tk.Frame(self.root)
        palette.pack(side=tk.TOP, fill=tk.X)

        colors = [
            "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF", "#808080", "#A0522D",
            "#8B0000", "#006400", "#00008B", "#FFD700", "#FF69B4",
            "#40E0D0", "#C0C0C0", "#7FFFD4", "#9932CC", "#FFA500"
        ]

        for c in colors:
            sw = tk.Canvas(palette, width=24, height=24, bg=c, highlightthickness=1, highlightbackground="black")
            sw.pack(side=tk.LEFT, padx=2, pady=4)
            sw.bind("<Button-1>", lambda e, col=c: self.set_color(col))

    def build_canvases(self):
        left = tk.Frame(self.root)
        left.pack(side=tk.LEFT, padx=10, pady=10)

        # Main (32x32)
        self.main_canvas = self.make_canvas(left, 32, 32, "Main (32x32)")

        # Edge (32x6)
        self.edge_canvas = self.make_canvas(left, 32, 6, "Edge (32x6)")

        # Corner (6x6)
        self.corner_canvas = self.make_canvas(left, 6, 6, "Corner (6x6)")

        # Draw transparent checker background on each canvas
        self.draw_checker(self.main_canvas, 32, 32)
        self.draw_checker(self.edge_canvas, 32, 6)
        self.draw_checker(self.corner_canvas, 6, 6)

    def build_preview_panel(self):
        right = tk.Frame(self.root)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(right, text="Tile previews (TRBL bitmask)").pack(pady=(0, 8))

        # 4x4 grid of previews
        grid = tk.Frame(right)
        grid.pack()

        self.preview_canvases = []
        for row in range(4):
            rframe = tk.Frame(grid)
            rframe.pack()
            for col in range(4):
                idx = row * 4 + col
                c = tk.Canvas(rframe, width=32, height=32, bg="#c0c0c0", highlightthickness=1, highlightbackground="black")
                c.pack(side=tk.LEFT, padx=4, pady=4)
                self.preview_canvases.append(c)

        self.preview_images = [None] * 16

    def make_canvas(self, parent, w, h, label):
        frame = tk.Frame(parent)
        frame.pack(pady=6)

        tk.Label(frame, text=label).pack()
        canvas = tk.Canvas(frame, width=w * SCALE, height=h * SCALE, bg="white", highlightthickness=1, highlightbackground="black")
        canvas.pack()

        # Bind interactions
        canvas.bind("<B1-Motion>", lambda e, c=canvas, W=w, H=h: self.paint_drag(e, c, W, H))
        canvas.bind("<Button-1>",  lambda e, c=canvas, W=w, H=h: self.paint_click(e, c, W, H))

        return canvas

    def draw_checker(self, canvas, w, h, cell=2):
        # Draw a checkerboard to visualize transparency (light/dark)
        for y in range(h):
            for x in range(w):
                if ((x // cell) + (y // cell)) % 2 == 0:
                    color = "#eeeeee"
                else:
                    color = "#dddddd"
                canvas.create_rectangle(x*SCALE, y*SCALE, (x+1)*SCALE, (y+1)*SCALE, fill=color, outline=color)


    def set_color(self, color):
        self.current_color = color
        self.current_color_view.configure(bg=color)

    def set_tool(self, tool):
        self.tool = tool

    def paint_drag(self, event, canvas, w, h):
        if self.tool not in ("brush", "eraser"):
            return
        x, y = int(event.x / SCALE), int(event.y / SCALE)
        if not (0 <= x < w and 0 <= y < h):
            return

        fill = self.current_color if self.tool == "brush" else "white"
        canvas.create_rectangle(x*SCALE, y*SCALE, (x+1)*SCALE, (y+1)*SCALE, fill=fill, outline="")
        self.putpixel(w, h, x, y, fill)

    def paint_click(self, event, canvas, w, h):
        x, y = int(event.x / SCALE), int(event.y / SCALE)
        if not (0 <= x < w and 0 <= y < h):
            return

        if self.tool == "fill":
            self.flood_fill(canvas, w, h, x, y)
        elif self.tool in ("brush", "eraser"):
            fill = self.current_color if self.tool == "brush" else "white"
            canvas.create_rectangle(x*SCALE, y*SCALE, (x+1)*SCALE, (y+1)*SCALE, fill=fill, outline="")
            self.putpixel(w, h, x, y, fill)

    def get_image(self, w, h):
        if (w, h) == (32, 32):
            return self.main_img
        elif (w, h) == (32, 6):
            return self.edge_img
        elif (w, h) == (6, 6):
            return self.corner_img
        else:
            raise ValueError("Unknown image size")

    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:  # short form #rgb
            hex_color = "".join([c*2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, 255)

    def putpixel(self, w, h, x, y, fill_hex):
        img = self.get_image(w, h)
        img.putpixel((x, y), self.hex_to_rgba(fill_hex))
        self.generate_previews()

    def flood_fill(self, canvas, w, h, x, y):
        img = self.get_image(w, h)
        pixels = img.load()
        target = pixels[x, y]
        new_color = self.hex_to_rgba(self.current_color)
        if target == new_color:
            return

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < w and 0 <= cy < h):
                continue
            if pixels[cx, cy] == target:
                pixels[cx, cy] = new_color
                canvas.create_rectangle(cx*SCALE, cy*SCALE, (cx+1)*SCALE, (cy+1)*SCALE,
                                        fill=self.current_color, outline="")
                stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])
        self.generate_previews()

    def save_textures(self):
        tile_name = simpledialog.askstring("Save Tile", "Enter tile name:")
        if not tile_name:
            return

        input_path = os.path.join(self.base_input, tile_name)
        output_path = os.path.join(self.base_output, tile_name)

        if os.path.exists(input_path):
            overwrite = messagebox.askyesno("Overwrite?", f"Tile '{tile_name}' already exists. Overwrite?")
            if not overwrite:
                return

        os.makedirs(input_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)

        # Save base textures
        self.main_img.save(os.path.join(input_path, "main.bmp"))
        self.edge_img.save(os.path.join(input_path, "edges.bmp"))
        self.corner_img.save(os.path.join(input_path, "corners.bmp"))

        # Generate live previews 
        self.generate_previews()

        messagebox.showinfo("Saved", f"Tile '{tile_name}' saved and previews updated.")

    def load_textures(self):
        folder = filedialog.askdirectory(title="Select texture folder")
        if not folder:
            return

        try:
            main_path = os.path.join(folder, "main.bmp")
            edge_path = os.path.join(folder, "edges.bmp")
            corner_path = os.path.join(folder, "corners.bmp")

            if os.path.exists(main_path):
                self.main_img = Image.open(main_path).convert("RGBA")
            if os.path.exists(edge_path):
                self.edge_img = Image.open(edge_path).convert("RGBA")
            if os.path.exists(corner_path):
                self.corner_img = Image.open(corner_path).convert("RGBA")

            self.refresh_canvas(self.main_canvas, self.main_img, 32, 32)
            self.refresh_canvas(self.edge_canvas, self.edge_img, 32, 6)
            self.refresh_canvas(self.corner_canvas, self.corner_img, 6, 6)

            self.generate_previews()

            messagebox.showinfo("Loaded", f"Textures loaded from {folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load textures:\n{e}")

    def refresh_canvas(self, canvas, img, w, h):
        canvas.delete("all")
        self.draw_checker(canvas, w, h)
        pixels = img.load()
        for y in range(h):
            for x in range(w):
                r, g, b, a = pixels[x, y]
                if a > 0:  # only draw non‑transparent
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    canvas.create_rectangle(x*SCALE, y*SCALE, (x+1)*SCALE, (y+1)*SCALE,
                                            fill=hex_color, outline="")

    def generate_previews(self):
        for mask in range(16):
            tile = self.generate_tile(mask)

            # Show in preview canvas
            img_tk = ImageTk.PhotoImage(tile)
            self.preview_images[mask] = img_tk  # keep ref
            pc = self.preview_canvases[mask]
            pc.delete("all")
            pc.create_image(0, 0, anchor="nw", image=img_tk)

    def generate_tile(self, mask):
        """
        Build a single 32x32 tile from base images according to TRBL bitmask.
        Bit order: Top(3), Right(2), Bottom(1), Left(0).
        """
        tile = self.main_img.copy()
        width, height = tile.size  # 32, 32

        # Decode mask
        top, right, bottom, left = [(mask >> i) & 1 for i in (3, 2, 1, 0)]

        if top:
            tile.paste(self.edge_img, (0, 0))
        if bottom:
            tile.paste(self.edge_img, (0, height - 6))
        if left:
            left_edge = self.edge_img.rotate(90, expand=True)  # 6x32
            tile.paste(left_edge, (0, 0))
        if right:
            right_edge = self.edge_img.rotate(90, expand=True)  # 6x32
            tile.paste(right_edge, (width - 6, 0))

        # Corners (corner_img is 6x6)
        if top and left:
            tile.paste(self.corner_img, (0, 0))
        if top and right:
            tile.paste(self.corner_img, (width - 6, 0))
        if bottom and left:
            tile.paste(self.corner_img, (0, height - 6))
        if bottom and right:
            tile.paste(self.corner_img, (width - 6, height - 6))

        return tile

if __name__ == "__main__":
    root = tk.Tk()
    app = TextureEditor(root)
    root.mainloop()
