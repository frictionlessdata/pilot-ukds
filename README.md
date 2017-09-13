# UKDS Pipeline Pilot

[![Travis](https://img.shields.io/travis/frictionlessdata/pilot-ukds/master.svg)](https://travis-ci.org/frictionlessdata/pilot-ukds)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/pilot-ukds.svg?branch=master)](https://coveralls.io/r/frictionlessdata/pilot-ukds?branch=master)

An example [Data Package Pipeline](https://github.com/frictionlessdata/datapackage-pipelines/) to export data from UKDS, transform, validate, define visualizations, and import into datahub.io. The basic flow from the UKDS Reshare resource, to the final datahub.io entry is outlined in the diagrame below:

```
    UKDS Reshare

              +--------------------+
              |                    |
              |  UKDS open access  |
              |  resource          |
              |                    |
              +--------------------+

 +-------------------------------------------------------------+

    UKDS Datapackage Pipeline

          +-----------------------------+
          |                             |
          |  datapackage-pipeline-ukds  |
          |   - spss                    |
          |   - csv                     |
          |                             |
          +--------------+--------------+
                         |
               +---------+---------------------+
     CSV       |                               |    SPSS
               |                               |
+--------------v--------------+  +-------------v---------------+
|                             |  |                             |
|  datapackage-pipelines.lib  |  |  datapackage-pipeline-spss  +-----+ tableschema-spss-py
|   - add_resource            |  |   - add_spss                |
|   - stream_remote_resource  |  |                             |
|                             |  +-------------+---------------+
+--------------+--------------+                |
               |                               |
               +---------+---------------------+
                         |
       +-----------------v-----------------+
       |                                   |
       |  datapackage-pipeline-goodtables  +-------+ goodtables-py
       |   - validate                      |
       |                                   |
       +-----------------+-----------------+
                         |
                         |
         +---------------v----------------+
         |                                |
         |  datapackage-pipeline-datahub  |
         |   - dump_to.datahub            |
         |                                |
         +---------------+----------------+
                         |
+-----------------------------------------------------------------+
                         |
     datahub.io          |
                         |
              +----------v---------+
              |                    |
              |  datahub.io entry  |
              |                    |
              +--------------------+
```

Each entry is defined in `/entries/ukds.source-spec.yaml`, in the following way:

```yml
my-first-entry:  # a remote spss resource
  source: http://reshare.ukdataservice.ac.uk/851500/2/my-spss-file.sav
  format: spss

my-second-entry:  # a local csv resource
  source: ../data/my-csv-file.csv
  format: csv
  tabulator:
    headers: 1
```
