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
python average_color.py
python pad.py
python text_extraction.py
python image_classifier.py
python object_detection.py
```

## How to find
``` bash
python find.py <replace_with_your_searchstring> # can be regex  
```

## How to composit image
Find small image to recreate (100x100 is fine).  
Extract all data.  
In `composit_meme.py` change line 41 to new source.  

``` bash
python composit_meme.py
``` 