#!/usr/bin/env python3
"""抓取微博热门话题并导出到 CSV。"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, List, Optional
from urllib.parse import urljoin

import requests
from requests import Response
from requests.exceptions import RequestException


DEFAULT_URL = "https://s.weibo.com/top/summary?cate=realtimehot"
BASE_URL = "https://s.weibo.com"
DEFAULT_OUTPUT = "weibo_hot_topics.csv"
DEFAULT_TIMEOUT = 10
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/134.0.0.0 Safari/537.36"
)


@dataclass
class HotTopic:
    name: str
    heat: str
    link: str


class WeiboHotParser(HTMLParser):
    """解析微博热门话题表格。"""

    def __init__(self) -> None:
        super().__init__()
        self.topics: List[HotTopic] = []
        self._current_row: Optional[dict] = None
        self._current_td_class: Optional[str] = None
        self._in_topic_anchor = False
        self._in_heat_span = False
        self._current_span_parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attrs_dict = dict(attrs)

        if tag == "tr":
            self._current_row = {
                "rank_parts": [],
                "name_parts": [],
                "link": "",
                "heat_candidates": [],
            }
            self._current_td_class = None
            self._in_topic_anchor = False
            self._in_heat_span = False
            self._current_span_parts = []
            return

        if self._current_row is None:
            return

        if tag == "td":
            self._current_td_class = attrs_dict.get("class", "")
            return

        if tag == "a" and self._current_td_class and "td-02" in self._current_td_class:
            if not self._current_row["link"]:
                self._current_row["link"] = attrs_dict.get("href", "")
            self._in_topic_anchor = True
            return

        if tag == "span" and self._current_td_class and "td-02" in self._current_td_class:
            self._in_heat_span = True
            self._current_span_parts = []

    def handle_endtag(self, tag: str) -> None:
        if self._current_row is None:
            return

        if tag == "a":
            self._in_topic_anchor = False
            return

        if tag == "span" and self._in_heat_span:
            heat_text = self._clean_text("".join(self._current_span_parts))
            if heat_text:
                self._current_row["heat_candidates"].append(heat_text)
            self._in_heat_span = False
            self._current_span_parts = []
            return

        if tag == "td":
            self._current_td_class = None
            return

        if tag == "tr":
            topic = self._build_topic(self._current_row)
            if topic is not None:
                self.topics.append(topic)
            self._current_row = None
            self._current_td_class = None
            self._in_topic_anchor = False
            self._in_heat_span = False
            self._current_span_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_row is None:
            return

        cleaned = self._clean_text(data)
        if not cleaned:
            return

        if self._current_td_class and "td-01" in self._current_td_class:
            self._current_row["rank_parts"].append(cleaned)

        if self._in_topic_anchor:
            self._current_row["name_parts"].append(cleaned)

        if self._in_heat_span:
            self._current_span_parts.append(cleaned)

    @staticmethod
    def _clean_text(value: str) -> str:
        return re.sub(r"\s+", " ", value).strip()

    def _build_topic(self, row: dict) -> Optional[HotTopic]:
        rank_text = self._clean_text(" ".join(row["rank_parts"]))
        name = self._clean_text(" ".join(row["name_parts"]))
        link = row["link"].strip()
        heat = self._pick_heat(row["heat_candidates"])

        if not name or not link:
            return None

        if "广告" in rank_text:
            return None

        return HotTopic(name=name, heat=heat, link=self._normalize_link(link))

    @staticmethod
    def _pick_heat(candidates: Iterable[str]) -> str:
        cleaned_candidates = [candidate.strip() for candidate in candidates if candidate.strip()]
        for candidate in cleaned_candidates:
            if re.search(r"\d", candidate):
                return candidate
        return cleaned_candidates[0] if cleaned_candidates else ""

    @staticmethod
    def _normalize_link(link: str) -> str:
        return urljoin(BASE_URL, link)


def fetch_hot_topics_html(url: str = DEFAULT_URL, timeout: int = DEFAULT_TIMEOUT) -> str:
    headers = {"User-Agent": USER_AGENT}

    try:
        response: Response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except RequestException as exc:
        raise RuntimeError(f"请求微博页面失败：{exc}") from exc

    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding or "utf-8"

    return response.text


def parse_hot_topics(html: str) -> List[HotTopic]:
    parser = WeiboHotParser()
    parser.feed(html)
    parser.close()

    topics: List[HotTopic] = []
    seen: set[tuple[str, str]] = set()
    for topic in parser.topics:
        key = (topic.name, topic.link)
        if key in seen:
            continue
        seen.add(key)
        topics.append(topic)

    if not topics:
        raise ValueError("没有解析到任何热门话题，微博页面结构可能已变化。")

    return topics


def save_hot_topics_to_csv(topics: Iterable[HotTopic], output_path: Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["话题名称", "热度", "链接"])
            for topic in topics:
                writer.writerow([topic.name, topic.heat, topic.link])
    except OSError as exc:
        raise OSError(f"写入 CSV 文件失败：{exc}") from exc


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="抓取微博热门话题并保存为 CSV 文件。")
    parser.add_argument(
        "-u",
        "--url",
        default=DEFAULT_URL,
        help=f"热门话题页面地址，默认值：{DEFAULT_URL}",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"CSV 输出文件路径，默认值：{DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP 请求超时时间（秒），默认值：{DEFAULT_TIMEOUT}",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=None,
        help="仅保存前 N 条热门话题。",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    if args.limit is not None and args.limit <= 0:
        print("错误：--limit 必须是大于 0 的整数。", file=sys.stderr)
        return 1

    output_path = Path(args.output)

    print("正在请求微博热门话题页面...")
    try:
        html = fetch_hot_topics_html(url=args.url, timeout=args.timeout)
        topics = parse_hot_topics(html)
        if args.limit is not None:
            topics = topics[: args.limit]
        save_hot_topics_to_csv(topics, output_path)
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"处理失败：{exc}", file=sys.stderr)
        return 1

    print(f"成功获取 {len(topics)} 条热门话题。")
    print(f"CSV 文件已保存到：{output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
