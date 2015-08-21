# coding=utf-8

"""
Mantrid - Python HTTP load balancer

#### Dependencies

 * /usr/local/bin/mantrid-client

Author: Slawomir Skowron <szibis@gmail.com>

"""

import diamond.collector
import subprocess
import os
import string
from diamond.collector import str_to_bool


class MantridCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        super(MantridCollector, self).__init__(*args, **kwargs)

        self.statcommand = [self.config['bin'], 'stats']

        if str_to_bool(self.config['use_sudo']):
            self.statcommand.insert(0, self.config['sudo_cmd'])

    def get_default_config_help(self):
        config_help = super(MantridCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'Path to mantrid-client binary',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MantridCollector, self).get_default_config()
        config.update({
            'bin':              '/usr/local/bin/mantrid-client',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
            'path':             'mantrid'
        })
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK):
            self.log.error("%s is not executable", self.config['bin'])
            return False

        if (str_to_bool(self.config['use_sudo'])
            and not os.access(self.config['sudo_cmd'], os.X_OK)):

            self.log.error("%s is not executable", self.config['sudo_cmd'])
            return False

        client = subprocess.Popen(self.statcommand,
			stdout=subprocess.PIPE).communicate()

        columns = {
            'open': 1,
            'completed': 2,
            'inbytes': 3,
            'outbytes': 4,
        }

	for i, line in enumerate(client[0][:-1].split("\n")):
            if i < 1:
                continue
            row = line.split()

            host = string.replace(row[0], ".", "_")
            external = host_under

            for metric, column in columns.iteritems():
                metric_name = ".".join([external, metric])
                metric_value = row[column]

                self.publish(metric_name, metric_value)
