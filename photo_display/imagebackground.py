from PIL import ImageTk

class imageBackground:
    def __init__(self, image, canvas, root):
        new_dims = self.get_photo_dims(root, image)
        image = image.resize((new_dims['x'], new_dims['y']))

        self.bk_img = ImageTk.PhotoImage(image)
        canvas.create_image(root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2, image=self.bk_img)

    def get_photo_dims(self, root, image):
        '''
        Simple method to appropriate size the image to the screen and keep the ratio.
        :param root:
        :param image:
        :return:
        '''
        min_ratio = min(image.width / root.winfo_screenwidth(), image.height / root.winfo_screenheight())
        new_dims = {
            'x': int(image.width / min_ratio),
            'y': int(image.height / min_ratio)
        }
        return new_dims
