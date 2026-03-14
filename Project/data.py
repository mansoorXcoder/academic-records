from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import re
import random
import json

def setup_driver():
    """Setup Chrome driver with enhanced anti-detection measures"""
    options = Options()
    
    # Ask user for browser mode
    mode = input("Run in headless mode? (y/n, recommend 'n' for Meesho): ").strip().lower()
    if mode == 'y':
        options.add_argument("--headless=new")
        print("✅ Running in background mode")
    else:
        print("✅ Running with visible browser (you can see what's happening)")
    
    # Enhanced anti-detection options
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", [
        "enable-automation",
        "enable-logging"
    ])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Browser settings
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # More realistic browser fingerprint
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-3d-apis")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    # Updated user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={user_agent}")
    
    # Additional CDP commands to mask automation
    options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
    
    try:
        # Initialize Chrome with options
        driver = webdriver.Chrome(options=options)
        
        # Execute CDP commands to mask automation
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": user_agent,
            "platform": "Win32",
            "userAgentMetadata": {
                "platform": "Windows",
                "platformVersion": "10.0",
                "architecture": "x86",
                "model": "",
                "mobile": False
            }
        })
        
        # Additional anti-detection measures
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set additional headers
        driver.execute_cdp_cmd('Network.enable', {})
        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
            'headers': {
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'DNT': '1'
            }
        })
        
        print("✅ Browser initialized successfully with enhanced anti-detection")
        return driver
        
    except Exception as e:
        print(f"❌ Error initializing browser: {str(e)}")
        print("\n💡 Common fixes:")
        print("  1. Install/Update ChromeDriver: pip install --upgrade webdriver-manager")
        print("  2. Update Chrome browser to latest version")
        print("  3. Install selenium: pip install --upgrade selenium")
        print("  4. Check if Chrome is installed in the default location")
        raise

def detect_site(url):
    """Detect if URL is Meesho or Flipkart"""
    url_lower = url.lower()
    if 'meesho.com' in url_lower:
        return 'Meesho'
    elif 'flipkart' in url_lower or 'fkrt.in' in url_lower:
        return 'Flipkart'
    return None

def resolve_shortened_url(driver, url):
    """Resolve shortened URLs to full URLs"""
    try:
        if 'amzn.in' in url or 'amzn.to' in url or 'fkrt.in' in url:
            print(f"    🔗 Resolving shortened URL...")
            driver.get(url)
            human_delay(2, 3)
            resolved_url = driver.current_url
            print(f"    ✅ Resolved to: {resolved_url[:70]}...")
            return resolved_url
        return url
    except Exception as e:
        print(f"    ⚠️ Could not resolve URL: {str(e)[:50]}")
        return url

def human_delay(min_sec=1, max_sec=3):
    """Add random human-like delay"""
    time.sleep(random.uniform(min_sec, max_sec))

def check_access_denied(driver):
    """Check if access is denied by the website"""
    if "Access Denied" in driver.title or "Access Denied" in driver.page_source:
        print("    🔒 Access Denied: Meesho has blocked automated access")
        return True
    return False

def handle_meesho_verification(driver):
    """Handle Meesho's verification challenges if they appear"""
    try:
        # Check for Cloudflare or other verification
        if "challenge" in driver.current_url or "verification" in driver.page_source.lower():
            print("    🔄 Verification required. Please complete the verification in the browser...")
            input("    🚦 Press Enter after completing verification in the browser...")
            return True
    except:
        pass
    return False

