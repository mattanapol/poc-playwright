from playwright.async_api import async_playwright, Response
import io
from PIL import Image
import asyncio
import time
import argparse

# settings
parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, metavar='str',
                    required=True)
parser.add_argument('--use_original_name', action='store_true', default=True)

args = parser.parse_args()
use_original_name = args.use_original_name

def get_image_name(url):
    if use_original_name:
        return url.split('/')[-1]
    return str(time.time()) + ".jpg"

def get_folder_name(url):
    import urllib.parse as urlparse
    par = urlparse.parse_qs(urlparse.urlparse(url).query)
    # check if par['id'] exists
    if 'id' in par:
        return par['id'][0]
    return str(hash(url))

async def on_response(resp: Response):
    if resp.status != 200:
        return
    if not resp.url.endswith('.jpg'):
        return
    img_bytes = await resp.body()
    image_file = io.BytesIO(img_bytes)
    image  = Image.open(image_file)

    width, height = image.size
    if width < 400 or height < 400:
        print("Image too small: ", width, height)
        return
    
    print("Image size: ", width, height)
    with open("./" + folder_name + "/" + get_image_name(resp.url) , "wb") as f:
          image.save(f)
          print("Success!!!!")

async def main(url: str):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1030, "height": 1080})
        page = await context.new_page()

        page.on("response", on_response)
        # go to url
        await page.goto(url)
        # wait for finish loading
        while True:
            await page.wait_for_timeout(2000)
            try:
                await page.click("a > .fa-arrow-right", timeout=10000)
            except:
                print("Click failed. Refreshing page...")
                try:
                    await page.reload()
                except:
                    print("Reload failed, skipping...")

        while True:
            await page.wait_for_timeout(10000)

if __name__ == '__main__':
    url = args.url
    # hash url to folder name
    folder_name = get_folder_name(url)
    print("Folder name: ", folder_name)
    # create folder
    import os
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    asyncio.run(main(url))