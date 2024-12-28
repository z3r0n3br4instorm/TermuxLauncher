import subprocess

def search_package(package_name):
    try:
        command = f"sudo dumpsys package {package_name} | grep -i Main | grep filter"
        result = subprocess.check_output(command, shell=True, text=True)
        intents = result.splitlines()
        if intents:
            main_intent = intents[0].split()[1]
            return main_intent
        else:
            print(f"No Main activity found for {package_name}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error searching package {package_name}: {e}")
        return package_name

def launch_package(package_name):
    main_intent = search_package(package_name)
    if main_intent and len(main_intent.split(".")):
        try:
            launch_command = f"am start {main_intent}"
            subprocess.run(launch_command, shell=True)
            print(f"Launched {package_name} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error launching package {package_name}: {e}")

def getPackageNAme(appName):
    try:
        command = f"sudo pm list packages | grep -i {appName}"
        result = subprocess.check_output(command, shell=True, text=True)
        packages = result.splitlines()
        if packages:
            package_name = packages[0].split(":")[1]
            return package_name
        else:
            print(f"No package found for {appName}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error searching package {appName}: {e}")
        return None

while True:
    app_name = input("> ")
    # find package name
    package_name = getPackageNAme(app_name)
    launch_package(package_name)