def scrape_meesho(driver, url, max_retries=3):
    """Scrape Meesho product reviews with enhanced error handling and retries"""
    reviews = []
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n    🔄 Attempt {attempt}/{max_retries} - Loading Meesho product page...")
            
            # Load the page with randomized delays
            driver.get("about:blank")
            human_delay(1, 2)
            driver.get(url)
            
            # Check for access denied
            if check_access_denied(driver):
                if attempt < max_retries:
                    print(f"    ⏳ Waiting before retry {attempt + 1}...")
                    time.sleep(5)  # Wait longer between retries
                    continue
                else:
                    print("    ❌ Max retries reached. Meesho is blocking automated access.")
                    print("    💡 Try these solutions:")
                    print("       1. Run in non-headless mode (answer 'n' when asked)")
                    print("       2. Complete any CAPTCHA manually in the browser")
                    print("       3. Try again later")
                    return []
            
            # Handle verification if needed
            if handle_meesho_verification(driver):
                # After verification, reload the page
                driver.get(url)
                human_delay(3, 5)
                
                # Check again after verification
                if check_access_denied(driver):
                    continue
            
            # Check if we're on a product page
            if "product" not in driver.current_url.lower():
                print(f"    ⚠️ Not a product page. Current URL: {driver.current_url[:100]}...")
                if "search" in driver.current_url:
                    print("    🔍 Search results page detected. Please provide a direct product URL.")
                return []
            
            # Get product name
            product_name = "N/A"
            try:
                product_name = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1[class*='title'], h1[class*='Title'], .product-title"))
                ).text.strip()
                print(f"    ✅ Product found: {product_name[:50]}...")
            except Exception as e:
                print(f"    ⚠️ Could not find product title: {str(e)[:50]}")
            
            # Scroll down to load more content
            print("    🔄 Loading page content...")
            for i in range(3):
                driver.execute_script(f"window.scrollTo(0, {i * 500});")
                human_delay(1, 2)
            
            # Try to find and click on reviews section
            try:
                reviews_section = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Ratings') or contains(text(), 'Reviews')]"))
                )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", reviews_section)
                human_delay(1, 2)
                reviews_section.click()
                human_delay(2, 3)
            except Exception as e:
                print(f"    ⚠️ Could not find/click reviews section: {str(e)[:50]}")
            
            # Try to load more reviews by scrolling
            print("    🔄 Loading more reviews...")
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scroll_attempts = 5
            
            while scroll_attempts < max_scroll_attempts:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                human_delay(2, 3)
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                last_height = new_height
                
                # Check for "Load More" button and click it
                try:
                    load_more = driver.find_element(By.XPATH, "//button[contains(text(), 'Load More')]")
                    if load_more.is_displayed():
                        driver.execute_script("arguments[0].click();", load_more)
                        human_delay(2, 3)
                except:
                    pass
            
            # Parse the page
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Try different selectors for review containers
            review_containers = []
            possible_selectors = [
                "div[class*='review']", 
                "div[class*='comment']",
                ".review-item",
                ".comment-item"
            ]
            
            for selector in possible_selectors:
                review_containers = soup.select(selector)
                if review_containers:
                    break
            
            print(f"    📊 Found {len(review_containers)} review(s)")
            
            if not review_containers:
                print("    ⚠️ No reviews found. The page structure might have changed.")
                # Save page for debugging
                with open("meesho_debug.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("    📁 Saved page source as 'meesho_debug.html' for inspection")
                return []
            
            # Extract reviews
            for idx, container in enumerate(review_containers[:50], 1):  # Limit to 50 reviews max
                try:
                    review_id = f"MEE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}"
                    
                    # Rating
                    rating = "N/A"
                    rating_elem = container.find("div", class_=re.compile("rating|stars|Rating"))
                    if rating_elem:
                        rating_text = rating_elem.get_text(strip=True)
                        # Extract first number from rating text (e.g., "4.5" from "4.5 ★★★★★")
                        rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                        if rating_match:
                            rating = rating_match.group(1)
                    
                    # Skip if rating is 4 or 5
                    if rating != "N/A" and float(rating) > 3:
                        continue
                    
                    # Review text
                    review_text = "N/A"
                    text_elem = container.find("div", class_=re.compile("content|text|comment"))
                    if not text_elem:
                        text_elem = container.find("p")
                    if text_elem:
                        review_text = text_elem.get_text(" ", strip=True)
                    
                    # Skip if no review text
                    if not review_text or len(review_text) < 5:
                        continue
                    
                    # Reviewer name
                    reviewer_name = "Anonymous"
                    name_elem = container.find("div", class_=re.compile("name|user|reviewer"))
                    if name_elem:
                        reviewer_name = name_elem.get_text(strip=True)
                    
                    # Date
                    date = "N/A"
                    date_elem = container.find("div", class_=re.compile("date|time"))
                    if date_elem:
                        date = date_elem.get_text(strip=True)
                    
                    # Review title (Meesho doesn't typically have titles)
                    review_title = ""
                    
                    reviews.append({
                        "Review_ID": review_id,
                        "Review_Title": review_title,
                        "Review_Text": review_text,
                        "Rating": rating,
                        "Date_Time": date,
                        "Reviewer_Name": reviewer_name,
                        "Location": "N/A",
                        "Product_Name": product_name[:100],
                        "Category": "N/A",
                        "Verified_Purchase": "N/A",
                        "Site": "Meesho"
                    })
                    
                    print(f"      ✅ Review {idx}: Rating {rating}")
                    
                except Exception as e:
                    print(f"      ❌ Review {idx} failed: {str(e)[:40]}")
                    continue
            
            # If we got here, we successfully scraped some reviews
            if reviews:
                return reviews
                
        except Exception as e:
            print(f"    ❌ Attempt {attempt} failed: {str(e)}")
            if attempt < max_retries:
                print(f"    ⏳ Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("    ❌ Max retries reached. Could not scrape Meesho reviews.")
                print("    💡 Try these solutions:")
                print("       1. Run in non-headless mode (answer 'n' when asked)")
                print("       2. Complete any CAPTCHA manually in the browser")
                print("       3. Try again later")
    
    return reviews

def scrape_flipkart(driver, url):
    """Scrape Flipkart reviews with updated selectors"""
    reviews = []
    
    try:
        print("    Loading Flipkart product page...")
        driver.get(url)
        human_delay(4, 6)
        
        wait = WebDriverWait(driver, 15)
        
        # Scroll to load content
        for i in range(3):
            driver.execute_script(f"window.scrollTo(0, {(i+1)*600});")
            human_delay(1, 2)
        
        # Get product name
        product_name = "N/A"
        product_selectors = [
            (By.CLASS_NAME, "B_NuCI"),
            (By.CLASS_NAME, "yhB1nd"),
            (By.TAG_NAME, "h1"),
            (By.CSS_SELECTOR, "span.VU-ZEz")
        ]
        
        for by, selector in product_selectors:
            try:
                elem = driver.find_element(by, selector)
                product_name = elem.text.strip()
                if product_name:
                    print(f"    ✅ Product: {product_name[:50]}...")
                    break
            except:
                continue
        
        # Try to click "View All Reviews"
        try:
            view_all_buttons = [
                (By.XPATH, "//div[contains(text(), 'All') and contains(text(), 'reviews')]"),
                (By.XPATH, "//span[contains(text(), 'All') and contains(text(), 'reviews')]"),
                (By.XPATH, "//div[contains(@class, 'col') and contains(text(), 'Ratings')]/..//div"),
            ]
            
            for by, selector in view_all_buttons:
                try:
                    button = driver.find_element(by, selector)
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    human_delay(1, 2)
                    driver.execute_script("arguments[0].click();", button)
                    print("    ✅ Clicked 'View All Reviews'")
                    human_delay(3, 4)
                    break
                except:
                    continue
        except Exception as e:
            print(f"    ℹ️ Scraping visible reviews only")
        
        # Scroll more after clicking
        for i in range(2):
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight - {i*500});")
            human_delay(1, 2)
        
        # Parse page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        print("    🔍 Analyzing page structure...")
        
        # Find review containers
        review_containers = soup.find_all("div", class_=re.compile("col.*12"))
        
        # Filter for actual reviews (must have rating)
        actual_reviews = []
        for container in review_containers:
            rating_elem = container.find("div", class_=re.compile("XQDdHH|_3LWZlK|hGSR34"))
            if rating_elem:
                actual_reviews.append(container)
        
        print(f"    📊 Found {len(actual_reviews)} review(s)")
        
        review_count = 0
        for container in actual_reviews:
            try:
                review_count += 1
                review_id = f"FK_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{review_count}"
                
                # Rating
                rating_elem = container.find("div", class_=re.compile("XQDdHH|_3LWZlK|hGSR34"))
                rating = rating_elem.get_text(strip=True) if rating_elem else "N/A"
                
                # Title
                title_elem = container.find("p", class_=re.compile("z9E0IG"))
                review_title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Text
                text_elem = container.find("div", class_=re.compile("ZmyHeo"))
                if not text_elem:
                    text_elem = container.find("div", {"class": ""})
                review_text = text_elem.get_text(strip=True) if text_elem else "N/A"
                
                # Reviewer name
                name_elem = container.find("p", class_=re.compile("_2NsDsF|_2sc7ZR"))
                reviewer_name = name_elem.get_text(strip=True) if name_elem else "N/A"
                
                # Date and location
                date_elems = container.find_all("p", class_=re.compile("_2NsDsF|_2sc7ZR"))
                date = "N/A"
                location = "N/A"
                
                for elem in date_elems:
                    text = elem.get_text(strip=True)
                    if any(m in text for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                        date = text
                    elif text != reviewer_name and len(text) < 50:
                        location = text
                
                # Verified purchase
                certified = container.find(text=re.compile("Certified Buyer"))
                verified_purchase = "Yes" if certified else "No"
                
                # Only add negative (1-2 stars) and neutral (3 stars) reviews
                if rating != "N/A" and float(rating) <= 3:
                    reviews.append({
                        "Review_ID": review_id,
                        "Review_Title": review_title,
                        "Review_Text": review_text,
                        "Rating": rating,
                        "Date_Time": date,
                        "Reviewer_Name": reviewer_name,
                        "Location": location,
                        "Product_Name": product_name[:100],
                        "Category": "N/A",
                        "Verified_Purchase": verified_purchase,
                        "Site": "Flipkart"
                    })
                
                print(f"      ✅ Review {review_count}: Rating {rating}")
                
            except Exception as e:
                print(f"      ❌ Review {review_count} failed: {str(e)[:40]}")
                continue
                
    except Exception as e:
        print(f"    ❌ Flipkart scraping error: {str(e)}")
        import traceback
        print(f"    📋 Details: {traceback.format_exc()[:200]}")
    
    return reviews

def main():
    """Main function"""
    print("\n" + "="*70)
    print("🛒 MEESHO & FLIPKART REVIEW SCRAPER")
    print("="*70)
    
    # Get URLs
    print("\n📝 Enter product URLs (comma-separated)")
    print("\n✅ Supported formats:")
    print("   Meesho:   https://meesho.com/product-name/p/abcdef")
    print("   Flipkart: https://www.flipkart.com/product-name/p/itm...")
    print()
    
    urls_input = input("Enter URLs: ").strip()
    
    if not urls_input:
        print("❌ No URLs provided!")
        return
    
    # Parse and validate URLs
    urls = [url.strip() for url in urls_input.split(',')]
    valid_urls = []
    
    print(f"\n🔍 Validating {len(urls)} URL(s)...")
    for url in urls:
        site = detect_site(url)
        if site:
            valid_urls.append((url, site))
            print(f"  ✅ {site} URL detected")
        else:
            print(f"  ❌ Unsupported URL: {url[:50]}...")
    
    if not valid_urls:
        print("\n❌ No valid URLs found!")
        return
    
    print(f"\n✅ {len(valid_urls)} valid URL(s) ready")
    proceed = input("Start scraping? (y/n): ").strip().lower()
    
    if proceed != 'y':
        print("❌ Cancelled")
        return
    
    # Setup driver
    print("\n⚙️ Setting up browser...")
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"\n❌ Failed to start browser: {str(e)}")
        return
    
    # Scrape all URLs
    all_reviews = []
    
    print("\n" + "="*70)
    print("🔄 SCRAPING IN PROGRESS")
    print("="*70)
    
    for idx, (url, site) in enumerate(valid_urls, 1):
        print(f"\n[{idx}/{len(valid_urls)}] Processing {site}...")
        print(f"  🔗 URL: {url[:65]}...")
        
        if site == 'Meesho':
            reviews = scrape_meesho(driver, url)
        elif site == 'Flipkart':
            reviews = scrape_flipkart(driver, url)
        else:
            continue
        
        all_reviews.extend(reviews)
        print(f"  ✅ Scraped: {len(reviews)} review(s)")
        
        if idx < len(valid_urls):
            wait_time = random.randint(5, 10)  # Slightly longer wait between sites
            print(f"  ⏳ Waiting {wait_time} seconds...")
            time.sleep(wait_time)
    
    # Close driver
    print("\n🔒 Closing browser...")
    driver.quit()
    
    # Save results
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.insert(0, 'SNo', range(1, len(df) + 1))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        meesho_count = len(df[df['Site'] == 'Meesho'])
        flipkart_count = len(df[df['Site'] == 'Flipkart'])
        
        filename = f"reviews_{timestamp}_M{meesho_count}_F{flipkart_count}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print("\n" + "="*70)
        print("✅ SCRAPING COMPLETED!")
        print("="*70)
        print(f"📊 Total Reviews: {len(df)}")
        if meesho_count > 0:
            print(f"   • Meesho: {meesho_count}")
        if flipkart_count > 0:
            print(f"   • Flipkart: {flipkart_count}")
        print(f"\n💾 File saved: {filename}")
        
        # Sample
        print("\n📋 Sample reviews:")
        print("-"*70)
        for i in range(min(3, len(df))):
            print(f"\n{i+1}. {df.iloc[i]['Site']} - Rating: {df.iloc[i]['Rating']}")
            print(f"   Review: {df.iloc[i]['Review_Text'][:100]}...")
    
    else:
        print("\n" + "="*70)
        print("⚠️ NO REVIEWS SCRAPED")
        print("="*70)
        print("\n🔍 Troubleshooting steps:")
        print("  1. ✅ Run in NON-headless mode (answer 'n') to see what's happening")
        print("  2. ✅ Check if the product has any reviews")
        print("  3. ✅ Try manually opening the URL in Chrome first")
        print("  4. ✅ Update ChromeDriver: pip install --upgrade selenium")
    
    print("\n👋 Done!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        print(traceback.format_exc())