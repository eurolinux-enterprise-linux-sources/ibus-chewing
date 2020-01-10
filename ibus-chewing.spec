Name:           ibus-chewing
Version:        1.4.4
Release:        14%{?dist}
Summary:        The Chewing engine for IBus input platform
License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://code.google.com/p/ibus/
Source0:        http://ibus.googlecode.com/files/%{name}-%{version}-Source.tar.gz
Patch0:         ibus-chewing-1.4.4-1.4.7.patch
Patch1:         ibus-chewing-1.4.4.rhbz1119963.patch
Patch2:         ibus-chewing-1.4.4.rhbz1062133.patch
Patch3:         ibus-chewing-1.4.4.rhbz1073797.patch

BuildRequires:  cmake >= 2.6.2
BuildRequires:  gob2 >= 2.0.16
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  ibus-devel >= 1.3
BuildRequires:  libchewing-devel >= 0.3.3
BuildRequires:  libX11-devel
BuildRequires:  libXtst-devel
BuildRequires:  gettext-devel
BuildRequires:  GConf2-devel
Requires:       GConf2
Requires:       gtk2
Requires:       ibus >= 1.3
Requires:       libchewing >= 0.3.3
Requires(pre):  GConf2
Requires(post): GConf2
Requires(preun):GConf2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
IBus-chewing is an IBus front-end of Chewing, an intelligent Chinese input
method for Zhuyin (BoPoMoFo) users.
It supports various Zhuyin keyboard layout, such as standard (DaChen),
IBM, Gin-Yeah, Eten, Eten 26, Hsu, Dvorak, Dvorak-Hsu, and DaChen26.

Chewing also support toned Hanyu pinyin input.

%description -l zh_TW
IBus-chewing 是新酷音輸入法的IBus前端。
新酷音輸入法是個智慧型注音輸入法，支援多種鍵盤布局，諸如：
標準注音鍵盤、IBM、精業、倚天、倚天26鍵、許氏、Dvorak、Dvorak許氏
及大千26鍵。

本輸入法也同時支援帶調漢語拼音輸入。



%prep
%setup -q -n %{name}-%{version}-Source
%patch0 -p1 -b .1.4.7
%patch1 -p0 -b .rhbz1119963
%patch2 -p0 -b .rhbz1062133
%patch3 -p0 -b .rhbz1073797

%build
# $RPM_OPT_FLAGS should be loaded from cmake macro.
%cmake -DCMAKE_FEDORA_ENABLE_FEDORA_BUILD=1 .
make VERBOSE=1 %{?_smp_mflags}
make VERBOSE=1 translations

%install
%__rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# We install document using doc 
(cd %{buildroot}/usr/share/doc/%{name}-%{version}
   rm -fr *
)

%find_lang %{name}

%pre
if [ "$1" -gt 1 ] ; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    [ -r %{_sysconfdir}/gconf/schemas/%{name}.schemas ] &&
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas\
    >/dev/null || :

    # Upgrading 1.0.2.20090302-1.fc11 or older?
    [ -r %{_sysconfdir}/gconf/schemas/%{name}.schema ] &&
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%{name}.schema\
    >/dev/null || :
fi


%preun
if [ "$1" -eq 0 ] ; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :


%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :


%clean

%files -f %{name}.lang

%defattr(-,root,root,-)
%doc AUTHORS README ChangeLog COPYING USER-GUIDE
%{_libexecdir}/ibus-engine-chewing
%config %{_sysconfdir}/gconf/schemas/ibus-chewing.schemas
%{_datadir}/ibus/component/chewing.xml
%{_datadir}/%{name}/icons

%changelog
* Thu Dec 18 2014 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-14
- Remove the multilib fix, as ibus-chewing is unlikely required
  multilib installation.

* Thu Dec 18 2014 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-13
- Fix the multilib mo conflict.

* Wed Dec 17 2014 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-9
- Resolves Bug 1119963 - Slow focus change with ibus-chewing
- Resolves Bug 1062133 - ibus-chewing may not handle key event after focus change
- Resolves Bug 1073797 - Cannot identify input mode for Chinese IME (ibus-chewing)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.4.4-8
- Mass rebuild 2014-01-24

