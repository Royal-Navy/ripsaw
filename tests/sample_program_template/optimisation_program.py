import math as math
import sys
epsilon = sys.float_info.epsilon

# print("Starting Sample Optimisation Program:")
with open("input.txt", 'r') as in_fs:
    lines = in_fs.readlines()

    x = int()
    z = int()
    for i, line in enumerate(lines):
        if "X" in line:
            x = float(lines[i+1])
            # print("X was found and identified as ", x)
        if "Z" in line:
            z = float(lines[i+1])
            # print("Z was found and identified as ", z)

    y = -(abs((x-1)/math.exp(math.sin(1/(x-1+epsilon)))) * abs((z-1)/math.exp(math.sin(1/(z-1+epsilon))))) + 2

    # print("Y was calculated as", y)
    with open("output.txt", 'w') as out_fs:
        out_fs.write("Result was " + str(y))
