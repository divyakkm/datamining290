###
# Implement simple k-means clustering using 1 dimensional data
##/
import random

dataset = [-13.65089255716321, -0.5409562932238607, -88.4726466247223, 39.30158828358612, 4.066458182574449, 64.64143300482378, 38.68269424751338, 33.42013676314311, 31.18603331719732, -0.2027616409406292, 45.13590038987272, 30.791899783552395, 61.1727490302448, 18.167220741624856, 88.88077709786394, -1.3808002119514704, 50.14991362212521, 55.92029956281276, -6.759813255299466, 34.28290084421072]

k = 2 # number of clusters

def pick_centroids(xs, num):
    """Return list of num centroids given a list of numbers in xs"""
    #Randomly chose k centroids from the dataset
    centroids = random.sample(xs,num)
    print "Initial Centroids - ", centroids
    return centroids

def distance(a, b):
    """Return the distance of numbers a and b"""
    return abs(a - b)

def centroid(xs):
    """Return the centroid number given a list of numbers, xs"""
    centroid = sum(xs)/len(xs)
    # print "Centroid",centroid
    return centroid

def cluster(xs, centroids):
    """Return a list of clusters centered around the given centroids.  Clusters
    are lists of numbers."""
    clusters = [[] for c in centroids]
    for x in xs:
        # find the closest cluster to x
        dist, cluster_id = min((distance(x, c), cluster_id)
                for cluster_id, c in enumerate(centroids))
        # place x in cluster
        clusters[cluster_id].append(x)
    return clusters

def iterate_centroids(xs, centroids):
    """Return stable centroids given a dataset and initial centroids"""

    err = 0.001  # minimum amount of allowed centroid movement
    observed_error = 1  # Initialize: maxiumum amount of centroid movement
    new_clusters = [[] for c in centroids]  # Initialize: clusters
    i=1
    print
    print "Clustering iterations:"
    while observed_error > err:
        print "Iteration#", i
        new_clusters = cluster(xs, centroids)
        new_centroids = map(centroid, new_clusters)
        i=i+1
        observed_error = max(abs(new - old) for new, old in zip(new_centroids, centroids))
        centroids = new_centroids
        print "Cetnroids: ",centroids
        print "Clusters: ",new_clusters
        print

    return (centroids, new_clusters)


###
# Main part of program:
# Pick initial centroids
# Iterative to find final centroids
# Print results
##/

initial_centroids = pick_centroids(dataset, k)
final_centroids, final_clusters = iterate_centroids(dataset, initial_centroids)

i=1
print "Final Clusters after multiple iterations:"
for centroid, cluster in zip(final_centroids, final_clusters):
    print "Cluster #",i, "- Size:",len(cluster)
    i=i+1
    print "Centroid: %s" % centroid
    print "Cluster contents: %r" % cluster
    print


"""
OUTPUT:

Initial Centroids -  [4.066458182574449, 55.92029956281276]

Clustering iterations:
Iteration# 1
Cetnroids:  [-11.096773957387704, 47.79719382891219]
Clusters:  [[-13.65089255716321, -0.5409562932238607, -88.4726466247223, 4.066458182574449, -0.2027616409406292, 18.167220741624856, -1.3808002119514704, -6.759813255299466], [39.30158828358612, 64.64143300482378, 38.68269424751338, 33.42013676314311, 31.18603331719732, 45.13590038987272, 30.791899783552395, 61.1727490302448, 88.88077709786394, 50.14991362212521, 55.92029956281276, 34.28290084421072]]

Iteration# 2
Cetnroids:  [-11.096773957387704, 47.79719382891219]
Clusters:  [[-13.65089255716321, -0.5409562932238607, -88.4726466247223, 4.066458182574449, -0.2027616409406292, 18.167220741624856, -1.3808002119514704, -6.759813255299466], [39.30158828358612, 64.64143300482378, 38.68269424751338, 33.42013676314311, 31.18603331719732, 45.13590038987272, 30.791899783552395, 61.1727490302448, 88.88077709786394, 50.14991362212521, 55.92029956281276, 34.28290084421072]]

Final Clusters after multiple iterations:
Cluster # 1 - Size: 8
Centroid: -11.0967739574
Cluster contents: [-13.65089255716321, -0.5409562932238607, -88.4726466247223, 4.066458182574449, -0.2027616409406292, 18.167220741624856, -1.3808002119514704, -6.759813255299466]

Cluster # 2 - Size: 12
Centroid: 47.7971938289
Cluster contents: [39.30158828358612, 64.64143300482378, 38.68269424751338, 33.42013676314311, 31.18603331719732, 45.13590038987272, 30.791899783552395, 61.1727490302448, 88.88077709786394, 50.14991362212521, 55.92029956281276, 34.28290084421072]

"""
