# el6

Summary: Utilities and libraries to record, convert and stream audio and video
Name: ffmpeg
Version: 0.9
Release: 1%{?dist}
License: GPL
Group: Applications/Multimedia
URL: http://ffmpeg.org/

Source: http://www.ffmpeg.org/releases/ffmpeg-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: SDL-devel
BuildRequires: freetype-devel
BuildRequires: imlib2-devel
BuildRequires: zlib-devel
BuildRequires: openjpeg-devel
%{!?_without_a52dec:BuildRequires: a52dec-devel}
%{!?_without_dc1394:BuildRequires: libdc1394-devel}
%{!?_without_dirac:BuildRequires: dirac-devel}
%{!?_without_faac:BuildRequires: faac-devel}
%{!?_without_gsm:BuildRequires: gsm-devel}
%{!?_without_lame:BuildRequires: lame-devel}
%{!?_without_nut:BuildRequires: libnut-devel}
%{!?_without_opencore_amr:BuildRequires: opencore-amr-devel}
%{!?_without_rtmp:BuildRequires: librtmp-devel}
%{!?_without_schroedinger:BuildRequires: schroedinger-devel}
%{!?_without_texi2html:BuildRequires: texi2html}
%{!?_without_theora:BuildRequires: libogg-devel, libtheora-devel}
%{!?_without_vorbis:BuildRequires: libogg-devel, libvorbis-devel}
%{!?_without_vpx:BuildRequires: libvpx-devel}
%{!?_without_x264:BuildRequires: x264-devel}
%{!?_without_a52dec:Requires: a52dec}
%{!?_without_speex:BuildRequires: libspeex-devel}

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

%package devel
Summary: Header files and static library for the ffmpeg codec library
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: imlib2-devel, SDL-devel, freetype-devel, zlib-devel, pkgconfig
Requires: openjpeg-devel
%{!?_without_a52dec:Requires: a52dec-devel}
%{!?_without_dc1394:Requires: libdc1394-devel}
%{!?_without_dirac:Requires: dirac-devel}
%{!?_without_faac:Requires: faac-devel}
%{!?_without_gsm:Requires: gsm-devel}
%{!?_without_lame:Requires: lame-devel}
%{!?_without_opencore_amr:Requires: opencore-amr-devel}
%{!?_without_rtmp:Requires: librtmp-devel}
%{!?_without_schroedinger:Requires: schroedinger-devel}
%{!?_without_theora:Requires: libogg-devel, libtheora-devel}
%{!?_without_vorbis:Requires: libogg-devel, libvorbis-devel}
%{!?_without_vpx:Requires: libvpx-devel}
%{!?_without_x264:Requires: x264-devel}
%{!?_without_xvid:Requires: xvidcore-devel}

%description devel
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Install this package if you want to compile apps with ffmpeg support.

%package libpostproc
Summary: Video postprocessing library from ffmpeg
Group: System Environment/Libraries
Provides: ffmpeg-libpostproc-devel = %{version}-%{release}
Provides: libpostproc = 1.0-1
Provides: libpostproc-devel = 1.0-1
Obsoletes: libpostproc < 1.0-1
Obsoletes: libpostproc-devel < 1.0-1
Requires: pkgconfig

%description libpostproc
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.

This package contains only ffmpeg's libpostproc post-processing library which
other projects such as transcode may use. Install this package if you intend
to use MPlayer, transcode or other similar programs.

%prep
%setup

%build
export CFLAGS="%{optflags}"
# We should be using --disable-opts since configure is adding some default opts
# to ours (-O3), but as of 20061215 the build fails on asm stuff when it's set
./configure \
    --prefix="%{_prefix}" \
    --libdir="%{_libdir}" \
    --shlibdir="%{_libdir}" \
    --mandir="%{_mandir}" \
    --incdir="%{_includedir}" \
    --disable-avisynth \
%{?_without_v4l:--disable-indev="v4l" --disable-indev="v4l2"} \
%ifarch %ix86
    --extra-cflags="%{optflags}" \
%endif
%ifarch x86_64
    --extra-cflags="%{optflags} -fPIC" \
%endif
    --enable-avfilter \
