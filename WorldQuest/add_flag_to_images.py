import pandas as pd
from PIL import Image
import os

# === CONFIGURATION ===
csv_file_path = "capitals.csv"
main_images_path = "capitals"         # Folder with main images (1.jpg, 2.jpg, ...)
flag_images_path = "w160-jpeg"        # Folder with flags (fr.jpg, gb.jpg, ...)
output_path = "capitals"         # Folder to save output images

# Ensure output folder exists
os.makedirs(output_path, exist_ok=True)

# === Load CSV ===
df = pd.read_csv(csv_file_path)

# === Ask user for ID range ===
try:
    start_id = int(input("Enter starting quiz_id: "))
    end_id = int(input("Enter ending quiz_id: "))
except ValueError:
    print("Invalid input. Please enter integers.")
    exit()

# === Process rows in the given range ===
for _, row in df[(df['quiz_id'] >= start_id) & (df['quiz_id'] <= end_id)].iterrows():
    quiz_id = row['quiz_id']
    code = row['code']

    try:
        # Load main image
        main_image_path = os.path.join(main_images_path, f"{quiz_id}.jpg")
        main_image = Image.open(main_image_path).convert("RGBA")

        # Load flag image
        flag_image_path = os.path.join(flag_images_path, f"{code}.jpg")
        flag_image = Image.open(flag_image_path).convert("RGBA")

        # Resize flag proportionally to 60px width
        flag_width = 60
        aspect_ratio = flag_image.height / flag_image.width
        flag_height = int(flag_width * aspect_ratio)
        flag_image = flag_image.resize((flag_width, flag_height), Image.Resampling.LANCZOS)

        # Paste flag on bottom-right corner with 10px padding
        main_w, main_h = main_image.size
        position = (main_w - flag_width - 10, main_h - flag_height - 10)
        main_image.paste(flag_image, position, mask=flag_image)

        # Save image in RGB format with high quality
        output_image_path = os.path.join(output_path, f"{quiz_id}.jpg")
        main_image.convert("RGB").save(output_image_path, format='JPEG', quality=95, subsampling=0)

        print(f"✅ Saved image {output_image_path}")

    except Exception as e:
        print(f"❌ Error processing quiz_id {quiz_id}: {e}")
