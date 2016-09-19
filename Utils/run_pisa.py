import os
from subprocess import call, check_output
import xml.etree.ElementTree as ET
#from subprocess import Popen, PIPE
import numpy as np

# pisa test -analyse c.0.0.pdb
# pisa test -xml interfaces >aaa.xml
pisa_prep = "pisa {0} -analyse {1}"
pisa_analyse = "pisa {0} -xml interfaces"
work_dir = "results_cur"

pdb_files = os.listdir(work_dir)
pdb_files.sort()

h_bonds_counts = np.zeros((553,553))
s_bridges_counts = np.zeros((553,553))

h_bonds_counts_flat = np.zeros(553)
s_bridges_counts_flat = np.zeros(553)

model_lists = []
for i in range(553):
    model_lists.append(set())

for i_file,pdb_file in enumerate(pdb_files):
    full_path = os.path.join(work_dir,pdb_file)
    file_name = pdb_file[:-4]
    #call(pisa_prep.format(file_name,full_path),shell=True)
    xml_out = check_output(pisa_analyse.format(file_name),shell=True)
    root = ET.fromstring(xml_out)
    interface = root.findall('interface')[0]
    hbonds = interface.findall('h-bonds')[0]
    for hbond in hbonds:
        if hbond.tag != 'bond':
            continue
        ind1 = int(hbond.find('seqnum-1').text)
        ind2 = int(hbond.find('seqnum-2').text)
        if ind1 < 157 or ind2 < 157:
            continue
        assert ind1 < ind2
        h_bonds_counts[ind1,ind2] += 1
        h_bonds_counts_flat[ind1] += 1
        h_bonds_counts_flat[ind2] += 1
        model_lists[ind1].update([i_file])
        model_lists[ind2].update([i_file])
    sbridges =interface.findall('salt-bridges')[0]
    for sbridge in sbridges:
        if sbridge.tag != 'bond':
            continue
        ind1 = int(sbridge.find('seqnum-1').text)
        ind2 = int(sbridge.find('seqnum-2').text)
        if ind1 < 157 or ind2 < 157:
            continue
        assert ind1 < ind2
        s_bridges_counts[ind1,ind2] += 1
        s_bridges_counts_flat[ind1] += 1
        s_bridges_counts_flat[ind2] += 1
        model_lists[ind1].update([i_file])
        model_lists[ind2].update([i_file])
    print pdb_file

total_counts = h_bonds_counts + s_bridges_counts
total_counts_flat = s_bridges_counts_flat+h_bonds_counts_flat
# hbonds_sorted = np.argsort(-h_bonds_counts)
# sbridges_sorted = np.argsort(-s_bridges_counts)

counts_sorted = np.argsort(-total_counts,axis=None)
counts_sorted_unr = np.unravel_index(counts_sorted,(553,553))
print "Bonds:"
print counts_sorted_unr[0][:10]
print counts_sorted_unr[1][:10]
print total_counts.flat[counts_sorted[:10]]

counts_sorted_flat = np.argsort(-total_counts_flat)
print "Participation:"
print counts_sorted_flat[:10]
print total_counts_flat[counts_sorted_flat[:10]]

set_all = set(range(553))
for i in range(10):
    set_tmp = set_all.intersection(model_lists[counts_sorted_flat[i]])
    if len(set_tmp) == 0:
        continue
    set_all = set_tmp
    print set_all

for item in set_all:
    print pdb_files[item]