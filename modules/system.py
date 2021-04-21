import ctypes as _ctypes
from ctypes import wintypes as _wintypes

_advapi32 = _ctypes.WinDLL('advapi32', use_last_error=True)

ERROR_INVALID_FUNCTION    = 0x0001
ERROR_FILE_NOT_FOUND      = 0x0002
ERROR_PATH_NOT_FOUND      = 0x0003
ERROR_ACCESS_DENIED       = 0x0005
ERROR_INSUFFICIENT_BUFFER = 0x007A

_LPBOOL  = _ctypes.POINTER(_wintypes.BOOL)
_LPDWORD = _ctypes.POINTER(_wintypes.DWORD)
_PSID = _ctypes.POINTER(_wintypes.BYTE)
_PSECURITY_DESCRIPTOR = _ctypes.POINTER(_wintypes.BYTE)
_SECURITY_INFORMATION = _wintypes.DWORD

OWNER_SECURITY_INFORMATION     = 0x00000001
GROUP_SECURITY_INFORMATION     = 0x00000002
DACL_SECURITY_INFORMATION      = 0x00000004
SACL_SECURITY_INFORMATION      = 0x00000008
LABEL_SECURITY_INFORMATION     = 0x00000010
ATTRIBUTE_SECURITY_INFORMATION = 0x00000020
SCOPE_SECURITY_INFORMATION     = 0x00000040
BACKUP_SECURITY_INFORMATION    = 0x00010000
UNPROTECTED_SACL_SECURITY_INFORMATION = 0x10000000
UNPROTECTED_DACL_SECURITY_INFORMATION = 0x20000000
PROTECTED_SACL_SECURITY_INFORMATION   = 0x40000000
PROTECTED_DACL_SECURITY_INFORMATION   = 0x80000000

class _SID_NAME_USE(_wintypes.DWORD):
    _sid_types = dict(enumerate('''
            User Group Domain Alias WellKnownGroup
            DeletedAccount Invalid Unknown
            Computer Label'''.split(), 1))

    def __init__(self, value=None):
        if value is not None:
            if value not in self._sid_types:
                raise ValueError('invalid SID type')
            super(_SID_NAME_USE, self).__init__(value)

    def __str__(self):
        if self.value not in self._sid_types:
            raise ValueError('invalid SID type')
        return self._sid_types[self.value]

_PSID_NAME_USE = _ctypes.POINTER(_SID_NAME_USE)

def _check_bool(result, func, args,
                WinError=_ctypes.WinError,
                get_last_error=_ctypes.get_last_error):
    if not result:
        raise WinError(get_last_error())
    return args

# msdn.microsoft.com/en-us/library/aa446639
_advapi32.GetFileSecurityW.errcheck = _check_bool
_advapi32.GetFileSecurityW.argtypes = (
    _wintypes.LPCWSTR,     # _In_      lpFileName
    _SECURITY_INFORMATION, # _In_      RequestedInformationRequested
    _PSECURITY_DESCRIPTOR, # _Out_opt_ pSecurityDescriptor
    _wintypes.DWORD,       # _In_      nLength
    _LPDWORD)              # _Out_     lpnLengthNeeded

# msdn.microsoft.com/en-us/library/aa446651
_advapi32.GetSecurityDescriptorOwner.errcheck = _check_bool
_advapi32.GetSecurityDescriptorOwner.argtypes = (
    _PSECURITY_DESCRIPTOR,  # _In_  pSecurityDescriptor
    _ctypes.POINTER(_PSID), # _Out_ pOwner
    _LPBOOL)                # _Out_ lpbOwnerDefaulted

# msdn.microsoft.com/en-us/library/aa379166
_advapi32.LookupAccountSidW.errcheck = _check_bool
_advapi32.LookupAccountSidW.argtypes = (
    _wintypes.LPCWSTR, # _In_opt_  lpSystemName
    _PSID,             # _In_      lpSid
    _wintypes.LPCWSTR, # _Out_opt_ lpName
    _LPDWORD,          # _Inout_   cchName
    _wintypes.LPCWSTR, # _Out_opt_ lpReferencedDomainName
    _LPDWORD,          # _Inout_   cchReferencedDomainName
    _PSID_NAME_USE)    # _Out_     peUse

def get_file_security(filename, request):
    length = _wintypes.DWORD()
    # N.B. This query may fail with ERROR_INVALID_FUNCTION
    # for some filesystems.
    try:
        _advapi32.GetFileSecurityW(filename, request,
                                   None, 0, _ctypes.byref(length))
    except WindowsError as e:
        if e.winerror != ERROR_INSUFFICIENT_BUFFER:
            raise
    if not length.value:
        return None
    sd = (_wintypes.BYTE * length.value)()
    _advapi32.GetFileSecurityW(filename, request,
                               sd, length, _ctypes.byref(length))
    return sd

def get_security_descriptor_owner(sd):
    sid = _PSID()
    sid_defaulted = _wintypes.BOOL()
    _advapi32.GetSecurityDescriptorOwner(sd,
                                         _ctypes.byref(sid),
                                         _ctypes.byref(sid_defaulted))
    return sid

def look_up_account_sid(sid):
    SIZE = 256
    name = _ctypes.create_unicode_buffer(SIZE)
    domain = _ctypes.create_unicode_buffer(SIZE)
    cch_name = _wintypes.DWORD(SIZE)
    cch_domain = _wintypes.DWORD(SIZE)
    sid_type = _SID_NAME_USE()
    _advapi32.LookupAccountSidW(None, sid,
                                name, _ctypes.byref(cch_name),
                                domain, _ctypes.byref(cch_domain),
                                _ctypes.byref(sid_type))
    return name.value, domain.value, sid_type

def get_file_info(filename):
    if isinstance(filename, bytes):
        filename = filename.decode('mbcs')

    request = OWNER_SECURITY_INFORMATION
    sd = get_file_security(filename, request)
    sid = get_security_descriptor_owner(sd)
    name, domain, sid_type = look_up_account_sid(sid)
    if domain:
        return '{0}\\{1}'.format(domain, name)
    return name


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]
    if isinstance(filename, bytes):
        filename = filename.decode('mbcs')

    request = OWNER_SECURITY_INFORMATION
    sd = get_file_security(filename, request)
    sid = get_security_descriptor_owner(sd)
    name, domain, sid_type = look_up_account_sid(sid)
    if domain:
        name =  '{0}\\{1}'.format(domain, name)
    print("File : {0}".format(filename))
    print("Owner: {0} ({1})".format(name, sid_type))