import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from neobytesd import NeobytesDaemon
from neobytes_config import NeobytesConfig


def test_neobytesd():
    config_text = NeobytesConfig.slurp_config_file(config.neobytes_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000002333ac985182810346a7c4c81dff5b73597e9aadc7dd2f5b23e80817d8c'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000348738de1d1d9dbc9633d2ed265fd8ca626edd91ff63001a2c3b97927fe'

    creds = NeobytesConfig.get_rpc_creds(config_text, network)
    neobytesd = NeobytesDaemon(**creds)
    assert neobytesd.rpc_command is not None

    assert hasattr(neobytesd, 'rpc_connection')

    # Neobytes testnet block 0 hash == 00000348738de1d1d9dbc9633d2ed265fd8ca626edd91ff63001a2c3b97927fe
    # test commands without arguments
    info = neobytesd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert neobytesd.rpc_command('getblockhash', 0) == genesis_hash
