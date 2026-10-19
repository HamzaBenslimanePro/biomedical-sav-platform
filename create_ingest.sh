
#!/usr/bin/env bash
set -euo pipefail

# Root package
mkdir -p ingest/domain ingest/generators ingest/tests

# Root files
touch ingest/__init__.py
touch ingest/config.py
touch ingest/cli.py
touch ingest/writer.py

# Documentation
cat > ingest/README.md <<'EOF'
# Ingest Generator

Synthetic data generation package.

## Usage

Generate equipment data:

```bash
python -m ingest generate --table equipment
```

Configure the generator using environment variables defined in config.py.
EOF

# Domain: static reference data
touch ingest/domain/__init__.py
touch ingest/domain/catalogs.py
touch ingest/domain/distributions.py

# Generators: generation logic
touch ingest/generators/__init__.py
touch ingest/generators/base.py
touch ingest/generators/equipment.py
touch ingest/generators/technicians.py
touch ingest/generators/failure_codes.py
touch ingest/generators/work_orders.py

# Tests
touch ingest/tests/__init__.py
touch ingest/tests/test_equipment.py
touch ingest/tests/test_contract.py

echo "Created ingest project structure:"
find ingest -print | sort