import numpy as np

def generate_partitions(n):
    a = np.zeros(n+1, dtype=np.int_)
    k = 1
    y = n - 1
    while k!=0:
        x = a[k-1] + 1
        k -= 1
        while 2*x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield np.concatenate(( np.flip(a[:k+2]), np.zeros(n-k-2,dtype=np.int_) ))
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield np.concatenate(( np.flip(a[:k+1]), np.zeros(n-k-1,dtype=np.int_) ))


def mckay(n):
    """
    Integer partitions of n, in reverse lexicographic order.
    Note that the generated output consists of the same list object,
    repeated the correct number of times; the caller must leave this
    list unchanged, and must make a copy of any partition that is
    intended to last longer than the next call into the generator.
    The algorithm follows Knuth v4 fasc3 p38 in rough outline.
    """
    if n == 0:
        yield []
    if n <= 0:
        return
    partition = [n]
    last_nonunit = (n > 1) - 1
    while True:
        yield partition
        if last_nonunit < 0:
            return
        if partition[last_nonunit] == 2:
            partition[last_nonunit] = 1
            partition.append(1)
            last_nonunit -= 1
            continue
        replacement = partition[last_nonunit] - 1
        total_replaced = replacement + len(partition) - last_nonunit
        reps,rest = divmod(total_replaced,replacement)
        partition[last_nonunit:] = reps*[replacement]
        if rest:
            partition.append(rest)
        last_nonunit = len(partition) - (partition[-1]==1) - 1


def revlex_partitions(n):
    """
    Integer partitions of n, in reverse lexicographic order.
    The output and asymptotic runtime are the same as mckay(n),
    but the algorithm is different: it involves no division,
    and is simpler than mckay, but uses O(n) extra space for
    a recursive call stack.
    """
    if n == 0:
        yield []
    if n <= 0:
        return
    for p in revlex_partitions(n-1):
        if len(p)==1 or (len(p)>1 and p[-1]<p[-2]):
            p[-1] += 1
            yield p
            p[-1] -= 1
        p.append(1)
        yield p
        p.pop()


print([[y for y in x] for x in revlex_partitions(4)])
print([x for x in generate_partitions(4)])
print([[y for y in x] for x in mckay(4)])





#  ----------------------------  CONTROLLARE  ---------------------------  #
"""
# A utility function to print an
# array p[] of size 'n'
def printArray(p, n):
    for i in range(0, n):
        print(p[i], end = " ")
    print()
 
def printAllUniqueParts(n):
    p = [0] * n     # An array to store a partition
    k = 0         # Index of last element in a partition
    p[k] = n     # Initialize first partition
                 # as number itself
 
    # This loop first prints current partition,
    # then generates next partition.The loop
    # stops when the current partition has all 1s
    while True:
         
            # print current partition
            printArray(p, k + 1)
 
            # Generate next partition
 
            # Find the rightmost non-one value in p[].
            # Also, update the rem_val so that we know
            # how much value can be accommodated
            rem_val = 0
            while k >= 0 and p[k] == 1:
                rem_val += p[k]
                k -= 1
 
            # if k < 0, all the values are 1 so
            # there are no more partitions
            if k < 0:
                print()
                return
 
            # Decrease the p[k] found above
            # and adjust the rem_val
            p[k] -= 1
            rem_val += 1
 
            # If rem_val is more, then the sorted
            # order is violated. Divide rem_val in
            # different values of size p[k] and copy
            # these values at different positions after p[k]
            while rem_val > p[k]:
                p[k + 1] = p[k]
                rem_val = rem_val - p[k]
                k += 1
 
            # Copy rem_val to next position
            # and increment position
            p[k + 1] = rem_val
            k += 1
 
"""