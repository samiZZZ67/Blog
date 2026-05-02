#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import ssl
import sys
from pathlib import Path


def patch_sslserver_compat():
    if hasattr(ssl, 'wrap_socket'):
        return

    def wrap_socket(sock, keyfile=None, certfile=None, server_side=False,
                    cert_reqs=ssl.CERT_NONE, ssl_version=None, ca_certs=None,
                    do_handshake_on_connect=True, suppress_ragged_eofs=True,
                    ciphers=None):
        protocol = ssl_version
        if server_side and protocol in (None, ssl.PROTOCOL_TLS):
            protocol = ssl.PROTOCOL_TLS_SERVER
        elif protocol is None:
            protocol = ssl.PROTOCOL_TLS_CLIENT
        context = ssl.SSLContext(protocol)
        context.verify_mode = cert_reqs

        if certfile:
            context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        if ca_certs:
            context.load_verify_locations(ca_certs)
        if ciphers:
            context.set_ciphers(ciphers)

        return context.wrap_socket(
            sock,
            server_side=server_side,
            do_handshake_on_connect=do_handshake_on_connect,
            suppress_ragged_eofs=suppress_ragged_eofs,
        )

    ssl.wrap_socket = wrap_socket


def configure_dev_https():
    if len(sys.argv) < 2 or sys.argv[1] != 'runserver':
        return

    sys.argv[1] = 'runsslserver'

    cert_dir = Path(__file__).resolve().parent / '.certs'
    certificate = cert_dir / 'localhost.crt'
    key = cert_dir / 'localhost.key'

    if certificate.exists() and not any(
        arg == '--certificate' or arg.startswith('--certificate=')
        for arg in sys.argv[2:]
    ):
        sys.argv.extend(['--certificate', str(certificate)])

    if key.exists() and not any(
        arg == '--key' or arg.startswith('--key=')
        for arg in sys.argv[2:]
    ):
        sys.argv.extend(['--key', str(key)])


def main():
    """Run administrative tasks."""
    patch_sslserver_compat()
    configure_dev_https()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
