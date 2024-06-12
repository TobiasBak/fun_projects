


# All missing implementations


## Major steps
1. Combine the images and the voiceover into a video. 
2. Implement a method for combining the videos into a single video.
3. Thumbnails, that are auto generated based on language of the video. 

## Improvements
1. Use a background for the video, such that adhd viewers stay
This background could be a rainy forest etc.    
2. Somehow get ai to write a better script by rewritiing the text and getting information from the images.
3. Some images are too large 1.8k+ pixels in height before they are resized. 
Create a script that determines an optimal point somewhere in the middle, where the picture can be split.
A determination could be the amount of white or black pixels in the image at that point in the middle.
4. Timings to see what is slow
5. Failure checks to see if specific images are missing text or something else is wrong.

## Conquer the world
1. Translate to different languages. (Indian, Spanish, Russian, Arabic, etc.)






possible image describers:
1. https://github.com/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/visual_captioning.ipynb
2. https://huggingface.co/Salesforce/blip2-opt-2.7b (local model)




pip install requests requests-toolbelt

