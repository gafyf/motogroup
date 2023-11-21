#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motoproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# import os
# import sys
# from multiprocessing import Process

# def run_scraper():
#     os.system("python new/scraper.py")  # Replace "scraper.py" with the path to your scraper file

# if __name__ == "__main__":
#     # Run the scraper in a separate process
#     scraper_process = Process(target=run_scraper)
#     scraper_process.daemon = True  # The scraper process will terminate when the main process (runserver) exits
#     scraper_process.start()

#     # Run the Django development server
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "motoproject.settings")
#     from django.core.management import execute_from_command_line

#     execute_from_command_line(sys.argv)

