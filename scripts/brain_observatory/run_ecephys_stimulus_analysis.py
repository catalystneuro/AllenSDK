import os
import io
import json
import subprocess
import glob
import pandas as pd
import numpy as np

def createInputJson(output_file):

    df = pd.read_csv('/mnt/md0/data/production_QC/experiment_table_2019-07-31.csv',index_col=0)

    bob_mice = np.sort(df[df['stimulus_set'].str.match('Brain')].index.values)

    nwb_files = ['/mnt/nvme0/ecephys_nwb_files_20190727/mouse' + str(mouse) + '.spikes.nwb2' for mouse in bob_mice[:24]]

    dictionary = { \

        "drifting_gratings" : 
        {
            "stimulus_key" : "drifting_gratings"
        },

        "static_gratings" : 
        {
            "stimulus_key" : "static_gratings"
        },

        "natural_scenes" : 
        {
            "stimulus_key" : "natural_scenes"
        },

        "natural_movies" : 
        {
            "stimulus_key" : "natural_movies"
        },

        "dot_motion" : 
        {
            "stimulus_key" : "dot_motion"
        },

        "contrast_tuning" : 
        {
            "stimulus_key" : "contrast_tuning"
        },


        "flashes" : 
        {
            "stimulus_key" : "flashes"
        },


        "receptive_field_mapping" : 
        {
            "stimulus_key" : "receptive_field_mapping",
            "mask_threshold" : 0.5,
            "minimum_spike_count" : 10
        },

        "output_file" : '/mnt/md0/data/production_QC/stimulus_analysis_TEST20190805.csv',

        "nwb_paths" : ['/mnt/nvme0/ecephys_nwb_files_20190727/mouse412804_integration_test_fc.spikes.nwb2',
                        '/mnt/nvme0/ecephys_nwb_files_20190727/integration_test.spikes.nwb2']#'
        #nwb_files[:20] 
    } 

    with io.open(output_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(dictionary, ensure_ascii=False, sort_keys=True, indent=4))

    return dictionary


json_directory = '/mnt/md0/data/json_files'

module = 'stimulus_analysis'

input_json = os.path.join(json_directory, module + '-input.json')
output_json = os.path.join(json_directory, module + '-output.json')

info = createInputJson(input_json)

command_string = ["python", "-W", "ignore", "-m", "allensdk.brain_observatory.ecephys." + module, 
                "--input_json", input_json,
                "--output_json", output_json]

subprocess.check_call(command_string)
