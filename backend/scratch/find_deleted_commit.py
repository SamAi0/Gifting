import subprocess

def main():
    try:
        output = subprocess.check_output(
            ['git', 'log', '--diff-filter=D', '--name-status', '--pretty=format:COMMIT||%h||%an||%ad||%s'],
            cwd=r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting",
            text=True
        )
    except Exception as e:
        print(f"Error running git log: {e}")
        return

    current_commit = None
    
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("COMMIT||"):
            parts = line.split("||")
            if len(parts) == 5:
                current_commit = {
                    "hash": parts[1],
                    "author": parts[2],
                    "date": parts[3],
                    "subject": parts[4],
                    "deleted_images": 0
                }
        elif line.startswith("D\t"):
            filename = line.split("\t", 1)[1]
            if "backend/static/products/" in filename or "frontend/public/static/products/" in filename:
                if current_commit:
                    current_commit["deleted_images"] += 1
        elif not line and current_commit and current_commit["deleted_images"] > 0:
            print(f"Commit {current_commit['hash']} by {current_commit['author']} on {current_commit['date']}")
            print(f"Subject: {current_commit['subject']}")
            print(f"Deleted {current_commit['deleted_images']} images in static products directories.\n")
            current_commit = None

if __name__ == "__main__":
    main()
