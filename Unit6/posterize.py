import random
import urllib.request
import io
from PIL import Image
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

k = 27


def naive_posterize(pix, img):
    colors = 3
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


def associate_means(img, pix, means):
    cache = dict()
    result = dict()
    for mean in means:
        result[mean] = list()
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            if pix[i, j] in cache:
                result[cache[pix[i, j]]].append(pix[i, j])
            smallest_mean = smallest_squared_error(pix[i, j], means)
            cache[pix[i, j]] = smallest_mean
            result[smallest_mean].append(pix[i, j])
    return result


def avg_pix(pixels: list):
    red = sum([i[0] for i in pixels]) // len(pixels)
    grn = sum([i[1] for i in pixels]) // len(pixels)
    blu = sum([i[2] for i in pixels]) // len(pixels)
    return red, grn, blu


def smallest_squared_error(pixel, means):
    means.sort(key=lambda mean: squared_error(pixel, mean))
    return means[0]


squared_cache = dict()


def squared_error(color, color2):
    vals = color2[0] - color[0], color2[1] - color[1], color2[2] - color[2]
    if vals not in squared_cache:
        squared_cache[vals] = vals[0] * vals[0] + vals[1] * vals[1] + vals[2] * vals[2]
    return squared_cache[vals]


def posterize(img, pix, means):
    for i in range(0, img.size[0]):
        for j in range(0, img.size[1]):
            tup = pix[i, j]
            pix[i, j] = smallest_squared_error(tup, means)


