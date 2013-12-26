#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch
from diamond.collector import Collector
from mantrid import MantridCollector

##########################################################################


class TestMantridCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('Mantridollector', {
            'interval': 10,
            'bin': 'true',
            'use_sudo': False
        })

        self.collector = MantridCollector(config, None)

    def test_import(self):
        self.assertTrue(MantridCollector)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        patch_communicate = patch('subprocess.Popen.communicate',
                                   Mock(return_value=(
                                    self.getFixture('stats').getvalue(),
				    '')))

        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        metrics = {
            "mantrid.-new_example_com.open": 0,
            "mantrid.-new_example_com.completed": 0,
            "mantrid.-new_example_com.inbytes": 0,
            "mantrid.-new_example_com.outbytes": 0,
            "mantrid._example_com.open": 0,
	    "mantrid._example_com.completed": 6,
	    "mantrid._example_com.inbytes": 4600,
	    "mantrid._example_com.outbytes": 0,
	    "mantrid.automate_example_com.open": 0,
	    "mantrid.automate_example_com.completed": 0,
	    "mantrid.automate_example_com.inbytes": 0,
	    "mantrid.automate_example_com.outbytes": 0,
	    "mantrid.example_com.open": 2,
	    "mantrid.example_com.completed": 1165,
	    "mantrid.example_com.inbytes": 2103000,
	    "mantrid.example_com.outbytes": 546100,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

if __name__ == "__main__":
    unittest.main()
