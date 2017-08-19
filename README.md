# Fedora-26-dolphin-root-access
Dolphin File Manager with unlocked root access for Fedora 26

Recently upgraded my Fedora to next major release: 26
And is it happens frequently with major Fedora upgrades there was nasty surprise: the some KDE applications refuse to run as root user.

This change is introduced for security reasons, explained by author here:
https://blog.martin-graesslin.com/blog/2017/02/editing-files-as-root/

For future is plan to introduce support of Policy-Kit:
https://bugs.kde.org/show_bug.cgi?id=179678

However, I share dissapointment and anger of many KDE users: closing root access before introducing Policy-Kit was wrong and unnaceptable.

After little search I found the "cure" in other GitHub repository:

https://github.com/domker/dolphin-kdesu-git

With dolphin-17.04.1-allow-root.patch and modified dolphin.spec from original source rpm package I built replacement dolphin package with root access restored:
dolphin-17.04.1-1.fc26.x86_64.rpm

Please note: this repository probably will go unmaintained.
If someone want to take it over, most welcome.

