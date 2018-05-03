with open('pool.txt', 'w') as p:
    for e in [1]:
        den = 8
        for t in [25, 30]:
            for d in [5, 10]:
                for i in range(10):
                    p.writelines('-d ' + str(den) + ' -t ' + str(t) + ' -D ' + str(d) + ' -i ' + str(i) + ' -e ' + str(e) + '\n')
        den = 6
        for t in [35, 40]:
            for d in [5, 10]:
                for i in range(2):
                    p.writelines('-d ' + str(den) + ' -t ' + str(t) + ' -D ' + str(d) + ' -i ' + str(i) + ' -e ' + str(e) + '\n')
        for t in [45, 50]:
            for d in [5]:
                for i in range(2):
                    p.writelines('-d ' + str(den) + ' -t ' + str(t) + ' -D ' + str(d) + ' -i ' + str(i) + ' -e ' + str(e) + '\n')
        den = 10
        for t in [20]:
            for d in [4, 5, 10, 15, 19]:
                for i in range(10):
                    p.writelines('-d ' + str(den) + ' -t ' + str(t) + ' -D ' + str(d) + ' -i ' + str(i) + ' -e ' + str(e) + '\n')
        for t in [25]:
            for d in [5, 10]:
                for i in range(10):
                    p.writelines('-d ' + str(den) + ' -t ' + str(t) + ' -D ' + str(d) + ' -i ' + str(i) + ' -e ' + str(e) + '\n')
        for t in [30]:
            for d in [5]:
                for i in range(10):
                    p.writelines('-d ' + str(den) + ' -t ' + str(t) + ' -D ' + str(d) + ' -i ' + str(i) + ' -e ' + str(e) + '\n')
