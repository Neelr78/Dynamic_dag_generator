# Dynamic Airflow DAG Generator

This repository provides a framework to generate Airflow DAGs dynamically using YAML configuration files, Jinja2 templates, and BigQuery SQL scripts. DAG files are created locally and can be manually deployed to your Airflow environment as needed.

## 🧩 Project Structure
```
project-root/
├── config/
│ ├── attribution/
│ │ └── attribution.yaml
│ └── bpci/
│ └── bpci.yaml
│
├── sql/
│ ├── attribution/
│ └── bpci/
│
├── dags/
│ └── generated/
│ ├── attribution_dag.py
│ └── bpci_dag.py
│
├── scripts/
│ ├── dag_template.py.jinja2
│ └── generate_dags.py
│
└── README.md
```
## ⚙️ How It Works

1. **Write Configs:** Define DAG structure in a YAML file inside `config/<process_name>/`.
2. **Write SQL:** Store BigQuery SQL files in `sql/<process_name>/`.
3. **Generate DAGs:** Run the generator script locally to create DAG Python files.
4. **Upload Manually:** Copy generated DAGs from `dags/generated/` to your target Airflow environment as needed.

## 🚀 Usage

### Generate a DAG for a specific config file:

python scripts/generate_dags.py config/attribution/attribution.yaml

### Generate multiple DAGs:

python scripts/generate_dags.py config/attribution/attribution.yaml config/bpci/bpci.yaml

The generated DAGs will be placed under dags/generated/.

⚠️ Note: This script does not deploy to Airflow automatically. You must manually upload the generated DAG files into your Airflow environment (e.g., via SFTP, Git push to a DAG repo, etc.).

### 📄 YAML Format

Each DAG config YAML file defines:

DAG ID

List of tasks

Optional dependencies

### Example:

dag_id: attribution_dag
tasks:
  - task_id: task_1
    sql: test_1.sql

  - task_id: task_2
    sql: test_2.sql
    depends_on: task_1
depends_on can be a string or a list of task IDs.

#### 🛠 Requirements
Install dependencies locally:

pip install jinja2 pyyaml
Python 3.7+

Jinja2

PyYAML

The generated DAGs use the BigQueryInsertJobOperator, which must be available in your Airflow environment.

### 📦 Deployment Workflow
1. Generate DAGs locally:

python scripts/generate_dags.py config/your_process/*.yaml

2. Manually upload generated DAGs (dags/generated/*.py) to your Airflow environment’s DAG folder.

3. Restart/reload the scheduler if required.

### 🧪 Tips

Organize SQL by process under sql/<process_name>/

Match YAML and SQL naming conventions per process

Use version control (Git) to track DAG changes before deployment

### 🛤 Future Improvements

Add YAML schema validation

Add auto-deployment hooks (optional)

Add CLI options for dry-run and custom output folder
