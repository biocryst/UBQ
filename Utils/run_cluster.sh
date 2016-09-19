/usr/local/xray/rosetta/rosetta_source/bin/cluster.linuxgccrelease \
-database /usr/local/xray/rosetta/rosetta_database \
-in:file:s ../*.pdb \
-in:file:fullatom \
-cluster:radius -1 \
-cluster:sort_groups_by_energy \
-ignore_unrecognized_res