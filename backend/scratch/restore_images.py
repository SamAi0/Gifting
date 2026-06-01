import subprocess
import os

commits = [
    "c1ab323",
    "230cce6",
    "678c222",
    "55b717b",
    "379de4a"
]

def restore_deleted_files():
    repo_dir = r"c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting"
    restored_count = 0

    for commit in commits:
        print(f"Processing commit {commit}...")
        try:
            # Get list of files deleted in this commit
            output = subprocess.check_output(
                ['git', 'diff-tree', '--no-commit-id', '--name-status', '-r', commit],
                cwd=repo_dir,
                text=True
            )
        except Exception as e:
            print(f"Error getting diff for {commit}: {e}")
            continue

        deleted_files = []
        for line in output.splitlines():
            if line.startswith('D\t'):
                filepath = line.split('\t')[1]
                if 'static/products/' in filepath:
                    deleted_files.append(filepath)

        if not deleted_files:
            continue

        print(f"Found {len(deleted_files)} deleted static product files in {commit}. Restoring...")
        
        # We want to restore from the parent of this commit
        parent_commit = f"{commit}^"
        
        # Restore files in chunks to avoid command line length limits
        chunk_size = 50
        for i in range(0, len(deleted_files), chunk_size):
            chunk = deleted_files[i:i+chunk_size]
            try:
                subprocess.check_call(
                    ['git', 'checkout', parent_commit, '--'] + chunk,
                    cwd=repo_dir
                )
                restored_count += len(chunk)
            except subprocess.CalledProcessError as e:
                # Sometimes a file might not exist in the parent if the history is weird, 
                # but it should be there since it was marked as Deleted in 'commit'.
                print(f"Warning: Failed to restore some files from {parent_commit}: {e}")

    print(f"\nSuccessfully restored {restored_count} files!")

if __name__ == '__main__':
    restore_deleted_files()
