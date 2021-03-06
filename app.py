import os
import cv2

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./files/"
ALLOWED_EXTENSIONS = {'jpg'}
HEIGHT_A4 = 1123
WIDE_A4 = 796


@app.route('/')
def upload_file():
    return render_template('formulario.html')


@app.route('//uploader', methods=['POST'])
def uploader():
    try:
        if request.method == "POST":
            if 'image' in request.files:
                file = request.files['image']
                if file.filename:
                    filename = secure_filename(file.filename)
                    if file and allowed_file(file.filename):
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                        orientation, newSize = resize_image(image)
                        wide, height = newSize[0:2]
                        data = {
                            "statusCode": "200",
                            "response": {
                                "mensaje": "La imagen se proceso exitosamente!",
                                "datos": {
                                    "orientacion": orientation,
                                    "alto": height,
                                    "ancho": wide
                                }
                            }
                        }

                        # show_image(orientation, height, wide)
                        # save_resize_image(orientation, height, wide)
                    else:
                        raise TypeError
                else:
                    raise ValueError
            else:
                raise ValueError

        return data

    except ValueError:
        data = {
            "statusCode": "200",
            "response": {
                "mensaje": "Por favor revisa el Key o el archivo adjunto",
            }
        }
        return data
    except TypeError:
        data = {
            "statusCode": "415",
            "response": {
                "mensaje": "El formato de la imagen no es valido!",
            }
        }
        return data


# function to extract data from image (orientation, height and width)
def extract_data(file):
    height, wide = file.shape[0:2]
    if height == wide:
        orientation_image = "Cuadrada"
    elif height > wide:
        orientation_image = "Vertical"
    else:
        orientation_image = "Horizontal"

    return orientation_image, height, wide


# function to calculate image size
def resize_image(file):
    orientation, height, wide = extract_data(file)

    if orientation == "Cuadrada":
        if height >= WIDE_A4:
            new_wide = WIDE_A4
            new_height = WIDE_A4
        else:
            new_wide = wide
            new_height = height
    elif orientation == "Vertical":
        if height >= HEIGHT_A4:
            new_height = HEIGHT_A4
            proportion = wide / height
            new_wide = int(new_height * proportion)
        else:
            new_height = height
            new_wide = wide
    else:
        if wide >= HEIGHT_A4:
            new_wide = HEIGHT_A4
            proportion = height / wide
            new_height = int(new_wide * proportion)
        else:
            new_height = height
            new_wide = wide

    size_image = (new_wide, new_height)
    return orientation, size_image


# function to display resize image on A4 size sheet
def show_image(orientation, height, wide):

    if orientation == "Horizontal":
        new_image = cv2.imread(app.config['UPLOAD_FOLDER'] + "/a4_H.jpg")
        cv2.rectangle(new_image, (0, 0), (wide, height), (0, 0, 255), 5)
    else:
        new_image = cv2.imread(app.config['UPLOAD_FOLDER'] + "/a4_V.jpg")
        cv2.rectangle(new_image, (0, 0), (wide, height), (0, 0, 255), 5)

    # uncomment if the sheet is only vertical
    """newImage = cv2.imread(app.config['UPLOAD_FOLDER'] + "/a4_V.jpg")
    cv2.rectangle(newImage, (0, 0), (wide, height), (0, 0, 255), 5)"""

    cv2.imshow('image', new_image)
    cv2.waitKey(0)


# function to save a sketch of how the resized image is displayed on the A4 size sheet
def save_resize_image(orientation, height, wide):
    if orientation == "Horizontal":
        new_image = cv2.imread(app.config['UPLOAD_FOLDER'] + "/a4_H.jpg")
    else:
        new_image = cv2.imread(app.config['UPLOAD_FOLDER'] + "/a4_V.jpg")
    cv2.rectangle(new_image, (0, 0), (wide, height), (0, 0, 255), 5)
    cv2.imwrite(app.config['UPLOAD_FOLDER'] + "/newImage.jpg", new_image)
    return print("Save Image")


# function to validate image format
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
