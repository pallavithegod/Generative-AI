from transformers import pipeline

# RUNNING THIS WILL DOWNLOAD THIS HEAVY MODEL ON MY PC TO BE USED LOCALLY

pipe = pipeline("image-text-to-text", model="google/gemma-4-31B-it")
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG"},
            {"type": "text", "text": "What animal is on the candy?"}
        ]
    },
]
pipe(text=messages)