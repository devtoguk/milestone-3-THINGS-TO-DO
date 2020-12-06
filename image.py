from PIL import Image


def resize_image(image_file):
    image_folder = 'static/images/activities/'
    image = Image.open(image_folder + image_file)
    final_width = 286 * 2
    final_height = 214 * 2

    print(f'Image format: {image.format}')
    print(f'Image mode: {image.mode}')

    if image.mode != 'RGB':
        image = image.convert('RGB')

    print(f'Original image size: {image.size}')

    image_width = image.size[0]
    image_height = image.size[1]

    offset_x = 0
    offset_y = 0

    if image_width > image_height:
        print('Image wider')
        scale_factor = final_height / image_height
        scaled_height = final_height
        scaled_width = int(image_width * scale_factor)
        offset_x = ((scaled_width - final_width) / 2) - 4
    else:
        print('Image taller')
        scale_factor = final_width / image_width
        scaled_width = final_width
        scaled_height = int(image_height * scale_factor)
        offset_y = ((scaled_height - final_height) / 2) - 4

    print(f'Scaled Width: {scaled_width}')
    print(f'Scaled Height: {scaled_height}')
    print(f'Offset X is: {offset_x}')
    print(f'Offset Y is: {offset_y}')

    box = (offset_x, offset_y, (final_width + offset_x), final_height + offset_y)

    new_image = image.resize((scaled_width, scaled_height)).crop(box)

    # new_image = new_image.crop(box)

    new_image.save(image_folder + image_file, 'JPEG')

    print(f'Final Width: {new_image.size[0]}')
    print(f'Final Height: {new_image.size[1]}')
    print(f'Scale Factor used: {scale_factor}')
