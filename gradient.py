"""
Read data and create gradients for every point point
"""

points = []

with open("data/ncsutest.xyz") as f:
    # Read x, y, z points
    last = 0
    row = []

    for line in f.readlines():
        line = line.replace("\n", "")
        x, y, z = line.split()
        
        # If y value has advanced, add row to the list
        if y != last:
            if len(row) != 0:
                points.append(row)

            row = []

        row.append((float(x), float(y), float(z)))
        last = y
    
    points.append(row)
