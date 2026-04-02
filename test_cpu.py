import time
def run_loop():
    seconds = 2
    start_time = time.monotonic()
    last_second = -1
    iters = 0
    while True:
        iters += 1
        current_time = time.monotonic()
        elapsed = current_time - start_time
        remaining = seconds - elapsed

        current_second = int(elapsed)
        if current_second > last_second or remaining <= 0:
            last_second = current_second

        if remaining <= 0:
            break
        sleep_interval = 1.0 - (elapsed % 1.0)
        time.sleep(min(sleep_interval, remaining))
    print(f"Iters: {iters}")

run_loop()
