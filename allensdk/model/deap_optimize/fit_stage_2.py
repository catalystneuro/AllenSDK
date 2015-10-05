#!/usr/bin/env python

import argparse
import os, sys
import numpy as np
import subprocess

import allensdk.core.json_utilities as json_utilities

from fit_stage_1 import SEEDS, FIT_BASE_DIR, OPTIMIZE_SCRIPT, MPIEXEC

FIT_TYPES = {"f6": "f9", "f12": "f13"}

def prepare_stage_2(output_directory):
    config_base_data = json_utilities.read(os.path.join(FIT_BASE_DIR, 'config_base.json'))

    jobs = []

    best_error = 1e12
    best_seed = 0
    for fit_type in FIT_TYPES:
        fit_type_dir = os.path.join(output_directory, fit_type)

        if not os.path.exists(fit_type_dir):
            print "fit type directory does not exist for cell: %s" % fit_type_dir
            continue

        for seed in SEEDS:
            hof_fit_file = os.path.join(fit_type_dir, "s%d" % seed, "final_hof_fit.txt")
            if not os.path.exists(hof_fit_file):
                print "hof fit file does not exist for seed: %d", seed
                continue

            hof_fit = np.loadtxt(hof_fit_file)
            best_for_seed = np.min(hof_fit)
            if best_for_seed < best_error:
                best_seed = seed
                best_error = best_for_seed

        print "Best error for fit type %s is %f for seed %d" % (fit_type, best_error, best_seed)

        start_pop_file = os.path.join(fit_type_dir, "s%d" % best_seed, "final_hof.txt")
        new_fit_type_dir = os.path.join(output_directory, FIT_TYPES[fit_type])

        for seed in SEEDS:
            seed_dir = os.path.join(new_fit_type_dir, "s%d" % seed)
            if not os.path.exists(seed_dir):
                os.makedirs(seed_dir)

        target_file = os.path.join(output_directory, "target.json")
        target_data = json_utilities.read(target_file)
        has_apic = "apic" in target_data["passive"][0]["cm"]

        config = config_base_data.copy()
        config_path = os.path.join(new_fit_type_dir, "config.json")
        config["biophys"][0]["model_file"] = [ target_file, config_path]

        if has_apic:
            fit_style_file = os.path.join(FIT_BASE_DIR, "fit_styles", FIT_TYPES[fit_type] + "_fit_style.json")
        else:
            fit_style_file = os.path.join(FIT_BASE_DIR, "fit_styles", FIT_TYPES[fit_type] + "_noapic_fit_style.json")
        config["biophys"][0]["model_file"].append( fit_style_file )

        config["manifest"].append({"type": "dir", "spec": new_fit_type_dir, "key": "FITDIR"})
        config["manifest"].append({"type": "file", "spec": start_pop_file, "key": "STARTPOP"})

        json_utilities.write(config_path, config)

        for seed in SEEDS:
            logfile = os.path.join(new_fit_type_dir, 's%d' % seed, 'stage_2.log')

            jobs.append({
                    'config_path': os.path.abspath(config_path),
                    'fit_type': fit_type,
                    'log': os.path.abspath(logfile),
                    'seed': seed
                    })

    return jobs


def run_stage_2(jobs):
    for job in jobs:
        args = [MPIEXEC, '-np', '240', sys.executable, OPTIMIZE_SCRIPT, str(job['seed']), job['config_path']]
        print args
        with open(job['log'], "w") as outfile:
            subprocess.call(args, stdout=outfile)
        #subprocess.call(["/data/mat/nathang/deap_optimize/qsub_run.sh", "10", "24",
        #                 "{:s}_{:s}_{:s}_{:d}".format("eaf", cp[0], specimen_id, s), str(s), cp[1]],
        #                cwd="/data/mat/nathang/deap_optimize")



def main():
    parser = argparse.ArgumentParser(description='Set up DEAP-style fit for second stage')
    parser.add_argument('--output_dir', required=True)
    parser.add_argument('specimen_id', type=int)
    args = parser.parse_args()

    output_directory = os.path.join(args.output_dir, 'specimen_%d' % args.specimen_id)

    jobs = prepare_stage_2(output_directory)
    run_stage_2(jobs)

if __name__ == "__main__": main()

