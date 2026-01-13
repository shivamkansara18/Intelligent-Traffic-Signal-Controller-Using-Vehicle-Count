from ultralytics import YOLO
from flask import Flask, render_template, request
import os
from PIL import Image
import shutil
import traffic_signal
from typing import List


flask_app_folder_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=["GET"])
def starting_page():
    return render_template("index.html")

def import_image(image_path):
    image = Image.open(image_path)
    return image


yolo = YOLO(flask_app_folder_path+"/best.pt") # last.pt

def apply_yolo(yolo_model, image):
    detections_results = yolo_model.predict(image, save=True)
    return detections_results
    

@app.route("/", methods=["POST"])
def predict_image():
    # print("Entered predict_image()")
    if request.method == "POST":
        # Support both single-image legacy upload (name='image') and
        # multi-direction upload with fields: north, south, east, west
        directions = ["north", "south", "east", "west"]

        # Detect which mode we're in
        is_multi = any(k in request.files for k in directions)

        if not is_multi:
            # legacy single-image path
            if "image" not in request.files:
                return "No image part"
            image_file = request.files["image"]
            if image_file.filename == "":
                return "No selected file"

            uploaded_path = os.path.join(flask_app_folder_path, "static", "uploaded_images", image_file.filename)
            image_file.save(uploaded_path)

            # Apply YOLO
            image = import_image(uploaded_path)
            detections_results = apply_yolo(yolo, image)

            # Determine the save directory and pick the most-recent output file
            save_dir = os.path.abspath(str(detections_results[0].save_dir))
            try:
                candidates = [f for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
            except FileNotFoundError:
                candidates = []

            if not candidates:
                return "No prediction image found in save dir: {}".format(save_dir), 500

            latest_file = max(candidates, key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
            result_image_path = os.path.join(save_dir, latest_file)

            dest_dir = os.path.join(flask_app_folder_path, "static", "predicted_images")
            os.makedirs(dest_dir, exist_ok=True)

            shutil.copy(result_image_path, os.path.join(dest_dir, latest_file))
            return render_template("index.html", uploaded_path="uploaded_images/"+image_file.filename,
                                        predicted_path="predicted_images/"+latest_file )

        # Multi-direction mode
        direction_detections = {}
        saved_uploaded_paths = {}
        predicted_image_names = {}

        for direction in directions:
            f = request.files.get(direction)
            if not f or f.filename == "":
                # treat missing direction as empty
                direction_detections[direction] = []
                continue

            # save file
            filename = f"{direction}_" + os.path.basename(f.filename)
            uploaded_path = os.path.join(flask_app_folder_path, "static", "uploaded_images", filename)
            f.save(uploaded_path)
            saved_uploaded_paths[direction] = "uploaded_images/" + filename

            # run yolo and extract class labels
            image = import_image(uploaded_path)
            results = apply_yolo(yolo, image)

            # extract classes robustly
            classes = []
            try:
                res0 = results[0]
                names = getattr(res0, "names", None) or {}
                boxes = getattr(res0, "boxes", None)
                cls_vals = None
                if boxes is not None:
                    cls_vals = getattr(boxes, "cls", None)

                if cls_vals is not None:
                    # try to convert to a python list of ints
                    try:
                        cls_list = list(cls_vals.tolist())
                    except Exception:
                        try:
                            cls_list = list(cls_vals)
                        except Exception:
                            cls_list = []

                    for ci in cls_list:
                        try:
                            cls_idx = int(ci)
                            cls_name = names.get(cls_idx, str(cls_idx))
                            classes.append(cls_name)
                        except Exception:
                            continue
                else:
                    # fallback: look for labels folder saved by YOLO
                    save_dir = os.path.abspath(str(res0.save_dir))
                    labels_dir = os.path.join(save_dir, "labels")
                    if os.path.isdir(labels_dir):
                        # find most recent label file for this image
                        try:
                            txts = [p for p in os.listdir(labels_dir) if p.endswith('.txt')]
                            if txts:
                                # choose the most recent
                                lbl_file = max(txts, key=lambda p: os.path.getmtime(os.path.join(labels_dir, p)))
                                with open(os.path.join(labels_dir, lbl_file), 'r') as fh:
                                    for line in fh:
                                        parts = line.strip().split()
                                        if not parts:
                                            continue
                                        try:
                                            idx = int(float(parts[0]))
                                            name = res0.names.get(idx, str(idx))
                                            classes.append(name)
                                        except Exception:
                                            continue
                        except Exception:
                            pass

            except Exception:
                classes = []

            direction_detections[direction] = classes

            # copy predicted image to predicted_images (if created by YOLO)
            try:
                res0 = results[0]
                save_dir = os.path.abspath(str(res0.save_dir))
                # pick latest image file
                candidates = [f for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
                if candidates:
                    latest_file = max(candidates, key=lambda f: os.path.getmtime(os.path.join(save_dir, f)))
                    dest_dir = os.path.join(flask_app_folder_path, "static", "predicted_images")
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.copy(os.path.join(save_dir, latest_file), os.path.join(dest_dir, latest_file))
                    predicted_image_names[direction] = "predicted_images/" + latest_file
            except Exception:
                pass

        # compute timing
        timing = traffic_signal.determine_signal_timing(direction_detections, T_min=10, T_max=45)

        # Prepare human-friendly formatted outputs
        loads = timing.get('loads', {})
        green_times = timing.get('green_times', {})
        order = timing.get('priority_order', [])

        return render_template("index.html",
                               multi_mode=True,
                               uploaded_paths=saved_uploaded_paths,
                               predicted_paths=predicted_image_names,
                               loads=loads,
                               green_times=green_times,
                               priority_order=order)

    return render_template("index.html")

if __name__ == "__main__":
    # Bind explicitly and enable request logging to help debug local access issues.
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    # Use 0.0.0.0 for wider reach during debugging; change back to 127.0.0.1 for stricter local-only binding.
    app.run(debug=True, host='0.0.0.0', port=5001)


@app.route('/health', methods=['GET'])
def health():
    return 'ok', 200
