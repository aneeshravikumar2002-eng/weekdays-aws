import argparse
import json
import os
import sys
import importlib.util

def load_module_from_path(path):
    spec = importlib.util.spec_from_file_location("file1_module", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    p = argparse.ArgumentParser(description="Create RDS from JSON config")
    p.add_argument('--config', required=True, help='Path to JSON config file')
    args = p.parse_args()

    cfg_path = os.path.abspath(args.config)
    if not os.path.exists(cfg_path):
        print("Config file not found:", cfg_path, file=sys.stderr)
        sys.exit(2)

    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # minimal required keys
    required = ['identifier', 'username', 'password']
    missing = [k for k in required if k not in cfg]
    if missing:
        print("Missing required config keys:", missing, file=sys.stderr)
        sys.exit(2)

    # locate existing file1 by path relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file1_path = os.path.join(base_dir, 'file1')  # same filename as your existing file
    if not os.path.exists(file1_path):
        print("Could not find file1 at:", file1_path, file=sys.stderr)
        sys.exit(2)

    file1 = load_module_from_path(file1_path)
    create_fn = getattr(file1, 'create_rds_instance', None)
    if not callable(create_fn):
        print("create_rds_instance not found in file1", file=sys.stderr)
        sys.exit(2)

    # map config values to function parameters (use defaults where not provided)
    params = {
        'db_identifier': cfg.get('identifier'),
        'db_instance_class': cfg.get('db_class', 'db.t3.micro'),
        'engine': cfg.get('engine', 'mysql'),
        'master_username': cfg.get('username'),
        'master_password': cfg.get('password'),
        'allocated_storage': cfg.get('storage', 20),
        'db_name': cfg.get('dbname'),
        'publicly_accessible': cfg.get('public', False),
        'multi_az': cfg.get('multi_az', False),
        'storage_type': cfg.get('storage_type', 'gp2'),
        'tags': cfg.get('tags'),
        'region': cfg.get('region'),
    }

    create_fn(**params)

if __name__ == '__main__':
    main()
