import os
import sys
import pyheif
from PIL import Image

def convert_heic_to_jpg(heic_path, jpg_path):
    # Read HEIC image data using pyheif
    heif_file = pyheif.read(heic_path)

    # Convert HEIC image data to RGB
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # Reduce the image size
    basewidth = 500  # change this as required
    wpercent = (basewidth/float(image.size[0]))
    hsize = int((float(image.size[1])*float(wpercent)))
    img = image.resize((basewidth, hsize), Image.ANTIALIAS)

    # Save the image in JPEG format
    img.save(jpg_path, "JPEG")

def process_folder(folder_path):
    # Walk through the folder and its sub-folders
    for subdir, dirs, files in os.walk(folder_path):
        for filename in files:
            # Check if the file is a HEIC file
            if filename.lower().endswith(".heic"):
                file_path = os.path.join(subdir, filename)
                print(f"Processing {file_path}")

                # Convert the HEIC file to a JPEG file
                jpg_filename = filename.rsplit(".", 1)[0] + ".jpg"
                jpg_path = os.path.join(subdir, jpg_filename)
                convert_heic_to_jpg(file_path, jpg_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_heic_to_jpg.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)
