import asyncio
import aiohttp 

# fxn1 
async def request(request):             # co-routine
    print(f"Requested : {request}")
    await asyncio.sleep(2)
    print(f"Response recieved for : {request}")

# fxn2
async def fetch_url(session, url):
    async with session.get(url) as response:
        print(f"Fetched {url} with status {response.status}")


async def main_fxn():
    await asyncio.gather(             #send all 3 req at once by gather fxn
        request("IMAGE FROM WEB"),
        request("VIDEO FROM WEB"),
        request("JSON FROM WEB"),
    )

    urls = ["https://httpbin.org/delay/2"] * 3        # array of sites for 2 sec delay
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, i) for i in urls]
        await asyncio.gather(*tasks)                  # here "*" is spread oprtr for array - tasks

    print("\nProgram Completed")

asyncio.run(main_fxn())














































































