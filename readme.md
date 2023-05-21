# Meme Categorizer
Extract some data from saved memes.  

## Create config
rename config_template.py to config.py and change paths to your needs   
``` python
processed_meme_dir = r"\preprocessed"
data_dir = f"\data"
meme_dir = r"\Memes" # your meme dir
tesseract_cmd = "tesseract.exe" # tesseract executable
```

## How to extract data

``` bash
python preprocess_images.py
python text_extraction.py
python image_classifier.py
python object_detection.py
```

## How to find
``` bash
python find.py <replace_with_your_searchstring> # can be regeex  
```

