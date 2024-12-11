# karasub
Some self-made Karaoke subtitles

## FFmpeg Commands potentially helpful:
```
ffmpeg -ss 0.7 -i '.\1.wav' -c:a copy output.wav
ffmpeg -i '.\1.wav' -af "adelay=1355|1355" -b:a 2822k output.wav
ffmpeg -framerate 60 -i frame%05d.png -c:v libx264 -s 1280x720 -b:v 2023k -pix_fmt yuv420p -r 60 output_video.mp4
ffmpeg -loop 1 -i last_frame.png -c:v libx264 -t 0.6 -pix_fmt yuv420p fill_video.mp4
ffmpeg -i fill_video.mp4 -i needLe.mp4 -filter_complex "[0:v]fps=30[v0];[1:v]fps=30[v1];[v0][v1]concat=n=2:v=1:a=0[outv]" -map "[outv]" output.mp4
ffmpeg -i tmp.mp4 -i bili.png -filter_complex "[0:v][1:v]overlay=1542:35[outv]" -map "[outv]" -map 0:a -codec:a copy output.mp4
ffmpeg -i input.mp4 -r 60 -c:v libx264 -crf 0 output.mp4
ffmpeg -i 2dmvbl.mp4 -vf scale=1920:1080 -r 48 output.mp4
ffmpeg -i output.mp4 -vf ass=O1.ass -crf 23.5 output1.mp4
```

## Extend my thanks to:
[Vmoe字幕组Karaoke搜索引擎](https://karaoke.vmoe.info/)

[Aegisub docs](https://aegisub.org/docs/latest/automation/karaoke_templater/)

[qwe7989199@bilibili](https://www.bilibili.com/opus/349152760675887085)

[小军尼玛@bilibili](https://www.bilibili.com/opus/907830252460310576)
