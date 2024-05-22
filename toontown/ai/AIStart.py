from panda3d.core import *
from otp.otpbase import PythonUtil
import builtins
import os

import argparse

from toontown.toonbase.ErrorTrackingService import ErrorTrackingService, ServiceType, SentryErrorTrackingService

parser = argparse.ArgumentParser(description='Toontown: Archipelago - AI Server')
parser.add_argument(
    '--base-channel',
    default=os.environ.get('BASE_CHANNEL'),
    help='The base channel that the server will use.'
)
parser.add_argument(
    '--max-channels',
    default=os.environ.get('MAX_CHANNELS'),
    help='The number of channels that the server will be able to use.'
)
parser.add_argument(
    '--stateserver',
    default=os.environ.get('STATESERVER'),
    help='The control channel of this AI\'s designated State Server.'
)
parser.add_argument(
    '--district-name',
    default=os.environ.get('DISTRICT_NAME'),
    help='The name of the district on this AI server.'
)
parser.add_argument(
    '--astron-ip',
    default=os.environ.get('ASTRON_IP'),
    help='The IP address of the Astron Message Director that this AI will connect to.'
)
parser.add_argument(
    '--eventlogger-ip',
    default=os.environ.get('EVENTLOGGER_IP'),
    help='The IP address of the Astron Event Logger that this AI will log to.'
)
parser.add_argument(
    'config',
    nargs='*',
    default=['config/common.prc', 'config/development.prc'],
    help='PRC file(s) that will be loaded on this AI instance.'
)

args = parser.parse_args()
for prc in args.config:
    loadPrcFile(prc)

localConfig = ''
if args.base_channel:
    localConfig += 'air-base-channel %s\n' % args.base_channel
if args.max_channels:
    localConfig += 'air-channel-allocation %s\n' % args.max_channels
if args.stateserver:
    localConfig += 'air-stateserver %s\n' % args.stateserver
if args.district_name:
    localConfig += 'district-name %s\n' % args.district_name
if args.astron_ip:
    localConfig += 'air-connect %s\n' % args.astron_ip
if args.eventlogger_ip:
    localConfig += 'eventlog-host %s\n' % args.eventlogger_ip

loadPrcFileData('AI Args Config', localConfig)


class game:
    name = 'toontown'
    process = 'server'


builtins.game = game

from otp.ai.AIBaseGlobal import *

from toontown.ai.ToontownAIRepository import ToontownAIRepository

version = simbase.config.GetString('version', 'v???')
simbase.errorReportingService = SentryErrorTrackingService(ServiceType.AI, version)

simbase.air = ToontownAIRepository(
    config.ConfigVariableInt('air-base-channel', 401000000).getValue(),
    config.ConfigVariableInt('air-stateserver', 10000).getValue(),
    config.ConfigVariableString('district-name', 'Toon Valley').getValue()
)

host = config.ConfigVariableString('air-connect', '127.0.0.1').getValue()
port = 7199
if ':' in host:
    host, port = host.split(':', 1)
    port = int(port)

simbase.air.connect(host, port)

try:
    run()
except SystemExit:
    raise
except Exception as error:
    info = PythonUtil.describeException()
    simbase.air.writeServerEvent('ai-exception', avId=simbase.air.getAvatarIdFromSender(),
                                 accId=simbase.air.getAccountIdFromSender(), exception=info)
    simbase.errorReportingService.report(error)
    raise
