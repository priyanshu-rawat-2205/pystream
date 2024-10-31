# video_streaming/streaming.py

import os
import aiofiles

class VideoStreamer:
    def __init__(self, file_path, chunk_size=1024 * 1024):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.file_size = os.path.getsize(file_path)

    async def get_file_chunk(self, start: int, end: int):
        """Reads a specific byte range from the file asynchronously."""
        async with aiofiles.open(self.file_path, "rb") as file:
            await file.seek(start)
            bytes_to_read = end - start + 1
            while bytes_to_read > 0:
                chunk = await file.read(min(self.chunk_size, bytes_to_read))
                if not chunk:
                    break
                bytes_to_read -= len(chunk)
                yield chunk

    def parse_range(self, range_header):
        """Parses the Range header to determine the byte range requested."""
        range_start, range_end = 0, self.file_size - 1
        if range_header:
            byte_range = range_header.split("=")[1]
            range_start, range_end = byte_range.split("-")
            range_start = int(range_start) if range_start else 0
            range_end = int(range_end) if range_end else self.file_size - 1
            if range_end >= self.file_size:
                range_end = self.file_size - 1
        return range_start, range_end
