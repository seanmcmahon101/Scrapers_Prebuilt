def itemlistscraper():
    """
    Scrapes an item list from a specified URL, downloads the report as an Excel file, 
    and returns the data as a pandas DataFrame.

    The function navigates to a specific URL, interacts with various elements on the 
    webpage to generate a report, downloads the report in Excel format, and reads the 
    downloaded file into a pandas DataFrame. If no new file is downloaded within a 
    specified timeout period, it returns None.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the downloaded Excel file.
        None: If no file is downloaded or an error occurs during the process.

    Raises:
        Exception: Catches and logs any exceptions that occur during the scraping process.
    """

    def get_latest_file_with_item_name(directory, timeout=60):
        """
        Waits for the latest Excel file with 'Item' in its name to appear in the specified directory.

        This function continuously checks the specified directory for an Excel file with 
        'Item' in its name until the timeout period elapses.

        Parameters:
            directory (str): The path to the directory where the file is expected to be downloaded.
            timeout (int, optional): The maximum time to wait for the file to appear, in seconds. Default is 60 seconds.

        Returns:
            str: The full path to the latest file with 'Item' in its name if found within the timeout period.
            None: If no such file is found within the timeout period.
        """
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            for file_name in os.listdir(directory):
                if "Item" in file_name and file_name.endswith(".xlsx"):
                    return os.path.join(directory, file_name)
            time.sleep(1)
        return None

    try:
        item_url = "http://hffsuk02/Reports/report/ReportsUK/Item/ItemListMDeptWC"
        logger.debug(f"Starting itemlistscraper with URL: {item_url}")
        options = configure_options()
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

        driver.get(item_url)
        driver.fullscreen_window()
        time.sleep(5)

        frames = driver.find_elements(By.TAG_NAME, "iframe")
        if frames:
            driver.switch_to.frame(frames[0])
            logger.debug("Navigated to frame")

        dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='ReportViewerControl_ctl04_ctl03_ctl01']")))
        driver.execute_script("arguments[0].click();", dropdown_button)
        time.sleep(4)

        select_all_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ReportViewerControl_ctl04_ctl03_divDropDown_ctl00")))
        driver.execute_script("arguments[0].click();", select_all_button)
        time.sleep(2)

        view_report_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ReportViewerControl_ctl04_ctl00")))
        driver.execute_script("arguments[0].click();", view_report_button)
        time.sleep(18)

        excel_dropdown_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ReportViewerControl_ctl05_ctl04_ctl00_ButtonImg")))
        driver.execute_script("arguments[0].click();", excel_dropdown_button)
        time.sleep(3)

        excel_download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ReportViewerControl_ctl05_ctl04_ctl00_Menu > div:nth-child(2) > a")))
        driver.execute_script("arguments[0].click();", excel_download_button)
        logger.info("Download initiated")

        latest_file = get_latest_file_with_item_name(downloads_dir)
        driver.quit()

        if latest_file:
            logger.info(f"File downloaded successfully: {latest_file}")
            df = pd.read_excel(latest_file)
            return df
        else:
            logger.warning("No new file was downloaded")
            return None
    except Exception as e:
        logger.error(f"Error in itemlistscraper: {e}", exc_info=True)
        if 'driver' in locals():
            driver.quit()
        return None
