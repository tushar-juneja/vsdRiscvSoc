import os
import re

ROOT_README = "README.md"
WEEK_MD_NAME = "Week.md"
TASK_PATTERN = re.compile(r'Task[-_]?(\d+)\.md', re.IGNORECASE)
WEEK_FOLDER_PATTERN = re.compile(r'Week[-_ ]?(\d+)', re.IGNORECASE)


def find_week_folders():
    """Return list of folders like 'Week 1', 'Week_2', etc., sorted numerically."""
    week_folders = []
    for entry in os.listdir("."):
        if os.path.isdir(entry):
            match = WEEK_FOLDER_PATTERN.fullmatch(entry)
            if match:
                week_num = int(match.group(1))
                week_folders.append((week_num, entry))
    return sorted(week_folders)


def generate_week_md(week_folder):
    """Create a Week.md in the folder by combining Task-*.md files."""
    task_files = []
    for fname in os.listdir(week_folder):
        match = TASK_PATTERN.fullmatch(fname)
        if match:
            task_num = int(match.group(1))
            task_files.append((task_num, fname))

    task_files.sort(key=lambda x: x[0])  # Sort numerically

    week_md_path = os.path.join(week_folder, WEEK_MD_NAME)
    with open(week_md_path, "w", encoding="utf-8") as out:
        week_title = os.path.basename(week_folder)
        out.write(f"# {week_title} Summary\n\n")
        for task_num, fname in task_files:
            task_path = os.path.join(week_folder, fname)
            with open(task_path, "r", encoding="utf-8") as tf:
                content = tf.read().strip()
                out.write(content + "\n\n")
                out.write(f"---\n<br><br>\n")  # Separator between tasks


def update_main_readme(week_folders):
    """Combine all Week.md files into the main README.md."""
    with open(ROOT_README, "w", encoding="utf-8") as root:
        root.write("# Complete Weekly Summary\n\n")

        for week_num, folder in week_folders:
            week_md_path = os.path.join(folder, WEEK_MD_NAME)
            if os.path.exists(week_md_path):
                with open(week_md_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    root.write(content + "\n\n")
            else:
                print(f"⚠️ Skipped: {week_md_path} does not exist.")


def main():
    week_folders = find_week_folders()
    for _, folder in week_folders:
        generate_week_md(folder)
    update_main_readme(week_folders)
    print("✅ Week.md files generated and README.md updated.")


if __name__ == "__main__":
    main()
