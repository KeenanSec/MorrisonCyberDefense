"""Validated CSV storage and cooperative local workspace locking."""
import csv
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
import tempfile


def safe_path(path):
    """Reject symlinks in any component before following a user-supplied path."""
    path = Path(os.path.abspath(Path(path).expanduser()))
    for part in (*reversed(path.parents), path):
        if part.is_symlink():
            raise ValueError(f'Symlink paths are not supported: {part}')
    return path


def read_csv(path, fields):
    path = safe_path(path)
    with path.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.reader(stream, strict=True)
        if next(reader, None) != fields:
            raise ValueError(f'{path}: expected CSV header {fields}')
        result = []
        for values in reader:
            if len(values) != len(fields):
                raise ValueError(f'{path}: wrong column count near line {reader.line_num}')
            if any('\x00' in value for value in values):
                raise ValueError(f'{path}: NUL bytes are not permitted')
            result.append(dict(zip(fields, values)))
    return result


def write_csv(path, fields, records):
    """Replace a whole CSV atomically; failures leave the old file intact."""
    path = safe_path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8',
                                         dir=path.parent, prefix='.mcd-', delete=False) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fields)
            writer.writeheader()
            writer.writerows(records)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


@contextmanager
def locked(root):
    """Serialize CLI reads/writes. Editors outside the CLI must coordinate."""
    path = safe_path(root / '.mcd.lock')
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Workspace is busy; retry after the other command finishes') from None
        yield
    finally:
        os.close(fd)
