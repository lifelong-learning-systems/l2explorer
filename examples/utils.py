#(c) 2019 The Johns Hopkins University Applied Physics Laboratory LLC (JHU/APL).
#All Rights Reserved. This material may be only be used, modified, or reproduced
#by or for the U.S. Government pursuant to the license rights granted under the
#clauses at DFARS 252.227-7013/7014 or FAR 52.227-14. For any other permission,
#please contact the Office of Technology Transfer at JHU/APL.

#NO WARRANTY, NO LIABILITY. THIS MATERIAL IS PROVIDED “AS IS.” JHU/APL MAKES NO
#REPRESENTATION OR WARRANTY WITH RESPECT TO THE PERFORMANCE OF THE MATERIALS,
#INCLUDING THEIR SAFETY, EFFECTIVENESS, OR COMMERCIAL VIABILITY, AND DISCLAIMS
#ALL WARRANTIES IN THE MATERIAL, WHETHER EXPRESS OR IMPLIED, INCLUDING (BUT NOT
#LIMITED TO) ANY AND ALL IMPLIED WARRANTIES OF PERFORMANCE, MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT OF INTELLECTUAL PROPERTY
#OR OTHER THIRD PARTY RIGHTS. ANY USER OF THE MATERIAL ASSUMES THE ENTIRE RISK
#AND LIABILITY FOR USING THE MATERIAL. IN NO EVENT SHALL JHU/APL BE LIABLE TO ANY
#USER OF THE MATERIAL FOR ANY ACTUAL, INDIRECT, CONSEQUENTIAL, SPECIAL OR OTHER
#DAMAGES ARISING FROM THE USE OF, OR INABILITY TO USE, THE MATERIAL, INCLUDING,
#BUT NOT LIMITED TO, ANY DAMAGES FOR LOST PROFITS.

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
