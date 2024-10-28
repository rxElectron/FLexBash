import ttkbootstrap as tb
import random
from gui import BashCommandParserApp

if __name__ == "__main__":
    themes = ["darkly", "solar", "superhero", "cyborg", "vapor", "litera", "cosmo", "flatly", "journal", "minty"]
    root = tb.Window(themename=random.choice(themes))

    # Set initial size correctly before starting the app
    root.geometry("1425x760+200+100")
    root.update_idletasks()

    app = BashCommandParserApp(root)
    root.mainloop()
