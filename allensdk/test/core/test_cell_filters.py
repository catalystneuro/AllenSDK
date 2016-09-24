# Copyright 2016 Allen Institute for Brain Science
# This file is part of Allen SDK.
#
# Allen SDK is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Allen SDK is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Allen SDK.  If not, see <http://www.gnu.org/licenses/>.
import pytest
import pandas as pd
from mock import patch, mock_open, MagicMock
from test_brain_observatory_cache import CACHE_MANIFEST
from allensdk.core.brain_observatory_cache import BrainObservatoryCache

try:
    import __builtin__ as builtins # @UnresolvedImport
except:
    import builtins # @UnresolvedImport

@pytest.fixture
def cells():
    return [{u'tld1_id': 177839004,
             u'natural_movie_one_b_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/natural_movie_one_large.png',
             u'natural_movie_two_small': None,
             u'natural_movie_one_a_small': None,
             u'speed_tuning_c_large': None,
             u'speed_tuning_c_small': None,
             u'drifting_grating_small': None,
             u'tld1_name': u'Cux2-CreERT2',
             u'imaging_depth': 275,
             u'natural_scene_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/natural_scenes_large.png',
             u'tlr1_id': 265943423, u'natural_movie_one_b_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/natural_movie_one_small.png', u'natural_movie_two_large': None, u'speed_tuning_a_small': None, u'speed_tuning_b_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/speed_tuning_large.png',
             u'pref_dir_dg': None,
             u'natural_scene_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/natural_scenes_small.png',
             u'osi_sg': 0.728589701688166,
             u'osi_dg': None,
             u'tlr1_name': u'Ai93(TITL-GCaMP6f)',
             u'area': u'VISpm',
             u'pref_image_ns': 89.0,
             u'natural_movie_one_c_small': None,
             u'locally_sparse_noise_on_small': None,
             u'drifting_grating_large': None,
             u'experiment_container_id': 511498500,
             u'natural_movie_one_a_large': None,
             u'natural_movie_one_c_large': None,
             u'tld2_name': u'Camk2a-tTA',
             u'p_ns': 2.64407299505246e-05,
             u'static_gratings_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/static_gratings_all_small.png',
             u'natural_movie_three_large': None,
             u'pref_ori_sg': 30.0,
             u'speed_tuning_a_large': None,
             u'p_dg': None,
             u'time_to_peak_sg': 0.199499999999999,
             u'p_sg': 7.60972815250796e-05,
             u'time_to_peak_ns': 0.299249999999998,
             u'locally_sparse_noise_on_large': None,
             u'speed_tuning_b_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/speed_tuning_small.png',
             u'dsi_dg': None,
             u'pref_tf_dg': None,
             u'static_gratings_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394843/static_gratings_all_large.png',
             u'natural_movie_three_small': None,
             u'pref_sf_sg': 0.32,
             u'tld2_id': 177837320,
             u'locally_sparse_noise_off_large': None,
             u'locally_sparse_noise_off_small': None,
             u'cell_specimen_id': 517394843,
             u'pref_phase_sg': 0.5},
             {u'tld1_id': 177839004,
             u'natural_movie_one_b_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/natural_movie_one_large.png',
             u'natural_movie_two_small': None,
             u'natural_movie_one_a_small': None,
             u'speed_tuning_c_large': None,
             u'speed_tuning_c_small': None,
             u'drifting_grating_small': None,
             u'tld1_name': u'Cux2-CreERT2',
             u'imaging_depth': 275,
             u'natural_scene_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/natural_scenes_large.png',
             u'tlr1_id': 265943423,
             u'natural_movie_one_b_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/natural_movie_one_small.png',
             u'natural_movie_two_large': None,
             u'speed_tuning_a_small': None,
             u'speed_tuning_b_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/speed_tuning_large.png',
             u'pref_dir_dg': None,
             u'natural_scene_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/natural_scenes_small.png',
             u'osi_sg': 0.899272239777491,
             u'osi_dg': None,
             u'tlr1_name': u'Ai93(TITL-GCaMP6f)',
             u'area': u'VISpm',
             u'pref_image_ns': 15.0,
             u'natural_movie_one_c_small': None,
             u'locally_sparse_noise_on_small': None,
             u'drifting_grating_large': None,
             u'experiment_container_id': 511498500,
             u'natural_movie_one_a_large': None,
             u'natural_movie_one_c_large': None,
             u'tld2_name': u'Camk2a-tTA',
             u'p_ns': 0.000356823517642681,
             u'static_gratings_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/static_gratings_all_small.png',
             u'natural_movie_three_large': None,
             u'pref_ori_sg': 0.0,
             u'speed_tuning_a_large': None,
             u'p_dg': None,
             u'time_to_peak_sg': 0.565249999999996,
             u'p_sg': 0.0565790644804479,
             u'time_to_peak_ns': 0.432249999999997,
             u'locally_sparse_noise_on_large': None,
             u'speed_tuning_b_small': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/speed_tuning_small.png',
             u'dsi_dg': None,
             u'pref_tf_dg': None,
             u'static_gratings_large': u'/external/neuralcoding/prod6/specimen_503292439/ophys_experiment_510518066/thumbnails/517394850/static_gratings_all_large.png',
             u'natural_movie_three_small': None,
             u'pref_sf_sg': 0.32,
             u'tld2_id': 177837320,
             u'locally_sparse_noise_off_large': None,
             u'locally_sparse_noise_off_small': None,
             u'cell_specimen_id': 517394850,
             u'pref_phase_sg': 0.5}]

