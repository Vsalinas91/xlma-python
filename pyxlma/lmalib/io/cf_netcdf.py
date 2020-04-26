import copy

import numpy as np
import xarray as xr

# this dictionary describes the minmum variables that must be included for a valid LMA NetCDF event and flash file.
__template_dataset = {'coords': {},
 'attrs': {'title': 'Lightning Mapping Array dataset',
  'production_date': '1970-01-01 00:00:00 +00:00',
  'production_site': 'Default',
  'event_algorithm_name':'unknown',
  'event_algorithm_version':'unknown',
  'flash_algorithm_name':'unknown',
  'flash_algorithm_version':'unknown',
  'cf_tree_order':"number_of_flashes number_of_events",
  },
 'dims': {'number_of_events': 1,
  'number_of_flashes': 1,
  'number_of_stations': 1,
  'string1': 1,
  'string32': 32
  },
 'data_vars': {
  'flash_distance_separation_threshold': {'dims': (),
     'attrs': {'long_name': 'Separation threshold distance in three spatial dimensions for flash grouping',
      'units': 'meters'},
     'dtype': 'float32',
     'data' : 0.0,
     'shape': ()},
  'flash_time_separation_threshold': {'dims': (),
     'attrs': {'long_name': 'Separation threshold in time for flash grouping',
      'units': 'seconds'},
     'dtype': 'float32',
     'data' : 0.0,
     'shape': ()},
  'flash_duration_threshold': {'dims': (),
     'attrs': {'long_name': 'Maximum flash duration',
      'units': 'seconds'},
     'dtype': 'float32',
     'data' : 0.0,
     'shape': ()},
  'flash_time_merge_threshold': {'dims': (),
     'attrs': {'long_name': 'Secondary threshold in time for merger of flashes',
      'units': 'seconds'},
     'dtype': 'float32',
     'data' : 0.0,
     'shape': ()},
  'network_center_latitude': {'dims': (),
     'attrs': {'long_name': 'Latitude of network center used in event processing',
      'units': 'degrees_north',
      'standard_name': 'latitude'},
     'data' : 0.0,
     'dtype': 'float32',
     'shape': ()},
  'network_center_longitude': {'dims': (),
     'attrs': {'long_name': 'Longitude of network center used in event processing',
      'units': 'degrees_east',
      'standard_name': 'longitude',},
     'dtype': 'float32',
     'data' : 0.0,
     'shape': ()},
  'flash_id': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.iinfo(np.uint64).max,
             'child':'event_id', 'cf_role':'tree_id'},
   'dtype': 'uint64',
   },
  'flash_time_start': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'standard_name': 'time',
    'long_name': 'Start time of flash',
    'units': 'seconds since 2018-09-13 00:00:00 +00:00'},
   'dtype': 'float64',
   },
  # must have either flash_time_end or flash_duration, or both.
  'flash_time_end': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'standard_name': 'time',
    'long_name': 'End time of flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    'units': 'seconds since 2018-09-13 00:00:00 +00:00'},
   'dtype': 'float64',
   },
  'flash_duration': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'long_name': 'Duration of flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    'units': 'seconds'},
   'dtype': 'float64',
   },
  'flash_init_latitude': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'degrees_east',
    'standard_name': 'latitude',
    'long_name': 'Latitude of flash origin',},
   'dtype': 'float32',
   },
  'flash_init_longitude': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'degrees_north',
    'standard_name': 'longitude',
    'long_name': 'Longitude of flash origin',
    },
   'dtype': 'float32',
   },
  'flash_init_altitude': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'meters',
    'standard_name': 'altitude',
    'long_name': 'Altitude of flash origin',
    },
   'dtype': 'float32',
   },
  'flash_area': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'km^2',
    'long_name': 'Area of flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    },
   'dtype': 'float32',
   },
  'flash_volume': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'km^3',
    'long_name': 'Volume of flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    },
   'dtype': 'float32',
   },
  'flash_center_latitude': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'degrees_east',
    'standard_name': 'latitude',
    'long_name': 'centroid latitude of the flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    },
   'dtype': 'float32',
   },
  'flash_center_longitude': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'degrees_north',
    'standard_name': 'longitude',
    'long_name': 'centroid longitude of the flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    },
   'dtype': 'float32',
   },
  'flash_center_altitude': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.nan,
    'units': 'meters',
    'standard_name': 'altitude',
    'long_name': 'centroid altitude of the flash',
    'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
    },
   'dtype': 'float32',
   },
  'flash_event_count': {'dims': ('number_of_flashes',),
   'attrs': {'_FillValue': np.iinfo(np.uint32).max,
     'long_name':'Count of events in flash',
     'coordinates':'flash_id flash_time_start flash_init_altitude flash_init_latitude flash_init_longitude',
     'valid_min':1},
   'dtype': 'uint32',
   },
  'event_id': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.iinfo(np.uint64).max,
    'parent_id':'event_parent_flash_id',
    'parent':'flash_id', 'cf_role':'tree_id'},
   'dtype': 'uint64',
   },
  'event_parent_flash_id': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.iinfo(np.uint64).max,
             'cf_role':'tree_id', 'coordinates':'event_id'},
   'dtype': 'uint64',
   },
  'event_latitude': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.nan,
    'valid_range': [-90.0, 90.0],
    'units': 'degrees_north',
    'standard_name': 'latitude',
    'long_name': 'Latitude of event'},
   'dtype': 'float32',
   },
  'event_longitude': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.nan,
    'valid_range': [-180.0, 180.0],
    'units': 'degrees_east',
    'standard_name': 'longitude',
    'long_name': 'Longitude of event'},
   'dtype': 'float32',
   },
  'event_altitude': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.nan,
    'valid_range': [-100.0, 40000.0],
    'units': 'meters',
    'standard_name': 'altitude',
    'long_name': 'Altitude of event',
    'positive': 'up'},
   'dtype': 'float32',
   },
  'event_time': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.nan,
    'standard_name': 'time',
    'long_name': 'Time of event',
    'units': 'seconds since 2018-09-13 00:00:00 +00:00'},
   'dtype': 'float64',
   },
  'event_power': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.nan, 'units': 'dB milliwatts',
    'long_name': 'Power emitted at event location',
    'coordinates':'event_id event_time event_latitude event_longitude'},
   'dtype': 'float32',
   },
  'event_mask': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': 0,
    'long_name': 'Bitwise mask of contributing stations',
    'coordinates':'event_id event_time event_latitude event_longitude'},
   'dtype': 'uint32',
   },
  'event_stations': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': 0, 'long_name': 'Number of contributing stations ',
    'coordinates':'event_id event_time event_latitude event_longitude',
    'valid_range': [5, 255],},
   'dtype': 'uint8',
   },
  'event_chi2': {'dims': ('number_of_events',),
   'attrs': {'_FillValue': np.nan,
    'long_name': 'Reduced chi-square goodness of fit to arrival time differences',
    'coordinates':'event_id event_time event_latitude event_longitude',
    'valid_range': [0.0, 1.0],},
   'dtype': 'float32',
   },
  'station_code': {'dims': ('number_of_stations',),# 'string1'),
   'attrs': {'_FillValue': ' ',
   'long_name': 'LMA station identifier and event station mask order'},
   'dtype': '|S1',
   },
  'station_network': {'dims': ('number_of_stations',),# 'string32'),
   'attrs': {'_FillValue': ' '*32, 'long_name': 'LMA network'},
   'dtype': '|S32',
   },
  'station_latitude': {'dims': ('number_of_stations',),
   'attrs': {'_FillValue': np.nan,
    'valid_range': [-90.0, 90.0],
    'units': 'degrees_north',
    'standard_name': 'latitude'},
   'dtype': 'float32',
   },
  'station_longitude': {'dims': ('number_of_stations',),
   'attrs': {'_FillValue': np.nan,
    'valid_range': [-180.0, 180.0],
    'units': 'degrees_east',
    'standard_name': 'longitude'},
   'dtype': 'float32',
   },
  'station_altitude': {'dims': ('number_of_stations',),
   'attrs': {'_FillValue': np.nan,
    'valid_range': [-100.0, 40000.0],
    'units': 'meters',
    'standard_name': 'altitude',
    'positive': 'up'},
   'dtype': 'float32',
   },
}}

