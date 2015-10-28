import os
import imp
import inspect
import json
import tarfile


def is_test_valid(test_module):
    """Test if the test_module file is valid

    We only check for the transaction class, since the generic transaction
    parent will raise a NotImplemented exception if the run method is not present
    :return: True if the test is valid, else False
    :rtype: bool
    :raises: InvalidTestError
    """
    if not hasattr(test_module, "Transaction"):
        raise Exception("No transaction class found in test script")
    getattr(test_module, "Transaction")
    return True


def load_module(path):
    """Load a single module based on a path on the system

    :param str path: the full path of the file to load as a module
    :return: the module imported
    :rtype: mixed
    :raises: ImportError, InvalidTestError
    """
    if not os.path.exists(path):
        raise ImportError("File does not exists: {}".format(path))
    try:
        module_name = inspect.getmodulename(os.path.basename(path))
        module = imp.load_source(module_name, path)
        if is_test_valid(module):
            return module
        raise Exception("Module not valid")
    except ImportError as e:
        raise Exception("Error importing the tests script {}\nError: {}".format(module_name, e))


def load_file(file_name):
    """Load a single file based on its full path as a module

    :param str filename: the full path of the file
    :return: the module loaded
    :rtype: mixed
    :raises: ImportError, InvalidTestError
    """
    if not os.path.exists(file_name):
        raise ImportError("File does not exists: {}".format(file_name))
    realpath = os.path.realpath(os.path.abspath(file_name))
    return load_module(realpath)


def is_valid_conf(config_file, tar=0):
    """Check for valid config.json and check if test script is present

    :param str config_file: the full config.json path
    :param str tar: the full tar file path
    :return: boolean 1 true 0 false
    :rtype: int
    """

    if os.path.isfile(config_file):
            with open(config_file) as f:
                conf_file = f.read()
    else:
        conf_file = config_file
        json_parsed = json.loads(conf_file)
        tarinfo = tar.getmember(json_parsed['script'])
        if tarinfo.isfile():
            conf_file = config_file
        else:
            conf_file = 0

    json_parsed = json.loads(conf_file)

    if json_parsed['script'] and os.path.isfile(os.path.abspath(json_parsed['script'])):
        return(1)
    else:
        return(0)
