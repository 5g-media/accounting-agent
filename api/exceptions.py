class VnfListNotAvailable(Exception):
    """VNF list is not included in the openmano instance"""
    pass


class VmListNotAvailable(Exception):
    """VM list is not included in the VNF record, part of the openmano instance"""
    pass


class InstanceNotFound(Exception):
    """Openmano instance not found"""
    pass


class DateFormatParseError(Exception):
    """ Date format parse error """
    pass
