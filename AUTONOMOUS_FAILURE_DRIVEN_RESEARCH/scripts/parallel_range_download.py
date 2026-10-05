from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests


def fetch_one(url: str, start: int, end: int, path: Path, timeout: int) -> tuple[int, int, str]:
    if path.exists() and path.stat().st_size == end - start + 1:
        return start, end, "cached"
    response = requests.get(
        url,
        headers={"Range": f"bytes={start}-{end}"},
        timeout=(15, timeout),
        stream=True,
    )
    response.raise_for_status()
    content_range = response.headers.get("Content-Range", "")
    expected = f"bytes {start}-{end}/"
    if response.status_code != 206 or not content_range.startswith(expected):
        raise RuntimeError(f"unexpected range response: {response.status_code} {content_range}")
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                handle.write(chunk)
    if temp.stat().st_size != end - start + 1:
        raise RuntimeError(f"short part {start}-{end}: {temp.stat().st_size}")
    temp.replace(path)
    return start, end, "downloaded"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--parts", type=Path, required=True)
    parser.add_argument("--chunk-size", type=int, default=4 * 1024 * 1024)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    args.parts.mkdir(parents=True, exist_ok=True)
    ranges = []
    start = 0
    index = 0
    while start < args.size:
        end = min(args.size - 1, start + args.chunk_size - 1)
        ranges.append((index, start, end, args.parts / f"part_{index:04d}.bin"))
        index += 1
        start = end + 1

    failures = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(fetch_one, args.url, start, end, path, args.timeout): (index, start, end)
            for index, start, end, path in ranges
        }
        for future in as_completed(futures):
            index, start, end = futures[future]
            try:
                _, _, status = future.result()
                print(f"part={index} range={start}-{end} status={status}", flush=True)
            except Exception as exc:
                failures.append((index, start, end, repr(exc)))
                print(f"part={index} range={start}-{end} ERROR={exc!r}", flush=True)
    if failures:
        raise SystemExit(f"{len(failures)} range downloads failed")

    temp_output = args.output.with_suffix(args.output.suffix + ".tmp")
    with temp_output.open("wb") as out:
        for _, start, end, path in ranges:
            if path.stat().st_size != end - start + 1:
                raise RuntimeError(f"invalid cached part {path}")
            with path.open("rb") as inp:
                shutil.copyfileobj(inp, out, length=1024 * 1024)
    if temp_output.stat().st_size != args.size:
        raise RuntimeError(f"invalid output size {temp_output.stat().st_size}")
    temp_output.replace(args.output)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f"complete bytes={args.output.stat().st_size} sha256={digest}", flush=True)


if __name__ == "__main__":
    main()