* Fri Jan 17 2014 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-7
- Target "translation" is built separately with all, 
  in order to tame multiple job make.
- Resolves Bug 1013977 - ibus-chewing needs to have ibus write-cache --system in %post and %postun
- Resolves Bug 1027031 - CVE-2013-4509 ibus-chewing: ibus: visible password entry flaw [rhel-7.0]
- Resolves Bug 1028911 - [zh_TW]'Chinese<->English' switch does not work when clicking on the Chewing menu list.
- Resolves Bug 1045868 - ibus-chewing *again* not built with $RPM_OPT_FLAGS
- Option "Sync between caps lock and IM":
  + Default of  is changed to "disable",  because the previous default
    "keyboard" cause bug 1028911 for GNOME Shell.
  + Now Sync from "input method" can control Caps LED in GNOME shell.
- Translation added: de_DE, es_ES, it_IT, pt_BR, uk_UA
- Set environment IBUS_CHEWING_LOGFILE for ibus-chewing log.

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4.4-3
- Mass rebuild 2013-12-27

* Thu Dec 19 2013 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-2
- Resloves Bug 1027031 - CVE-2013-4509 ibus-chewing: ibus: visible password entry flaw [rhel-7.0]

* Wed Dec 18 2013 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-1
- Resolves Bug 842856 - ibus-chewing 1.4.3-1 not built with $RPM_OPT_FLAGS
- Resolves Bug 1027030 - CVE-2013-4509 ibus-chewing: ibus: visible 
  password entry flaw [fedora-all]
  Thanks czchen for the GitHub pull request 39.
- Added translations: fr_FR, ja_JP, ko_KR
- Adopt cmake-fedora-1.2.0
* Wed Dec 18 2013 Ding-Yi Chen <dchen at redhat.com> - 1.4.4-1
- Resolves Bug 842856 - ibus-chewing 1.4.3-1 not built with $RPM_OPT_FLAGS
- Resolves Bug 1027030 - CVE-2013-4509 ibus-chewing: ibus: visible 
  password entry flaw [fedora-all]
  Thanks czchen for the GitHub pull request 39.
