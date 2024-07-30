import subprocess
import os
import time

from GLOBAL import GLOBAL

# Path to your Android SDK
ANDROID_SDK_PATH = GLOBAL.PATH.ANDROID_SDK_PATH

# Path to the emulator executable
EMULATOR_PATH = GLOBAL.PATH.ANDROID_EMULATOR_PATH

# Path to the AVD (Android Virtual Device) configuration
AVD_PATH = os.path.join(ANDROID_SDK_PATH, 'avd')

# Name of the AVD to create and launch
AVD_NAME = 'MyEmulator'

# Path to `avdmanager` (adjust based on SDK structure)
AVDMANAGER_PATH = os.path.join(ANDROID_SDK_PATH, 'cmdline-tools', 'latest', 'bin', 'avdmanager')

# Function to create an Android Virtual Device (AVD)
def create_avd():
    create_avd_command = [
        AVDMANAGER_PATH,
        'create', 'avd',
        '-n', AVD_NAME,
        '-k', 'system-images;android-30;google_apis;x86_64',
        '--sdcard', '512M'
    ]
    subprocess.run(create_avd_command, check=True)

# Function to launch the emulator
def launch_emulator():
    # Start the emulator
    subprocess.Popen([EMULATOR_PATH, '-avd', AVD_NAME])

    # Wait for the emulator to fully boot
    print("Waiting for emulator to boot...")
    time.sleep(60)  # Adjust the sleep time if needed

if __name__ == "__main__":
    # Create AVD
    if not os.path.exists(os.path.join(AVD_PATH, AVD_NAME + '.avd')):
        print("Creating AVD...")
        create_avd()
    else:
        print("AVD already exists.")

    # Launch the emulator
    print("Launching Emulator...")
    launch_emulator()
