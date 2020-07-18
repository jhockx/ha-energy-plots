import json
import sys
from datetime import datetime, date

now = datetime.now()

print('--- start test script ---')
print('Arguments passed to test script:')
for arg in sys.argv[1:]:
	print(arg)
	assert arg != "null", "One of the arguments is empty, check your settings!"

predicted_solar = json.loads(sys.argv[7])
print(predicted_solar)
print("predicted_solar current year, current month:")
print(predicted_solar[str(now.year)][str(now.month)])
print('--- end test script ---')
