import os
import re

MAIN_README = "README"
WEEK_README_NAME = "README.md"

TASK_FILE_PATTERN = re.compile(r'task[-_]?(\d+)\.md', re.IGNORECASE)

def generate_weekly_readme(week_folder):
    task_files = []

    for fname in os.listdir(week_folder):
        match = TASK_FILE_PATTERN.match(fname)
        if match:
            task_num = int(match.group(1))
            task_files.append((task_num, fname))

    # Sort by task number (not alphabetically)
    task_files.sort(key=lambda x: x[0])

    week_readme_path = os.path.join(week_folder, "README.md")
    with open(week_readme_path, "w", encoding="utf-8") as week_readme:
        week_title = os.path.basename(week_folder)
        week_readme.write(f"# {week_title} Summary\n\n")

        for task_num, fname in task_files:
            full_path = os.path.join(week_folder, fname)
            with open(full_path, "r", encoding="utf-8") as tf:
                content = tf.read()
                week_readme.write(f"## Task {task_num}: {fname}\n\n")
                week_readme.write(content.strip() + "\n\n")
                
def update_main_readme():
    all_week_folders = sorted(
        [f for f in os.listdir('.') if os.path.isdir(f) and f.lower().startswith("week")],
        key=lambda x: int(re.search(r'\d+', x).group())
    )

    with open(MAIN_README, "w", encoding="utf-8") as main_readme:
        main_readme.write("# Complete Weekly Summary\n\n")

        for week_folder in all_week_folders:
            generate_weekly_readme(week_folder)

            week_readme_path = os.path.join(week_folder, WEEK_README_NAME)
            with open(week_readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                main_readme.write(content + "\n")

if __name__ == "__main__":
    update_main_readme()
    print("✅ All week READMEs generated and main README assembled.")
