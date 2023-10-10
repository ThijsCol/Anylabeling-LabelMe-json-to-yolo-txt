import os
import json
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Define the class labels 
class_labels = {"car": 0, "bike": 1, "plane": 2} # Change/add more for your database

# Define the directories
input_dir = '/anylabeling_data/dataset' # Replace with your directory
output_dir = '/data/yolo' # Replace with your directory

# Define the train-validate split
split_ratio = 0.2 # 20% of the data will go to the validation set

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Create train and validate directories
train_dir = os.path.join(output_dir, 'train')
os.makedirs(train_dir, exist_ok=True)

if split_ratio > 0:
    validate_dir = os.path.join(output_dir, 'validate')
    os.makedirs(validate_dir, exist_ok=True)

json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

if split_ratio > 0:
    train_files, validate_files = train_test_split(json_files, test_size=split_ratio)
else:
    train_files = json_files

# Use tqdm for progress bar
for filename in tqdm(json_files):
    with open(os.path.join(input_dir, filename)) as f:
        data = json.load(f)

    if filename in train_files:
        current_output_dir = train_dir
    else:
        current_output_dir = validate_dir

    with open(os.path.join(current_output_dir, filename.replace('.json', '.txt')), 'w') as out_file:
        for shape in data['shapes']:
            x1, y1 = shape['points'][0]
            x2, y2 = shape['points'][1]

            dw = 1./data['imageWidth']
            dh = 1./data['imageHeight']
            w = x2 - x1
            h = y2 - y1
            x = x1 + (w/2)
            y = y1 + (h/2)

            x *= dw
            w *= dw
            y *= dh
            h *= dh

            class_label = class_labels[shape['label']]

            out_file.write(f"{class_label} {x} {y} {w} {h}\n")

    image_filename = filename.replace('.json', '')
    for ext in ['.jpg', '.png', '.jpeg']: # if your images have a different file extension, modify/add it here
        if os.path.isfile(os.path.join(input_dir, image_filename + ext)):
            shutil.copy(os.path.join(input_dir, image_filename + ext), current_output_dir)
            break

print("Conversion and split completed successfully!")
