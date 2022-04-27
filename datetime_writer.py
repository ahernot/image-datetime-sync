import os
import datetime
import subprocess

from preferences import *


def sync_datetime (dirpath: str, offset=datetime.timedelta(0, 0, 0)):

    # Default to offset in hours
    if isinstance(offset, int) or isinstance(offset, float):
        offset = datetime.timedelta(0, offset * 3600, 0)

    with os.scandir( dirpath ) as file_list:
        for file in file_list:

            # Unpack & read file data
            filepath = file.path

            # Get file access time
            atime = os.stat(filepath).st_atime

            # Read EXIF datetime
            process = subprocess.Popen(
                [EXIFTOOL_PATH, '-DateTimeOriginal', filepath],
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            out_split = stdout.decode('utf-8') .split('\n')

            # Get file modification time
            for item in out_split:
                if 'Date/Time Original' in item:
                    datetime_original_str = item.split(': ')[1]
                    datetime_original_dt = datetime.datetime.strptime(datetime_original_str, '%Y:%m:%d %H:%M:%S')
                    mtime = datetime_original_dt.timestamp()


            # Update file atime and mtime
            os.utime(filepath, (atime, mtime + offset))