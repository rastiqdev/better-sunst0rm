# better-sunst0rm
iOS Tether Downgrader for 64-bit checkm8 devices, based on the once legendary sunst0rm, by mineek.

Based on [mineek's guide](https://github.com/mineek/iostethereddowngrade), with a lot of changes

## /!\ Using this tool on A9 devices or newer is NOT recommended at all, at this is considered "obsolete" (it will probably not work with newer iOS versions). Instead, use [downr1n](https://github.com/edwin170/downr1n) (tethered downgrades) or [dualra1n](https://github.com/dualra1n/dualra1n) (tethered dualboots), those are maintained projects. Using better-sunst0rm on A7/A8 devices is fine though.

## /!\ Using the dev branch is also not recommended, because I don't maintain it.

## Notes
- It is a *tethered* downgrade meaning you will have to boot tethered every single time from your PC if your battery dies or if you reboot your phone.
- On A10-A11 devices crucial functionality such as the Home Button, Audio, Microphone, Vibration does NOT work at the moment (and probably never will, because other tools already fix this).
- On iPhone X touch doesn't work but iPhone 8 and 8 Plus are fine.
- You should NOT be tether downgrading your main device, it is only recommended to tether downgrade a second device.
- For some frequently asked fixes go [here](https://github.com/Arna13/sunst0rm-guide/blob/main/docs/misc/EXTRAS.md) for help.

## Installation

1. Install the latest version of Python. (the bundled version of Python in macOS has issues with better-sunst0rm)
2. Clone the git repo (`git clone https://github.com/rastiqdev/better-sunst0rm`)
3. Install the pip requirements (`pip3 install -r requirements.txt`)
4. Done!!! :)

## How to use?
| Option (short)  | Option (long)               | Description                              |
|-----------------|-----------------------------|------------------------------------------|
| `-i IPSW`       | `--ipsw IPSW`               | Path to IPSW                             |
| `-t SHSH2`      | `--blob SHSH2`              | Path to SHSH2                            |
| `-r`       | `--restore`            | Restore mode                             |
| `-b`       | `--boot`               | Boot mode                                |
| `-d BOARDCONFIG`| `--boardconfig BOARDCONFIG` | BoardConfig to use  (E.g: `d221ap`)      |
| `-kpp`     | `--kpp`                | Use KPP (A9 or lower)                    |
| `-id IDENTIFIER`| `--identifier IDENTIFIER`   | Identifier to use  (E.g: `iPhone10,6`)   |
|                 | `--legacy`             | Use Legacy Mode (iOS 11 or lower)        |
|                 | `--skip-baseband`           | Skip Baseband sending, do NOT do this if your device does have baseband this argument is only ment to be passed when your device does *not* have baseband such as WiFi only iPads.                  |
### Restoring
```py
python3 sunstorm.py -i 'IPSW' -t 'SHSH2' -r -d 'BOARDCONFIG'
```
- Use `--kpp` if you have KPP, otherwise don't add
- A10+ Devices do NOT have KPP so do not add `--kpp` if you are attempting to tether downgrade an A10+ device, A7-A9X devices does have KPP so that means you will pass `--kpp` and to clear things up having KPP or not does not change the fact if you are able to tether downgrade your device.
### Booting
```py
python3 sunstorm.py -i 'IPSW' -t 'SHSH2' -b -d 'BOARDCONFIG' -id 'IDENTIFIER'
```
- Use `--kpp` if you have KPP, otherwise don't add
```
./boot.sh
```

## Credits:

### sunst0rm
[M1n1Exploit](https://github.com/Mini-Exploit) - Some code from ra1nstorm

[Arna13](https://github.com/Arna13) - Writing an easy to understand [guide](https://github.com/Arna13/sunst0rm-guide)

[swayea](https://github.com/swayea) - Logo's

### better-sunst0rm
[rastiqdev](https://github.com/rastiqdev) - Me! Adding the required fixes for sunst0rm to still work today.

[m1stadev's wikiproxy](https://github.com/m1stadev/wikiproxy) - iBSS/iBEC IV/Key grabber's code (modified so it uses some already installed pip modules)

[edwin170's downr1n](https://github.com/edwin170/downr1n) - Dependencies and futurerestore downloader