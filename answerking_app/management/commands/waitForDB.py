import time
import os

import django.db
from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Wait to connect to db until db is initialised"""

    def handle(self, *args, **options):
        MAX_NUM_CONNECTION_TRYS = 20

        start = time.time()
        self.stdout.write("Waiting for database...")
        num_connection_trys = 1
        connected = False
        while num_connection_trys <= MAX_NUM_CONNECTION_TRYS:
            try:
                connection.ensure_connection()
                connected = True
                break
            except OperationalError:
                num_connection_trys += 1
                time.sleep(1)

        end = time.time()
        if connected:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Database available! "
                    f"Time taken: {end-start:.4f} second(s). "
                    f"Number of tries: {num_connection_trys}"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Could not connect to database. "
                    f"Tried {MAX_NUM_CONNECTION_TRYS} times."
                )
            )
            raise django.db.DatabaseError(f"Could not connect to database.")
