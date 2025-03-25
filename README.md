# karasub
Some self-made Karaoke subtitles

## FFmpeg Commands potentially helpful:
```
ffmpeg -i '.\1.mp4' -t 27.58 -b:a 320k 2758.mp4
ffmpeg -ss 0.7 -i '.\1.wav' -c:a copy output.wav
ffmpeg -i '.\1.wav' -af "adelay=1355|1355" -b:a 2822k output.wav
ffmpeg -i input1.mp3 -i input2.mp3 -filter_complex amix=inputs=2:duration=longest -b:a 320k output.mp3

ffmpeg -framerate 60 -i frame%05d.png -c:v libx264 -s 1280x720 -b:v 2023k -pix_fmt yuv420p -r 60 output_video.mp4
ffmpeg -loop 1 -i last_frame.png -c:v libx264 -t 0.6 -pix_fmt yuv420p fill_video.mp4
ffmpeg -loop 1 -y -i 1.png -i on.MP3 -shortest -r 60 -b:a 320k out.mp4

ffmpeg -i .\2758.mp4 -i '.\Off Vocal.mp4' -filter_complex "[0:a:0][1:a:0]concat=n=2:v=0:a=1[a]" -map "[a]" out.mp3
ffmpeg -i fill_video.mp4 -i needLe.mp4 -filter_complex "[0:v]fps=30[v0];[1:v]fps=30[v1];[v0][v1]concat=n=2:v=1:a=0[outv]" -map "[outv]" output.mp4
ffmpeg -i tmp.mp4 -i bili.png -filter_complex "[0:v][1:v]overlay=1542:35[outv]" -map "[outv]" -map 0:a -codec:a copy output.mp4

ffmpeg -i 2dmvbl.mp4 -vf scale=1920:1080 -r 60 -b:a 320k main.mp4
ffmpeg -i main.mp4 -vf ass=main.ass -c:a copy -crf 23.5 onvocal.mp4
ffmpeg -i main.mp4 -i 25.png -filter_complex "[0:v][1:v]overlay=258:18,ass=main.ass[outv]" -map "[outv]" -map 0:a -c:a copy onvocal.mp4
ffmpeg -i .\onvocal.mp4 -itsoffset 1.5 -i .\offvocala.mp4 -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 offvocalv.mp4
ffmpeg -i 1.mp4 -vf "scale=1920:1080,ass='E\:\\Videos\\nicokara\\tag.ass'" -r 60 output.mp4

ffmpeg -i output2.mp4 -vf hflip output_hflip.mp4
ffmpeg -i .\1.mp4 -filter:v "crop=800:600:280:1320" output.mp4
ffmpeg -i .\1.mp4 -vf "pad=640:360:(ow-iw)/2:(oh-ih)/2:color=black" output.mp4
```

## Extend my thanks to:
[Vmoe字幕组Karaoke搜索引擎](https://karaoke.vmoe.info/)

[Aegisub docs](https://aegisub.org/docs/latest/automation/karaoke_templater/)

[qwe7989199@bilibili](https://www.bilibili.com/opus/349152760675887085)

[小军尼玛@bilibili](https://www.bilibili.com/opus/907830252460310576)

[鹤翔万里的笔记本](https://note.tonycrane.cc/others/subs/ass/)

[フックン's note](https://note.com/fukkun_mochikara/n/nd8a636467e71)