

def check_systemd_service(unit, service):
    '''Return true if the systemd service is running and enabled. If it is not
    active, get the journal for that service.'''
    systemctl_is_active = 'systemctl is-active {0}'
    output, active = run(unit, systemctl_is_active.format(service))
    if active != 0:
        journalctl = 'journalctl -u {0}'
        run(unit, journalctl.format(service))
    systemctl_is_enabled = 'systemctl is-enabled {0}'
    output, enabled = run(unit, systemctl_is_enabled.format(service))
    return active == 0 and enabled == 0


def kubectl(command, kubeconfig='', namespace='', json=False):
    '''Run kubectl commands and return the output and return code.'''
    kubectl = 'kubectl'
    # Is there a kubeconfig to use?
    if kubeconfig:
        # Append the kubeconfig flag and path.
        kubectl = '{0} --kubeconfig={0}'.format(kubectl, kubeconfig)
    # Is there a namespace to use?
    if namespace:
        # Append the namespace flag and namespace.
        kubectl = '{0} --namespace={1}'.format(kubectl, namespace)
    # Does the output need to be JSON?
    if json:
        # Append the output flag to the command
        kubectl = '{0} --output=json'.format(kubectl)
    return '{0} {1}'.format(kubectl, command)


def run(unit, command):
    '''Print out the command, run the command and print out the output.'''
    # Print the command so the results show what command was run.
    print(command)
    # Run the command on the unit.
    output, rc = unit.run(command)
    print(output)
    # Return the output and return code.
    return output, rc


def valid_certificate(unit, path):
    '''Return true if the certificate is valid, false otherwise.'''
    # Getting a large number of certificates would be expensive, this code
    # just verifies the file exists and contains valid being and end.
    output, begin = unit.run('grep "BEGIN CERTIFICATE" {0}'.format(path))
    output, end = unit.run('grep "END CERTIFICATE" {0}'.format(path))
    return begin == 0 and end == 0


def valid_key(unit, path):
    '''Return true if the file at path is a valid key.'''
    # Getting a large number of key files would be expensive, this code
    # just verifies the file exists and contains a valid begin and end.
    output, begin = unit.run('grep "BEGIN PRIVATE KEY" {0}'.format(path))
    output, end = unit.run('grep "END PRIVATE KEY" {0}'.format(path))
    return begin == 0 and end == 0
