# Audio-Joiner
read all WAV audio files from a specified directory, then sort them by filename in the correct numerical order. After sorting, the program should concatenate all audio files in order and produce a single final output audio file.

After sorting, the program should concatenate all audio files in order and produce a single final output audio file.

If possible, the program should also insert a configurable duration of absolute silence between each audio file (for example, 1 second by default, but adjustable).
For instance, after 1.wav finishes and before 2.wav starts, one second of complete silence should be added.


Install FFmpeg
Windows: https://ffmpeg.org/download.html
macOS (Homebrew): brew install ffmpeg
Linux (Debian/Ubuntu): sudo apt-get install ffmpeg




ffmpeg -version