%{!?_without_dc1394:--enable-libdc1394} \
%{!?_without_dirac:--enable-libdirac} \
%{!?_without_faac:--enable-libfaac} \
%{!?_without_gsm:--enable-libgsm} \
%{!?_without_lame:--enable-libmp3lame} \
%{!?_without_nut:--enable-libnut} \
%{!?_without_opencore_amr:--enable-libopencore-amrnb --enable-libopencore-amrwb} \
%{!?_without_rtmp: --enable-librtmp} \
%{!?_without_schroedinger:--enable-libschroedinger} \
%{!?_without_speex:--enable-libspeex} \
%{!?_without_theora:--enable-libtheora} \
%{!?_without_vorbis: --enable-libvorbis} \
%{!?_without_vpx: --enable-libvpx} \
%{!?_without_x264:--enable-libx264} \
%{!?_without_xvid:--enable-libxvid} \
    --enable-gpl \
    --enable-nonfree \
    --enable-libopenjpeg \
    --enable-postproc \
    --enable-pthreads \
    --enable-shared \
    --enable-swscale \
    --enable-vdpau \
    --enable-version3 \
    --enable-x11grab

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot} _docs
%{__make} install DESTDIR="%{buildroot}"

# Remove unwanted files from the included docs
%{__cp} -a doc _docs
%{__rm} -rf _docs/{Makefile,*.texi,*.pl}

# The <postproc/postprocess.h> is now at <ffmpeg/postprocess.h>, so provide
# a compatibility symlink
%{__mkdir_p} %{buildroot}%{_includedir}/postproc/
%{__ln_s} ../ffmpeg/postprocess.h %{buildroot}%{_includedir}/postproc/postprocess.h

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
chcon -t textrel_shlib_t %{_libdir}/libav{codec,device,format,util}.so.*.*.* &>/dev/null || :

%postun -p /sbin/ldconfig

%post libpostproc -p /sbin/ldconfig
%postun libpostproc -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc COPYING* CREDITS INSTALL MAINTAINERS README
%doc %{_mandir}/man1/ffprobe.1*
%doc %{_mandir}/man1/ffmpeg.1*
%doc %{_mandir}/man1/ffplay.1*
%doc %{_mandir}/man1/ffserver.1*
%doc %{_mandir}/man1/avconv.1*
%{_bindir}/ffprobe
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffserver
%{_bindir}/avconv
%{_datadir}/ffmpeg/
%{_libdir}/libavcodec.so
%{_libdir}/libavcodec.so.*
%{_libdir}/libavdevice.so
%{_libdir}/libavdevice.so.*
%{_libdir}/libavfilter.so
%{_libdir}/libavfilter.so.*
%{_libdir}/libavformat.so
%{_libdir}/libavformat.so.*
%{_libdir}/libavutil.so
%{_libdir}/libavutil.so.*
%{_libdir}/libswscale.so
%{_libdir}/libswscale.so.*
%{_libdir}/libswresample.so
%{_libdir}/libswresample.so.*
%{_libdir}/pkgconfig/libavutil.pc
#%{_libdir}/vhook/

%files devel
%defattr(-, root, root, 0755)
%doc _docs/*
%{_includedir}/libavcodec/
%{_includedir}/libavdevice/
%{_includedir}/libavfilter/
%{_includedir}/libavformat/
%{_includedir}/libavutil/
%{_includedir}/libswscale/
%{_includedir}/libswresample/
%{_libdir}/libavcodec.a
%{_libdir}/libavdevice.a
%{_libdir}/libavfilter.a
%{_libdir}/libavformat.a
%{_libdir}/libavutil.a
%{_libdir}/libswscale.a
%{_libdir}/libavcodec.so
%{_libdir}/libavdevice.so
%{_libdir}/libavfilter.so
%{_libdir}/libavformat.so
%{_libdir}/libavutil.so
%{_libdir}/libswscale.so
%{_libdir}/libswresample.so
%{_libdir}/libswresample.a
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/pkgconfig/libswscale.pc
%{_libdir}/pkgconfig/libswresample.pc

%files libpostproc
%defattr(-, root, root, 0755)
%{_includedir}/libpostproc/
%{_includedir}/postproc/
%{_libdir}/libpostproc.a
%{_libdir}/libpostproc.so*
%{_libdir}/pkgconfig/libpostproc.pc

%changelog
* Thu Dec 13 2011 nawawi jamili <nawawi@rutweb.com>
- Initial rutweb version
