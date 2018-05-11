#!/bin/bash
INPUT_DATA=(img1.jpg vid1.mp4 img2.jpg vid2.mp4 img3.jpg)
IMAGE_TIME_SPAN=5
VIDEO_TIME_SPAN_1=6
VIDEO_TIME_SPAN_2=13
INPUT_DIR="input"
OUTPUT_DIR="output"
BACKGROUND_MUSIC="$INPUT_DIR/background.mp3"
OUTPUT_STEP1="$OUTPUT_DIR/tmp_video.mp4"
OUTPUT_STEP3="$OUTPUT_DIR/tmp_background.mp3"
OUTPUT_FILE="$OUTPUT_DIR/final.mp4"
SCALE_SIZE="320x240"

step1_create_temp_video()
{
    ffmpeg -y \
    -f lavfi -t 1 -i anullsrc \
    -i $INPUT_DIR/${INPUT_DATA[0]} \
    -t $VIDEO_TIME_SPAN_1 -i $INPUT_DIR/${INPUT_DATA[1]} \
    -i $INPUT_DIR/${INPUT_DATA[2]} \
    -t $VIDEO_TIME_SPAN_2 -i $INPUT_DIR/${INPUT_DATA[3]} \
    -i $INPUT_DIR/${INPUT_DATA[4]} \
    -filter_complex \
    "[1:v]zoompan=z='zoom+0.002':d=25*$IMAGE_TIME_SPAN:s=$SCALE_SIZE[img1]; \
    [2:v]scale=$SCALE_SIZE[v1]; \
    [3:v]zoompan=z='zoom+0.002':d=25*$IMAGE_TIME_SPAN:s=$SCALE_SIZE[img2]; \
    [4:v]scale=$SCALE_SIZE[v2]; \
    [5:v]zoompan=z='zoom+0.002':d=25*$IMAGE_TIME_SPAN:s=$SCALE_SIZE[img3]; \
    [img1][0:a][v1][0:a][img2][0:a][v2][0:a][img3][0:a]concat=n=5:v=1:a=1" \
    -pix_fmt yuv420p -c:v libx264 \
    $OUTPUT_STEP1
}

step2_extract_background_music()
{
    for i in "${INPUT_DATA[@]}"
    do
    extension="${i##*.}"
    filename="${i%.*}"
    if [ "$extension" = "mp4" ]; then
        ffmpeg -y -i "$INPUT_DIR/$i" "$OUTPUT_DIR/$filename.mp3"
    fi
    done
}

step3_merge_background_music()
{
    #TODO: 
    background1="output/vid1.mp3"
    background2="output/vid2.mp3"
    ffmpeg -y \
    -i "$BACKGROUND_MUSIC" \
    -i "$background1" \
    -i "$background2" \
    -filter_complex \
    "[0:0]volume=enable='between(t,5,11)':volume='0.1':eval=frame, volume=enable='between(t,16,29)':volume='0.1':eval=frame[a1]; \
     [1:0]adelay=5000|5000[a2]; \
     [2:0]adelay=16000|16000[a3]; \
     [a1][a2][a3] amix=inputs=3:duration=longest" \
    -c:a libmp3lame \
    -threads 5 -preset ultrafast -strict -2 \
    $OUTPUT_STEP3
}

step4_generate_video()
{
    ffmpeg -y -i $OUTPUT_STEP1 -i $OUTPUT_STEP3 -codec:a libmp3lame -ar 44100 -ab 64k -ac 1 -q:v 1 -pix_fmt yuv420p -map 0:0 -map 1:0 -shortest $OUTPUT_FILE
}

step5_remove_temp_files()
{
    echo "remove temp files"
    rm $OUTPUT_STEP1
    rm $OUTPUT_STEP3
    rm "output/vid1.mp3"
    rm "output/vid2.mp3" 
}

step1_create_temp_video
step2_extract_background_music
step3_merge_background_music
step4_generate_video
step5_remove_temp_files