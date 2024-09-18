from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager  

# تابع برای راه‌اندازی مرورگر کروم با درایور مناسب  
def start_chrome_driver():  
    # دانلود و نصب ChromeDriver به صورت خودکار  
    driver = webdriver.Chrome(ChromeDriverManager().install())  
    
    # به URL دلخواه منتقل می‌شود  
    driver.get("https://www.google.com")  
    
    # انجام سایر کارها ...  
    # به عنوان مثال، کار با فرم‌ها و یا استخراج داده‌ها    
    return driver  

# تست تابع  
if __name__ == "__main__":  
    driver = start_chrome_driver()  
    
    # تا زمانی که کاربر پنجره را ببندد، برنامه همچنان اجرا می‌شود  
    input("برای بستن پنجره Enter را بزنید...")  
    driver.quit()  # بستن مرورگر
