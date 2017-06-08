#!/usr/bin/env python3

'''
Plot the results you get from running './gather-data.sh' and then
'./merge-data.py'.

The sole argument should be the directory containing the gathered data.
This script expects a file 'full.json' to be present, and will create
a subdirectory 'plots' and save its plots there.
'''

import sys
import os
import json

from mbmlib import * # Local file with helper functions.

import numpy as np
import matplotlib
matplotlib.use('Agg') # For headless use.
import matplotlib.pyplot as plt


# SETTINGS


## INPUT
data_dir = sys.argv[1]

with open(os.path.join(data_dir, 'full.json')) as f:
    benchmarks = json.load(f)
benchmarks = list(benchmarks.items())


# PLOTTING
plots_dir = os.path.join(data_dir, 'plots')
os.makedirs(plots_dir, exist_ok=True)

for benchmark_name, benchmark_info in benchmarks:
    pdf_path = os.path.normpath(os.path.join(plots_dir, benchmark_name + '-runtimes.pdf'))
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    flat_results = []
    for dataset_name, dataset_info in benchmark_info['datasets'].items():
        for key, short_name, color in (
                ('with-in-place-lowering-without-memory-block-merging', 'disabled', 'red'),
                ('without-in-place-lowering-with-memory-block-merging', 'enabled', 'blue')
        ):
            runtime = dataset_info[key]['average_runtime']
            flat_results.append(('{}:\n{}'.format(short_name, dataset_name), runtime, color))

    print('Plotting {} runtimes into {}.'.format(benchmark_name, pdf_path),
          file=sys.stderr)

    ind = np.arange(len(flat_results))
    width = 0.9

    maximum = max(map(lambda x: x[1], flat_results))

    fig, ax = plt.subplots()
    ax.set_ylim([0, maximum * 1.1])
    ax.set_title('Runtimes of {}'.format(benchmark_name))
    ax.set_ylabel('Microseconds')
    ax.set_xticks(ind)
    ax.set_xticklabels(list(map(lambda x: x[0], flat_results)))
    plt.tick_params(axis='x', which='major', labelsize=4)

    plt.bar(ind,
            list(map(lambda x: x[1], flat_results)),
            width,
            color=list(map(lambda x: x[2], flat_results)))

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    plt.rc('text')
    plt.savefig(pdf_path, format='pdf')
    plt.close()


    # pdf_path = os.path.normpath(os.path.join(data_dir, benchmark_name + '-allocations.pdf'))
    # os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    # flat_results = []
    # for dataset_name, runtimes, total_alloc, _, _ in datasets:
    #     for json_path in ['without.json', 'with.json']:
    #         alloc = total_alloc[json_path]
    #         color = json_colors[json_path]
    #         flat_results.append(('{}:\n{}'.format(short_path_name(json_path),
    #                                               cut_desc(dataset_name)),
    #                              alloc, color))

    # print('Plotting total allocations {} into {}.'.format(benchmark_name, pdf_path),
    #       file=sys.stderr)

    # ind = np.arange(len(flat_results))
    # width = 0.35

    # maximum = max(map(lambda x: x[1], flat_results))

    # fig, ax = plt.subplots()
    # ax.set_ylim([0, maximum * 1.1])
    # ax.set_title('Cumulative allocations in {}'.format(benchmark_name))
    # ax.set_ylabel('Bytes')
    # ax.set_xticks(ind)
    # ax.set_xticklabels(list(map(lambda x: x[0], flat_results)))
    # plt.tick_params(axis='x', which='major', labelsize=4)

    # plt.bar(ind,
    #         list(map(lambda x: x[1], flat_results)),
    #         width,
    #         color=list(map(lambda x: x[2], flat_results)))

    # plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    # plt.rc('text')
    # plt.savefig(pdf_path, format='pdf')
    # plt.close()