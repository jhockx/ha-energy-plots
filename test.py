import sys

print('--- start test script ---')
print('Arguments passed to test script:')
for arg in sys.argv[1:]:
	print(arg)
	assert arg != "null", "One of the arguments is empty, check your settings!"
print('--- end test script ---')
