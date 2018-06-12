#!/usr/bin/python
import cPickle as pickle
import yaml
import sys
infile = sys.argv[1]
with open(sys.argv[1], 'r') as f:
    d = yaml.load(f)
    outfile = '%s.dat' % infile
    with open(outfile, 'wb') as f:
        pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)
        sys.exit(0)
print "Conversion failure."
sys.exit(1)
