# FFI auxiliary makefile script
PREFIX ?= /usr/local

PKG_CONFIG = pkg-config --with-path=$(PREFIX)/lib/pkgconfig

ffi_libdir = $(shell $(PKG_CONFIG) --variable=libdir intro_c-practice || echo .)
ffi_incdir = $(shell $(PKG_CONFIG) --variable=includedir intro_c-practice || echo .)
LD_LIBRARY_PATH := $(LD_LIBRARY_PATH):$(ffi_libdir)
export LD_LIBRARY_PATH

.PHONY: prep_swig
prep_swig build/classic_c_wrap.c : intro_py/scriptexplore/classic_c.i ## prepare Swig files
	-swig -python -I$(ffi_incdir) -outdir build -o build/classic_c_wrap.c intro_py/scriptexplore/classic_c.i
