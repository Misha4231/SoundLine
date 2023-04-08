from .models import Song
from pathlib import Path
from django.conf import settings
from django.shortcuts import get_object_or_404
from typing import IO, Generator

def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()

def open_file(request, slug: int) -> tuple:
    audio = get_object_or_404(Song, slug=slug)

    path = Path(settings.MEDIA_ROOT) / Path(audio.song_file.name)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_range = request.headers.get('range')
    status_code = 200
    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f'bytes {range_start}-{range_end}/{file_size}'
    return file, status_code, content_range
