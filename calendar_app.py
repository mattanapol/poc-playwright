import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    # Initialize Playwright and launch a browser
    async with async_playwright() as playwright:
        print("Launching browser")
        browser = await playwright.chromium.launch_persistent_context(
            user_data_dir="/Users/kaewsai/Library/Application Support/BraveSoftware/Brave-Browser/Profile 1/Default", 
            headless=False)
        # Create a new page in the browser
        print("Creating new page")
        page = await browser.new_page()
        print("Going to URL")
        # Navigate to a website
        await page.goto("https://calendar.google.com/calendar/u/0/r/agenda")
        
        input("Press Enter to continue...")

        # Close the browser
        await browser.close()

# Run the main function in an asyncio event loop
asyncio.run(main())