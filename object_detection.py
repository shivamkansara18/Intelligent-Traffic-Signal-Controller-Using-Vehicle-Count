from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")   # n=small, s=medium, m=large, l=xlarge

# Load image
image_path = "car_street.jpg"
results = model(image_path)

# Show results
# results.show()   # opens image with bounding boxes
for r in results:
    r.show() 

    
# Extract detections
for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])   # class id
        conf = float(box.conf[0])  # confidence score
        label = model.names[cls_id]  # class label (like 'car', 'truck')

        if label in ["car", "truck", "bus", "motorbike", "auto"]:
            print(f"Detected {label} with confidence {conf:.2f}")


img = cv2.imread(image_path)

for r in results:
    for box in r.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = model.names[cls_id]

        if label in ["car", "truck", "bus", "motorbike", "auto"]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # coordinates
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Convert BGR to RGB for matplotlib
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()