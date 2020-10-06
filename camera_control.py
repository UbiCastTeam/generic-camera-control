#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import requests
import argparse

LOG_RESTORE = '\033[1;0m'
LOG_GRAY = '\033[37m'
LOG_WHITE = '\033[1m'
LOG_YELLOW = '\033[1;93m'
LOG_RED = '\033[1;91m'

logging.addLevelName(logging.DEBUG, '%s%s%s' % (LOG_GRAY, logging.getLevelName(logging.DEBUG), LOG_RESTORE))
logging.addLevelName(logging.INFO, '%s%s%s' % (LOG_WHITE, logging.getLevelName(logging.INFO), LOG_RESTORE))
logging.addLevelName(logging.WARNING, '%s%s%s' % (LOG_YELLOW, logging.getLevelName(logging.WARNING), LOG_RESTORE))
logging.addLevelName(logging.ERROR, '%s%s%s' % (LOG_RED, logging.getLevelName(logging.ERROR), LOG_RESTORE))

logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    stream=sys.stdout,
    level=logging.INFO
)
logger = logging.getLogger('camera_control.py')

DRY_RUN = False


def do_request(url):
    response = None
    if not DRY_RUN:
        response = requests.get(url, timeout=5)

        if not response.status_code == 200:
            raise Exception('Request fail with status code %s and content \n %s' % (response.status_code, response.text))
        else:
            logger.info('Call success!')
            logger.debug(response.status_code)
            logger.debug(response.text)
    return response


def generic_preset(urls, preset_id, ip, params, proxy):
    url = urls['preset_call'].format(ip=ip, preset_id=preset_id)
    if proxy:
        url = url.replace('http://', proxy)
    if params:
        if '?' in url:
            url = '%s&%s' % (url, params)
        else:
            url = '%s?%s' % (url, params)
    logger.debug('Call preset %s' % url)
    do_request(url)


def panasonic_generic(action, action_data, params, ip, model, proxy, urls):
    if action not in ['preset']:
        raise Exception('Action %s not supported' % action)
    if action == 'preset':
        generic_preset(urls, action_data, ip, params, proxy)


def sony_generic(action, action_data, params, ip, model, proxy, urls):
    if action not in ['preset']:
        raise Exception('Action %s not supported' % action)
    if action == 'preset':
        generic_preset(urls, action_data, ip, params, proxy)


def canon_generic(action, action_data, params, ip, model, proxy, urls):
    if action not in ['apply-settings']:
        raise Exception('Action %s not supported' % action)
    url = urls['session_id'].format(ip=ip)
    if proxy:
        url = url.replace('http://', proxy)
    logger.debug('GET SESSION ID %s' % url)
    response = do_request(url)
    if not DRY_RUN:
        session_id = response.text.split('\n')[0].replace('s:=', '')
    else:
        session_id = 'test'
    logger.debug('SESSION ID is %s' % session_id)

    url = urls['request_control'].format(ip=ip, session_id=session_id)
    if proxy:
        url = url.replace('http://', proxy)
    logger.debug('Request control %s' % url)
    do_request(url)

    if action == 'apply-settings':
        url = urls['settings_call'].format(ip=ip, session_id=session_id, params=action_data)
        if proxy:
            url = url.replace('http://', proxy)
        if params:
            if '?' in url:
                url = '%s&%s' % (url, params)
            else:
                url = '%s?%s' % (url, params)
        logger.debug('Apply settings %s' % url)
        do_request(url)

    url = urls['leave_control'].format(ip=ip, session_id=session_id)
    if proxy:
        url = url.replace('http://', proxy)
    logger.debug('Leave control %s' % url)
    do_request(url)


CAMERA_SETTINGS = {
    'sony-generic': {
        'method': sony_generic,
        'urls': {
            'preset_call': 'http://{ip}/command/presetposition.cgi?PresetCall={preset_id}'
        }
    },
    'panasonic-generic': {
        'method': panasonic_generic,
        'urls': {
            'preset_call': 'http://{ip}/cgi-bin/aw_ptz?cmd=%23{preset_id}&res=1'
        }
    },
    'canon-generic': {
        'method': canon_generic,
        'urls': {
            'session_id': 'http://{ip}/-wvhttp-01-/open.cgi',
            'request_control': 'http://{ip}/-wvhttp-01-/claim.cgi?s={session_id}',
            'settings_call': 'http://{ip}/-wvhttp-01-/control.cgi?s={session_id}&{params}',
            'leave_control': 'http://{ip}/-wvhttp-01-/yield.cgi?s={session_id}'
        }
    }
}


def do_action(action, action_data, params, ip, model, proxy):
    if model not in CAMERA_SETTINGS.keys():
        logger.error('Model %s not supported' % model)
    else:
        try:
            CAMERA_SETTINGS[model]['method'](action, action_data, params, ip, model, proxy, CAMERA_SETTINGS[model]['urls'])
        except Exception as e:
            logger.error(e)


def main(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    actions_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "--ip",
        help="Camera ip. Example: 1.2.3.4",
        type=str,
        required=True
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Camera model in this list [sony-generic, panasonic-generic, canon-generic]",
        type=str
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Set verbosity to DEBUG",
        action="store_true"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="Avoid requesting and set verbosity to DEBUG",
        action="store_true"
    )
    actions_group.add_argument(
        "--call-preset",
        help="Action to call a particular preset. Examples: 1 | R00 | 1,24",
        type=str
    )
    actions_group.add_argument(
        "--apply-settings",
        help="Action to apply settings on a camera. Example: pan=-1053&tilt=-1219&zoom=2689&ae.brightness=0",
        type=str
    )
    parser.add_argument(
        "--params",
        help="Extra url params. Example: a=b&c=d",
        type=str
    )
    parser.add_argument(
        "--proxy",
        help="Proxy replace base uri. Example: https://proxy/12354/camera/",
        type=str
    )
    args = parser.parse_args()
    action = ''
    action_data = ''
    params = ''
    ip = None
    model = None
    proxy = None
    opt = ''
    for opt, arg in vars(args).items():
        if opt in ('h', 'help'):
            parser.print_help()
            sys.exit()
        elif opt in ('v', 'versbose'):
            logger.setLevel(logging.DEBUG)
            logger.debug('Verbose logs enabled')
        elif opt in ('d', 'dry_run'):
            logger.setLevel(logging.DEBUG)
            logger.debug('Dry run enabled')
            global DRY_RUN
            DRY_RUN = True
        elif opt == 'call_preset':
            action = 'preset'
            action_data = arg
        elif opt == 'apply_settings':
            action = 'apply-settings'
            action_data = arg
        elif opt == 'params':
            params = arg
        elif opt == 'ip':
            ip = arg
        elif opt == 'model':
            model = arg
        elif opt == 'proxy':
            proxy = arg
    if not ip or not model or not action:
        logger.error('--ip, --model and an action [--call-preset, --apply-settings] are required')
        parser.print_help()
        sys.exit(3)
    if proxy and not proxy.endswith('/'):
        proxy += '/'
    logger.debug('Params: action %s params %s ip %s model %s proxy %s' % (action, params, ip, model, proxy))
    do_action(action, action_data, params, ip, model, proxy)


if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit()
