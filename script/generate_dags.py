import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_ROOT = os.path.join(BASE_DIR, 'sql')
OUTPUT_DIR = os.path.join(BASE_DIR, 'dags', 'generated')
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = 'dag_template.py.jinja2'

# Jinja2 
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template(TEMPLATE_FILE)

os.makedirs(OUTPUT_DIR, exist_ok=True)

if len(sys.argv) < 2:
    print("Please provide one or more config YAML file paths.")
    print("Example: python scripts/generate_dags.py config/attribution/attribution.yaml")
    sys.exit(1)

# Process each config file passed via CLI
for config_path in sys.argv[1:]:
    if not config_path.endswith(('.yaml', '.yml')):
        print(f"⚠️ Skipping non-YAML file: {config_path}")
        continue

    if not os.path.isfile(config_path):
        print(f"File not found: {config_path}")
        continue

    with open(config_path) as f:
        config = yaml.safe_load(f)

    process_name = os.path.basename(os.path.dirname(config_path))
    dag_id = config.get('dag_id', f"{process_name}_dag")

    tasks = []
    for task in config['tasks']:
        depends = task.get('depends_on')
        depends_list = depends if isinstance(depends, list) else [depends] if depends else []

        tasks.append({
            'task_id': task['task_id'],
            'sql': task['sql'],
            'depends_on': depends_list
        })

    dag_code = template.render(
        dag_id=dag_id,
        process_name=process_name,
        tasks=tasks
    )

    output_file = os.path.join(OUTPUT_DIR, f"{dag_id}.py")
    with open(output_file, 'w') as f:
        f.write(dag_code)

    print(f" DAG generated: {output_file}")
