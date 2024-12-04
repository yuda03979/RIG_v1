import importlib.resources
import os
import shutil

from RIG.globals import GLOBALS
import subprocess
import time
import requests
import atexit
import os
import signal
import os
import subprocess
from pathlib import Path



class LlamaCppServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.process = None
        self.llama_server_path = GLOBALS.llama_server_path


    def start(self):

        if not os.path.exists(self.llama_server_path) or not os.access(self.llama_server_path, os.X_OK):
            print(f"{self.llama_server_path} does not exist or is not executable. Running make...")

            # Run make llama-server
            make_cmd = ['make', 'llama-server']
            try:
                make_process = subprocess.run(
                    make_cmd,
                    cwd=self.llama_server_path,
                    check=True,  # Raises CalledProcessError if the command fails
                    capture_output=True,
                    text=True
                )
                print("Successfully built llama-server")
            except subprocess.CalledProcessError as e:
                print(f"Error building llama-server: {e}")
                print(f"Stdout: {e.stdout}")
                print(f"Stderr: {e.stderr}")
                raise

        # Proceed with starting the server
        server_cmd = [
            self.llama_server_path,
            '-m', GLOBALS.gpt_model_path,
            '-c', str(GLOBALS.max_context_length),
            '--host', self.host,
            '--port', str(self.port),
            # '--temp', 0.0,
            '--no-mmap',
            '--seed', '0',
            # '--max-tokens', str(GLOBALS.max_new_tokens)
        ]

        try:
            self.process = subprocess.Popen(
                server_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                start_new_session=True
            )

            def log_server_output(process):
                for line in process.stdout:
                    print(f"Server Log: {line.strip()}")
                for line in process.stderr:
                    print(f"Server Error: {line.strip()}")

            import threading
            log_thread = threading.Thread(target=log_server_output, args=(self.process,), daemon=True)
            log_thread.start()
            time.sleep(5)

            self._wait_for_server()

            def log_output():
                while self.process and self.process.poll() is None:
                    try:
                        output = self.process.stdout.readline()
                        if output:
                            print(f"Server Output: {output.decode().strip()}")
                    except Exception:
                        break

            # Start logging in a separate thread
            import threading
            output_thread = threading.Thread(target=log_output, daemon=True)
            output_thread.start()

            # Register cleanup function
            atexit.register(self.stop)

            print(f"Server started on {self.host}:{self.port}")
            return self

        except Exception as e:
            print(f"Failed to start server: {e}")
            return None

    def _wait_for_server(self, timeout=60 * 3):
        """
        Wait for the server to be ready with extended timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f'http://{self.host}:{self.port}/health', timeout=2)
                if response.status_code == 200:
                    return
            except requests.RequestException:
                time.sleep(1)

        raise RuntimeError("Server did not start within the expected time")

    def stop(self):
        if self.process:
            try:
                # Try graceful shutdown
                try:
                    requests.post(f'http://{self.host}:{self.port}/shutdown', timeout=2)
                except:
                    pass

                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

                # Wait for termination
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)

                print("Server stopped successfully")
            except Exception as e:
                print(f"Error stopping server: {e}")
            finally:
                self.process = None


class GPTServer:

    def __init__(self):
        self.server = LlamaCppServer().start()
        if not self.server:
            raise RuntimeError("Failed to start server")

    def __del__(self):
        if hasattr(self, 'server'):
            self.server.stop()

    def predict(self, prompt, host='localhost', port=8080):
        try:
            response = requests.post(f'http://{host}:{port}/v1/chat/completions',
                                     json={
                                         'messages': [{'role': 'user', 'content': prompt}],
                                         'temperature': 0.0
                                     })
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Query failed: {e}")
            raise
