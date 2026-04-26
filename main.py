from ui.cli import CLI

if __name__ == "__main__":
    app = CLI()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting System. Goodbye!")
