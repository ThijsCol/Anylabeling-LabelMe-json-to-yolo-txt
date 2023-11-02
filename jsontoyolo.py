import os
import json
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Define the class labels 
class_labels = {"car": 0, "bike": 1, "plane": 2} # Change/add more for your database

# Define the directories
input_dir = r'/anylabeling_data/dataset' # Replace with your directory
output_dir = r'/data/yolo' # Replace with your directory

# Define the train-validate split
split_ratio = 0.2 # 20% of the data will go to the validation set

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Create train and validate directories
train_dir = os.path.join(output_dir, 'train')
os.makedirs(train_dir, exist_ok=True)

validate_dir = os.path.join(output_dir, 'validate')
if split_ratio > 0:
    os.makedirs(validate_dir, exist_ok=True)

json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

if split_ratio > 0:
    train_images, validate_images = train_test_split(image_files, test_size=split_ratio)
else:
    train_images = image_files

# Copy all images to train and validate directories
for image_file in tqdm(image_files, desc="Copying images"):
    current_output_dir = train_dir if image_file in train_images else validate_dir
    shutil.copy(os.path.join(input_dir, image_file), current_output_dir)

# Use tqdm for progress bar
for filename in tqdm(json_files, desc="Copying annotations"):
    with open(os.path.join(input_dir, filename)) as f:
        data = json.load(f)

    image_filename = filename.replace('.json', '')
    if any(os.path.isfile(os.path.join(input_dir, image_filename + ext)) for ext in ['.jpg', '.png', '.jpeg']):
        if image_filename + '.jpg' in train_images or image_filename + '.png' in train_images or image_filename + '.jpeg' in train_images:
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

print("Conversion and split completed successfully!")
