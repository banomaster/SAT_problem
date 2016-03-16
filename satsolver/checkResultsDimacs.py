import sys
#our result
with open(sys.argv[1]) as f1:
    #true result
    with open(sys.argv[2]) as f2:
        res1 = f1.readline().strip().split(" ")
        res2 = f2.readline().strip().split(" ")

        containsAll = True
        for val in res1:
            if (val not in res2):
                containsAll = False

print containsAll
