def ldap_authenticate(server, auth_username, username, password):
    from ldap3 import Server, Connection
    server = Server(server, use_ssl=True)
    with Connection(server, auth_username.format(username), password,
                    raise_exceptions=False) as conn:
        return conn.bind()
