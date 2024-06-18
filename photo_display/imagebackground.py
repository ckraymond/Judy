from PIL import ImageTk

class imageBackground:
    def __init__(self, image, canvas, root, screen_dims):
        new_dims = self.get_photo_dims(root, image, screen_dims)
        image = image.resize((new_dims['x'], new_dims['y']))

        self.bk_img = ImageTk.PhotoImage(image)
        canvas.create_image(screen_dims['x'] / 2, screen_dims['y'] / 2, image=self.bk_img)

    def get_photo_dims(self, root, image, screen_dims):
        '''
        Simple method to appropriate size the image to the screen and keep the ratio.
        :param root:
        :param image:
        :return:
        '''
        max_ratio = max(image.width / screen_dims['x'], image.height / screen_dims['y'])

        new_dims = {
            'x': int(image.width / max_ratio),
            'y': int(image.height / max_ratio)
        }

        return new_dims
