import subprocess
import time
import os
from .models import New
from .scrap import scraped_data
import requests
from django.core.files.images import ImageFile
from io import BytesIO


def update_news():
    for data in scraped_data:
        title = data['article_title']
        # Check if a New object with the same title already exists
        if not New.objects.filter(title=title).exists():
            response = requests.get(data['article_image'])
            response.raise_for_status()
            # Get the image data in bytes
            image_data = response.content
            # Create a BytesIO object to create a Django File object
            image_file = ImageFile(BytesIO(image_data), name=f"{data['article_title']}.jpg")

            new = New(
                title=data['article_title'], 
                description=data['article_description'], 
                text=data['article_block_text'], 
                link=data['link'],
                image=image_file,
                )
            new.save()
        else:
            print('Exista deja')

def run_file_periodically():
    # Get the current directory where this script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Full path to file.py in the same directory
    file_py_path = os.path.join(script_directory, "scrap.py")
    subprocess.run(["python", file_py_path])
    # while True:
    #     # Run file.py as a separate process
    #     subprocess.run(["python", file_py_path])

    #     # Delay for 24 hours (24 * 60 * 60 seconds)
    #     # time.sleep(0 * 0 * 60)
    #     time.sleep(60)

if __name__ == "__main__":
    # Start updating the database and running file.py in parallel
    import threading

    # Create a thread for updating the database
    db_update_thread = threading.Thread(target=update_news)
    db_update_thread.start()

    # Run file.py periodically in the main thread
    run_file_periodically()
