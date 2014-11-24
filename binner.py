def find_bins(perbin, counts):
    cur_count = 0
    bins = []
    for v, c in counts:
        cur_count += c
        if cur_count >=perbin:
            cur_count = 0
            bins.append(v)
    return bins

b = {}
for city in linkranks.keys():
    d = linkranks[city]
    values = d.values()
    counts = sorted([(k,v) for (k,v) in Counter(values).iteritems()], key=lambda x: x[0])
    perbin = 100
    while True:
        perbin +=1
        bins = find_bins(perbin, counts)
        if len(bins) == 4:
            break
    bins.sort(reverse=True)
    b[city] = bins