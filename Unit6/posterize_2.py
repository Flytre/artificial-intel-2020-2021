import random
import sys
import urllib.request
import io
from PIL import Image

k = 16


def naive_posterize(pix, img):
    colors = 2
    val = 256 // colors
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            tup = pix[i, j]
            pix[i, j] = (tup[0] // val * val, tup[1] // val * val, tup[2] // val * val)


def choose_rand_pixels(img, pix, ct):
    size = img.size
    result = list()
    while len(result) < ct:
        result.append(pix[random.randint(0, size[0] - 1), random.randint(0, size[1] - 1)])
    return result


def image_data_structures(img):
    pix = img.load()
    d = dict()
    s = set()
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            tup = pix[i, j]
            s.add(tup)
            if tup not in d:
                d[tup] = 1
            else:
                d[tup] = d[tup] + 1
    return s, d


def associate_means(img_set, means):
    result = dict()
    for mean in means:
        result[mean] = set()
    for pix in img_set:
        smallest_mean = smallest_squared_error(pix, means)
        result[smallest_mean].add(pix)
    return result


def associate_means_prev(previous: dict, means):
    result = dict()
    count = 0
    for mean in means:
        result[mean] = set()
    for key in previous:
        for pix in previous[key]:
            smallest_mean = smallest_squared_error(pix, means)
            if smallest_mean != key:
                count += 1
            result[smallest_mean].add(pix)
    return result, count


def smallest_squared_error(pixel, means):
    means.sort(key=lambda mean: squared_error(pixel, mean))
    return means[0]


def squared_error(color, color2):
    return (color2[0] - color[0]) ** 2 + (color2[1] - color[1]) ** 2 + (color2[2] - color[2]) ** 2


def average_pix(associated_pixels: set, img_dict: dict):
    num_red, num_green, num_blue, den = 0, 0, 0, 0
    for pixel in associated_pixels:
        num_red += pixel[0] * img_dict[pixel]
        num_green += pixel[1] * img_dict[pixel]
        num_blue += pixel[2] * img_dict[pixel]
        den += img_dict[pixel]
    return (int(num_red // den), int(num_green // den), int(num_blue // den)) if den > 0 else (0, 0, 0)


def posterize(img, pix, means):
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            tup = pix[i, j]
            pix[i, j] = smallest_squared_error(tup, means)


# URL = "https://lh4.googleusercontent.com/Xjbs-bBIxrBCYqLgIOt87ocmjiLB5JGzDy-mdxDlcZD0MdMfn9JGeRMOULWAxwQ7XctlLSvqxBunGviXkWgaQYatHB7KL8P246w78efDvqS8leWqhYMgH8ZDgYaDJDW_PQ=w1280"
# f = io.BytesIO(urllib.request.urlopen(URL).read())  # Download the picture at the url as a file object
img = Image.open(
    "icon.png")  # You can also use this on a local file; just put the local filename in quotes in place of f.
img_set, img_dict = image_data_structures(img)
means = choose_rand_pixels(img, img.load(), k)
previous_associated = None
pix = img.load()
while True:
    associated, count = None, 0
    if previous_associated is None:
        associated, count = associate_means(img_set, means), 0
    else:
        associated, count = associate_means_prev(previous_associated, means)
    new_means = list()
    for mean in means:
        new_means.append(average_pix(associated[mean], img_dict))
    if len(set(new_means)) < k:
        new_means = list(set(new_means))
        new_means.append(pix[random.randint(0, img.size[0] - 1), random.randint(0, img.size[1] - 1)])
    if set(new_means) == set(means) and count == 0:
        break
    means = new_means
    previous_associated = associated

posterize(img, pix, means)
img.save("kmeansout.png")
