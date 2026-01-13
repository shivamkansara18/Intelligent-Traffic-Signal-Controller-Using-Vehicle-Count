import os

# Path to the folder containing YOLO annotation .txt files
labels_path = r"C:\Users\Shivam\OneDrive\Desktop\COLLEGE\minor_project"

# Class name for autorickshaw (case-sensitive, check your annotation files)
AUTORICKSHAW_CLASS_NAME = "Auto"   # update based on exact spelling in labels

# Counter
total_autorickshaws = 0

# Loop through all .txt files in the labels folder
for file_name in os.listdir(labels_path):
    if file_name.endswith(".txt"):
        file_path = os.path.join(labels_path, file_name)
        
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) > 0:
                    class_name = parts[0]
                    if class_name.lower() == AUTORICKSHAW_CLASS_NAME.lower():
                        total_autorickshaws += 1

print(f"Total autorickshaws in dataset: {total_autorickshaws}")