def validate_events(ds, dim='number_of_events', check_events=True, check_flashes=True):
    """ Take an xarray dataset ds and check to ensure all expected variables
        and attributes exist. Print a report of anything that doesn't match.
    """
    # Will need to make dimensions and data equal for this to work. Subset to
    # zero-length dimensions? I think that drops the dim. So subset to single length and then assing a value of zero to each variable?
    # http://xarray.pydata.org/en/stable/generated/xarray.testing.assert_identical.html#xarray.testing.assert_identical
    # should come with a diff report https://github.com/pydata/xarray/pull/1507
    # use try: except: because we expect differences, and simply want to report them
    pass

def new_dataset(events=None, flashes=None, stations=None, **kwargs):
    """ Create a new, empty xarray dataset for LMA data.

    Keyword arguments:
      events (int, optional): number of events
      flashes (int, optional): number of flashes
      stations (int, optional): number of stations
      production_date: a datetime object
      production_site (string): Information about the production site
      event_algorithm_name (string): The name of the algorithm used to locate
        station-level triggers as events. For LMA data, usually lma_analysis.
        May also be the command issued to process the data, with any relevant
        information regarding data quality thresholds also reported in
        data variables reserved for that purpose.
      event_algorithm_version (string): The event algorithm version
      flash_algorithm_name (string): The name of the algorithm used to cluster
        events to flashes. May also be the command issued to process the data,
        with any relevant information regarding space-time separation thresholds
        also reported in data variables reserved for that purpose.
      flash_algorithm_version (string): The flash algorithm version
     Any other keyword arguments are also added as a global attribute.

    If event, flash, or station information are not known, passing None
    (default) will drop variables associated with that dimension
    """
    ds_dict = copy.deepcopy(__template_dataset)
    event_keys = [k for k in ds_dict['data_vars'].keys()
                  if k.startswith('event')]
    flash_keys = [k for k in ds_dict['data_vars'].keys()
                  if k.startswith('flash')]
    station_keys = [k for k in ds_dict['data_vars'].keys()
                    if k.startswith('station')]

    global_attr_kwargs = ['production_date', 'production_site',
        'event_algorithm_name', 'event_algorithm_version',
        'flash_algorithm_name', 'flash_algorithm_version']
    ds_dict['attrs'].update(kwargs)


    if events is not None:
        ds_dict['dims']['number_of_events'] = events
        for k in event_keys:
            if 'data' not in ds_dict['data_vars'][k].keys():
                fill = ds_dict['data_vars'][k]['attrs']['_FillValue']
                dtype = ds_dict['data_vars'][k]['dtype']
                ds_dict['data_vars'][k]['data'] = np.full(events,
                                                          fill, dtype=dtype)
    else:
        # remove events dimension and variables and flash child info
        ds_dict['dims'].pop('number_of_events')
        for k in event_keys: ds_dict['data_vars'].pop(k)
        # No longer have a tree, so remove parent-child info
        ds_dict['flash_id']['attrs'].pop('child')
        ds_dict['flash_id']['attrs'].pop('cf_role')
        ds_dict['attrs'].pop('cf_tree_order')

    if flashes is not None:
        ds_dict['dims']['number_of_flashes'] = flashes
        for k in flash_keys:
            if 'data' not in ds_dict['data_vars'][k].keys():
                fill = ds_dict['data_vars'][k]['attrs']['_FillValue']
                dtype = ds_dict['data_vars'][k]['dtype']
                ds_dict['data_vars'][k]['data'] = np.full(flashes,
                                                          fill, dtype=dtype)
    else:
        # remove flashes dimension and variables and flash child info
        ds_dict['dims'].pop('number_of_flashes')
        for k in flash_keys: ds_dict['data_vars'].pop(k)
        # No longer have a tree, so remove parent-child info
        ds_dict['data_vars'].pop('event_parent_flash_id')
        ds_dict['event_id']['attrs'].pop('parent')
        ds_dict['event_id']['attrs'].pop('parent_id')
        ds_dict['event_id']['attrs'].pop('cf_role')
        ds_dict['attrs'].pop('cf_tree_order')

    if stations is not None:
        ds_dict['dims']['number_of_stations'] = stations
        for k in station_keys:
            if 'data' not in ds_dict['data_vars'][k].keys():
                fill = ds_dict['data_vars'][k]['attrs']['_FillValue']
                dtype = ds_dict['data_vars'][k]['dtype']
                ds_dict['data_vars'][k]['data'] = np.full(stations,
                                                          fill, dtype=dtype)
    else:
        ds_dict['dims'].pop('number_of_stations')
    # import pprint; pprint.pprint(ds_dict)
    return xr.Dataset.from_dict(ds_dict)