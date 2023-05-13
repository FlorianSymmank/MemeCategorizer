# Meme Categorizer
Extract some data from saved memes.  

## Create config
rename config_template.py to config.py and change paths to your needs   
```
processed_meme_dir = r"\preprocessed"
data_dir = f"\data"
meme_dir = r"\Memes" # your meme dir
tesseract_cmd = "tesseract.exe" # tesseract executable
```

## How to run

```
python preprocess_images.py
python text_extraction.py
python image_classifier.py
```