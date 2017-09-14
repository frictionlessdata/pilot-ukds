from .test_utils import TestBase


class TestOAIRepository(TestBase):

    def test_get_record_identifier(self):
        oai_id = '851500'
        record_id = self.oai_repo.get_oai_record_identifier(oai_id)
        self.assertEqual(record_id, 'oai:reshare.ukdataservice.ac.uk:851500')

    def test_get_record_metadata(self):
        oai_id = '851500'
        record_metadata = self.oai_repo.get_oai_record_metadata(oai_id)
        expected_dict = {
            'title': ['Farm Management Survey- SPSS data set'],
            'creator': ['Winter, Michael'],
            'subject': ['Environment, conservation and land use',
                        'History', 'Economics', 'Industry and management'],
            'description': ['A description of the data set...'],
            'publisher': ['UK Data Archive'],
            'type': ['Data Collection', 'NonPeerReviewed'],
            'format': ['other', 'other', 'other', 'other'],
            'identifier': ['http://reshare.ukdataservice.ac.uk/851500/1/RES-062-23-1831%20SPSS%20data%20handbook.xlsx',  # noqa
                           'http://reshare.ukdataservice.ac.uk/851500/2/RES-062-23-1831%20FBS%20data%20for%20ESRC%20archive.sav',  # noqa
                           'http://reshare.ukdataservice.ac.uk/851500/3/nofile/',  # noqa
                           'unknown://notapath',
                           '  Winter, Michael   Farm Management Survey- SPSS data set.  [Data Collection]   [error in script]  '],  # noqa
            'relation': ['http://reshare.ukdataservice.ac.uk/851500/']}
        self.assertEqual(record_metadata, expected_dict)
