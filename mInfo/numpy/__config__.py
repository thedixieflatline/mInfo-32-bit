# This file is generated by D:\Build\numpy\numpy-1.8.x-MKL\setup.py
# It contains system_info results at the time of building this package.
__all__ = ["get_info","show"]

blas_mkl_info={'library_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/lib/ia32'], 'include_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/include'], 'libraries': ['mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd'], 'define_macros': [('SCIPY_MKL_H', None)]}
blas_opt_info={'library_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/lib/ia32'], 'include_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/include'], 'libraries': ['mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd'], 'define_macros': [('SCIPY_MKL_H', None)]}
lapack_mkl_info={'library_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/lib/ia32'], 'include_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/include'], 'libraries': ['mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd', 'mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd'], 'define_macros': [('SCIPY_MKL_H', None)]}
openblas_info={}
lapack_opt_info={'library_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/lib/ia32'], 'include_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/include'], 'libraries': ['mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd', 'mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd'], 'define_macros': [('SCIPY_MKL_H', None)]}
mkl_info={'library_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/lib/ia32'], 'include_dirs': ['C:/Program Files (x86)/Intel/Composer XE/mkl/include'], 'libraries': ['mkl_lapack95', 'mkl_blas95', 'mkl_intel_c', 'mkl_intel_thread', 'mkl_core', 'libiomp5md', 'libifportmd'], 'define_macros': [('SCIPY_MKL_H', None)]}

def get_info(name):
    g = globals()
    return g.get(name, g.get(name + "_info", {}))

def show():
    for name,info_dict in globals().items():
        if name[0] == "_" or type(info_dict) is not type({}): continue
        print(name + ":")
        if not info_dict:
            print("  NOT AVAILABLE")
        for k,v in info_dict.items():
            v = str(v)
            if k == "sources" and len(v) > 200:
                v = v[:60] + " ...\n... " + v[-60:]
            print("    %s = %s" % (k,v))
    