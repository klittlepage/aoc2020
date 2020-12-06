from typing import Iterator, List, IO


def read_chunked(input_file: IO) -> Iterator[List[str]]:
    chunk: List[str] = list()
    for line in input_file:
        if line == '\n':
            yield chunk
            chunk = list()
        else:
            chunk.append(line.strip())
    if chunk:
        yield chunk
