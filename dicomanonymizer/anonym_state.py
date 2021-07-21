"""This module wraps some state loading, holding, and saving
functionality into python class implementation.
"""
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, Mapping, Optional
from collections import Counter


@dataclass
class AnonState:
    state_path: Path
    vf_filename: str = "state_cache.json"
    tc_filename: str = "tag_cache.json"
    _inited: bool = False

    def init_state(self):
        self.visited_folders = {}
        self.tag_counter = Counter()
        self._inited = True

    def _assert_inited(self):
        if not self._inited:
            raise AssertionError(f"Run {self.__repr__()}.init_state() method first")

    def load_state(self):
        self._assert_inited()

        vf_path = self.state_path / self.vf_filename
        tc_path = self.state_path / self.tc_filename
        if vf_path.exists() and vf_path.is_file():
            with open(vf_path, "r") as fout:
                self.visited_folders = json.load(fout)
        if tc_path.exists() and tc_path.is_file():
            with open(tc_path, "r") as fout:
                self.tag_counter = Counter(json.load(fout))

    def save_state(self):
        self._assert_inited()
        vf_path = self.state_path / self.vf_filename
        tc_path = self.state_path / self.tc_filename
        with open(vf_path, "w") as fin:
            json.dump(self.visited_folders, fin)
        with open(tc_path, "w") as fin:
            json.dump(self.tag_counter, fin)


if __name__ == "__main__":
    test_state = AnonState(Path.cwd())
    test_state.init_state()
    test_state.save_state()
    test_state.load_state()
    print(test_state.visited_folders)
    print(test_state.tag_counter)
