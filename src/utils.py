def graceful_input(prompt: str, exit_message: str = '') -> str:
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt (Ctrl+C) - exiting.')
    except EOFError:
        print('EOFError (Ctrl+Z Enter on Windows, Ctrl+D on *nix) - exiting.')
    print(exit_message)
    exit(0)