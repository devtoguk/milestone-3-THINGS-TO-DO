from PIL import Image


def resize_image(image_file):
    """Crop & resize image then save in temporary image folder

    :param image_file: string - image filename without path
    """
    image_folder = 'static/images/activities/'
    image = Image.open(image_folder + image_file)
    final_width = 286 * 2
    final_height = 214 * 2

    if image.mode != 'RGB':
        image = image.convert('RGB')

    image_width = image.size[0]
    image_height = image.size[1]

    offset_x = offset_y = 0

    if image_width > image_height:
        scale_factor = final_height / image_height
        scaled_height = final_height
        scaled_width = int(image_width * scale_factor)
        offset_x = ((scaled_width - final_width) / 2)
    else:
        scale_factor = final_width / image_width
        scaled_width = final_width
        scaled_height = int(image_height * scale_factor)
        offset_y = ((scaled_height - final_height) / 2)

    box = (offset_x, offset_y, (final_width + offset_x), final_height + offset_y)

    new_image = image.resize((scaled_width, scaled_height)).crop(box)
    new_image.save(image_folder + image_file, 'JPEG')
