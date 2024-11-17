from concurrent.futures import ThreadPoolExecutor, as_completed

class ConcurrencyManager:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers

    def process_concurrently(self, items, process_item_fn):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(process_item_fn, item): item for item in items}
            for future in as_completed(futures):
                item = futures[future]
                try:
                    future.result()
                    print(f"Processing complete for: {item}")
                except Exception as e:
                    print(f"Error processing item {item}: {e}")
