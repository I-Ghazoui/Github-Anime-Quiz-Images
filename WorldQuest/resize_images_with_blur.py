from PIL import Image, ImageFilter
import os

# === CONFIGURATION ===
images_path = "w2560"              # Folder with images to process
target_size = 550                  # Target size for the larger dimension (width or height)
final_size = 600                   # Final image size (600x600)
background_blur = 360               # Blur radius for background

# === Process all images in the folder ===
if not os.path.exists(images_path):
    print(f"❌ Error: Folder '{images_path}' does not exist.")
    exit()

# Get all image files
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
image_files = [f for f in os.listdir(images_path) 
               if f.lower().endswith(image_extensions)]

if not image_files:
    print(f"❌ No image files found in '{images_path}' folder.")
    exit()

print(f"📁 Found {len(image_files)} image(s) to process...\n")

# === Process each image ===
processed_count = 0
for filename in image_files:
    try:
        # Load image
        image_path = os.path.join(images_path, filename)
        base = Image.open(image_path).convert("RGB")
        
        # Determine which dimension is larger and resize accordingly
        original_width, original_height = base.size
        if original_height > original_width:
            # Height is larger, resize height to target_size
            aspect_ratio = original_width / original_height
            new_height = target_size
            new_width = int(target_size * aspect_ratio)
        else:
            # Width is larger or equal, resize width to target_size
            aspect_ratio = original_height / original_width
            new_width = target_size
            new_height = int(target_size * aspect_ratio)
        
        resized_image = base.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create 600x600 canvas
        W, H = final_size, final_size
        final_image = Image.new("RGB", (W, H))
        
        # Background (blurred fill)
        bg = base.copy().resize((W, H), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(background_blur))
        final_image.paste(bg, (0, 0))
        
        # Center the resized image on the blurred background
        x_offset = (W - new_width) // 2
        y_offset = (H - new_height) // 2
        final_image.paste(resized_image, (x_offset, y_offset))
        
        # Save with maximum quality (overwrite original)
        # Determine format from original file extension
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in ('.jpg', '.jpeg'):
            # Maximum JPEG quality (100) with no subsampling for best quality
            final_image.save(image_path, format='JPEG', quality=100, subsampling=0, optimize=False)
        elif file_ext == '.png':
            # PNG is lossless, save with maximum compression level 9 for best compression
            final_image.save(image_path, format='PNG', compress_level=9, optimize=False)
        else:
            # Default to JPEG for other formats with maximum quality
            new_path = os.path.splitext(image_path)[0] + '.jpg'
            final_image.save(new_path, format='JPEG', quality=100, subsampling=0, optimize=False)
            if new_path != image_path:
                os.remove(image_path)
        
        processed_count += 1
        print(f"✅ Processed: {filename}")
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")

print(f"\n✨ Completed! Processed {processed_count}/{len(image_files)} image(s).")

