%bcond_with	preconfigured
Summary:	System V initialization program
Summary(de):	System V-Intialisierungsprogramm
Summary(es):	Programa de inicializaci�n System V
Summary(fr):	Programme d'initialisation Sys V
Summary(pl):	Program inicjalizuj�cy w Systemie V
Summary(pt_BR):	Programa de inicializa��o System V
Summary(ru):	���������, ����������� �������� ���������� ����������
Summary(tr):	System V ba�latma program�
Summary(uk):	��������, �� ������� �������� ���������� ���������
Name:		SysVinit
Version:	2.85
Release:	8
License:	GPL
Group:		Base
Source0:	ftp://ftp.cistron.nl/pub/people/miquels/software/sysvinit-%{version}.tar.gz
# Source0-md5:	8a2d8f1ed5a2909da04132fefa44905e
Source1:	sysvinit.logrotate
Source2:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/sysvinit-non-english-man-pages.tar.bz2
# Source2-md5:	9ae8a63a4685368fae19707f95475cca
Patch0:		sysvinit-paths.patch
Patch1:		sysvinit-bequiet.patch
Patch2:		sysvinit-md5-bigendian.patch
Patch3:		sysvinit-wtmp.patch
Patch4:		sysvinit-man.patch
Patch5:		sysvinit-halt.patch
Patch6:		sysvinit-blowfish.patch
Patch7:		sysvinit-initctl.patch
Patch8:		sysvinit-autofsck.patch
Patch9:		sysvinit-pidof.patch
Patch10:	sysvinit-log-signals.patch
Patch11:	sysvinit-killall5.patch
# based on http://www.nsa.gov/selinux/patches/sysvinit-selinux.patch.gz
Patch12:	sysvinit-selinux.patch
BuildRequires:	libselinux-devel >= 1.14
BuildRequires:	rpmbuild(macros) >= 1.159
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(post):	fileutils
Requires(postun):	/usr/sbin/groupdel
Requires:	/bin/awk
Requires:	login
%if %{with preconfigured}
Requires:	logrotate
%endif
Requires:	mingetty
Requires:	libselinux >= 1.14
Provides:	group(utmp)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The SysVinit package contains a group of processes that control the
very basic functions of your system. SysVinit includes the init
program, the first program started by the Linux kernel when the system
boots. Init then controls the startup, running and shutdown of all
other programs.

%description -l de
SysVinit ist das erste Programm, das beim Systemstart vom Linux-Kernel
gestartet wird. Es steuert das Starten, Ausf�hren und Beenden aller
anderen Programme.

%description -l es
SysVinit es el primer programa ejecutado por el kernel Linux cuando se
inicia el sistema. Controla arranque, funcionamiento y cierre de todos
los otros programas.

%description -l fr
SysVinit est le premier programme ex�cut� par le noyau de Linux
lorsque le syst�me d�marre, il contr�le le lancement, l'ex�cution et
l'arr�t de tous les autres programmes.

%description -l pl
SysVinit jest pierwszym programem uruchamianym przez j�dro podczas
startu systemu. Kontroluje start, prac� oraz zamykanie wszystkich
innych program�w.

%description -l pt_BR
SysVinit � o primeiro programa executado pelo kernel Linux quando o
sistema � inicializado. Controla inicializa��o, funcionamento e
finaliza��o de todos os outros programas.

%description -l ru
����� SysVinit �������� ������ ���������, ������� ��������� ������
�������� ��������� ����� �������. SysVinit �������� ��������� init,
����� ������ ���������, ������� ����������� ����� Linux ��� ��������
�������. ����� ����� init ��������� ��������, ����������� � ���������
���� ��������� ��������.

%description -l tr
SysVinit, sistem a��l�rken Linux �ekirde�i taraf�ndan �al��t�r�lan ilk
programd�r. Di�er programlar�n ba�lamalar�n�, �al��malar�n� ve
sonlanmalar�n� sa�lar/denetler.

%description -l uk
����� SysVinit ͦ����� ����� �����Ӧ�, ���Ҧ ������� ������ ��������
����æ��� ���ϧ �������. SysVinit ͦ����� �������� init, �����
��������, ��� �������� ���� Linux Ц� ��� �������� �������. ����
����� init ���դ ��������, ���������� �� �������� �Ӧ� ����� �������.

%prep
%setup -q -n sysvinit-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
%{__make} -C src \
	CC="%{__cc}" \
	LCRYPT="-lcrypt" \
	OPTIMIZE="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/logrotate.d,/var/log}

%{__make} install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=`id -u` \
	BIN_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf killall5 $RPM_BUILD_ROOT%{_sbindir}/pidof

> $RPM_BUILD_ROOT%{_sysconfdir}/ioctl.save
> $RPM_BUILD_ROOT/var/log/faillog
> $RPM_BUILD_ROOT/var/log/lastlog
> $RPM_BUILD_ROOT/var/log/wtmpx
> $RPM_BUILD_ROOT/var/log/btmpx

echo .so last.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lastb.1
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/poweroff.8
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/reboot.8
echo .so init.8 > $RPM_BUILD_ROOT%{_mandir}/man8/telinit.8
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid utmp`" ]; then
	if [ "`/usr/bin/getgid utmp`" != 22 ]; then
		echo "Error: group utmp doesn't have gid=22. Correct this before installing SysVinit." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 22 utmp 1>&2
fi

%post
touch %{_sysconfdir}/ioctl.save /var/log/{fail,last}log
chmod 000 %{_sysconfdir}/ioctl.save /var/log/{fail,last}log
chown root:root %{_sysconfdir}/ioctl.save /var/log/faillog
chown root:utmp /var/log/lastlog
chmod 600 %{_sysconfdir}/ioctl.save
chmod 640 /var/log/faillog
chmod 660 /var/log/lastlog

%{_sbindir}/telinit u || :

%postun
if [ "$1" = "0" ]; then
	%groupremove utmp
fi

%files
%defattr(644,root,root,755)
%doc doc/{Propaganda,Changelog,*.lsm}

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/last
%attr(755,root,root) %{_bindir}/lastb
%attr(755,root,root) %{_bindir}/mesg
%attr(755,root,root) %{_bindir}/utmpx-dump
%attr(2755,root,tty) %{_bindir}/wall

%attr(640,root,root) /etc/logrotate.d/sysvinit
%ghost %{_sysconfdir}/initrunlvl
%attr(600,root,root) %ghost %{_sysconfdir}/ioctl.save
%attr(640,root,root) %ghost /var/log/faillog
%attr(660,root,utmp) %ghost /var/log/lastlog
%attr(664,root,utmp) %ghost /var/log/wtmpx
%attr(640,root,root) %ghost /var/log/btmpx

%{_mandir}/man[158]/*
%lang(de) %{_mandir}/de/man[158]/*
%lang(es) %{_mandir}/es/man[158]/*
%lang(fi) %{_mandir}/fi/man[158]/*
%lang(fr) %{_mandir}/fr/man[158]/*
%lang(hu) %{_mandir}/hu/man[158]/*
%lang(id) %{_mandir}/id/man[158]/*
%lang(it) %{_mandir}/it/man[158]/*
%lang(ja) %{_mandir}/ja/man[158]/*
%lang(ko) %{_mandir}/ko/man[158]/*
%lang(pl) %{_mandir}/pl/man[158]/*
