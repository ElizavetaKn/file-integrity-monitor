# File Integrity Monitor

A defensive Python utility that creates a SHA-256 baseline for a directory and reports added, modified, and deleted files.

## What it demonstrates

- Endpoint security concepts
- File integrity monitoring
- Hashing with SHA-256
- Secure baseline comparison
- JSON reporting
- Unit tests

## Create a baseline

```bash
python -m file_integrity_monitor.cli baseline ./watched baseline.json
```

## Check for changes

```bash
python -m file_integrity_monitor.cli check ./watched baseline.json --report report.json
```

## Tests

```bash
python -m unittest discover -s tests -v
```

Use this project only on directories you own or are authorized to monitor.
