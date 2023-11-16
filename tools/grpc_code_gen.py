#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import glob
import os
import re

import pkg_resources
import warnings
from grpc_tools import protoc
from packaging import version

warnings.filterwarnings("ignore", category=DeprecationWarning)
grpc_tools_version = pkg_resources.get_distribution('grpcio-tools').version
dest_dir = 'stackinsights/protocol'
src_dir = 'protocol'


def touch(filename):
    open(filename, 'a').close()


def codegen():
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    touch(os.path.join(dest_dir, '__init__.py'))
    protoc_args = [
        'grpc_tools.protoc',
        f'--proto_path={src_dir}',
        f'--python_out={dest_dir}',
        f'--grpc_python_out={dest_dir}'
    ]
    if version.parse(grpc_tools_version) >= version.parse('1.49.0'):
        # https://github.com/grpc/grpc/issues/31247
        protoc_args += [f'--pyi_out={dest_dir}']
    protoc_args += list(glob.iglob(f'{src_dir}/**/*.proto'))
    protoc.main(protoc_args)

    for py_file in glob.iglob(os.path.join(dest_dir, '**/*.py')):
        touch(os.path.join(os.path.dirname(py_file), '__init__.py'))
        with open(py_file, 'r+') as file:
            code = file.read()
            file.seek(0)
            file.write(re.sub(r'from (.+) (import .+_pb2.*)', 'from ..\\1 \\2', code))
            file.truncate()


if __name__ == '__main__':
    codegen()
