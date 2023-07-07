from PIL import Image
import os

def op_g():
    with Image.open('girl.gif') as im:
        im.seek(0)
        i = 0
        try:
            while True:
                im.seek(im.tell() + 1)
                i += 1
                im.save("gframes/{}.png".format(i))
        except EOFError:
            pass
def _togif(speedup_factor=1):
    directory = 'gframes'
    image_path_list = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.png')]
    image_path_list = sorted(image_path_list)
    image_list = [Image.open(file) for file in image_path_list]
    new_duration = int(250 / speedup_factor)#скорость анимации gif
    image_list[0].save(
        'res.gif',
        save_all=True,
        append_images=image_list[1:],
        duration=new_duration,
        loop=0)



op_g()
_togif(speedup_factor=2)
