# Anylabeling-json-to-yolo-txt
Python scripts for converting .json annotations from [Anylabeling](https://github.com/vietanhdev/anylabeling) to YOLO .txt files.

-**jsontoyolo.py** will convert the .json annotation files to YOLO .txt files, split them into 'train' and 'validate' folders and copy over the corresponding pictures. 
Tracks progress using a progress bar. Requires *scikit-learn* and *tqdm*.

-**jsontoyolo_simple.py** will only convert the .json files to YOLO .txt files and copy them to your specified directory. Only uses built-in Python modules.

**Usage:**

-Define the `class_labels` for your dataset, example: `{"car": 0, "bike": 1, "plane": 2}`.

-Change `input_dir` and `output_dir` to your required directories.

-set the `split_ratio`, example: `0.2 # 20% of the data will go to the validation set`.           

-If your pictures are a different file extension then *'.jpg', '.png', '.jpeg'* you have to modify or add the required extension to `['.jpg', '.png', '.jpeg']:`.

-Run the script and it should generate the .txt files in the specified directory.

---

