# V29 stopped

{
  "state": "EXECUTION_FAILED",
  "error": "FileNotFoundError(2, 'No such file or directory')",
  "traceback": "Traceback (most recent call last):\n  File \"/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/scripts/zero29.py\", line 502, in supervise\n    preflight()\n  File \"/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/scripts/zero29.py\", line 496, in preflight\n    configure('canonical');check_history();retrospective()\n                                           ^^^^^^^^^^^^^^^\n  File \"/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/scripts/zero29.py\", line 270, in retrospective\n    keys=np.load(p/'validation_keys.npy');st=np.load(p/'validation_stats.npy');pp=np.sort(np.load(ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}/valid_pairs.npy'),axis=1);n=len(t.sealed(ds)['x']);stats=st[np.searchsorted(keys,pp[:,0]*n+pp[:,1])];scores={}\n                                                                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/ubuntu/anaconda3/envs/mei_env/lib/python3.11/site-packages/numpy/lib/npyio.py\", line 427, in load\n    fid = stack.enter_context(open(os_fspath(file), \"rb\"))\n                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^\nFileNotFoundError: [Errno 2] No such file or directory: '/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/CHRI_V18_1/cache/cora/seed_0/valid_pairs.npy'\n",
  "test_opened": false,
  "storage": {
    "available_bytes": 13168918528,
    "available_inodes": 13346504,
    "margin_bytes": 3221225472
  }
}
