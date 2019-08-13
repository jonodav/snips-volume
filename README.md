### Snips ALSA mixer volume control

A simple snips app I made to control the volume of the device alsamixer on my raspberry pi. I know its a bit janky to use subprocess instead of a proper library but I couldn't get it to work straight away and I'm too lazy to bother trying.

Requires the user to add the "_snips-skills" user to the "audio" group on the raspberry pi:
```sudo usermod -a -G audio _snips-skills```
If you know a better way to do this please put through a pull request :-)
