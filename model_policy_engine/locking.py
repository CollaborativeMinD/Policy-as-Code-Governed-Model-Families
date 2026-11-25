"""Serialize admission, rollback state, and local publication across processes."""
from contextlib import contextmanager
import os
from pathlib import Path
import threading

_lock = threading.RLock()
_local = threading.local()


@contextmanager
def state_transaction(directory):
    directory = Path(directory).resolve()
    with _lock:
        held = getattr(_local, "held", set())
        if directory in held:
            yield
            return
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / ".admission.lock").open("a+b") as stream:
            if os.name == "nt":
                import msvcrt
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX)
            _local.held = held | {directory}
            try:
                yield
            finally:
                _local.held = held
                if os.name == "nt":
                    stream.seek(0)
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream, fcntl.LOCK_UN)

