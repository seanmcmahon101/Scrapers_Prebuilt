"""
These are helper functions that aid the scraper functions by configuring browser options, 
retrieving the latest downloaded file, and waiting for a file download to complete.
"""

def configure_options():
    """
    Configures and returns the ChromeOptions for the WebDriver.

    This function sets various options for the Chrome WebDriver, including disabling 
    the GPU, allowing running insecure content, disabling web security, and treating 
    insecure origins as secure. It also sets preferences for file downloads, such as 
    the default download directory, disabling the download prompt, and enabling safe 
    browsing.

    Returns:
        selenium.webdriver.ChromeOptions: Configured options for the Chrome WebDriver.
    """
    options = Options()
    for arg in ["--disable-gpu", "--allow-running-insecure-content", "--disable-web-security", "--unsafely-treat-insecure-origin-as-secure=http://hffsuk02"]:
        options.add_argument(arg)
    prefs = {
        "download.default_directory": downloads_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-features=InsecureDownloadWarnings")
    return options

def get_latest_file_path(directory, extension=".xlsx"):
    """
    Gets the path of the latest file in the specified directory with the specified extension.

    This function searches the specified directory for files with the given extension 
    and returns the path of the most recently modified file.

    Parameters:
        directory (str): The path to the directory to search for files.
        extension (str, optional): The file extension to search for. Default is ".xlsx".

    Returns:
        str: The full path to the latest file with the specified extension if found.
        None: If no such file is found.
    """
    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(extension)]
    return max(files, key=os.path.getctime) if files else None

def wait_for_file_download(timeout=120):
    """
    Waits for a new file to be downloaded in the specified directory within the given timeout.

    This function continuously checks the specified directory for any new files that 
    appear within the timeout period. If a new file with the ".xlsx" extension is found, 
    its path is returned.

    Parameters:
        timeout (int, optional): The maximum time to wait for a file download, in seconds. Default is 120 seconds.

    Returns:
        str: The full path to the newly downloaded file if found within the timeout period.
        None: If no new file is downloaded within the timeout period.
    """
    initial_files = set(os.listdir(downloads_dir))
    elapsed_time = 0
    while elapsed_time < timeout:
        current_files = set(os.listdir(downloads_dir))
        new_files = current_files - initial_files
        if new_files:
            new_file = new_files.pop()
            new_file_path = os.path.join(downloads_dir, new_file)
            if new_file_path.endswith(".xlsx"):
                return new_file_path
        time.sleep(1)
        elapsed_time += 1
    return None
