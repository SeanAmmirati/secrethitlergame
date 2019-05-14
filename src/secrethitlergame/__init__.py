# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound

if __name__ == "__main__":
    sh = SecretHilter()
    sh.vote_for_government('2', {'0': 'Ja', '1': 'Nein', '2': 'Ja', '3': 'Ja', '4': 'Ja', '5': 'Ja', '6':'Nein'})
    sh.enact_policy([['L', 'F', 'F'], ['L', 'F']], ['F', 'F'], 'F')
    sh.vote_for_government('4', {'0':'Ja', '1':'Nein', '2':'Ja', '3': 'Ja', '4': 'Ja', '5': 'Ja', '6':'Nein'})
    sh.enact_policy([['L', 'F', 'F'], ['L', 'F']], ['L', 'F'], 'F')
    sh.determine_suspicions()
