from PIL import Image

def brightness_alignment(img1, img2):
    img1_pixels = list(img1.getdata())
    img1_mean_brightness = sum(pixel[0] + pixel[1] + pixel[2] for pixel in img1_pixels) / (len(img1_pixels) * 3)
    img2_pixels = list(img2.getdata())
    img2_mean_brightness = sum(pixel[0] + pixel[1] + pixel[2] for pixel in img2_pixels) / (len(img2_pixels) * 3)

    brightness_difference = abs(img1_mean_brightness - img2_mean_brightness) / 2
    if img1_mean_brightness > img2_mean_brightness:
        new_img1_pixels = [(
            max(0, int(pixel[0] - brightness_difference)),
            max(0, int(pixel[1] - brightness_difference)),
            max(0, int(pixel[2] - brightness_difference))) for pixel in img1_pixels]
        new_img2_pixels = [(min(255, int(pixel[0] + brightness_difference)),
                            min(255, int(pixel[1] + brightness_difference)),
                            min(255, int(pixel[2] + brightness_difference))) for pixel in img2_pixels]
    else:
        new_img1_pixels = [(
            min(255, int(pixel[0] + brightness_difference)),
            min(255, int(pixel[1] + brightness_difference)),
            min(255, int(pixel[2] + brightness_difference))) \
            for pixel in img1_pixels]
        new_img2_pixels = [(
            max(0, int(pixel[0] - brightness_difference)),
            max(0, int(pixel[1] - brightness_difference)),
            max(0, int(pixel[2] - brightness_difference))) \
            for pixel in img2_pixels]
    new_img1 = Image.new('RGB', img1.size)
    new_img2 = Image.new('RGB', img2.size)
    new_img1.putdata(new_img1_pixels)
    new_img2.putdata(new_img2_pixels)
    return new_img1, new_img2

def open_images(img1_path: str, img2_path: str):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    new_img1, new_img2 = brightness_alignment(img1, img2)
    new_img1.save('result1.jpg')
    new_img2.save('result2.jpg')


if __name__ == "__main__":
    open_images('data/1.jpg', 'data/2.jpg')