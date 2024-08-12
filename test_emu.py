import os
import subprocess
import platform

# Path to the Android SDK
ANDROID_SDK_PATH = r'C:\Users\yra39\AppData\Local\Android\Sdk'
CMDLINE_TOOLS_PATH = os.path.join(ANDROID_SDK_PATH, 'cmdline-tools', 'latest', 'bin')
SDK_MANAGER_PATH = os.path.join(ANDROID_SDK_PATH, 'cmdline-tools', 'latest', 'bin', 'sdkmanager.bat')
AVD_MANAGER_PATH = os.path.join(ANDROID_SDK_PATH, 'cmdline-tools', 'latest', 'bin', '.\\avdmanager.bat')


class Terminal:

    @staticmethod
    def execute_command(cls, command):
        """Open PowerShell and execute a command."""
        try:
            if platform.system() == 'Windows':
                # Execute command in PowerShell
                # We use '/c' to run the command and terminate
                result = subprocess.run(['powershell', '-Command', command], shell=True)
                return result
            else:
                print("This method is currently only supported on Windows.")
                return None
        except Exception as e:
            print(f"Error: {e}")


def list_available_system_images():
    """List available system images using sdkmanager."""
    try:
        result = subprocess.run([SDK_MANAGER_PATH, '--list'], capture_output=True, text=True, check=True)
        # Filter lines that contain 'system-images\'
        system_images = [line for line in result.stdout.splitlines() if 'system-images\\' in line]
        return system_images
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")


def list_available_devices():
    """List available devices using avdmanager."""
    try:
        result = subprocess.run([AVD_MANAGER_PATH, 'list', 'devices'], capture_output=True, text=True, check=True)
        list_devices = [line for line in result.stdout.splitlines() if 'id: ' in line]
        return list_devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command: {' '.join(e.cmd)}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")


def create_emulator_command(name, system_image, device):
    """Create an emulator command using."""
    return f"{CMDLINE_TOOLS_PATH}\\avdmanager.bat create avd -n {name} -k {system_image} -d {device}"



# Example usage


if __name__ == "__main__":
    terminal = Terminal()
    terminal.execute_command(create_emulator_command("test2", '"system-images;android-35;google_apis_playstore_ps16k;x86_64"', "pixel_6"))

    # create_emulator("test2", '"system-images;android-35;google_apis_playstore_ps16k;x86_64"', "pixel_6")

    # system_images = list_available_system_images()
    # devices = list_available_devices()
    # print("Available system images:")
    # for idx, image in enumerate(system_images):
    #     print(f"{idx}: {image}")
    #
    # print("Available devices:")
    # for idx, device in enumerate(devices):
    #     print(f"{idx}: {device}")
    #
    # selected_image = input("Select a system image number: ")
    # print(f"Selected system image: {selected_image}")
    #
    # selected_device = input("Select a device: ")
    #
    # print(f"Selected device: {selected_device}")

    # create_emulator(selected_image, selected_device)

    # # List available system images
    # system_images = list_available_system_images()
    #
    # # List available devices
    # devices = list_available_devices()
    #
    # #show installed system images and let user choose one
    # if system_images:
    #     print("Available system images:")
    #     for idx, image in enumerate(system_images):
    #         print(f"{idx}: {image}")
    #
    #     image_index = int(input("Select a system image number: "))
    #     selected_image = system_images[image_index].split()[0]
    #     print(f"Selected system image: {selected_image}")
    #
    #     if devices:
    #         print("Available devices:")
    #         for idx, device in enumerate(devices):
    #             print(f"{idx}: {device}")
    #
    #         device_index = int(input("Select a device number: "))
    #         selected_device = devices[device_index].split()[0]
    #         print(f"Selected device: {selected_device}")
    #
    #         create_emulator(selected_image, selected_device)
    #     else:
    #         print("No devices found.")
    # else:
    #     print("No system images found.")


