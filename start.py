#!/usr/bin/env python3
"""Bootstrap and run the SiliconCrew backend, frontend, and Docker engine."""

import hashlib
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
VENV_PYTHON = VENV / "bin" / "python"
FRONTEND = ROOT / "frontend"


def run(command, *, cwd=ROOT, env=None):
    print("$", " ".join(map(str, command)), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def ensure_environment():
    if not shutil.which("node") or not shutil.which("npm"):
        raise RuntimeError("Node.js and npm are required; install them and rerun this script.")

    version = None
    if VENV_PYTHON.exists():
        result = subprocess.run(
            [str(VENV_PYTHON), "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            version = result.stdout.strip()

    if version != "3.14":
        python314 = shutil.which("python3.14")
        if not python314:
            raise RuntimeError("Python 3.14 is required; install python3.14 and rerun this script.")
        run([python314, "-m", "venv", "--clear", str(VENV)])

    requirements = ROOT / "requirements.txt"
    fingerprint = hashlib.sha256(b"python=3.14\n" + requirements.read_bytes()).hexdigest()
    stamp = VENV / ".requirements.sha256"
    if not stamp.exists() or stamp.read_text().strip() != fingerprint:
        run([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(requirements)])
        stamp.write_text(fingerprint + "\n")

    lockfile = FRONTEND / "package-lock.json"
    installed_lock = FRONTEND / "node_modules" / ".package-lock.json"
    next_binary = FRONTEND / "node_modules" / ".bin" / "next"
    if (
        not next_binary.exists()
        or not installed_lock.exists()
        or lockfile.stat().st_mtime > installed_lock.stat().st_mtime
    ):
        npm = shutil.which("npm")
        if not npm:
            raise RuntimeError("Node.js and npm are required; install them and rerun this script.")
        run([npm, "ci"], cwd=FRONTEND)

    env_file = ROOT / ".env"
    example = ROOT / ".env.example"
    if not env_file.exists() and example.exists():
        shutil.copyfile(example, env_file)
        print("Created .env from .env.example; add your LLM provider API key there.", flush=True)


def ensure_docker():
    docker = shutil.which("docker")
    if not docker:
        raise RuntimeError("Docker CLI not found; install Docker and rerun this script.")

    def info():
        return subprocess.run(
            [docker, "info"], capture_output=True, text=True, timeout=30
        )

    result = info()
    if result.returncode == 0:
        print("Docker is ready.", flush=True)
        return

    error = (result.stderr + result.stdout).strip()
    if "permission denied" in error.lower():
        raise RuntimeError(
            "Docker socket permission denied. Run `sudo usermod -aG docker $USER`, "
            "then log out and back in before starting the app."
        )

    systemctl = shutil.which("systemctl")
    if not systemctl:
        raise RuntimeError(f"Docker is unavailable: {error}")
    command = [systemctl, "start", "docker"]
    if os.geteuid() != 0:
        sudo = shutil.which("sudo")
        if not sudo:
            raise RuntimeError("Starting Docker requires sudo or root privileges.")
        command.insert(0, sudo)

    print("Starting Docker (sudo may prompt for your password)...", flush=True)
    subprocess.run(command, check=True)
    result = info()
    if result.returncode != 0:
        raise RuntimeError(f"Docker did not become ready: {(result.stderr + result.stdout).strip()}")
    print("Docker is ready.", flush=True)


def wait_for_backend(process):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Backend exited during startup (status {process.returncode}).")
        try:
            with urlopen("http://127.0.0.1:8000/api/health", timeout=1) as response:
                if response.status == 200:
                    return
        except (URLError, TimeoutError, OSError):
            time.sleep(0.25)
    raise RuntimeError("Backend did not become healthy within 45 seconds.")


def launch(command, *, cwd, env):
    print("$", " ".join(map(str, command)), flush=True)
    return subprocess.Popen(command, cwd=cwd, env=env, start_new_session=True)


def stop(process):
    if process is None or process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=10)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def main():
    ensure_environment()
    ensure_docker()

    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(VENV)
    env["PATH"] = str(VENV / "bin") + os.pathsep + env.get("PATH", "")
    env["PYTHONUNBUFFERED"] = "1"

    backend = frontend = None
    try:
        backend = launch(
            [str(VENV_PYTHON), "-m", "uvicorn", "api:app", "--reload", "--host", "127.0.0.1", "--port", "8000"],
            cwd=ROOT,
            env=env,
        )
        wait_for_backend(backend)
        npm = shutil.which("npm")
        frontend = launch([npm, "run", "dev"], cwd=FRONTEND, env=os.environ.copy())
        print("\nSiliconCrew is running: http://localhost:3000", flush=True)
        print("Press Ctrl+C to stop the frontend and backend.\n", flush=True)

        while True:
            for name, process in (("Backend", backend), ("Frontend", frontend)):
                status = process.poll()
                if status is not None:
                    raise RuntimeError(f"{name} exited with status {status}.")
            time.sleep(0.5)
    finally:
        stop(frontend)
        stop(backend)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping SiliconCrew...", flush=True)
    except (RuntimeError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        print(f"Startup failed: {error}", file=sys.stderr, flush=True)
        sys.exit(1)