# https://i.pinimg.com/originals/95/2a/04/952a04ea85a8d1b0134516c52198745e.jpg
# data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVFRgVEhISFRgYEhIYGBESEhIREhERGBgZGRgYGBgcIS4lHB4rHxgYJjgmKy8xNTU1GiQ7QDszPy40NTEBDAwMEA8QGhISGDQhISExMTQ0NDE0NDQxNDQxMTQxNDQ0MTQxNDE0MTQ0NDQ/NDQxNDQ/NDQ0MTQ0MTQxMT8xMf/AABEIAMIBAwMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAgMEBQYBBwj/xABBEAACAQIDAwgIAwYGAwEAAAAAAQIDEQQhMQUSQQYiMlFxc7GyBxM0YXKBkaFCYsEjUnSi0eEUM0NjgvAVkvEk/8QAGQEBAQEBAQEAAAAAAAAAAAAAAAECBAMF/8QAIREBAQEBAQACAwADAQAAAAAAAAECETEDIRIyQQQiQhP/2gAMAwEAAhEDEQA/APGQAAAAADT4Xh8i/wABwKHCLT5GgwC0PGunCJyt/wBH4avjTKSJdcrdaPw1PGBSUsxPDX7J+H2TXqRUqdGpNPjThKWfyIeOwlejLdq0qkLr8dOUfuz2jYdP1GFpQjrKmpyejTlml9ArwhUW5UhGcb33ZpNJ9a6jN3JW58Vs68Npzalfci/cSN+T/BFfoe/R2ZhqsN2WGoONs4qnBP5NK9zFYz0dT9c/USi6bzi5vOH5ZdZuXrz1mx5csNPWz+g9BzVtXb8Lzi/ke24H0f4eHTbm+rRLLQsqPIzBR/0Iyv8AvNsrPOPDYVpuPMjG1842fzs/+6Back3qpK17aSXRT7bHv8NgYWKssPSWf7kde05T2Hho33aFNb3SSgkpdqCvA9nRak1JNZaSTT0JM9Ue3YzYGGmmnSgskrpJNI815Xcnv8LNTjnTm7RebcWl0X9zNWMZt7oxL3kX/ly+IotudGJf8i/8t/H/AEN/8p/WwhouwkwIsPw9hMpnk2eiSKYxAepASLiOE+1L7C0NS6Mvjf2RirDKmKUyNvnHMK8s9KDvjF/D0/NMxpr/AElv/wDWu4p+MjIHVnyOXXtAABWQAAAAAAAAAGpwS0+RpMBDQpNnUr27EajAYfQ8tOjCg5X9Kj8NXxgU2DjdpdbS+rL7lxDdlR98a3jAp9jK9ektb1aat2yQk+jX3p7VjJ7tl1RivorEOFS4/td2lYqfW2epy3134z/pF/gcVus0OHxcWtbMxcK2ZLVd2yZ651x4/J8crWyxMeDQj1pm6OKzSbLGFZmuvH8OJ86w2qzZGnUyGoTZTibOrYqNtYWOIpypztmm4v8AcqLov6ncTWcU5N2S4spMBt+nUqOCmt1LKd1be6gcjy3lHQlB7lSLjKE2mvf7nxNByHpt0m7/AI3+hvNtcmsNjYx9cmmujUptRnbqfWsyLs7kjHDQ3aVSU1vXtOyln2ZFmv8AVjn2acbW4Za8CTTkh5wcVuyWfvGv8LCWjcH1xtb6PIxW7D0WP0mQJ4apHo7s+x7sv/V5P6keG1N2W7NWfVJbj++oRfxGW+Y/imN0cZB8bfIarYyEYqMppSalZcbt5Gapuxxo5TY9uiq8k9JXta7in4yMibD0mq2MXcU/GRjzqz5HLr2gAArIAAAAAAAAAD0fZeFyWXBGqwOG0Gtl7OtGOX4Y+Bo8NhLWMV74rzn0iQtLD/DX8aZS8mKLniqKSu/XU38lJNml9Kcd2eG+HEeNIk+ifZanUnXlmqasvjkvGw/hf2a3lHLdd+0yuJxVja7aoKalB5PVPqZ51tK8G4vVSsc/4y19DGuZXGDxV2k3rxLpTvHeWqyaMdgG5xy1i+x2LSGLmlu3eqzNzPGN66uqV5O980724MuKNS/9Chwsubn9btMuMKm7dfXxFeOk9N6WY7uZZIk4akrc7N+8dmkidZ6xnKDY2JxEJQVRQi7c2GTktbNvgee4PZOJw9VQqUakM7b0YucJJdUo5M9snIjTRZpParNkUmo3d9FqWFWTtzdROUSPXrZZGeqpp4qo61pxnGNnm1k2lwJEZZna+Iyzz7RhzyuU1rp6eKs7MVWownZSSmmr2kk0YXa/KiDg/UN7+8udKKso3zaT1NFye2i6tKE21vbu7K2S3otps1rFk6zLFtT2Ko505zh+R8+m/lLNfJorcXsqvv7+7TlFWcpescck7tpW6loaWNa0G8skFfG/sneKu6Tu0rZuJ5tKnDyJ0UVeEkWUGKjyX0o+2L+Hp+aRjTZelH2xfw9PzSMadWfI5r7QAAVkAAAAAAAAAB9LYDBcyHwR8EWMaFuBKwlLmQ7uHlQ7KB5WvePJvSrh5TrYSFODnOaxEYwirucnKlZJHoPI7YLweFjTnZzbc520U3wXYrL5FlR2fTlVjWlBSnCM4wk/wKe7vW973VmWM9C9+kv7dZvaSW9no/sZzaWzYSfPWdrb9tbaJmq2hRvcqasLrncFqvA8b9V1Y3Ga/wDDzU06S5jhzmtVNPPLih2eEtLPJ8ci5o0U5ayXUorO5I2nhr+rcU95y3NLXvnmJqtasVuFir268jS4DDRSvaxHobOhDd3udLi3p2WLNVIrLTThkOvHVEp2YSmIlOL0afYNzbXC/YRlypMg1a1hyeJ64Ne8qsbilcKkVMTcj1quRE9ZcYr4lJNvKyYVHxOKUc5ySSu7v3FBtLlDOUZqlGMI7rSlJXm1a2miE7bnKULvS9vuVUZqMJKyd1q9VxyLb9zjUzOdUEYS3FK3Nvu396Wn0NpyCqvcmnwqK3uvExrx091wUrQk7uCyi3lZ/Y1vIF82p8cfIjs+X9HPn9no2/8As5v8r8AxUOZLPJU3lxuojN/2cvfZfXIfxb5s/hn4M43sqMHLQtKbyKrCFpTYqR5P6T/bF/D0/NMxxsfSf7Yv4en5pmOOnPkc2vaAACsgAAAAAAAAAPrfC9CHdw8qFyEYV8yHdw8qFTPCveFUHqOykM0WFSQ/gYxMblPiaaWf/wALmq8iqxUzOmpXdnxja+TvxJO5FtN52vb3PrK7ByWa0zZJhO1zK2nWsx7LiRYzFTqhKXOlHVZPrQxNSXHeQ3KrLqI0qk+CB0rE1n1W95n8TBt3uW1eL1kV1ScephUR1Wk8v7kFxcm97jwGNt7ZhTVk1fq94rY+JdSEZv8AEr/c1J/Tqwlgozg4SV1Jf9aMvtXYk4QnKLjOMYN5O0kks7o2a0IuJipRlGV7OLT7GrPxJ/WpXkUom65DwtTb/eqP7JIrtpcnYq3qVJu+anLhwNJsjCqlGMFw1f5nr9zo38kueR5zNlaeGcEv9ymv5kSMR0ZfDLwZHoaQ99RfbP8AQer9GXwy8Dm62rcNHQsIEHDonQLaR5R6T/bF/D0/NMxxsfSf7Yu4p+aZjjpz5HNr2gAArIAAAAAAAAAD62wvQh3cPKhUmIwnQh3cPKhUjwr3hVHickFNhNgIlDIp8ZSzLWVYh1JpvQxViuhBpjrR2sxreIpW/Y5OtkMOoJ3kA68QclXGmkNTqRXEBNes3qZ3bmM9XHTW6v1FzXqZZGX5QUZVejlZaPi78BLJW851r9Ywu0Krk2+tm95OL9hT+BHn2LjZ27T0Lk6v2FPu4nrf1efPtfLQj1dCXGnkMVqbsebXKp5ySld555r3EzDO8r9bImIg7kzCw0IsXmH1p9s3/LIeq9GXwy8GM4Zc6HwTf6fqPTeT7H4AqFQRLgRqaJMAPJ/Sf7Yu4p+aZjzYek/2xdxT80zHnVnyObXtAABWQAAAAAAAAAH1rhOhDu4eVCpCcJ0Id3DyoVI8K94IBI7TFNEEacRicLEmZFrJ8DNEKpNcSLOVnpk+I/NJ5PJ+JHq3jwduPaRol00Nyic9Zn4e9Bv31yBw2/eclFHZkDGY5QTcmtNBw4erzS1aXa0l9yix0oyneEotbuaTT519TN8odpTqStm42VkuDM1UqNaNr52Zr/yunr8Xyz4dd51acosJuzutHn2XzNdydnejT+BI87p1XfNuS6m20zd8lqt6aWlnkuo3c/jnjGtzerZONdF5EerUQ5GDsQsTA8l6j1c2SsOisw025TT4SVuxot6ETIsqPT7KfjKI5NZPsfgN4fpy90IL6t/0Hp6PsZYlRKZIgMUyRAqPJvSf7Yu4p+aZjzYek/2xdxT80zHnVnyOfXtAABWQAAAAAAAAAH1rhOhDu4eVC5CMJ0Id3DyocPCveO0wkEQZkMTQzJcCTJDUomaIeIw0Za69ZEnCcXaSv7/cT6lC4OD45heqypThJWf90yNKm1k8yzq011EOtEqq3EzUU2+oxe18S5yd7fLqNhtWhKUHuv5dZjnhJ5+sir3yt1GswhGAwinF369eo7idnR1k4vquldlhhae5BXi96WaVtERqmFqTej+hjXy8vI7P8b/Gm7+W7yKTEYSCkkorTgki85K0spW03lb7k3Dcmpzs5Wh8XUzTbK2RChBQjm9XJrVlmrc/by+fGc/JZnw3uZELEwLmpTK3FR1MPJQ0I/tpr8sH4r9C5oLQq6FvXTt+5DxkXVCGnyCpGGWc+2C+SuOPR9j8BGGXT7zwihyej7GWIjwQ/AZiPQKPJvSf7Yu4p+aZjzYek/2xdxT80zHnVnyObXtAABWQAAAAAAAAAH1rhOhDu4eVDlxnCPmQ7uHlQ6znr3jsQkzlwuQBzdBnN4yBxG2kOSkMzkAzUiiFVgmTZyGZQKKvEU1ZlL/hLvN8dLGjrQKurGzyJ2xqU1DDQX4bvreeXUTqcEtEiLFj8JmWvy1znUiI7EgzxSRyGNXWaT1NrSS1KTalSybX9xeN2hfKKbZTVZSev0MrIi7Jk5TnN8ZJfQ0mG1RntlRtve+bL6gr5MNWcSaLsnfjUl+g7J5fJiKHR/5Tf8zFS0fYzTNNxQuIiItAeT+k72xdxT8ZGPNh6TfbF3FPxkY86s+RzX2gAArIAAAAAAAAAD6ywr5kO7h4IcuM4V8yHdw8EOHPXvPHJ34CY34i7nN4cHN5nLXETmhmdZ8CWByctzXTr6hE530G05NDdmiBSl1jjkhCOSQDFcq6yzJ9dtFfWmrkqw1PIalWEVqxX4ivJK8Yub/dWrDRyvU1cnZe92K/DbRU6ypx0zv13/oRamGr1pJ1OYlJWp8WvqLpYbdxNKSjbejUv/xtbxHGpF7Ck5O0SX/45WvLMnbNoq17Z6Fn6lWB1icTRjTknDTeV11XZbUI5fIb5SUFuuSWazv2ZjuFzin1pGVt6eoPmR7G/qxUlk+xiaPQh8EfAXLR9jNM01EciNwHIAryb0ne2LuIeaZjzYek/wBsXcU/NMx51Z8jm17QAAVkAAAAAAAAAB9W4V8yHdw8qHbjGFfMh3cPKh1s569yZyyG0FRiIMoXuXDdQmU7IRKoA6xuTEuQEsBvCZSBo40ZEas7lJjZWZb4iZU1KEpyyjl1kaiix+PULXUn7krndnVp1G0oTjl0mjTYbYkb70s/y2yRa08KorKKXYg33Mnn2zcNkzk01wi85a34Flh9jwi1OXOlZpN8L62LmFMU4DqSq7Drde77yRUrNZITXhmmuv7DdWqZVSbe391ttbtnfrWQYaX7NP8AIn9hrlBWtSm/yy8DtHKkl/t2/lNKnx0Xwx8EKk8vkck8zkhGSYjkRuI7EFeS+k/2xdxT80zHmw9J/ti7in5pmPOrPkc2vaAACsgAAAAAAAAAPqnCvmQ7uHlQu4xhZcyHdw8qHd48HvI5VY1F6jjVxLQaIa8BLR0JIAucucbBMlC4ipLJjakOxzMiDHB7zvL6Zkylhkh6ERxIgbUEju6LEuRRwanITUq2Isq6vqQhypIq8TK3EXicco5FFjsZdPMca6g7YxO+9xPJtIuEuZb4V9WkZ3D86afvNJF82PeU/Mg0mbrzfC7zCUHa9nbPO2Wj/oO0qu6muOdtMr2/uKdda2zW9bJZKz+ubLGKjUoN6K/0F2trlrr7gc4yVndcbpLN2SeXyHalW6t7+3KyWb+QK8g9J3ti7iHmmZA2HpN9sXcU/GRjzpz5HPfaAACsgAAAAAAAACwfUWF6EPgh5UPABzuh1CZABFIETAChB2IASjqHYABih+IoAA4xqYAUQapW1emvhYAFVWM1ZVYnRgBRBwPT+bNRT0j3kPEAPNYms7wfzADRTdMeAAV5N6TPbF3FPxkZAAOrPkc19oAAKyAAAP/Z
# URL = 'https://i.pinimg.com/originals/95/2a/04/952a04ea85a8d1b0134516c52198745e.jpg'
URL = 'https://s.france24.com/media/display/de24f508-9621-11eb-b789-005056bff430/w:980/p:16x9/de26203e88b87ea71a9fb2a6f9c7012b9ed86c13.jpg'
f = io.BytesIO(urllib.request.urlopen(URL).read())  # Download the picture at the url as a file object
img = Image.open(f)  # You can also use this on a local file; just put the local filename in quotes in place of f.
# # img.show()  # Send the image to your OS to be displayed as a temporary file
# print(img.size)  # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
# pix = img.load()  # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
# # print(pix[2, 5])  # Access the color at a specific location; note [x, y] NOT [row, column].
# means = choose_rand_pixels(img, pix, 8)
# while True:
#     associated = associate_means(img, pix, means)
#     new_means = list()
#     for mean in means:
#         new_means.append(avg_pix(associated[mean]))
#     if set(new_means) == set(means):
#         break
#     means = new_means
# # pix[2, 5] = (255, 255, 255)  # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.
# # img.show()  # Now, you should see a single white pixel near the upper left corner
# posterize(img, pix, means)
naive_posterize(img.load(), img)
img.show()
img.save("my_image.png")  # Save the resulting image. Alter your filename as necessary.
