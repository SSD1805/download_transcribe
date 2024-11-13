import os
import threading
from src.core.logger_manager import LoggerManager

class FileUploader:
    def __init__(self):
        self.file_chunks = {}
        self.locks = {}
        self.logger = LoggerManager().get_logger()

    def get_lock(self, tab_id):
        if tab_id not in self.locks:
            self.locks[tab_id] = threading.Lock()
        return self.locks[tab_id]

    def save_chunks_to_file(self, save_path, chunks):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as f:
            for chunk in chunks:
                f.write(chunk)

    def handle_chunk(self, data, target_directory, lock_id):
        directory = data.get("directory")
        file_name = data.get("fileName")
        chunk = data.get("chunk")
        is_last_chunk = data.get("isLastChunk")

        if not (lock_id and directory and file_name and chunk is not None):
            self.logger.error("Invalid data received in handle_chunk")
            return {"error": "Invalid data"}

        with self.get_lock(lock_id):
            try:
                if lock_id not in self.file_chunks:
                    self.file_chunks[lock_id] = {}
                file_key = os.path.join(directory, file_name)

                if file_key not in self.file_chunks[lock_id]:
                    self.file_chunks[lock_id][file_key] = []

                self.file_chunks[lock_id][file_key].append(chunk)

                if is_last_chunk:
                    save_path = os.path.join(target_directory, file_key)
                    self.save_chunks_to_file(save_path, self.file_chunks[lock_id][file_key])
                    del self.file_chunks[lock_id][file_key]
                    if not self.file_chunks[lock_id]:
                        del self.file_chunks[lock_id]
                        del self.locks[lock_id]
                    self.logger.info(f"File {file_name} saved successfully at {save_path}")
                    return {"status": "File uploaded successfully"}
            except Exception as e:
                self.logger.error(f"Error handling chunk for {file_name}: {e}")
                return {"error": f"Failed to upload file {file_name}"}