@pytest.fixture
def unmocked_boc():
    boc = BrainObservatoryCache()
    
    return boc

@pytest.fixture
def brain_observatory_cache():
    boc = None

    try:
        manifest_data = bytes(CACHE_MANIFEST,
             'UTF-8')  # Python 3
    except:
        manifest_data = bytes(CACHE_MANIFEST)  # Python 2.7

    with patch('os.path.exists',
               return_value=True):
        with patch(builtins.__name__ + ".open",
                   mock_open(read_data=manifest_data)):
            # Download a list of all targeted areas
            boc = BrainObservatoryCache(manifest_file='boc/manifest.json',
                                        base_uri='http://testwarehouse:9000')

    boc.api.json_msg_query = MagicMock(name='json_msg_query')

    return boc


@pytest.fixture
def example_filters():
    f = [
        { "field": "p_dg",
             "op": "<=",
             "value": 0.001 },
        { "field": "pref_dir_dg",
             "op": "=", "value": 45 },
        { "field": "area", "op": "in", "value": [ "VISpm" ] },
        { "field": "tld1_name", "op": "in", "value": [ "Rbp4-Cre", "Cux2-CreERT2", "Rorb-IRES2-Cre" ] }
    ]
    
    return f

FILTER_OPERATORS = ["=", "<", ">", "<=", ">=", "between", "in", "is"]
QUERY_TEMPLATES = {
    "=": '({0} == {1})',
    "<": '({0} < {1})',
    ">": '({0} > {1})',
    "<=": '({0} <= {1})',
    ">=": '({0} >= {1})',
    "between": '({0} >= {1}) and ({0} <= {1})',
    "in": '({0} == {1})',
    "is": '({0} == {1})'
}


@pytest.mark.skipif(True, reason="not done")
def test_dataframe_query(brain_observatory_cache,
                         example_filters,
                         cells):
    brain_observatory_cache = unmocked_boc
    with patch('os.path.exists',
               MagicMock(return_value=True)) as ope:
        with patch('allensdk.core.json_utilities.read',
                   MagicMock(return_value=cells)) as mju:
            cells = brain_observatory_cache.get_cell_specimens(
                filters=example_filters)
    
            assert len(cells) > 0


def test_dataframe_query_unmocked(unmocked_boc,
                                  example_filters,
                                  cells):
    brain_observatory_cache = unmocked_boc

    cells = brain_observatory_cache.get_cell_specimens(
        filters=example_filters)
    
    # total lines = 18260, can make fail by passing no filters
    expected = 105
    assert len(cells) == expected
