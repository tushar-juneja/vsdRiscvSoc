import os
import glob
import re

root_dir = os.getcwd()
readme_path = os.path.join(root_dir, "README.md")

def merge_tasks_to_week_md(week_path, week_number):
    task_files = sorted(glob.glob(os.path.join(week_path, "Task-*.md")))
    output_file = os.path.join(week_path, f"Week-{week_number}.md")

    with open(output_file, "w") as out:
        for task_file in task_files:
            with open(task_file, "r") as f:
                # out.write(f"\n\n---\n\n## {os.path.basename(task_file)}\n\n")
                out.write(f.read())
                out.write(f"\n<br><br>\n")

    return output_file

def collect_weeks():
    return sorted([
        d for d in os.listdir(root_dir)
        if os.path.isdir(d) and re.match(r"Week\s+\d+", d)
    ])

def update_readme(week_files):
    with open(readme_path, "w") as readme:
        readme.write("# Weekly Tasks Summary\n")

        for week_file in week_files:
            week_name = os.path.basename(week_file).replace(".md", "")
            readme.write(f"\n\n## {week_name}\n\n")

            with open(week_file, "r") as f:
                readme.write(f.read())

if __name__ == "__main__":
    week_dirs = collect_weeks()
    week_md_files = []

    for week_dir in week_dirs:
        week_num = ''.join(filter(str.isdigit, week_dir))
        print(f"Merging tasks in: {week_dir}")
        week_md = merge_tasks_to_week_md(week_dir, week_num)
        week_md_files.append(week_md)

    print("Updating README.md...")
    update_readme(week_md_files)
    print("Done.")
