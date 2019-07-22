import os
import io
import json
import subprocess
import glob

def createInputJson(output_file):

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
            "stimulus_key" : "Natural Images"
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
            "stimulus_key" : "flash_250ms"
        },


        "receptive_field_mapping" : 
        {
            "stimulus_key" : "gabor_20_deg_250ms",
            "spatial_p_value_n_iter" : 20,
            "mask_threshold" : 0.5,
            "minimum_spike_count" : 10
        },

        "output_file" : '/mnt/md0/data/production_QC/stimulus_analysis_TEST.csv',

        "nwb_paths" : ['/mnt/nvme0/ecephys_nwb_files/750749662.spikes.nwb2']
        
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
