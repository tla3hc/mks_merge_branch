import tkinter as tk
from models.app_model import AppModel
from views.app_view import AppView
from controllers.app_controller import AppController
from utils.log import Logger

def main():
    logger = Logger()
    root = tk.Tk()

    # Initialize the MVC components
    model = AppModel()
    view = AppView(root)
    controller = AppController(model, view)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
