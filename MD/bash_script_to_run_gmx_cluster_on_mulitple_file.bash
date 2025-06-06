for xtc in all_replica_combine_*.xtc; do echo $xtc ; echo 4  4 | gmx cluster -f "$xtc" -s mtb_avg_all_replica_${xtc:20:-4}.pdb -cl "${xtc:20:-4}_cluster.pdb" -cutoff 0.2 -sz "${xtc:20:-4}_clust-size.xvg" -g "${xtc:20:-4}_cluster.log";  done

