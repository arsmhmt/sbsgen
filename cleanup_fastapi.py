import os

# Set your routes directory
routes_dir = "app/routes"

# List of files to keep (Flask blueprints)
keep_files = [
    "user.py",
    "admin.py",
    "main.py",
    "auth.py",  # Add any other Flask blueprint files you want to keep
]

for filename in os.listdir(routes_dir):
    if filename.endswith(".py") and filename not in keep_files:
        file_path = os.path.join(routes_dir, filename)
        # Rename instead of delete for safety
        os.rename(file_path, file_path + ".bak")
        print(f"Renamed {filename} to {filename}.bak")

print("Cleanup complete. Only Flask blueprint files remain in app/routes/.")