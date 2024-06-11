import tkinter              # Careful as this can only be called once

class photoItem:

    def __init__(self, image = '', date = '', location = '', people = ''):
        self.image = image                      # URL for where image is on Bubble CDN
        self.date = date                        # Datetime in str format of the date taken
        self.location = location                # Where the photo taken
        self.people = people                    # People in the photo

    def __str__(self):
        return f'{self.image} | {self.date} | {self.location} | {self.people}'

    def display(self):
        root = tkinter.Tk()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        root.focus_set()
        canvas = tkinter.Canvas(root, width=w, height=h)
        canvas.pack()
        canvas.configure(background='black')

        imgWidth, imgHeight = pilImage.size
        # resize photo to full screen
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)
        imagesprite = canvas.create_image(w / 2, h / 2, image=image)
        root.update_idletasks()
        root.update()
    #    root.bind("<Esc
