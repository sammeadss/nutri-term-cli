import json
import shutil
from pathlib import Path
import pytest
from nutri_term.user_profile import save_profile, load_profile, PROFILE_FILE, CONFIG_DIR

def test_save_and_load_profile(tmp_path, monkeypatch):
    # Redirect CONFIG_DIR to a temp directory for isolation
    monkeypatch.setattr("nutri_term.user_profile.CONFIG_DIR", tmp_path / ".nutri-term")
    monkeypatch.setattr("nutri_term.user_profile.PROFILE_FILE", tmp_path / ".nutri-term" / "profile.json")

    data = {
        "name": "Test User",
        "weight": 75,
        "height": 175,
        "age": 30,
        "gender": "male",
        "activity": "moderate",
        }

    # Start with no file
    assert load_profile() is None

    # Save
    save_profile(data)

    # Directory and file exist
    assert (tmp_path / ".nutri-term").is_dir()
    assert (tmp_path / ".nutri-term" / "profile.json").is_file()

    # Load back and compare
    loaded = load_profile()
    assert loaded == data

def test_load_profile_missing(tmp_path, monkeypatch):
    # Point PROFILE_FILE to a non-existent location
    monkeypatch.setattr("nutri_term.user_profile.PROFILE_FILE", tmp_path / "no-such.json")
    assert load_profile() is None
