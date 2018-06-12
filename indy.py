#!/usr/bin/python -OOtt

import cPickle as pickle

class Indy(object):

    def __init__(self):
        """load blueprints data from file"""
        self.b = pickle.load(open('data/blueprints.yaml.dat', 'rb'))
        self.size = len(self.b)
        print "[Blueprints loaded]"

    def build(self, typeID):
        """returns tuple of product and list of typeID's and quantities of each material required"""
        try:
            # this is manufacturing
            return self.b[typeID]['activities']['manufacturing']
        except:
            if typeID not in self.b:
                print "ERROR %s typeID not found in blueprints!" % typeID
            elif 'manufacturing' not in self.b[typeID]['activities']:
                if 'invention' not in self.b[typeID]['activities']:
                    # fubar
                    print 'No idea why, but build broke!'
                else:
                    # this is invention
                    return self.b[typeID]['activities']['invention']
            else:
                # fubar
                print "No freaking clue why build failed!"
            return False


if __name__ == '__main__':

    indy = Indy()

    print "="*42
    print """<row itemID="128228522" locationID="60002353" typeID="821" typeName="200mm AutoCannon I Blueprint" flagID="4" quantity="-1" timeEfficiency="20" materialEfficiency="10" runs="-1" />"""
    print "="*42
    print "indy.build(821)"
    bp = indy.build(821)
    for k,v in bp.items():
        print k,v

    print "="*42
    print """<row itemID="1224925891227" locationID="60003469" typeID="30605" typeName="Wrecked Electromechanical Component" flagID="4" quantity="1" timeEfficiency="0" materialEfficiency="0" runs="-1" />"""
    print "="*42
    print "indy.build(30605)"
    bp = indy.build(30605)
    for k,v in bp.items():
        print k,v

