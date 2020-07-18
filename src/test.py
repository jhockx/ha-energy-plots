import json
import sys
from datetime import datetime

now = datetime.now()

print('--- start test script ---')
print('Arguments passed to test script:')
for arg in sys.argv[1:]:
    print(arg)
    assert arg != "null", "One of the arguments is empty, check your settings!"

print("Check if statement")
print(json.loads(sys.argv[7]) if sys.argv[7] != 'none' else 'ELSE')
print('--- end test script ---')
