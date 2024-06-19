import tkinter.font as tkfont
import tkinter as tk

class imageLabel:
    '''Class to create the label that goes with an image.'''

    def __init__(self, canvas, root, screen_dims, photo_item):
        self.font = tkfont.Font(family = 'Arial Rounded MT Bold', size = 22, weight='normal')
        SCREEN_RATIO_MAX = .4               # Constant to determine max size of label
        CIRCLE_DIAMETER = 100

        #TODO: Need to truncate text if going to wide in label
        #                    self.font.measure(photo_item.location),
        #                    self.font.measure(photo_item.date),
        #                    self.font.measure(photo_item.people)))
        l_width = SCREEN_RATIO_MAX * screen_dims['x'] + 40

        self.l_circle = canvas.create_oval(screen_dims['x'] - (l_width + 20 + CIRCLE_DIAMETER),
                                      screen_dims['y'] - (40 + CIRCLE_DIAMETER),
                                      screen_dims['x'] - (l_width + 20),
                                      screen_dims['y'] - 40,
                                      fill='#FFFFFF')
        self.r_circle = canvas.create_oval(screen_dims['x'] - (20 + CIRCLE_DIAMETER),
                                      screen_dims['y'] - (40 + CIRCLE_DIAMETER),
                                      screen_dims['x'] - 20,
                                      screen_dims['y'] - 40,
                                      fill='#FFFFFF')
        self.c_box = canvas.create_rectangle(screen_dims['x'] - (l_width + 20 + .5 * CIRCLE_DIAMETER),
                                        screen_dims['y'] - (40 + CIRCLE_DIAMETER),
                                        screen_dims['x'] - (20 + .5 * CIRCLE_DIAMETER),
                                        screen_dims['y'] - 40,
                                        fill='#FFFFFF')
        self.label = tk.Label(root,
                              text=f'Place: {photo_item.location}\nDate: {photo_item.date},'+
                                   f' 2024\nPeople: {photo_item.people}',
                              bg = '#ffffff',
                              fg = '#000000',
                              font = self.font)
        self.label.place(x = screen_dims['x'] - (.5 * l_width + 20 + .5 * CIRCLE_DIAMETER),
                         y = screen_dims['y'] - (40 + CIRCLE_DIAMETER * .5),
                         anchor = 'center')

        root.update()
        print("Label Width: ", self.label.winfo_width())

    def destroy_self(self, canvas):
        canvas.delete(self.l_circle)
        canvas.delete(self.r_circle)
        canvas.delete(self.c_box)
        self.label.destroy()
