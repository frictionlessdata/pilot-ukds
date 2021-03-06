# UKDS Pipeline Pilot

[![Travis](https://img.shields.io/travis/frictionlessdata/pilot-ukds/master.svg)](https://travis-ci.org/frictionlessdata/pilot-ukds)
[![Coveralls](http://img.shields.io/coveralls/frictionlessdata/pilot-ukds.svg?branch=master)](https://coveralls.io/r/frictionlessdata/pilot-ukds?branch=master)

An example [Data Package Pipeline](https://github.com/frictionlessdata/datapackage-pipelines/) to harvest data from UKDS, transform, validate, define visualizations, and import into datahub.io. 

As well as the pipeline, this repository maintains a pipeline processor to add [OAI-PMH](http://www.openarchives.org/OAI/openarchivesprotocol.html) dataset metadata to the datapackage: `ukds.add_oai_metadata`. View specs can be added to a datapackage with the `ukds.add_datapackage_views` processor.

The following pipeline plugins are also used by the pipeline:
- [datapackage-pipelines-spss](https://github.com/frictionlessdata/datapackage-pipelines-spss): `spss.add_spss`
- [datapackage-pipelines-goodtables](https://github.com/frictionlessdata/datapackage-pipelines-goodtables): `goodtables.validate`
- [datapackage-pipelines-datahub](https://github.com/datahq/datapackage-pipelines-datahub): `datahub.dump.to_datahub` ([`datahub-cli`](https://github.com/datahq/datahub-cli) is required for this plugin)

The basic flow from the UKDS Reshare resource, to the final datahub.io entry is outlined in the diagram below:

![Pipeline flow](https://raw.githubusercontent.com/frictionlessdata/pilot-ukds/master/data/ukds_flow.png)

The source-spec is defined in `/entries/ukds.source-spec.yaml`:

```yml
oai-url:
  http://reshare.ukdataservice.ac.uk/cgi/oai2

entries:
  my-first-entry:  # a remote spss resource
    source:
      - url: http://reshare.ukdataservice.ac.uk/851500/2/my-spss-file.sav
        format: spss
    oai-id: 851500

  my-second-entry:  # a local csv resource with a view
    source:
      - url: ../data/my-csv-file.csv
        format: csv
        tabulator:
          headers: 1
    views:
      - views/my-views-spec.json

  my-multiple-item:  # multiple resources
    source:
      - url: ../data/Employee data.sav
        format: spss
      - url: ../data/invalid.csv
        format: csv
    oai-id: 851501
```

Where `oai-url` is the entry point for the OAI service, and `entries` is a collection of resources which we're interested in harvesting from UKDS, and uploading to datahub.io.

If an entry has an `oai-id` property, this will be used to harvest dataset metadata from UKDS to populate the datapackage.

The `views` property is a list of file paths to json files containing [view-spec](https://specs.frictionlessdata.io/views/) compatible views.
