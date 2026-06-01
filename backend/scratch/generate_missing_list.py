import os
import sqlite3

def main():
    db_path = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\backend\db.sqlite3"
    actual_files_dir = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\frontend\public\static\products"
    output_markdown = r"C:\Users\Asus\.gemini\antigravity-ide\brain\eb564b8c-a2dc-4a8b-ad27-46b45376a848\missing_images_list.md"
    
    try:
        actual_files = {f.lower() for f in os.listdir(actual_files_dir)}
    except Exception as e:
        print(f"Error reading files directory: {e}")
        return

    missing_images = []
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, image FROM products_product ORDER BY id")
        for row in cursor.fetchall():
            pid, name, img_path = row
            if img_path:
                img_name = os.path.basename(img_path).lower()
                if img_name not in actual_files:
                    missing_images.append((pid, name, img_name))
    except Exception as e:
        print(f"Error reading database: {e}")
        return
    finally:
        conn.close()

    # Generate Markdown
    md_content = "# List of Missing Product Images\n\n"
    md_content += f"> [!WARNING]\n> A total of **{len(missing_images)}** product images are missing from the `frontend/public/static/products/` directory.\n\n"
    
    md_content += "| Product ID | Product Name | Missing Image File |\n"
    md_content += "|---|---|---|\n"
    for pid, name, img_name in missing_images:
        md_content += f"| {pid} | {name} | `{img_name}` |\n"
        
    with open(output_markdown, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"Successfully generated artifact at {output_markdown}")

if __name__ == '__main__':
    main()
