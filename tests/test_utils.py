from src.utils import graceful_input
import pytest


def test_graceful_input_normal(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'user_text')
    result = graceful_input("Prompt: ")
    assert result == 'user_text'


def test_graceful_input_keyboard_interrupt(monkeypatch, capsys):
    def mock_input(_):
        raise KeyboardInterrupt

    monkeypatch.setattr('builtins.input', mock_input)

    with pytest.raises(SystemExit) as e:
        graceful_input("Prompt: ", exit_message="Exiting...")

    assert e.value.code == 0
    out, _ = capsys.readouterr()
    assert "KeyboardInterrupt" in out
    assert "Exiting..." in out


def test_graceful_input_eof_error(monkeypatch, capsys):
    def mock_input(_):
        raise EOFError

    monkeypatch.setattr('builtins.input', mock_input)

    with pytest.raises(SystemExit) as e:
        graceful_input("Prompt: ")

    assert e.value.code == 0
    out, _ = capsys.readouterr()
    assert "EOFError" in out
