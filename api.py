import os
from flask import Flask, flash, request, redirect, url_for, jsonify

from werkzeug.utils import secure_filename
import tensorflow as tf
import tensorflow_hub as hub
import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# For downloading the image.
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import face_recognition
import pandas as pd

# For measuring the inference time.
import time

print("The following GPU devices are available: %s" % tf.test.gpu_device_name())
annotations = pd.read_csv("Known_Person/data_annotation.csv")
UPLOAD_FOLDER = '/home/ali/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

module_handle = "my_module_cache/6e850c920451d5243d1fb87a3242c087535b9183"
# @param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1",
# "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]
# module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
print("not start")
with tf.Graph().as_default():
    print("strat")
    config = tf.ConfigProto()
    config.gpu_options.allocator_type = 'BFC'
    # config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 1
    detector = hub.Module(module_handle)
    print("model loaded!")
    image_string_placeholder = tf.placeholder(tf.string)
    decoded_image = tf.image.decode_jpeg(image_string_placeholder)
    # Module accepts as input tensors of shape [1, height, width, 3], i.e. batch
    # of size 1 and type tf.float32.
    decoded_image_float = tf.image.convert_image_dtype(
        image=decoded_image, dtype=tf.float32)
    module_input = tf.expand_dims(decoded_image_float, 0)
    result = detector(module_input, as_dict=True)
    init_ops = [tf.global_variables_initializer(), tf.tables_initializer()]
    session = tf.Session(config=tf.ConfigProto(device_count={'GPU': 0}))
    session.run(init_ops)
    print("finsish load sess")


def display_image(image):
    image = Image.fromarray(image)
    image.show()


def get_boxes(image,
              ymin,
              xmin,
              ymax,
              xmax):
    """Adds a bounding box to an image."""
    # draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    # draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
    #            (left, top)],
    #           width=thickness,
    #           fill=color)
    #
    # # If the total height of the display strings added to the top of the bounding
    # # box exceeds the top of the image, stack the strings below the bounding box
    # # instead of above.
    # display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # # Each display_str has a top and bottom margin of 0.05x.
    # total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)
    #
    # if top > total_display_str_height:
    #     text_bottom = top
    # else:
    #     text_bottom = bottom + total_display_str_height
    # # Reverse list and print from bottom to top.
    # for display_str in display_str_list[::-1]:
    #     text_width,  text_height = font.getsize(display_str)
    #     margin = np.ceil(0.05 * text_height)
    #     draw.rectangle([(left, text_bottom - text_height - 2 * margin),
    #                     (left + text_width, text_bottom)],
    #                    fill=color)
    #     draw.text((left + margin, text_bottom - text_height - margin),
    #              display_str,
    #               fill="black",
    #               font=font)
    #     text_bottom -= text_height - 2 * margin
    return left, right, top, bottom


def get_classes(image, boxes, class_names, scores, max_boxes=10, min_score=0.3):
    # """Overlay labeled boxes on an image with formatted scores and label names."""
    # colors = list(ImageColor.colormap.values())
    #
    # try:
    #     font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
    #                               25)
    # except IOError:
    #     print("Font not found, using default font.")
    #     font = ImageFont.load_default()
    lis_class = []
    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i].tolist())
            # display_str = "{}: {}%".format(class_names[i].decode("ascii"),
            #                                int(100 * scores[i]))
            # color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            left, right, top, bottom = get_boxes(
                image_pil,
                ymin,
                xmin,
                ymax,
                xmax)
            clas = {"class_name": class_names[i].decode("ascii"), "top": int(top), "right": int(right), "bottom": int(bottom),
                    "left": int(left)}
            lis_class.append(clas)
            # np.copyto(image, np.array(image_pil))
    return lis_class


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part\
        args = str(request.args)
        form = str(request.form)
        files = str(request.files)
        print("{}__{}___{}".format(args, form, files))
        if 'myfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['myfile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success send " + file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return "wrong post", 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    downloaded_image_path = filename
    with tf.Graph().as_default():
        # Load the downloaded and resized image and feed into the graph.
        with tf.gfile.Open(downloaded_image_path, "rb") as binfile:
            image_string = binfile.read()
        # im = Image.open(downloaded_image_path)
        # print(im.size)
        result_out, image_out = session.run(
            [result, decoded_image],
            feed_dict={image_string_placeholder: image_string})
        print("Found %d objects." % len(result_out["detection_scores"]))

    lis_class = get_classes(
        np.array(image_out), result_out["detection_boxes"],
        result_out["detection_class_entities"], result_out["detection_scores"])
    image_out = np.array(image_out)
    lis_dic_face = []
    for clas in lis_class:
        if clas["class_name"] == "Person" or clas["class_name"] == "Man" or clas["class_name"] == "Woman":
            unknown_image = image_out[int(clas["top"]):int(clas["bottom"]), int(clas["left"]):int(clas["right"])]
            unknowns_face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0,
                                                                      model="cnn")
            
            unkown_images_encoding = face_recognition.face_encodings(unknown_image, unknowns_face_locations)
            for un_im, un_face_loc in zip(unkown_images_encoding, unknowns_face_locations):
                for index, row in annotations.iterrows():
                    face_locations = [row["top"], row["right"], row["bottom"], row["left"]]
                    #print(face_locations)
                    name = row["Name"]
                    path_image = row["path_image"]
                    image = face_recognition.load_image_file("Known_Person/" + path_image)
                    image_encoding = face_recognition.face_encodings(image, [face_locations])[0]
                    result_face = face_recognition.compare_faces([image_encoding], un_im, tolerance=0.5)[0]
                     
                    #print(result_face,name)
                    if result_face:
                        top, right, bottom, left = un_face_loc
                        #             face_image = unkown_image[top:bottom, left:right]
                        #             pil_image = Image.fromarray(face_image)
                        #             display(pil_image)
                        dic_loc = {"name": name, "top": top, "right": right, "bottom": bottom, "left": left}
                        lis_dic_face.append(dic_loc)
    lis_dic_face = list({v['name']:v for v in lis_dic_face}.values())
    json_detctor = {"object_detection": lis_class, "face recognition": lis_dic_face}
    return jsonify(json_detctor)



app.run(debug=True, host="0.0.0.0", port=5000)
