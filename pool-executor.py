import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def check_stock(item):
    print(f"Checking {item} in store...")
    time.sleep(2) # Blocking operation - but get_running_loop() used to prevent this
    return f"{item} stock: 42"

def heavy_encryption(data):
    return f"encrypted data : {data[::-1]}"

async def main():

    
    loop = asyncio.get_running_loop()

    #thread
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, check_stock, "Item ABC")
        print(result)

    #process - in single fxn
    with ProcessPoolExecutor() as pool2:
        result2 = await loop.run_in_executor(pool2, heavy_encryption, "credit_card_1234")
        print(result2)


if __name__ == "__main__":
    asyncio.run(main())

