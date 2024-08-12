import re
import subprocess

from proxy import Proxy, EmptyProxy
from utils.worker import WorkerThread

from GLOBAL import GLOBAL


class Terminal:

    @staticmethod
    def execute_command(command):
        """Open PowerShell and execute a command."""
        try:

            # Execute command in PowerShell
            # We use '/c' to run the command and terminate
            result = subprocess.run(['powershell', '-Command', command], shell=True)
            return result

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def available_system_images():
        """List available system images using sdkmanager."""
        try:
            result = subprocess.run([GLOBAL.PATH.SDK_MANAGER_PATH, '--list'], capture_output=True, text=True,
                                    check=True)
            # Filter lines that contain 'system-images\'
            system_images = [line for line in result.stdout.splitlines() if 'system-images\\' in line]
            formatted_system_images = []
            for system_image_string in system_images:
                parts = [part.strip() for part in system_image_string.split('|')]
                if len(parts) == 4:
                    program_name = parts[0]
                    num = parts[1]
                    human_name = parts[2]
                    path = parts[3]
                    formatted_system_images.append(
                        {'program_name': program_name, 'num': num, 'human_name': human_name, path: path})

            return formatted_system_images
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Output: {e.output}")
            print(f"Error: {e.stderr}")

    @staticmethod
    def list_available_devices():
        """List available devices using avdmanager."""
        try:
            result = subprocess.run([GLOBAL.PATH.AVD_MANAGER_PATH, 'list', 'devices'], capture_output=True, text=True,
                                    check=True)
            list_devices = [re.search(r'"([^"]*)"', line).group(1) for line in result.stdout.splitlines() if
                            'id: ' in line]
            return list_devices
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Output: {e.output}")
            print(f"Error: {e.stderr}")

    @classmethod
    def install_default_system_image(cls):
        """Install the System Image: sdkmanager "system-images;android-35;google_apis_playstore_ps16k;x86_64"."""
        result = cls.execute_command(
            f'{GLOBAL.PATH.SDK_MANAGER_PATH} --install "system-images;android-35;google_apis_playstore_ps16k;x86_64"')
        return result

    @classmethod
    def list_initialized_emulators(cls) -> list:
        """List initialized emulators using emulator -list-avds."""
        try:
            # Define the command
            command = f'{GLOBAL.PATH.ANDROID_EMULATOR_PATH}\\emulator -list-avds'

            # Execute the command
            result = subprocess.run(command, shell=True, text=True, capture_output=True)

            # Check if the command was successful
            if result.returncode == 0:
                # Process stdout to extract emulator names only
                lines = result.stdout.splitlines()
                # Filter out any empty or None values
                emulators = [line for line in lines if line.strip()]

                print("Initialized emulators:")
                result_list = []
                for emulator in emulators:
                    if "SDE" in emulator:
                        print(emulator)
                        result_list.append(emulator)

                return result_list
            else:
                print(f"Error: {result.stderr}")

        except Exception as e:
            print(f"An error occurred while listing emulators: {e}")

    @classmethod
    def open_emulator(cls, avd_name):
        """Open an emulator using emulator -avd."""
        worker = WorkerThread(cls.execute_command, f'{GLOBAL.PATH.ANDROID_EMULATOR_PATH}\\emulator -avd {avd_name}')
        worker.start()
        worker.join()

    @classmethod
    def update_parameters(cls, avd_name, account_name, proxy: Proxy | EmptyProxy):
        # TODO: implement account name
        # command = f''
        # worker = WorkerThread(cls.execute_command, command)
        # worker.start()
        # worker.join()

        if proxy is not EmptyProxy:
            command = f'{GLOBAL.PATH.AVD_MANAGER_PATH} create avd -n {avd_name} -p {proxy}'
            worker = WorkerThread(cls.execute_command, command)
            worker.start()
            worker.join()

        command = f'exit'
        worker = WorkerThread(cls.execute_command, command)
        worker.start()
        worker.join()


"""
test
"""
if __name__ == '__main__':
    terminal = Terminal()

    print(terminal.open_emulator('SDE1'))
