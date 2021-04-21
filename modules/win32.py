import win32api, win32con, win32security

_sid_types = ['', 'User', 'Group', 'Domain', 'Alias', 'WellKnownGroup', 'DeletedAccount', 'Invalid', 'Unknown', 'Computer', 'Label']

def get_file_info(path, mode='long'):
    name, domain, type = win32security.LookupAccountSid(None, win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner())
    if mode == 'short':
        return name
    else:
        return name, domain, _sid_types[type]