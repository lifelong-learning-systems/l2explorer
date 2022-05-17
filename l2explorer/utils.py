"""
Copyright © 2021 The Johns Hopkins University Applied Physics Laboratory LLC
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os


def get_l2explorer_app_location():
    try:
        app_file_name = os.environ['L2EXPLORER_APP']
    except:
        app_file_name = ''
        print('ERROR: Set L2EXPLORER_APP path to executable. For Linux/OSX users, please run export'
              ' L2EXPLORER_APP="/path/to/my/executable" to the executable downloaded. For Windows 10'
              ' users run setx L2EXPLORER_APP "C:\Path\To\Executable.exe" ')
        raise
    return app_file_name


def get_l2explorer_worker_id():
    try:
        worker_id = int(os.environ['L2EXPLORER_WORKER_ID'])
    except:
        worker_id = ''
        print('ERROR: Set L2EXPLORER_WORKER_ID to a valid integer. For Linux/OSX users, please run export'
              ' L2EXPLORER_WORKER_ID=0 to the executable downloaded. For Windows 10'
              ' users run setx L2EXPLORER_WORKER_ID 0 ')
        raise
    return worker_id
