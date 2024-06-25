def itemlistscraper():
    def get_latest_file_with_item_name(directory, timeout=60):
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
