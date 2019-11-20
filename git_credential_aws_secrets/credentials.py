import os
import sys
import json
import configparser
import botocore
import botocore.session
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig


def parse_config():
    try:
        cfgfile = os.environ['GIT_CREDENTIALS_AWS_CONFIG']
    except KeyError:
        cfgfile = os.path.join(os.getenv('HOME'), '.git_credential_aws')
    config = configparser.ConfigParser()
    config.read_file(open(cfgfile, 'r'))
    return config


def lookup(args, pfile):
    if len(args) < 2:
        print("Usage: %s get" % os.path.basename(sys.argv[0]), file=sys.stderr)
        return 1
    # only support retrieval, not storage or deletion
    if args[1] != "get":
        return 1
    params = {}
    for line in pfile:
        key, val = line.strip().split('=')
        params[key.strip()] = val.strip()
    cfg = parse_config()
    if 'host' not in params:
        return 1
    if 'username' in params:
        key = '%s@%s' % (params['username'], params['host'])
        if key not in cfg:
            return 1
        username = params['username']
    else:
        key = params['host']
        if key not in cfg:
            return 1
        try:
            username = cfg[key]['username']
        except KeyError:
            username = None

    secretname = cfg[key]['secretname']
    client = botocore.session.get_session().create_client('secretsmanager')
    cache = SecretCache(config=SecretCacheConfig(), client=client)
    pwent = cache.get_secret_string(secretname)
    pwdict = json.loads(pwent)
    if username:
        print("username=%s" % username)
    print("password=%s" % pwdict[secretname])
    return 0


def main():
    return lookup(sys.argv, sys.stdin)


if __name__ == "__main__":
    try:
        ret = main()
        sys.exit(ret)
    except SystemExit:
        pass
    except Exception:
        import traceback

        traceback.print_exc(5)
        sys.exit(1)