- Added translations: fr_FR, ja_JP, ko_KR
- Adopt cmake-fedora-1.2.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.4.3-3
- Build with $RPM_OPT_FLAGS (#842856).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Ding-Yi Chen <dchen at redhat.com> - 1.4.3-1
- Fixed GitHub issue #30: Rework decorate_preedit
  by merging pull request #30 from buganini
- Fixed GitHub issue #31: Properly refresh property
  by merging pull request #31 from buganini

* Thu Aug 23 2012 Ding-Yi Chen <dchen at redhat.com> - 1.4.2-1
- Fixed GitHub issue #7: highlighted text be cut after switch back to pure ibus
  by merging pull request #24 from buganini
- Fixed GitHub issue #20: Shift key will send duplicated strings
  by merging pull request #22 from buganini
- Fixed GitHub issue #21: somethings wrong with cmake
- Fixed GitHub issue #25: Weird symbol when input with somethings highlighted
  by merging pull request #26 from buganini
- Fixed GitHub issue #27: Local path committed into tree
- Fixed: Bug 713033 -  [zh_TW] ibus-chewing problem
- Fixed: Bug 745371 -  ibus-chewing: mode confusion In Temporary English mode and Chinese mode later on
- Fixed: Google Issue 1172: [ibus-chewing] move elf file to standard directory.
- Fixed: Google Issue 1426: ibus-chewing-1.3.10 installs directory /gconf to root filesystem
- Fixed: Google Issue 1428: ibus-chewing-1.3.10 fails to save it's settings
- Fixed: Google Issue 1481: Some characters are missing when a long string in preedit buffer.
- Fixed: Google Issue 1490: Cannot change INSTAL prefix for ibus-chewing-1.4.0

* Mon Jul 23 2012 Ding-Yi Chen <dchen at redhat.com> - 1.4.0-1
- Merge pull request #13 from hiroshiyui to Fix wrong data type conversion
- Fixed: Google Issue 1079: Use shift key to switch to English mode in ibus-chewing
  Also list as GitHub pull request #17
- Fixed: Google Issue 1089: Ibus-chewing cause window flicker when compiz enabled
- Fixed: Google Issue 1329, Github Issue 3: Merge with buganini at gmail.com
- Fixed: Google Issue 1351: ibus-chewing 1.3.10 mistakenly send uncommitted charactor.
- Fixed: Google Issue 1374: ibus-chewing: cannot save the preference with gnomeshell
- Fixed: Google Issue 1427: ibus-chewing-1.3.10 is not compatible with ibus-1.4.0 and higher
  Also list as GitHub pull request #16
- Fixed: GitHub Issue 5: Word missing when with libchewing-0.3.3 and  ibus-chewing 1.3.10
  Also list as GitHub pull request #15
- Fixed: Launchpad bug: 1014456 bus-chewing deletes characters if too many of them are entered
  Also list as GitHub pull request #19

* Thu Dec 15 2011 Ding-Yi Chen <dchen at redhat.com> - 1.3.10-1
- Fixed Bug 726335 (Google issue 1281)- [abrt] ibus-chewing-1.3.9.2-3.fc15: g_atomic_int_get:
  Process /usr/libexec/ibus-engine-chewing was killed by signal 11 (SIGSEGV) using patch from Scott Tsai
- Fixed Bug 727018 - ibus compose file needs a symbol tag for gnome-shell
- Fixed characters duplication problem (Google issue 1245, GitHub ibus-chewing issue 2)
- Fixed KP-Enter not been able to commit preedit buffer. (Google issue 1303, GitHub ibus-chewing issue 4)
- Depends on cmake-fedora now.
- Fixed issue 1274, which is addressed by yusake's comments on d9009bf.
- Add compile flag for GNOME3.
- Add command line option: showFlags
- ibus-gnome special symbol
- Thanks Fred Chien's patch against that candidate window cannot be closed
  with escape key since selected tone.
- Thanks Fourdollar's patch for Fix plain zhuyin with space as selection problem.
- Remove support for ibus-1.2 and prior.

* Tue Feb 01 2011 Ding-Yi Chen <dchen at redhat.com> - 1.3.5.20100714-3
- Resolves: #627794
- Add USER-GUIDE

* Fri Nov 19 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.9.2-1
- Fixed Bug 652909
- Added back a Changlog item that mention Nils Philippsen's change.
- Apply Jim Huang's patch for zh_TW.po

* Wed Nov 17 2010 Nils Philippsen <nils@redhat.com> - 1.3.8-2
- fix scriptlets

* Fri Nov 12 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.8-1
- Quick fix for f15 and ibus-1.4 build
- Version scheme change.

* Fri Sep 10 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.7.20100910-1
- Input style of ibus-chewing is decommissioned under ibus >=1.3.
  Now the input style is determined solely on the setting of
  "Embed preedit in application window" in IBus.
- Fixed: #608991, #632043
- Fixed Issue 1022: chewing commit some text in reset method
  (patched by Peng Huang).
- Fixed Issue 1032: [ibus-chewing] Chewing not commit some single Chinese
  char into application when press enter.
- Rewrite CMake modules to make them cleaner, and documents in cmake module
  help format.
- [For developer and distro maintainer]
  Various targets changed. Use 'make help' to obtain a list of available
  targets.

* Fri Jul 30 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.6.20100730-1
- Resolves: #608991
- Sort of fix upstream issue 993.
- Include USER-GUIDE
- Remove NEWS, as this project does not use it.
- Fix upstream Issue 1016: [ibus-chewing] Chewing should commit the complete string before disable chewing. But only for ibus-1.3.0 and later.
- Mouse candidate selection now work in plain Zhuyin mode.
- Default setting changes: (Won't affect current user though).
  + Auto move cursor: TRUE
  + Add phrases in front: TRUE
  + spaceAsSelection: FALSE

* Wed Jul 14 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.5.20100714-1
- Resolves: #608991
- Removes Ctrl-v/V Hotkey

* Wed Jul 07 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.5.20100706-1
- Fixed google issue 965:
  Candidate missing if both "Plain Zhuyin" and "Space As selection" are enabled.
- Revised Basic.macro
- Resolved: #608991

* Tue Jun 08 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.4.20100608-1
- ibus-chewing can now use mouse to click on mouse. Thus
  Fix Issue 951: Chewing does not support selection of candidates via mouseclick
  Thanks zork@chromium.org for the patch.

* Fri Jun 04 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.4.20100605-1
- Fix Issue 942: Fix unsunk references in ibus-chewing
  Applied the patch provided by zork@chromium.org.
- Rename CVS_DIST_TAGS to FEDORA_DIST_TAGS, and move its
  definition to cmake_modules/
- Gob2 generated file is now removed, because
  Bug 519108 is fixed from Fedora 11.

* Wed Apr 07 2010 Peng Huang <shawn.p.huang@gmail.com> - 1.2.99.20100317-2
- Rebuild with ibus-1.3.0

* Wed Mar 17 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100317-1
- Fix google 796: English input for dvorak
- Fix google 797: Zhuyin input for dvorak
- Fix google 807: ibus-chewing shows the over-the-spot panel
  even when not necessary

* Fri Feb 19 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100217-1
- Fixed the CMake description that leads summary incorrect.

* Tue Feb 16 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100216-1
- Fixed when typing English immediately after incomplete Chinese character.
- Add zh_TW summary.
- Revised description and write its zh_TW translation.

* Mon Feb 15 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100215-1
- "Macroize" rpm spec.
- Resolves: #565388

* Fri Feb 12 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100212-1
- Fixed Google issue 505.
- Google issue 755 is fixed in libchewing-0.3.2-22,
  See Chewing Google issue 10
- Fixed behavior of Del, Backspace,  Home, End
- Revert the change that fix Google issue 758.
- Change the default input style to "in candidate window",
  because not all application handle the on-the-spot mode well.
- Fixed Google issue 776

* Tue Feb 09 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20100210-1
- Revert the change that fix Google issue 758.
- Remove "tag" target, add "commit" which do commit and tag.

* Tue Feb 09 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20100209-1
- Fixed Google issue 754: commit string is missing when inputting
  long English text in the end.
- Fixed Google issue 758: Space is irresponsive in Temporary English mode
  if no Chinese in preedit buffer.
- Fixed Google Issue 763: [ibus-chewing] [qt] Shift-Up/Down does not mark
  text area properly.
- Change the String "on the spot" to "in application window",
  Chinese translation change to "在輸入處組詞"
- Change the "over the spot" to "in candidate window",
  Chinese translation remain the same
- Fixed bodhi submission.

* Mon Feb 08 2010 Adam Jackson <ajax@redhat.com> - 1.2.0.20100125-2
- Rebuild for new libibus.so.2 ABI.

* Mon Jan 25 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20100125-1
- Add over-the-spot editing mode.
- Possible fixed of Google issue 505: ibus acts strange in Qt programs.
- Implemented Google issue 738:  Add a mode that allow editing in candidate window
  (thus over-the-spot mode).

* Fri Dec 11 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20091211-1
- Fix Google issue 608: ibus-chewing does not show cursor in xim mode.
- Fix Google issue 611: ibus-chewing keyboard setting reverts to default unexpectlly.
- Fix Google issue 660: failed to build with binutils-gold.
- Remove make target commit.
- Add make target tag

* Fri Oct 09 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20091002-1
- Bug 518901 - ibus-chewing would not work with locale zh_TW.Big
- Fix Google issue 501: ibus-chewing buffer doesn't get cleared when
toggling ibus on/off
- Fix Google issue 502: ibus-chewing: character selection window stays
behind when toggling ibus off- Use WM's revised ibus-chewing icon.
- Debug output now marked with levels.

* Wed Sep 30 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090917-2
- Rebuild with ibus-1.2.0

* Thu Sep 17 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090917-1
- Addressed Upstream (IBUS Google code) issue 484:
  + Find the source that why the / and . are not working.
- Pack the gob2 generation source to avoid the [Bug 519108]:
  [gob2] class and enum names convert incorrectly in mock / koji.

* Wed Sep 09 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090831-1
- IBusProperty and IBusPropList are free upon destruction.
- Fixed Red Hat Bugzilla [Bug 519328] [ibus-chewing] inconsistent between normal mode and plain Zhuyin mode.
- Addressed Upstream (IBUS Google code) issue 484:
  Arithmetic symbols (+-*/) on number pad does not input properly.

* Wed Aug 26 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090818-1
- Merged 1.2 and 1.1 source code.
- Addressed Upstream (IBUS Google code) issue 471.
- Remove libX11 dependency.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090624-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090624-1
- Lookup table now shows the selection key.

* Mon Jun 22 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090622-1
- Update to 1.2.0.20090622.

* Fri May 22 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.10.20090523-2
- Add back the export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`

* Fri May 22 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.10.20090523-1
- Applied Lubomir Rintel's patch

* Fri May 22 2009 - Ding-Yi Chen <dchen at redhat.com> - 1.0.10.20090522-1
- Now the 1st down key brings the longest possible phrases.
  The 2nd down key brings the 2nd longest possible phrases from the back,
  unlike the previous versions where the cursor stays in the head of longest phrase.
- Add force lowercase in English mode option.
- Fix double free issue when destroy ibus-chewing.
- Hide ibus-chewing-panel when ibus-chewing is focus-out

* Mon May 11 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.9.20090508-1
Now commit is forced when switch of ibus-chewing or current application loses focus.
- New ibus-chewing.png is contribute by WM.
- input-keyboard.png is no longer needed and removed.
- ibus-engine-chewing -v option now need an integer as verbose level.
- ibus-chewing.schemas is now generated.
- Fix some CMake modules bugs.

* Tue Apr 28 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.8.20090428-1
Fix the errors which Funda Wang as pointing out:
- Move src/chewing.xml.in to data/
- Fixed some typo in next_version targets.
- Remove GConf2 package requirement, while add gconftool-2 requirement.

* Mon Mar 30 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.5.20090330-1
- Added tooltips.
- Revealed the sync caps lock setting.
- Fixed Right key bug.
- Added CMake policy 0011 as OLD.

* Mon Mar 23 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.4.20090323-2
- Fix koji build issues.

* Mon Mar 23 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.4.20090323-1
- Various Settings are now in dialog.
- Integer settings are now revealed.
- MakerDialog.gob is now available.
- Work around of easy symbol input.
- Fix iBus Google issue 310.

* Sun Mar 22 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0.3.20090311-2
- Properly reinstall the schema when updating from 1.0.2.20090303-1 or older

* Wed Mar 11 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.3.20090311-1
- IBus Google issue 305:  ibus-chewing.schema -> ibus-chewing.schemas
- IBus Google issue 307:  hardcoded chewing datadir
    - Sync chewing candPerPage and IBusTable->page_size
- Sync between IM and keyboard (Experimental)
    - ibus-chewing.schema -> ibus-chewing.schemas

* Tue Mar 03 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.2.20090303-1
- Required gconf2 -> GConf2.
- Fix RPM install issues.

* Fri Feb 27 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.1.20090227-1
- Setting shows/hides KBType, selKeys, and various settings.
- Add gconf schema.
- Fix some memory leaking checked.
- Move some function to cmake_modules.
- Fix Google code issue 281

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1.20081023-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.0.20090220-1
- First working version for IBus C

* Wed Jan 28 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.0.20090128-1
- Fix the binding with libchewing 0.3.2.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081023-2
- Rebuild for Python 2.6

* Thu Oct 23 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080923-1
- Update to 0.1.1.20080923.

* Wed Sep 17 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080917-1
- Update to 0.1.1.20080917.

* Tue Sep 16 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080916-1
- Update to 0.1.1.20080916.

* Tue Sep 09 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Fri Aug 15 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081023-1
- The first version.

