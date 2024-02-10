file_path = 'transform/dbt_project.yml'
line_to_comment = "- ../.meltano/transformers/dbt/target"

with open(file_path, 'r') as file:
    lines = file.readlines()

with open(file_path, 'w') as file:
    for line in lines:
        if line.strip() == line_to_comment:
            file.write(f"# {line}")
        else:
            file.write(line)