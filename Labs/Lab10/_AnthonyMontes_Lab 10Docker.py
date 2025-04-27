import time
import threading
import docker

client = docker.from_env()

# List all container names and status
def list_running_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        print(f"{container.name} - {container.status}")

# Monitor container status and restart if not running
def monitor_container(container_name):
    failure_count = 0
    max_failures = 3
    last_status = None

    while True:
        try:
            container = client.containers.get(container_name)
            container.reload()
            status = container.status

            if status != 'running':
                print(f"{container_name} is not running. Attempting restart...")

                container.start()
                time.sleep(10)
                container.reload()

                if container.status == 'running':
                    print(f"{container_name} restarted successfully.")
                    failure_count = 0
                else:
                    print(f"{container_name} failed to restart.")
                    failure_count += 1

                    if failure_count >= max_failures:
                        print(f"{container_name} has failed {max_failures} times. Stopping monitoring.")
                        break
            else:
                if status != last_status:
                    print(f"{container_name} is running.")
                failure_count = 0

            last_status = status

        except docker.errors.NotFound:
            print(f"{container_name} not found.")
        except Exception as e:
            print(f"Error monitoring {container_name}: {e}")

        time.sleep(30)

# Scheduled restart every 24 hours
def restart_container_daily(container_name):
    while True:
        try:
            container = client.containers.get(container_name)
            print(f"Scheduled restart for {container_name}...")
            container.restart()
        except Exception as e:
            print(f"Error restarting {container_name}: {e}")
        time.sleep(86400)  # 24 hours

# Start containers
def start_specific_containers(container_names):
    for name in container_names:
        try:
            container = client.containers.get(name)
            container.reload()
            if container.status != 'running':
                print(f"Starting container: {name}")
                container.start()
            else:
                print(f"{name} is already running.")
        except Exception as e:
            print(f"Error starting {name}: {e}")

# Stop containers
def stop_specific_containers(container_names):
    for name in container_names:
        try:
            container = client.containers.get(name)
            container.reload()
            if container.status == 'running':
                print(f"Stopping container: {name}")
                container.stop()
            else:
                print(f"{name} is already stopped.")
        except Exception as e:
            print(f"Error stopping {name}: {e}")

# Run the full setup
if __name__ == "__main__":
    containers_to_manage = ["mysql", "adminer"]

    print("=== Docker Container Monitor ===")
    list_running_containers()

    for name in containers_to_manage:
        threading.Thread(target=monitor_container, args=(name,), daemon=True).start()
        threading.Thread(target=restart_container_daily, args=(name,), daemon=True).start()

    while True:
        time.sleep(60)
